"""Offline SocialIQA scoring; formal responses and historical billing are separate."""
from collections import Counter,defaultdict
from pathlib import Path
import json, math, random

ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def lines(p):return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l]
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
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
    events=lines(ROOT/'result/attempts.jsonl');ends=[e for e in events if e['event']=='end'];cost={}
    for phase in ['debug','test']:
        ee=[e for e in ends if e['split']==phase];uu=[(e.get('response') or {}).get('usage') or {} for e in ee]
        attempts=sum(e['event']=='start' and e['split']==phase for e in events)
        cost[phase]={'attempts':attempts,'input_tokens':sum(u.get('input_tokens',0) for u in uu),'output_tokens':sum(u.get('output_tokens',0) for u in uu),'reported_usd':sum(u.get('cost',0) for u in uu),'unknown_cost_attempts':attempts-sum(isinstance(u.get('cost'),(int,float)) for u in uu)}
    first=[v[0] for v in clusters.values()];uk=sum(r['correct'] for r in first)
    rng=random.Random(20260929);blocks=[(sum(r['correct'] for r in rr),len(rr)) for rr in clusters.values()];boot=[]
    for _ in range(3000):
        draw=rng.choices(blocks,k=len(blocks));boot.append(sum(x[0] for x in draw)/sum(x[1] for x in draw))
    boot.sort()
    summary={'split':'test','n':n,'valid':n,'failed_or_missing':0,'correct':k,'accuracy':k/n,'valid_accuracy':k/n,'wilson95':wilson(k,n),'groups':dict(sorted(groups.items())),'predictions':dict(Counter(r['prediction'] for r in items)),'wrong_sources':dict(Counter(r['wrong_source'] for r in items if r['wrong_source'])),'models':dict(Counter(r['response']['model'] for r in records)),'technical_failed_attempts':sum(e.get('error') is not None for e in ends),'technical_failure_statuses':dict(Counter(str(e.get('status')) for e in ends if e.get('error') is not None)),'cost':cost,'total_charged_or_reserved_usd':sum(v['reported_usd']+v['unknown_cost_attempts']*.01 for v in cost.values()),'unique_first_occurrence':{'n':len(first),'correct':uk,'accuracy':uk/len(first),'wilson95':wilson(uk,len(first))},'cluster_bootstrap95':[boot[74],boot[2924]]}
    out=ROOT/'report/generated';out.mkdir(exist_ok=True)
    write(out/'summary.json',summary)
    (out/'items.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in items),encoding='utf-8')
    print(json.dumps({'n':n,'correct':k,'accuracy':k/n}))

if __name__=='__main__':main()
