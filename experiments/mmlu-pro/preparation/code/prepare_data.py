"""Download the pinned MMLU-Pro test split and build the snapshot and dataset."""

import io
import json
import string
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import pyarrow.parquet as parquet

REVISION = 'b189ec765aa7ed75c8acfea42df31fdae71f97be'
DATASET_NAME = 'mmlu_pro'
URL = (
    f'https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro/resolve/{REVISION}/'
    'data/test-00000-of-00001.parquet'
)
PREPARATION = Path(__file__).resolve().parents[1]
RAW_PATH = PREPARATION / f'raw/{DATASET_NAME}.test.json'
DATASET_PATH = PREPARATION.parent / 'data/dataset.json'
EXPECTED_ROWS = 12032
INSTRUCTIONS = 'Pick the correct option.'
LETTERS = string.ascii_uppercase


def fetch_rows() -> list[dict[str, Any]]:
    """Download the pinned parquet, keeping the fields needed for grading and grouping."""
    with urlopen(URL, timeout=60) as response:
        original = response.read()
    table = parquet.read_table(io.BytesIO(original))
    return [
        {
            'question_id': row['question_id'],
            'question': row['question'],
            'options': row['options'],
            'answer': row['answer'],
            'answer_index': row['answer_index'],
            'category': row['category'],
            'src': row['src'],
        }
        for row in table.to_pylist()
    ]


def check_rows(rows: list[dict[str, Any]]) -> None:
    """Check that the answer letter, index, and option count agree."""
    for index, row in enumerate(rows):
        count = len(row['options'])
        if not 2 <= count <= len(LETTERS):
            raise ValueError(f'第 {index} 条选项数量异常：{count}')
        if not 0 <= row['answer_index'] < count:
            raise ValueError(f'第 {index} 条答案下标越界：{row["answer_index"]}')
        if LETTERS[row['answer_index']] != row['answer']:
            raise ValueError(
                f'第 {index} 条答案字母与下标不一致：'
                f'{row["answer"]} != {LETTERS[row["answer_index"]]}'
            )


def build_dataset(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Convert the MMLU-Pro rows into the single-turn dataset."""
    samples = []
    for index, row in enumerate(rows):
        letters = LETTERS[: len(row['options'])]
        samples.append({
            'id': f'mmlu-pro-{index + 1:05d}',
            'input': {
                'state': row['question'],
                'questions': {
                    'answer': {
                        'type': 'choice',
                        'instructions': INSTRUCTIONS,
                        'criteria': dict(zip(letters, row['options'])),
                    },
                },
            },
            'reference': {'answer': {'choice': row['answer']}},
            'metadata': {
                'category': row['category'],
                'src': row['src'],
                'source_index': index,
                'question_id': row['question_id'],
            },
        })
    return {'schema_version': 1, 'samples': samples}


def write_json(path: Path, value: Any) -> None:
    """Write JSON preserving non-ASCII characters and key order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as file:
        json.dump(value, file, ensure_ascii=False, indent=2, allow_nan=False)
        file.write('\n')


def main() -> None:
    """Download the source data and write the snapshot and dataset."""
    rows = fetch_rows()
    if len(rows) != EXPECTED_ROWS:
        raise ValueError(f'预期 {EXPECTED_ROWS} 条，实际 {len(rows)} 条')
    check_rows(rows)
    dataset = build_dataset(rows)
    write_json(RAW_PATH, rows)
    write_json(DATASET_PATH, dataset)
    print(f'源数据 {len(rows)} 条：{RAW_PATH}')
    print(f'数据集 {len(dataset["samples"])} 条：{DATASET_PATH}')


if __name__ == '__main__':
    main()
