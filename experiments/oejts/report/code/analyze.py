"""Recompute numerical scale results from responses; no questionnaire is needed."""
from collections import Counter
from decimal import Decimal
from pathlib import Path
import json,statistics

ROOT=Path(__file__).resolve().parents[2]
RULES={'IE':(30,[-3,-7,-11,15,-19,23,27,-31],'I','E'),
       'SN':(12,[4,8,12,16,20,-24,-28,32],'S','N'),
       'FT':(30,[-2,6,10,-14,-18,22,-26,-30],'F','T'),
       'JP':(18,[1,5,-9,13,-17,21,-25,29],'J','P')}

def score(choices):
    if len(choices)!=32 or any(type(x) is not int or x not in range(1,6) for x in choices):raise ValueError('Expected 32 integer positions in 1..5')
    scores={a:base+sum((1 if q>0 else -1)*choices[abs(q)-1] for q in terms) for a,(base,terms,lo,hi) in RULES.items()}
    return {'type':''.join(hi if scores[a]>24 else lo for a,(_,_,lo,hi) in RULES.items()),'scores':scores,'boundary_axes':[a for a,v in scores.items() if v==24]}

def main():
    rounds=[];records=[];counts=[Counter() for _ in range(32)]
    for rd in range(1,11):
        rows=[json.loads(l) for l in (ROOT/f'result/responses_{rd}.jsonl').read_text(encoding='utf-8').splitlines()]
        byid={r['id']:r for r in rows};assert len(rows)==len(byid)==32
        assert set(byid)=={f'oejts-q{q:02}' for q in range(1,33)}
        values=[]
        for n in range(1,33):
            row=byid[f'oejts-q{n:02}'];assert row['error'] is None
            answer=row['response']['answers']['position'];assert answer['type']=='choice'
            value=int(answer['choice']);values.append(value);counts[n-1][value]+=1
        rounds.append({'round':rd,**score(values)});records.extend(rows)
    dims={a:{'mean':statistics.mean(r['scores'][a] for r in rounds),'min':min(r['scores'][a] for r in rounds),'max':max(r['scores'][a] for r in rounds),'mean_distance_from_24':statistics.mean(abs(r['scores'][a]-24) for r in rounds),'boundary_rounds':sum(r['scores'][a]==24 for r in rounds)} for a in RULES}
    usage=[r['response']['usage'] for r in records]
    summary={'scale':'OEJTS 1.2','official_mbti':False,'completed_answers':len(records),'question_count':32,'rounds':rounds,'types':dict(Counter(r['type'] for r in rounds)),'models':sorted({r['response']['model'] for r in records}),'known_cost_usd':str(sum((Decimal(str(u['cost'])) for u in usage),Decimal(0))),'input_tokens':sum(u['input_tokens'] for u in usage),'output_tokens':sum(u['output_tokens'] for u in usage),'unknown_charge_requests':0,'dimensions':dims,'item_stability':[{'question':n,'counts':dict(c),'modal_agreement':max(c.values())/sum(c.values())} for n,c in enumerate(counts,1)],'fully_stable_questions':sum(len(c)==1 for c in counts)}
    (ROOT/'report/generated/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'answers':len(records),'types':summary['types'],'cost':summary['known_cost_usd']}))

if __name__=='__main__':main()
