"""Strict JSON parsing and schema validation."""

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
    """Reject nonstandard JSON numeric constants."""
    raise ValueError(f'invalid JSON numeric constant: {value}')


def unique_keys(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate object fields."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON field: {key}')
        result[key] = value
    return result


def _finite_float(value: str) -> float:
    """Parse finite floating-point JSON numbers."""
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f'JSON number exceeds finite float range: {value}')
    return number


def loads(text: str) -> Any:
    """Parse JSON without duplicate fields or nonfinite numbers."""
    return json.loads(
        text,
        parse_constant=reject_constant,
        parse_float=_finite_float,
        object_pairs_hook=unique_keys,
    )


def load_validator(path: Path) -> Draft202012Validator:
    """Load a local JSON schema validator."""
    return Draft202012Validator(loads(path.read_text(encoding='utf-8')))


def validate(data: Any, validator: Draft202012Validator, label: str) -> None:
    """Include the field location of the first schema error."""
    error = next(validator.iter_errors(data), None)
    if error is not None:
        location = '.'.join(str(part) for part in error.absolute_path) or '$'
        raise ValueError(f'{label} {location}: {error.message}')
