"""JSONL result persistence, history validation, and resume-file protection."""

import fcntl
import json
import logging
import re
from collections.abc import Iterator
from contextlib import contextmanager
from http.client import HTTPException as HTTPException
from pathlib import Path
from typing import Any, BinaryIO, TextIO

from jsonschema import Draft202012Validator

from .client import Transport as Transport
from .client import request_sample as request_sample
from .json_utils import JSONValue as JSONValue
from .json_utils import load_validator, loads, validate

SCHEMA = Path(__file__).resolve().parents[2] / 'schema/result.schema.json'
logger = logging.getLogger(__name__)


def drop_failed(path: Path) -> set[str]:
    """Drop failed records and return their ids for requeueing; the caller must hold the output lock."""
    if not path.exists():
        return set()
    kept: list[str] = []
    failed: set[str] = set()
    with path.open(encoding='utf-8') as file:
        for line in file:
            record = loads(line)
            if record['error'] is None:
                kept.append(line)
            else:
                failed.add(record['id'])
    if failed:
        path.write_text(''.join(kept), encoding='utf-8')
    return failed


def write_result(file: TextIO, result: dict[str, Any]) -> None:
    """Write and flush each finished result so completed requests survive."""
    file.write(json.dumps(result, ensure_ascii=False, allow_nan=False) + '\n')
    file.flush()


@contextmanager
def locked_output(path: Path) -> Iterator[None]:
    """Hold the output file exclusively across history scan, tail repair, and appends."""
    with path.open('a+b') as file:
        try:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError(f'result file is in use by another run: {path}') from exc
        try:
            yield
        finally:
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)


def load_recorded_ids(path: Path) -> set[str]:
    """Validate the recorded history and repair the trailing partial line; the caller holds the output lock."""
    if not path.exists():
        return set()
    validator = load_validator(SCHEMA)
    with path.open('r+b') as file:
        recorded, truncate_at, needs_newline = _scan_records(file, validator)
        if truncate_at is not None:
            file.truncate(truncate_at)
            logger.warning('truncated the partial trailing line of the result file: %s', path)
        elif needs_newline:
            file.write(b'\n')
            logger.info('added the missing trailing newline to the result file: %s', path)
    return recorded


def _scan_records(
    file: BinaryIO, validator: Draft202012Validator
) -> tuple[set[str], int | None, bool]:
    """Validate each line, returning the recorded ids and any tail repair still to do."""
    recorded: set[str] = set()
    offset = 0
    needs_newline = False
    for number, raw in enumerate(file, start=1):
        record = _parse_record(raw, number, validator)
        if record is None:
            return recorded, offset, False
        sample_id = record['id']
        if sample_id in recorded:
            raise ValueError(f'duplicate sample id on line {number} of the result file: {sample_id}')
        recorded.add(sample_id)
        offset += len(raw)
        needs_newline = not raw.endswith(b'\n')
    return recorded, None, needs_newline


def _parse_record(
    raw: bytes, number: int, validator: Draft202012Validator
) -> dict[str, Any] | None:
    """Decode and validate one line, returning None only for a repairable unterminated tail."""
    terminated = raw.endswith(b'\n')
    label = f'malformed line {number} of the result file'
    try:
        record = loads(raw.decode('utf-8'))
    except UnicodeDecodeError as exc:
        if (
            not terminated
            and exc.reason == 'unexpected end of data'
            and exc.end == len(raw)
        ):
            return None
        raise ValueError(f'{label}: invalid UTF-8') from exc
    except json.JSONDecodeError as exc:
        if not terminated and _is_truncated_json(exc):
            return None
        raise ValueError(f'{label}: invalid JSON') from exc
    except ValueError as exc:
        raise ValueError(f'{label}: {exc}') from exc
    validate(record, validator, label)
    return record


def _is_truncated_json(error: json.JSONDecodeError) -> bool:
    """Recognize an unfinished trailing JSON token, rejecting clear syntax damage."""
    text = error.doc.rstrip()
    if not text.lstrip().startswith('{'):
        return False
    if error.msg.startswith('Unterminated string'):
        return True
    if error.pos >= len(text):
        return True
    tail = text[error.pos :]
    if error.msg == 'Expecting value':
        return tail in {
            'n',
            'nu',
            'nul',
            't',
            'tr',
            'tru',
            'f',
            'fa',
            'fal',
            'fals',
            '-',
        }
    if error.msg == "Expecting ',' delimiter":
        return tail in {'.', 'e', 'E', 'e+', 'e-', 'E+', 'E-'}
    if error.msg == 'Invalid \\uXXXX escape':
        return re.fullmatch(r'u[0-9a-fA-F]{0,3}', tail) is not None
    return False
