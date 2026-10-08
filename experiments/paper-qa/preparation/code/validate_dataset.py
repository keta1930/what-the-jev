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
    validate(loads(DATASET.read_text(encoding='utf-8')), load_validator(SCHEMA), 'invalid dataset format')
    report.check(True, 'repo loader and jsonschema accept the dataset',
                 'load_dataset / Draft202012Validator rejected the dataset')

    report.check(len(samples) == EXPECTED_TOTAL, 'total == 240', f'got {len(samples)}')
    ids = [s['id'] for s in samples]
    report.check(len(ids) == len(set(ids)), 'ids are globally unique', 'duplicate ids')

    types_global = Counter()
    for slug in slugs:
        expected_ids = [f'{slug}-{i:02d}' for i in range(1, EXPECTED_PER_PAPER + 1)]
        got = [s['id'] for s in samples if s['id'].rsplit('-', 1)[0] == slug]
        report.check(got == expected_ids, f'{slug} has exactly 10 samples ordered -01..-10', f'got {got}')
        per_paper = Counter(
            next(iter(s['input']['questions'].values()))['type']
            for s in samples
            if s['id'].rsplit('-', 1)[0] == slug
        )
        report.check(
            dict(per_paper) == {'noul': EXPECTED_PER_PAPER},
            f'{slug} has 10 noul samples',
            f'got {dict(per_paper)}',
        )
        types_global.update(per_paper)
    report.check(
        dict(types_global) == {'noul': EXPECTED_TOTAL},
        'all 240 samples are noul',
        f'got {dict(types_global)}',
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

        report.check(set(meta) == METADATA_KEYS, 'metadata has all six keys', sid)
        report.check(meta.get('paper') == slug, 'metadata.paper==slug', sid)
        report.check(meta.get('arxiv_id') == arxiv_by_slug[slug], 'metadata.arxiv_id matches the snapshot', sid)

        report.check(
            set(questions[qkey]) == {'type', 'instructions'},
            'questions has no criteria',
            f'{sid} has {sorted(questions[qkey])}',
        )

        excerpt = sample['input']['state']['paper_excerpt']
        chunk = CHUNKS / slug / str(meta.get('source_part'))
        if chunk.is_file():
            report.check(excerpt == chunk.read_text(encoding='utf-8'), 'excerpt equals the chunk', sid)
        else:
            report.check(False, 'excerpt equals the chunk', f'{sid} missing chunk {chunk}')
        excerpt_sizes.append(len(excerpt.encode('utf-8')))

        evidence = meta.get('evidence', '')
        report.check(evidence in excerpt, 'evidence is a substring', sid)
        report.check(len(evidence) <= 400, 'evidence <= 400', f'{sid} length {len(evidence)}')
        evidence_lens.append(len(evidence))

        reference = sample['reference']
        report.check(list(reference) == list(questions), 'reference keys match questions', sid)
        report.check(meta.get('question_type') == qtype, 'question_type matches the question', sid)
        report.check(
            list(reference.get(qkey, {})) == ['noul'] and isinstance(answer, bool),
            'reference value is valid',
            f'{sid} ({qtype})',
        )
        if isinstance(answer, bool):
            labels_by_paper.setdefault(slug, Counter())[answer] += 1

    for slug in slugs:
        labels = labels_by_paper.get(slug, Counter())
        report.check(
            labels[True] >= MIN_PER_LABEL and labels[False] >= MIN_PER_LABEL,
            f'{slug} has at least 3 true and 3 false',
            f'true={labels[True]} false={labels[False]}',
        )

    print('=== checks (category: passed/total) ===')
    for category, total in report.total.items():
        passed = report.passed[category]
        print(f'{"PASS" if passed == total else "FAIL"}  {category}: {passed}/{total}')
    if report.failures:
        print('\n=== failures ===')
        for line in report.failures:
            print('  !!', line)

    print('\n--- summary ---')
    print(f'total {len(samples)}')
    print(f'question types {dict(types_global)}')
    labels_total = Counter()
    for labels in labels_by_paper.values():
        labels_total.update(labels)
    print(f'labels true {labels_total[True]} / false {labels_total[False]}')
    domains = Counter()
    domain_by_slug = {p['slug']: p['domain'] for p in papers}
    for sample in samples:
        domains[domain_by_slug[sample['id'].rsplit('-', 1)[0]]] += 1
    print(f'domains by sample count {dict(domains)}')
    print(f'excerpt bytes {min(excerpt_sizes)}-{max(excerpt_sizes)}')
    print(f'evidence length {min(evidence_lens)}-{max(evidence_lens)}')

    if report.failures:
        print(f'\nvalidation failed: {len(report.failures)} checks')
        return 1
    print('\nall checks passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
