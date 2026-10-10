"""Test journaled execution, failures and resumable decisions."""
from pathlib import Path
import copy
import json
import threading
import pytest
from jsonschema import validate
from game_theory import runner, storage
from game_theory.plan import conditions, totals, MODEL, ENDPOINT, seed
from game_theory.rules import baseline, observation, execute, continues

@pytest.fixture
def setup(tmp_path,monkeypatch):
    game=tmp_path/'games'/'game-theory'
    monkeypatch.setattr(storage,'GAME',game)
    monkeypatch.setattr(runner,'GAME',game)
    def make(s='prisoner-dilemma',players=('jev','jev'),rounds=20):
        c=copy.deepcopy(next(c for c in conditions() if c['scenario']==s and c['players']==list(players) and c['rounds']==rounds and c['variant']=='base'))
        c['matches']=1
        return {'batch_id':'test','model':MODEL,'endpoint':ENDPOINT,'conditions':[c],'totals':totals([c])},c
    return make

def success(payload,key,endpoint):
    option=next(iter(payload['questions']['action']['criteria']))
    return 200,json.dumps({'model':MODEL,'provider':'test-double','answers':{'action':{'type':'choice','choice':option}},'usage':{'cost':.001}}),{}

def events(m,c): return storage.read(storage.condition_path(m,c)/'events.jsonl')

def test_success_resume_does_not_repeat_requests_or_settlements(setup):
    m,c=setup(); calls=[]
    def send(*args): calls.append(args[0]); return success(*args)
    r=runner.Runner(m,send,key='test-key'); r.play(c,1)
    assert len(calls)==40
    first=events(m,c); settlements=[e for e in first if e['kind']=='settlement']
    assert len(settlements)==20
    assert settlements[-1]['record']['cumulative']==[60,60]
    r.play(c,1); assert len(calls)==40 and events(m,c)==first
    assert len(storage.read(storage.condition_path(m,c)/'responses.jsonl'))==40
    for payload in calls:
        rno=payload['state']['round']
        assert all(h['round']<rno for h in payload['state']['settled_history'])
        assert 'original' not in json.dumps(payload['state']['settled_history'])

def test_success_response_before_action_survives_crash(setup,monkeypatch):
    m,c=setup(rounds=1); calls=[]
    def send(*args): calls.append(1); return success(*args)
    old=runner.ConditionJournal.event
    crash=[True]
    def event(self,kind,**kwargs):
        if kind=='action' and crash[0]: crash[0]=False; raise RuntimeError('power-loss')
        return old(self,kind,**kwargs)
    monkeypatch.setattr(runner.ConditionJournal,'event',event)
    r=runner.Runner(m,send,key='test-key')
    with pytest.raises(RuntimeError): r.play(c,1)
    assert len(calls)==1
    r.play(c,1); assert len(calls)==2
    assert sum(e['kind']=='settlement' for e in events(m,c))==1

def test_settlement_before_completion_survives_crash(setup,monkeypatch):
    m,c=setup(rounds=1); calls=[]
    def send(*args): calls.append(1); return success(*args)
    old=runner.ConditionJournal.event; crash=[True]
    def event(self,kind,**kwargs):
        if kind=='match_complete' and crash[0]: crash[0]=False; raise RuntimeError('power-loss')
        return old(self,kind,**kwargs)
    monkeypatch.setattr(runner.ConditionJournal,'event',event)
    r=runner.Runner(m,send,key='test-key')
    with pytest.raises(RuntimeError): r.play(c,1)
    r.play(c,1)
    assert len(calls)==2
    assert sum(e['kind']=='settlement' for e in events(m,c))==1

def test_sequential_offer_and_role_alternation(setup):
    m,c=setup(s='ultimatum'); calls=[]
    def send(*args): calls.append(args[0]); return success(*args)
    runner.Runner(m,send,key='test-key').play(c,1)
    assert len(calls)==40
    for i in range(20):
        proposal,response=[x['state'] for x in calls[i*2:i*2+2]]
        assert proposal['role']=='proposal' and 'current_offer_to_responder' not in proposal
        assert response['role']=='response' and response['current_offer_to_responder']==0
        assert proposal['player']==('P1' if i%2==0 else 'P2')

def test_semantic_failure_is_not_action_and_keeps_schema(setup):
    m,c=setup(rounds=1)
    r=runner.Runner(m,lambda *_:(200,'{"answers":{"action":{"type":"choice","choice":"bogus"}}}',{}),key='test-key')
    r.play(c,1)
    es=events(m,c)
    assert any(e['kind']=='validation_failure' for e in es)
    assert not any(e['kind'] in ('action','settlement') for e in es)
    schema=json.loads((Path(__file__).resolve().parents[1]/'src/game_theory/schema'/'result.schema.json').read_text(encoding='utf-8'))
    for row in storage.read(storage.condition_path(m,c)/'responses.jsonl'):
        assert row['error'] is None; validate(row,schema)

@pytest.mark.parametrize('body',[None,[],{'answers':None},{'answers':[]},{'answers':{'action':None}},{'answers':{'action':'cooperate'}},{'answers':{'action':{'type':'score','choice':'cooperate'}}},{'answers':{'action':{'type':'choice','choice':True}}}])
def test_malformed_answer_shape_pauses_only_match(setup,body):
    m,c=setup(rounds=1)
    r=runner.Runner(m,lambda *_:(200,json.dumps(body),{}),key='test-key')
    r.play(c,1)
    assert r.state['matches'][c['id']+'/m001']['status']=='paused'
    assert any(e['kind']=='validation_failure' for e in events(m,c))
    assert not any(e['kind']=='action' for e in events(m,c))

def test_retry_after_case_date_and_cap():
    from datetime import datetime,timedelta,timezone
    from email.utils import format_datetime
    assert runner.retry_after({'retry-after':'200'})==('200',60)
    assert runner.retry_after({'RETRY-AFTER':'-4'})==('-4',0)
    date=format_datetime(datetime.now(timezone.utc)+timedelta(seconds=40),usegmt=True)
    raw,seconds=runner.retry_after({'Retry-After':date})
    assert raw==date and 38<seconds<=40
    assert runner.retry_after({'Retry-After':'bad'})==('bad',0)

def test_network_retry_unique_attempts_and_401_stop(setup):
    m,c=setup(rounds=1); calls=[]; waits=[]
    def send(*args):
        calls.append(1)
        if len(calls)<3: raise OSError('temporarily offline')
        return success(*args)
    r=runner.Runner(m,send,key='test-key',wait=waits.append); r.play(c,1)
    assert len(calls)==4 and waits==[2,5]
    responses=storage.read(storage.condition_path(m,c)/'responses.jsonl')
    assert len({x['id'] for x in responses})==4
    m['batch_id']='unauthorized'
    r=runner.Runner(m,lambda *_:(401,'{"error":{"message":"invalid"}}',{}),key='test-key')
    r.play(c,1); assert r.gate.blocked=='Global dependency HTTP 401'
    assert len(storage.read(storage.condition_path(m,c)/'responses.jsonl'))==1
    r.play(c,1); assert len(storage.read(storage.condition_path(m,c)/'responses.jsonl'))==1

def test_partial_tail_repair_refuses_complete_corruption(tmp_path):
    p=tmp_path/'journal.jsonl'
    p.write_bytes(b'{"id":"ok"}\n{"id":')
    assert storage.read(p,repair=True)==[{'id':'ok'}]
    assert p.read_bytes()==b'{"id":"ok"}\n'
    p.write_bytes(b'{"id":"ok"}\nnot json\n')
    with pytest.raises(ValueError): storage.read(p,repair=True)

def test_streams_history_noise_and_baseline_definitions(setup):
    m,c=setup(players=('tit_for_tat','cooperate'))
    h=[dict(round=1,actions=['cooperate','defect'],original=['cooperate','defect'],payoffs=[0,5])]
    assert baseline(c,1,h,0,2,'simultaneous')=='defect'
    c['history_window']=0
    assert baseline(c,1,h,0,2,'simultaneous')=='cooperate'
    c['intervention']=10
    assert execute(c,1,0,10,'cooperate')=='defect'
    assert execute(c,1,1,10,'cooperate')=='cooperate'
    assert execute(c,1,0,9,'cooperate')=='cooperate'
    assert len({seed(c['id'],1,p,2,stream) for p in range(2) for stream in ('noise','strategy','termination')})==6
    c['horizon']='geometric'
    a=[continues(c,1,r) for r in range(1,101)]
    assert a==[continues(c,1,r) for r in range(1,101)]
    assert any(not x for x in a)

def test_parallel_matches_and_os_lock(setup):
    m,c=setup(rounds=1); c['matches']=3; m['totals']=totals([c])
    r=runner.Runner(m,success,key='test-key')
    r.dispatch([(c,n) for n in (1,2,3)],workers=3)
    es=events(m,c)
    assert len([e for e in es if e['kind']=='settlement'])==3
    assert len({e['settlement_id'] for e in es if e['kind']=='settlement'})==3
    from game_theory.persistence import locked_output
    r.batch.mkdir(parents=True,exist_ok=True)
    with locked_output(r.batch/'batch.lock'):
        with pytest.raises(ValueError): r.run(rules_only=True)

def test_gate_limits_and_two_circuit_recovery_windows(setup):
    m,c=setup(rounds=1);waits=[]
    r=runner.Runner(m,success,key='test-key',wait=waits.append)
    assert r.gate.limit==4
    for _ in range(20):r.gate.enter();r.gate.leave(200)
    assert r.gate.limit==8
    r.gate.enter();r.gate.leave(429)
    assert r.gate.limit==4
    for _ in range(9):r.gate.enter();r.gate.leave(503)
    assert r.gate.circuit
    for window in (1,2):
        r.recover_circuit()
        assert not r.gate.circuit and r.gate.limit==1
        assert r.state['circuit_windows']==window
        r.gate.enter();r.gate.leave(503)
        assert r.gate.circuit
    r.recover_circuit()
    assert r.gate.blocked=='Persistent transient API failures after two recovery windows'
    assert waits==[1]*600
    with pytest.raises(runner.DependencyBlocked):r.gate.enter()

def test_persistence_failure_stops_dispatch_and_releases_gate(setup,monkeypatch):
    m,c=setup(rounds=1);calls=[]
    def send(*args):calls.append(1);return success(*args)
    old=runner.ConditionJournal.event
    def fail_start(self,kind,**kwargs):
        if kind=='request_started':raise OSError('test disk unavailable')
        return old(self,kind,**kwargs)
    monkeypatch.setattr(runner.ConditionJournal,'event',fail_start)
    r=runner.Runner(m,send,key='test-key')
    with pytest.raises(OSError,match='disk unavailable'):r.dispatch([(c,1)],workers=1)
    assert r.stop.is_set() and r.gate.active==0 and calls==[]

def test_interruption_after_partial_submission_is_not_dependency_failure(setup):
    m,c=setup(rounds=1);r=None
    def send(*args):
        r.stop.set()
        return success(*args)
    r=runner.Runner(m,send,key='test-key');r.play(c,1)
    assert r.state['matches'][c['id']+'/m001']['status']=='paused'
    es=events(m,c)
    assert sum(e['kind']=='action' for e in es)==1
    assert not any(e['kind']=='settlement' for e in es)
    paused=next(e for e in es if e['kind']=='match_paused')
    assert not paused['dependency'] and r.gate.blocked is None
