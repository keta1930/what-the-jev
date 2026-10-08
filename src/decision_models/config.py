"""Loading and validating the experiment configuration."""

from pathlib import Path
from typing import TypedDict

import yaml

REQUIRED_FIELDS = {'model', 'endpoint', 'data', 'output'}
DEFAULT_CONCURRENCY = 4
MAX_CONCURRENCY = 16
DEFAULT_REPEAT = 1


class RunConfig(TypedDict):
    """A validated run configuration."""

    model: str
    endpoint: str
    data: str | list[str]
    output: str | list[str]
    concurrency: int
    repeat: int


def load_config(path: Path) -> RunConfig:
    """Read the config and validate its fields, keeping paths relative to the config file."""
    config = yaml.safe_load(path.read_text(encoding='utf-8'))
    optional = {'concurrency', 'repeat'}
    if not isinstance(config, dict) or set(config) - optional != REQUIRED_FIELDS:
        raise ValueError(
            f'config fields must be {sorted(REQUIRED_FIELDS)}, optionally plus concurrency and repeat'
        )
    for name in ('model', 'endpoint'):
        value = config[name]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'config {name} must be a non-empty string')
    datas = _paths(config['data'], 'data')
    outputs = _paths(config['output'], 'output')
    if any(Path(name).suffix != '.jsonl' for name in outputs):
        raise ValueError('output must be a .jsonl file path')
    if len(datas) > 1 and len(outputs) != len(datas):
        raise ValueError('when data lists several files, output must be a list of the same length')
    if len(set(outputs)) != len(outputs):
        raise ValueError('output paths must not repeat')
    config['data'] = datas[0] if len(datas) == 1 else datas
    config['concurrency'] = _concurrency(config.get('concurrency'))
    config['repeat'] = _repeat(config.get('repeat'))
    if config['repeat'] > 1:
        expanded = [
            _repeat_outputs(name, config['repeat'])
            for name in outputs
        ]
        config['output'] = [
            name for names in expanded for name in names
        ]
    else:
        config['output'] = outputs[0] if len(outputs) == 1 else outputs
    return config


def _paths(value: object, name: str) -> list[str]:
    """Validate a path field as one non-empty string or a list of non-empty strings."""
    if isinstance(value, str) and value.strip():
        return [value]
    if isinstance(value, list) and value:
        items: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f'config {name} must be a non-empty string or a list of non-empty strings')
            items.append(item)
        return items
    raise ValueError(f'config {name} must be a non-empty string or a list of non-empty strings')


def _concurrency(value: object) -> int:
    """Validate the initial concurrency, falling back to the default when absent."""
    if value is None:
        return DEFAULT_CONCURRENCY
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 1 <= value <= MAX_CONCURRENCY
    ):
        raise ValueError(f'config concurrency must be an integer from 1 to {MAX_CONCURRENCY}')
    return value


def _repeat(value: object) -> int:
    """Validate the repeat count, falling back to a single run when absent."""
    if value is None:
        return DEFAULT_REPEAT
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError('config repeat must be an integer of at least 1')
    return value


def _repeat_outputs(output: str, repeat: int) -> list[str]:
    """Expand an output path into one path per round, numbered from 1, such as responses_1.jsonl."""
    base = Path(output)
    return [
        str(base.with_name(f'{base.stem}_{index}{base.suffix}'))
        for index in range(1, repeat + 1)
    ]
