"""Download the Hugging Face MMLU-Pro leaderboard snapshot, overwriting the previous one."""

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

URL = 'https://huggingface.co/api/datasets/TIGER-Lab/MMLU-Pro/leaderboard'
PREPARATION = Path(__file__).resolve().parents[1]
RAW_PATH = PREPARATION / 'raw/leaderboard-latest.json'
EXPECTED_FIELDS = {'modelId', 'value'}


def fetch_leaderboard() -> list[dict[str, Any]]:
    """Download the leaderboard JSON and check its basic shape."""
    with urlopen(URL, timeout=60) as response:
        data = json.load(response)
    if not isinstance(data, list) or not data:
        raise ValueError(f'leaderboard 响应异常：{type(data).__name__}')
    bad = [index for index, row in enumerate(data) if not EXPECTED_FIELDS <= set(row)]
    if bad:
        raise ValueError(f'第 {bad[:3]} 条记录缺少必填字段')
    return data


def write_json(path: Path, value: Any) -> None:
    """Write JSON preserving non-ASCII characters and key order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as file:
        json.dump(value, file, ensure_ascii=False, indent=2, allow_nan=False)
        file.write('\n')


def main() -> None:
    """Fetch the leaderboard and overwrite the latest snapshot."""
    rows = fetch_leaderboard()
    write_json(RAW_PATH, rows)
    print(f'leaderboard {len(rows)} 条：{RAW_PATH}')


if __name__ == '__main__':
    main()
