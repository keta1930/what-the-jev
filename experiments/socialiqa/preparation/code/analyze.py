"""Offline SocialIQA scoring on the formal test split."""
from collections import Counter,defaultdict
from decimal import Decimal
from pathlib import Path
import json, math, random

ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def lines(p):return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l]
def wilson(k,n):
    z=1.959963984540054;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [c-h,c+h]
def main():
    samples=read(ROOT/'data/dataset.json')['samples'];gold=read(ROOT/'data/reference.json')
    records=lines(ROOT/'result/responses.jsonl');byid={r['id']:r for r in records}
    assert len(records)==len(byid)==len(samples)==len(gold) and set(byid)==set(gold)
    assert all(r['error'] is None for r in records)
    groups=defaultdict(lambda:dict(n=0,valid=0,correct=0));items=[];clusters=defaultdict(list)
    for sample in samples:
        sid=sample['id'];g=gold[sid];answer=byid[sid]['response']['answers']['answer'];p=answer['choice']
        assert p in sample['input']['questions']['answer']['criteria']
        correct=p==g['answer'];d=groups[g['promptDim']];d['n']+=1;d['valid']+=1;d['correct']+=correct
        item={'id':sid,'dimension':g['promptDim'],'gold':g['answer'],'prediction':p,'correct':correct,'selected_probability':answer['probabilities'][p],'wrong_source':g['answerSourcesOrigins']['ABC'.index(p)] if not correct else None}
        items.append(item);clusters[json.dumps(sample['input'],sort_keys=True)].append(item)
    for d in groups.values():d['accuracy']=d['correct']/d['n'];d['wilson95']=wilson(d['correct'],d['n'])
    n=len(items);k=sum(r['correct'] for r in items)
    # Billing is computed from final formal responses; the historical attempt log
    # (debug split, one unpriced failure, USD 0.01 reserved) was removed, see git history.
    usage=[r['response']['usage'] for r in records]
    cost={'test':{'responses':len(records),'input_tokens':sum(u['input_tokens'] for u in usage),'output_tokens':sum(u['output_tokens'] for u in usage),'reported_usd':str(sum((Decimal(str(u['cost'])) for u in usage),Decimal(0)))}}
    first=[v[0] for v in clusters.values()];uk=sum(r['correct'] for r in first)
    rng=random.Random(20260929);blocks=[(sum(r['correct'] for r in rr),len(rr)) for rr in clusters.values()];boot=[]
    for _ in range(3000):
        draw=rng.choices(blocks,k=len(blocks));boot.append(sum(x[0] for x in draw)/sum(x[1] for x in draw))
    boot.sort()
    summary={'split':'test','n':n,'valid':n,'failed_or_missing':0,'correct':k,'accuracy':k/n,'valid_accuracy':k/n,'wilson95':wilson(k,n),'groups':dict(sorted(groups.items())),'predictions':dict(Counter(r['prediction'] for r in items)),'wrong_sources':dict(Counter(r['wrong_source'] for r in items if r['wrong_source'])),'models':dict(Counter(r['response']['model'] for r in records)),'cost':cost,'unique_first_occurrence':{'n':len(first),'correct':uk,'accuracy':uk/len(first),'wilson95':wilson(uk,len(first))},'cluster_bootstrap95':[boot[74],boot[2924]]}
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
