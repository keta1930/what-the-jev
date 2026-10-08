"""Reproducible official BBQ -> Jev choice adapter. No network/model calls."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OFFICIAL = ROOT / 'preparation/raw'

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    # Merge distinct Q_id values that share exactly the same normalized template
    # context and both questions; do this without reading any model responses.
    parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    for f in sorted((OFFICIAL/'templates').glob('new_templates - *.csv')):
        category=f.stem.removeprefix('new_templates - ')
        identical={}
        for r in csv.DictReader(f.open(encoding='utf-8-sig')):
            if not r.get('Ambiguous_Context',''):continue
            tid=f"{category}:{r['Q_id']}"
            signature=tuple(re.sub(r'\s+',' ',r.get(k,'')).strip() for k in
                ['Ambiguous_Context','Question_negative_stereotype','Question_non_negative'])
            if signature in identical:parent[find(tid)]=find(identical[signature])
            else:identical[signature]=tid
    metadata = collections.defaultdict(list)
    for r in csv.DictReader((OFFICIAL/'additional_metadata.csv').open(encoding='utf-8')):
        metadata[(r['category'], int(r['example_id']), r['question_index'])].append(r)
    samples, rows = [], []
    groups = collections.defaultdict(list)
    for f in sorted((OFFICIAL/'data').glob('*.jsonl')):
        for line in f.open(encoding='utf-8'):
            r = json.loads(line)
            key = (r['category'], r['example_id'], r['question_index'])
            matches = metadata[key]
            assert matches
            for field in ['target_loc', 'label_type', 'full_cond', 'corr_ans_aligns_race', 'corr_ans_aligns_var2']:
                assert len({m[field] for m in matches}) == 1, (key, field)
            meta = matches[0]
            unknown = [i for i in range(3) if r['answer_info'][f'ans{i}'][1].lower() == 'unknown']
            assert len(unknown) == 1
            target = int(meta['target_loc']) if meta['target_loc'] != 'NA' else None
            assert target is None or target != unknown[0]
            assert (r['label'] == unknown[0]) == (r['context_condition'] == 'ambig')
            sid = f"{r['category']}:{r['example_id']}"
            # Source generator emits each context x polarity quartet consecutively.
            quartet = f"{r['category']}:{r['example_id']//4}"
            item = {'id': sid, 'input': {'state': r['context'], 'questions': {'answer': {
                'type': 'choice', 'instructions': r['question'],
                'criteria': {f'ans{i}': r[f'ans{i}'] for i in range(3)}}}},
                'reference': {'answer': {'choice': f'ans{r["label"]}'}},
                'metadata': {'category': r['category'], 'example_id': r['example_id'],
                             'template_id': f"{r['category']}:{r['question_index']}", 'quartet_id': quartet,
                             'template_family_id':find(f"{r['category']}:{r['question_index']}"),
                             'question_index': r['question_index'], 'question_polarity': r['question_polarity'],
                             'context_condition': r['context_condition'], 'label_type': meta['label_type'],
                             'full_cond': meta['full_cond'], 'unknown': unknown[0], 'biased_answer': target}}
            samples.append(item)
            groups[quartet].append(dict(item['metadata'], original=r))
            rows.append(r)
    assert len({s['id'] for s in samples}) == len(samples)
    for group in groups.values():
        assert len(group) == 4
        assert {(x['context_condition'], x['question_polarity']) for x in group} == {
            ('ambig','neg'),('ambig','nonneg'),('disambig','neg'),('disambig','nonneg')}
        assert len({x['template_id'] for x in group}) == 1
        assert len({tuple(x['original'][f'ans{i}'] for i in range(3)) for x in group}) == 1
        a = [x for x in group if x['context_condition']=='ambig']
        d = [x for x in group if x['context_condition']=='disambig']
        assert a[0]['original']['context'] == a[1]['original']['context']
        assert d[0]['original']['context'] == d[1]['original']['context']
        assert d[0]['original']['context'].startswith(a[0]['original']['context'])
        if group[0]['biased_answer'] is not None:
            assert a[0]['biased_answer'] != a[1]['biased_answer']
    dump(ROOT/'data/dataset.json', {'schema_version': 1, 'samples': samples})
    print(f'Prepared {len(samples)} BBQ samples; no model requests.')

if __name__ == '__main__':
    prepare()
