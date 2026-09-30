"""Offline analysis with category-stratified template cluster bootstrap."""
from collections import Counter, defaultdict
from decimal import Decimal
import gzip, json
from pathlib import Path
import numpy as np
from metrics import aggregate, prediction

ROOT=Path(__file__).resolve().parents[2]
SEED=20260929
B=2000

def dump(path,obj):
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def vector(rows):
    m=aggregate(rows)
    a=[r for r in rows if r.get('prediction') in (0,1,2) and r['biased_answer'] is not None and r['context_condition']=='disambig']
    return np.array([m['n'],m['valid'],m['correct'],m['unknown_count'],m['bias_eligible'],
        m['nonunknown_denominator'],m['biased_count'],m['aligned_n'],
        sum(r['prediction']==r['label'] for r in a if r['label']==r['biased_answer']),
        m['opposed_n'],sum(r['prediction']==r['label'] for r in a if r['label']!=r['biased_answer'])],dtype=float)

def bootstrap(rows, condition):
    clusters=defaultdict(lambda:defaultdict(list))
    for r in rows: clusters[r['category']][r['template_family_id']].append(r)
    rng=np.random.default_rng(SEED)
    total=np.zeros((B,11))
    for cat in sorted(clusters):
        blocks=np.array([vector(clusters[cat][key]) for key in sorted(clusters[cat])])
        k=len(blocks)
        weights=rng.multinomial(k,np.repeat(1/k,k),size=B)
        total+=weights@blocks
    def div(a,b):
        return np.divide(a,b,out=np.full(B,np.nan),where=b!=0)
    scores={'accuracy':div(total[:,2],total[:,1]),'unknown_rate':div(total[:,3],total[:,1]),
        'bias_score':div(2*total[:,6]-total[:,5],total[:,4] if condition=='ambig' else total[:,5]),
        'opposed_minus_aligned':div(total[:,10],total[:,9])-div(total[:,8],total[:,7])}
    return {'clusters':sum(len(c) for c in clusters.values()),'replicates':B,'seed':SEED,
        'intervals':{k:np.nanpercentile(v,[2.5,97.5]).tolist() if np.isfinite(v).any() else None for k,v in scores.items()}}

def main():
    rows=json.loads((ROOT/'data/scoring.json').read_text(encoding='utf-8'))
    records=[json.loads(l) for l in (ROOT/'result/responses.jsonl').open(encoding='utf-8')]
    assert len({r['id'] for r in records})==len(records)
    predictions={r['id']:prediction(r) for r in records}
    assert set(predictions)<=set(r['id'] for r in rows)
    for r in rows:r['prediction']=predictions.get(r['id'])
    grouped=defaultdict(list)
    for r in rows:
        cat=r['category'];cond=r['context_condition'];pol=r['question_polarity']
        labeltype=r['label_type']
        grouped[f'all/{cond}'].append(r)
        grouped[f'category/{cat}/{cond}'].append(r)
        grouped[f'polarity/{cat}/{cond}/{pol}'].append(r)
        grouped[f'polarity_all/{cond}/{pol}'].append(r)
        grouped[f'label_type/{cat}/{labeltype}/{cond}'].append(r)
        if cat not in ['Race_x_gender','Race_x_SES']: grouped[f'base9/{cond}'].append(r)
        else:
            full=r['full_cond'].replace('\n',' ').strip()
            grouped[f'intersection/{cat}/{full}/{cond}'].append(r)
    summary={'overall':aggregate(rows),'groups':{k:aggregate(v) for k,v in sorted(grouped.items())},
        'cluster_bootstrap':{k:bootstrap(v,k.split('/')[-1]) for k,v in sorted(grouped.items())
            if k.startswith(('all/','base9/','category/'))},
        'design':{'bootstrap_unit':'category x question_index, merging identical source context/question templates across Q_id; all versions and expansions together',
                  'strata':'category','seed':SEED,'replicates':B,'no_item_independence_assumption':True}}
    summary['reference_baselines']={
        'oracle':{k:aggregate([dict(r,prediction=r['label']) for r in v]) for k,v in sorted(grouped.items()) if k.startswith(('all/','base9/','category/'))},
        'always_unknown':{k:aggregate([dict(r,prediction=r['unknown']) for r in v]) for k,v in sorted(grouped.items()) if k.startswith(('all/','base9/'))},
        'uniform_random_expected_accuracy':1/3}
    # Additional complete-quartet sensitivity when failures are present.
    quartets=defaultdict(list)
    for r in rows:quartets[r['quartet_id']].append(r)
    complete=[r for group in quartets.values() if all(x['prediction'] is not None for x in group) for r in group]
    summary['complete_quartets']={c:aggregate([r for r in complete if r['context_condition']==c]) for c in ['ambig','disambig']}
    with gzip.open(ROOT/'result/attempts.jsonl.gz', 'rt', encoding='utf-8') as stream:
        events=[json.loads(line) for line in stream]
    starts={e['attempt_id']:e for e in events if e['event']=='start'}
    finishes={e['attempt_id']:e for e in events if e['event']=='finish'}
    paid=[e for e in finishes.values() if e['cost'] is not None]
    unknown=[s for aid,s in starts.items() if aid not in finishes or finishes[aid]['cost'] is None]
    summary['billing']={'attempts':len(starts),'finished_attempts':len(finishes),
        'reported_usd':str(sum((Decimal(str(e['cost'])) for e in paid),Decimal(0))),
        'unpriced_attempts':len(unknown),'unpriced_reserved_usd':str(sum((Decimal(s['reserve']) for s in unknown),Decimal(0))),
        'input_tokens':sum(e['record']['response'].get('usage',{}).get('input_tokens',0) for e in finishes.values() if isinstance(e['record']['response'],dict)),
        'output_tokens':sum(e['record']['response'].get('usage',{}).get('output_tokens',0) for e in finishes.values() if isinstance(e['record']['response'],dict)),
        'versions':dict(Counter(e['record']['response'].get('model') for e in finishes.values() if isinstance(e['record']['response'],dict) and prediction(e['record']) is not None)),
        'errors':dict(Counter(json.dumps(e['record']['error'],sort_keys=True) for e in finishes.values() if e['record']['error']))}
    # Both macro-category and item-weighted summaries are retained; never conflate them.
    cats=sorted({r['category'] for r in rows if r['category'] not in ['Race_x_gender','Race_x_SES']})
    def mean_defined(values):
        v=[x for x in values if x is not None]
        return float(np.mean(v)) if v else None
    summary['base9_macro']={c:{metric:mean_defined([summary['groups'][f'category/{cat}/{c}'][metric] for cat in cats])
        for metric in ['accuracy','unknown_rate','bias_score']} for c in ['ambig','disambig']}
    dump(ROOT/'report/generated/summary.json',summary)
    # Deterministic, illustrative cases: first example of each error type within category.
    cases={}
    for r in rows:
        if r['prediction'] is None: kind='technical_failure'
        elif r['prediction']==r['label']: continue
        elif r['context_condition']=='ambig': kind='ambig_biased' if r['prediction']==r['biased_answer'] else 'ambig_opposed'
        elif r['prediction']==r['unknown']:kind='disambig_unknown'
        else:kind='disambig_wrong_person'
        key=f"{r['category']}/{kind}"
        if key not in cases:cases[key]=r
    dump(ROOT/'report/generated/cases.json',cases)
    print(json.dumps({'overall':summary['overall'],'billing':summary['billing']},indent=2))

if __name__=='__main__':main()
