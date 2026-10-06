"""由 raw/questions-240.jsonl、raw/papers.json 与 raw/chunks/ 组装 data/dataset.json。

输入：raw/questions-240.jsonl（240 条 noul 主题题）、raw/papers.json、raw/chunks/<slug>/part-XX.md。
输出：data/dataset.json。用法：python build_dataset.py
"""

import json
from pathlib import Path

PREPARATION = Path(__file__).resolve().parents[1]
REPO_ROOT = PREPARATION.parents[2]
RAW = PREPARATION / 'raw'
PAPERS_PATH = RAW / 'papers.json'
QUESTIONS_PATH = RAW / 'questions-240.jsonl'
CHUNKS = RAW / 'chunks'
DATASET_PATH = PREPARATION.parent / 'data' / 'dataset.json'

EXPECTED_PER_PAPER = 10
EXPECTED_TOTAL = 240


def load_papers() -> list[dict]:
    """按 papers.json 的论文顺序返回论文条目。"""
    return json.loads(PAPERS_PATH.read_text(encoding='utf-8'))['papers']


def load_bank() -> dict[str, list[dict]]:
    """读取题目源，按论文分组。"""
    bank: dict[str, list[dict]] = {}
    for line in QUESTIONS_PATH.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        bank.setdefault(rec['paper'], []).append(rec)
    return bank


def build() -> list[dict]:
    """组装全量数据集并写出，返回样本列表。"""
    samples: list[dict] = []
    bank = load_bank()
    for paper in load_papers():
        slug = paper['slug']
        records = sorted(bank[slug], key=lambda r: r['id'])
        expected_ids = [f'{slug}-{i:02d}' for i in range(1, EXPECTED_PER_PAPER + 1)]
        if [r['id'] for r in records] != expected_ids:
            raise ValueError(f'{slug}: 题目源 id 不完整 {[r["id"] for r in records]}')
        if any(r['type'] != 'noul' for r in records):
            raise ValueError(f'{slug}: 存在非 noul 题目')
        for rec in records:
            excerpt = (CHUNKS / slug / rec['source_part']).read_text(encoding='utf-8')
            samples.append({
                'id': rec['id'],
                'input': {
                    'state': {'paper_excerpt': excerpt},
                    'questions': {
                        rec['name']: {
                            'type': rec['type'],
                            'instructions': rec['instructions'],
                        },
                    },
                },
                'reference': {rec['name']: {rec['type']: rec['answer']}},
                'metadata': {
                    'paper': slug,
                    'arxiv_id': paper['arxiv_id'],
                    'source_part': rec['source_part'],
                    'sections': rec['sections'],
                    'evidence': rec['evidence'],
                    'question_type': rec['type'],
                },
            })
    ids = [s['id'] for s in samples]
    if len(ids) != len(set(ids)):
        raise ValueError('样本 ID 重复')
    if len(samples) != EXPECTED_TOTAL:
        raise ValueError(f'样本总数 {len(samples)} != {EXPECTED_TOTAL}')
    DATASET_PATH.write_text(
        json.dumps({'schema_version': 1, 'samples': samples}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    return samples


if __name__ == '__main__':
    result = build()
    print(f'已写出 {DATASET_PATH.relative_to(REPO_ROOT)}')
    print(f'样本 {len(result)} 条，全部 noul')
