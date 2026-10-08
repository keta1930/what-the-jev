"""Validate experiments/paper-qa/data/dataset.json against its raw files and schema."""

import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / 'src'))

from decision_models.data import load_dataset  # noqa: E402
from decision_models.json_utils import (  # noqa: E402
    load_validator,
    loads,
    validate,
)

DATASET = REPO_ROOT / 'experiments/paper-qa/data/dataset.json'
PAPERS = REPO_ROOT / 'experiments/paper-qa/preparation/raw/papers.json'
CHUNKS = REPO_ROOT / 'experiments/paper-qa/preparation/raw/chunks'
SCHEMA = REPO_ROOT / 'schema/dataset.schema.json'
EXPECTED_TOTAL = 240
EXPECTED_PER_PAPER = 10
MIN_PER_LABEL = 3
METADATA_KEYS = {'paper', 'arxiv_id', 'source_part', 'sections', 'evidence', 'question_type'}


class Report:
    """Count checks per category and keep only the failure details."""

    def __init__(self):
        self.total = Counter()
        self.passed = Counter()
        self.failures = []

    def check(self, ok, category, message=''):
        """Record one check and keep its message when it fails."""
        self.total[category] += 1
        if ok:
            self.passed[category] += 1
        else:
            self.failures.append(f'[{category}] {message}')


def main():
    """Run the checks and return the exit code."""
    report = Report()
    papers = loads(PAPERS.read_text(encoding='utf-8'))['papers']
    slugs = [p['slug'] for p in papers]
    arxiv_by_slug = {p['slug']: p['arxiv_id'] for p in papers}

    samples = load_dataset(DATASET)
    validate(loads(DATASET.read_text(encoding='utf-8')), load_validator(SCHEMA), '数据格式错误')
    report.check(True, '仓库 loader + jsonschema 接受数据集',
                 'load_dataset / Draft202012Validator 校验失败')

    report.check(len(samples) == EXPECTED_TOTAL, '总数==240', f'实为 {len(samples)}')
    ids = [s['id'] for s in samples]
    report.check(len(ids) == len(set(ids)), 'id 全局唯一', '存在重复 id')

    types_global = Counter()
    for slug in slugs:
        expected_ids = [f'{slug}-{i:02d}' for i in range(1, EXPECTED_PER_PAPER + 1)]
        got = [s['id'] for s in samples if s['id'].rsplit('-', 1)[0] == slug]
        report.check(got == expected_ids, f'{slug} 恰好 10 条且顺序 -01..-10', f'实为 {got}')
        per_paper = Counter(
            next(iter(s['input']['questions'].values()))['type']
            for s in samples
            if s['id'].rsplit('-', 1)[0] == slug
        )
        report.check(
            dict(per_paper) == {'noul': EXPECTED_PER_PAPER},
            f'{slug} 10 条全为 noul',
            f'实为 {dict(per_paper)}',
        )
        types_global.update(per_paper)
    report.check(
        dict(types_global) == {'noul': EXPECTED_TOTAL},
        '全局 240 条全为 noul',
        f'实为 {dict(types_global)}',
    )

    labels_by_paper: dict[str, Counter] = {}
    excerpt_sizes, evidence_lens = [], []
    for sample in samples:
        sid = sample['id']
        slug = sid.rsplit('-', 1)[0]
        meta = sample['metadata']
        questions = sample['input']['questions']
        qkey = next(iter(questions))
        qtype = questions[qkey]['type']
        answer = sample['reference'].get(qkey, {}).get('noul')

        report.check(set(meta) == METADATA_KEYS, 'metadata 六键齐全', sid)
        report.check(meta.get('paper') == slug, 'metadata.paper==slug', sid)
        report.check(meta.get('arxiv_id') == arxiv_by_slug[slug], 'metadata.arxiv_id 一致', sid)

        report.check(
            set(questions[qkey]) == {'type', 'instructions'},
            'questions 无 criteria',
            f'{sid} 实为 {sorted(questions[qkey])}',
        )

        excerpt = sample['input']['state']['paper_excerpt']
        chunk = CHUNKS / slug / str(meta.get('source_part'))
        if chunk.is_file():
            report.check(excerpt == chunk.read_text(encoding='utf-8'), 'excerpt 与 chunk 字符级相等', sid)
        else:
            report.check(False, 'excerpt 与 chunk 字符级相等', f'{sid} chunk 缺失 {chunk}')
        excerpt_sizes.append(len(excerpt.encode('utf-8')))

        evidence = meta.get('evidence', '')
        report.check(evidence in excerpt, 'evidence 子串', sid)
        report.check(len(evidence) <= 400, 'evidence<=400', f'{sid} 长度 {len(evidence)}')
        evidence_lens.append(len(evidence))

        reference = sample['reference']
        report.check(list(reference) == list(questions), 'reference 键一致', sid)
        report.check(meta.get('question_type') == qtype, 'question_type 一致', sid)
        report.check(
            list(reference.get(qkey, {})) == ['noul'] and isinstance(answer, bool),
            'reference 取值合法',
            f'{sid} ({qtype})',
        )
        if isinstance(answer, bool):
            labels_by_paper.setdefault(slug, Counter())[answer] += 1

    for slug in slugs:
        labels = labels_by_paper.get(slug, Counter())
        report.check(
            labels[True] >= MIN_PER_LABEL and labels[False] >= MIN_PER_LABEL,
            f'{slug} 真假各 >=3',
            f'true={labels[True]} false={labels[False]}',
        )

    print('=== 校验明细（类别 : 通过/总数）===')
    for category, total in report.total.items():
        passed = report.passed[category]
        print(f'{"PASS" if passed == total else "FAIL"}  {category}: {passed}/{total}')
    if report.failures:
        print('\n=== 失败明细 ===')
        for line in report.failures:
            print('  !!', line)

    print('\n--- 统计 ---')
    print(f'总数 {len(samples)}')
    print(f'题型分布 {dict(types_global)}')
    labels_total = Counter()
    for labels in labels_by_paper.values():
        labels_total.update(labels)
    print(f'真假分布 true {labels_total[True]} / false {labels_total[False]}')
    domains = Counter()
    domain_by_slug = {p['slug']: p['domain'] for p in papers}
    for sample in samples:
        domains[domain_by_slug[sample['id'].rsplit('-', 1)[0]]] += 1
    print(f'领域分布（按样本数）{dict(domains)}')
    print(f'excerpt 字节范围 {min(excerpt_sizes)}–{max(excerpt_sizes)}')
    print(f'evidence 长度范围 {min(evidence_lens)}–{max(evidence_lens)}')

    if report.failures:
        print(f'\n校验失败：{len(report.failures)} 项')
        return 1
    print('\n全部校验通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
