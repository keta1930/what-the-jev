"""Recompute facts from journals; completeness is separate from validity."""
from collections import Counter
import hashlib
import json
import re
from jsonschema import Draft202012Validator
from .plan import conditions, totals, stable, seed
from .rules import legal, payoff, execute, baseline, observation, continues
from .storage import ROOT, GAME, condition_path, read, atomic, now
from pathlib import Path

SCHEMA = Path(__file__).with_name('schema')

def checksum(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def inspect_condition(m,c,result_validator=None,input_validator=None):
    path=condition_path(m,c)
    result_validator=result_validator or Draft202012Validator(json.loads((SCHEMA/'result.schema.json').read_text(encoding='utf-8')))
    input_validator=input_validator or Draft202012Validator(json.loads((SCHEMA/'dataset.schema.json').read_text(encoding='utf-8')))
    inputs=read(path/'inputs.jsonl'); responses=read(path/'responses.jsonl'); events=read(path/'events.jsonl')
    assert not re.search(r'sk-or-v1-[A-Za-z0-9_-]{16,}',json.dumps([inputs,responses,events],ensure_ascii=False)),'Credential-like material found in journal'
    if path.exists():
        assert json.loads((path/'config.json').read_text(encoding='utf-8'))==c,'Frozen config mismatch'
    ii={x['id']:x for x in inputs}; rr={x['id']:x for x in responses}
    assert len(ii)==len(inputs),'Duplicate input IDs'
    assert len(rr)==len(responses),'Duplicate attempt IDs'
    for response in responses: result_validator.validate(response)
    for inp in inputs:
        assert inp['payload']['model']==m['model']
        input_validator.validate({'schema_version':1,'samples':[{'id':inp['id'],'input':{k:v for k,v in inp['payload'].items() if k!='model'}}]})
        assert not any('\u4e00'<=ch<='\u9fff' for ch in json.dumps(inp['payload'],ensure_ascii=False)),'Non-English request'
    per_match={c['id']+f'/m{n:03}':[] for n in range(1,c['matches']+1)}
    for e in events:
        assert e.get('match_id') in per_match,'Event has unknown match ID'
        per_match[e['match_id']].append(e)
    matches=[]; used_inputs=set(); used_responses=set()
    for n,(mid,es) in enumerate(per_match.items(),1):
        history=[]; total=[0]*len(c['players']); pending={}; attempts={}; finished={}; complete=False; reason=None
        cost=0.; missing_cost=0; request_count=0; action_counts=[Counter() for _ in c['players']]; snapshots=Counter()
        for e in es:
            kind=e['kind']
            assert not complete,'Events recorded after match completion'
            if kind in ('match_started','match_resumed'): assert e['seed']==seed(c['id'],n)
            elif kind=='request_started':
                assert e['attempt_id'] not in attempts,'Duplicate request_started'
                assert e['decision_id'] in ii,'Missing actual input'
                assert e['payload_sha256']==stable(ii[e['decision_id']]['payload'])
                attempts[e['attempt_id']]=e
                used_inputs.add(e['decision_id']); request_count+=1
                inp=ii[e['decision_id']]; p=inp['player']; r=len(history)+1
                assert inp['match_id']==mid and inp['round']==r
                offer=int(pending[(r-1)%2]['executed'].split('_')[1]) if inp['stage']=='response' else None
                assert inp['payload']=={'model':m['model'],**observation(c,history,total,p,r,inp['stage'],offer)},'Submitted observation differs from settled state'
            elif kind=='request_finished':
                aid=e['attempt_id']; assert aid in attempts and aid not in finished
                assert attempts[aid]['decision_id']==e['decision_id']
                finished[aid]=e
                assert aid in rr,'Finished request is missing result row'
                used_responses.add(aid)
                assert rr[aid]['error']==e.get('error',rr[aid]['error'])
                raw=e['raw_text']
                try:
                    from game_theory.json_utils import loads
                    parsed=loads(raw) if raw is not None else None
                except ValueError: parsed=raw
                assert rr[aid]['response']==parsed,'Raw transport text differs from preserved result'
                if isinstance(parsed,dict) and parsed.get('model'):
                    snapshots[(str(parsed['model']),str(parsed.get('provider','not returned')))]+=1
                usage=e.get('usage')
                if isinstance(usage,dict) and isinstance(usage.get('cost'),(int,float)) and not isinstance(usage.get('cost'),bool): cost+=usage['cost']
                else: missing_cost+=1
            elif kind=='action':
                p=e['player']; r=len(history)+1
                assert e['round']==r and 0<=p<len(c['players'])
                assert p not in pending,'Duplicate action before settlement'
                proposer=(r-1)%2
                stage=('proposal' if p==proposer else 'response') if c['scenario']=='ultimatum' else 'simultaneous'
                assert e['stage']==stage and e['strategy']==c['players'][p]
                assert e['decision_id']==f'{mid}/r{r:03}/P{p+1}/{stage}'
                assert e['original'] in legal(c['scenario'],stage)
                assert e['executed']==execute(c,n,p,r,e['original'])
                assert e['intervened']==(e['executed']!=e['original'])
                offer=int(pending[proposer]['executed'].split('_')[1]) if stage=='response' else None
                if c['players'][p]=='jev':
                    did=e['decision_id']; aid=e['attempt_id']
                    assert aid in rr and rr[aid]['error'] is None and aid in finished
                    answer=rr[aid]['response']['answers']['action']
                    assert answer['type']=='choice' and answer['choice']==e['original']
                    expected={'model':m['model'],**observation(c,history,total,p,r,stage,offer)}
                    assert ii[did]['payload']==expected,'Observation isolation/history mismatch'
                else:
                    assert e['attempt_id'] is None
                    assert e['original']==baseline(c,n,history,p,r,stage,offer),'Baseline action differs from frozen strategy'
                pending[p]=e
            elif kind=='settlement':
                h=e['record']; r=len(history)+1
                assert e['settlement_id']==f'{mid}/r{r:03}' and h['round']==r
                assert len(pending)==len(c['players']),'Settlement before all actions'
                assert h['original']==[pending[p]['original'] for p in range(len(c['players']))]
                assert h['actions']==[pending[p]['executed'] for p in range(len(c['players']))]
                proposer=(r-1)%2
                assert h['proposer']==(proposer if c['scenario']=='ultimatum' else None)
                rewards=payoff(c['scenario'],h['actions'],proposer)
                assert h['payoffs']==rewards
                total=[round(a+b,10) for a,b in zip(total,rewards)]
                assert h['cumulative']==total,'Cumulative payoff mismatch'
                assert set(h['decision_ids'])=={a['decision_id'] for a in pending.values()}
                for p,a in enumerate(h['actions']): action_counts[p][a]+=1
                assert r<=c['rounds']
                if history: assert continues(c,n,history[-1]['round']),'Continued after random termination'
                history.append(h); pending={}
            elif kind=='match_complete':
                assert not complete and not pending and history,'Invalid or duplicate completion'
                assert len(history)==c['rounds'] or not continues(c,n,len(history)),'Premature completion'
                assert e['settled_rounds']==len(history) and e['cumulative']==total
                complete=True
            elif kind=='match_paused': reason=e['reason']
            elif kind=='validation_failure': assert e['attempt_id'] in rr
            elif kind=='retry_wait': pass
            else: raise ValueError('Unknown event kind: '+kind)
        state='complete' if complete else 'incomplete' if not es else 'dependency_blocked' if any(e['kind']=='match_paused' and e['dependency'] for e in es) else 'paused'
        missing_cost+=sum(aid not in finished for aid in attempts)
        for inp in inputs:
            if inp['match_id']==mid and inp['id'] not in used_inputs:
                r=len(history)+1
                offer=int(pending[(r-1)%2]['executed'].split('_')[1]) if inp['stage']=='response' else None
                assert inp['round']==r
                assert inp['payload']=={'model':m['model'],**observation(c,history,total,inp['player'],r,inp['stage'],offer)}
                used_inputs.add(inp['id'])
        matches.append(dict(id=mid,number=n,status=state,rounds=len(history),cumulative=total,actions=[dict(x) for x in action_counts],requests=request_count,cost_usd_returned=cost,cost_missing_attempts=missing_cost,reason=reason,pending_actions=len(pending),seed=seed(c['id'],n),returned_snapshots=[dict(model=k[0],provider=k[1],attempts=v) for k,v in snapshots.items()]))
    assert used_inputs==set(ii),'Orphan actual input'
    assert used_responses==set(rr),'Orphan raw response'
    return dict(condition_id=c['id'],scenario=c['scenario'],matches=matches),dict(inputs=inputs,responses=responses,events=events)

def validate_batch(m):
    assert m['conditions']==conditions(),'Suite enumeration differs from frozen manifest'
    assert m['totals']==totals(m['conditions'])
    batch=GAME/'output'/'records'/m['batch_id']
    for scenario in dict.fromkeys(c['scenario'] for c in m['conditions']):
        index_path=GAME/'output'/'records'/m['batch_id']/'scenarios'/scenario/'manifest.json'
        assert index_path.exists(),'Missing scenario manifest: '+scenario
        expected_index=dict(batch_id=m['batch_id'],conditions=[c['id'] for c in m['conditions'] if c['scenario']==scenario])
        assert json.loads(index_path.read_text(encoding='utf-8'))==expected_index,'Scenario manifest differs from frozen suite'
    for relative,digest in m['code_hashes'].items():
        snapshot=batch/'code-snapshot'/relative
        assert snapshot.exists() and stable(snapshot.read_text(encoding='utf-8'))==digest,'Frozen code snapshot missing or corrupt'
    state=json.loads((batch/'status.json').read_text(encoding='utf-8')) if (batch/'status.json').exists() else {'matches':{}}
    rv=Draft202012Validator(json.loads((SCHEMA/'result.schema.json').read_text(encoding='utf-8')))
    iv=Draft202012Validator(json.loads((SCHEMA/'dataset.schema.json').read_text(encoding='utf-8')))
    all_matches=[]; hashes={}; costs=0.; missing=0; settled=0; requests=0
    for c in m['conditions']:
        summary,_=inspect_condition(m,c,rv,iv)
        for match in summary['matches']:
            tracked=state['matches'].get(match['id'])
            if match['status']=='complete': assert tracked and tracked['status']=='complete','Status index differs from journal'
            elif tracked:
                assert tracked['status']!='complete','Unsettled match marked complete'
                match['status']=tracked['status']; match['reason']=tracked.get('reason',match['reason'])
            all_matches.append(dict(condition_id=c['id'],scenario=c['scenario'],**match))
            costs+=match['cost_usd_returned']; missing+=match['cost_missing_attempts']; settled+=match['rounds']; requests+=match['requests']
        path=condition_path(m,c)
        if path.exists():
            atomic(path/'summary.json',summary)
            for name in ('config.json','inputs.jsonl','responses.jsonl','events.jsonl'):
                p=path/name
                if p.exists(): hashes[str(p.relative_to(ROOT))]=checksum(p)
    counts=dict(Counter(x['status'] for x in all_matches))
    result=dict(batch_id=m['batch_id'],validated_at=now(),valid=True,complete=counts.get('complete',0)==m['totals']['matches'],counts=counts,settled_rounds=settled,request_attempts=requests,cost_usd_returned=costs,cost_missing_attempts=missing,expected=m['totals'],manifest_sha256=m['sha256'])
    atomic(batch/'summary.json',dict(**result,matches=all_matches))
    atomic(batch/'checksums.json',hashes)
    atomic(batch/'validation.json',result)
    return result
