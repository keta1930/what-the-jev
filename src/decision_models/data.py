"""Reading and validating the final input data."""

from pathlib import Path
from typing import Any

from .json_utils import load_validator, loads, validate
from .json_utils import reject_constant as reject_constant
from .json_utils import unique_keys as unique_keys

SCHEMA = Path(__file__).resolve().parents[2] / 'schema/dataset.schema.json'


def load_dataset(path: str | Path) -> list[dict[str, Any]]:
    """Validate the whole dataset and return its samples, without reading the source material."""
    data = loads(Path(path).read_text(encoding='utf-8'))
    validate(data, load_validator(SCHEMA), 'invalid dataset format')
    ids = set()
    for sample in data['samples']:
        if sample['id'] in ids:
            raise ValueError(f'duplicate sample id: {sample["id"]}')
        ids.add(sample['id'])
    return data['samples']
