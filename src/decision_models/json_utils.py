"""JSON numbers, key uniqueness, and schema validation."""

import json
import math
from collections.abc import Iterable
from pathlib import Path
from typing import Any, NoReturn, TypeAlias

from jsonschema import Draft202012Validator

JSONValue: TypeAlias = (
    str | int | float | bool | None | list['JSONValue'] | dict[str, 'JSONValue']
)


def reject_constant(value: str) -> NoReturn:
    """Reject NaN and Infinity, which JSON does not define."""
    raise ValueError(f'illegal JSON number: {value}')


def unique_keys(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate keys instead of silently dropping input."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def _finite_float(value: str) -> float:
    """Parse a JSON number that fits a finite float."""
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f'JSON number out of float range: {value}')
    return number


def loads(text: str) -> Any:
    """Parse JSON, rejecting duplicate keys and numbers that cannot round-trip safely."""
    return json.loads(
        text,
        parse_constant=reject_constant,
        parse_float=_finite_float,
        object_pairs_hook=unique_keys,
    )


def load_validator(path: Path) -> Draft202012Validator:
    """Build a validator from the local schema file."""
    return Draft202012Validator(loads(path.read_text(encoding='utf-8')))


def validate(data: Any, validator: Draft202012Validator, label: str) -> None:
    """Validate the data and name the failing field location in the first error."""
    error = next(validator.iter_errors(data), None)
    if error is not None:
        location = '.'.join(str(part) for part in error.absolute_path) or '$'
        raise ValueError(f'{label} {location}: {error.message}')
