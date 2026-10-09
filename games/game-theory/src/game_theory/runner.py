"""Resumable game execution with immutable observations and raw journals."""
import concurrent.futures
import copy
import json
import os
import re
import signal
import threading
import time
from pathlib import Path
from http.client import HTTPException
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime

from game_theory.json_utils import loads
from game_theory.persistence import locked_output
from .plan import stable, seed
from .rules import observation, legal, baseline, execute, payoff, continues
from .storage import GAME, ROOT, now, atomic, append, read, condition_path


def credential():
    value=os.environ.get('OPENROUTER_API_KEY')
    if value:
        if not re.fullmatch(r'sk-or-v1-[A-Za-z0-9_-]+',value.strip()):
            raise ValueError('OPENROUTER_API_KEY has invalid format')
        return value.strip()
    text=(ROOT.parent/'OpenRouter.txt').read_text(encoding='utf-8-sig')
    keys=set(re.findall(r'sk-or-v1-[A-Za-z0-9_-]+',text))
    if len(keys)!=1: raise ValueError('Credential file must contain exactly one unique OpenRouter key')
    return keys.pop()


def transport(payload,key,endpoint):
    request=Request(endpoint,data=json.dumps(payload,ensure_ascii=False,allow_nan=False).encode(),method='POST',headers={'Content-Type':'application/json','Authorization':'Bearer '+key})
    try:
        with urlopen(request,timeout=45) as response:
            return response.status,response.read().decode('utf-8',errors='replace'),dict(response.headers)
    except HTTPError as exc:
        with exc: return exc.code,exc.read().decode('utf-8',errors='replace'),dict(exc.headers)


class DependencyBlocked(Exception): pass
class MatchPaused(Exception): pass

def retry_after(headers):
    value=next((v for k,v in headers.items() if k.lower()=='retry-after'),None)
    if value is None:return None,0
    try: seconds=float(value)
    except (ValueError,TypeError):
        try: seconds=(parsedate_to_datetime(value)-datetime.now(timezone.utc)).total_seconds()
        except (ValueError,TypeError,OverflowError):seconds=0
    return value,max(0,min(60,seconds))


class Gate:
    """Global API budget and circuit state, shared by independent matches."""
    def __init__(self, stop):
        self.condition=threading.Condition()
        self.limit=4; self.active=0; self.failure_streak=0
        self.blocked=None; self.stop=stop; self.circuit=False
        self.total_requests=0

    def enter(self):
        with self.condition:
            while self.active>=self.limit or self.circuit:
                if self.blocked or self.stop.is_set(): raise DependencyBlocked(self.blocked or 'interrupted')
                self.condition.wait(.2)
            if self.blocked or self.stop.is_set(): raise DependencyBlocked(self.blocked or 'interrupted')
            self.active+=1; self.total_requests+=1

    def leave(self,status,network=False):
        with self.condition:
            self.active-=1
            transient=network or status==429 or status is not None and status>=500
            if status in (401,402,403,404): self.blocked=f'Global dependency HTTP {status}'
            if transient:
                self.limit=max(1,self.limit//2); self.failure_streak+=1
                if self.failure_streak>=10: self.circuit=True
            else:
                self.failure_streak=0
                if status is not None and 200<=status<300: self.limit=min(8,self.limit+1)
            self.condition.notify_all()


class ConditionJournal:
    def __init__(self,path,c):
        self.path=path; self.lock=threading.RLock(); path.mkdir(parents=True,exist_ok=True)
        config=path/'config.json'
        if config.exists():
            if json.loads(config.read_text(encoding='utf-8'))!=c: raise ValueError('Frozen condition config differs')
        else: atomic(config,c)
        self.events=read(path/'events.jsonl',repair=True)
        self.inputs={x['id']:x for x in read(path/'inputs.jsonl',repair=True)}
        self.responses=read(path/'responses.jsonl',repair=True)
        self.response_by_id={r['id']:r for r in self.responses}
        if len(self.response_by_id)!=len(self.responses): raise ValueError('Duplicate attempt ID')
        # Raw transport completion is persisted before its result row. Recover
        # that narrow local window without issuing another paid request.
        for e in self.events:
            if e['kind']=='request_finished' and e['attempt_id'] not in self.response_by_id:
                raw=e.get('raw_text')
                error=e.get('error')
                try: response=loads(raw) if raw is not None else None
                except ValueError:
                    response=raw
                    error=error or {'type':'invalid_json','message':'Response is not valid strict JSON'}
                status=e.get('http_status')
                if 'error' not in e and status is None:
                    error={'type':'network','message':'Transport completion recovered; original network error detail was not durably recorded'}
                elif status is not None and not 200<=status<300:
                    error={'type':'http','status':status,'message':f'HTTP {status}'}
                row=dict(id=e['attempt_id'],response=response,error=error)
                append(path/'responses.jsonl',row)
                self.responses.append(row); self.response_by_id[row['id']]=row
        self.attempts={}
        for e in self.events:
            if e['kind']=='request_started': self.attempts.setdefault(e['decision_id'],[]).append(e)

    def event(self,kind,**values):
        with self.lock:
            e=dict(kind=kind,time=now(),**values)
            append(self.path/'events.jsonl',e); self.events.append(e)
            if kind=='request_started': self.attempts.setdefault(e['decision_id'],[]).append(e)
            return e

    def input(self,decision_id,payload,**ids):
        with self.lock:
            if decision_id in self.inputs:
                old=self.inputs[decision_id]
                if old['payload']!=payload: raise ValueError('Recovered observation differs from saved input: '+decision_id)
                return
            x=dict(id=decision_id,payload=payload,**ids)
            append(self.path/'inputs.jsonl',x); self.inputs[decision_id]=x

    def response(self,value):
        with self.lock:
            if value['id'] in self.response_by_id: raise ValueError('Duplicate response attempt')
            append(self.path/'responses.jsonl',value)
            self.responses.append(value); self.response_by_id[value['id']]=value

    def model_choice(self,decision_id,options):
        for attempt in self.attempts.get(decision_id,[]):
            r=self.response_by_id.get(attempt['attempt_id'])
            if r and r['error'] is None:
                answers=r['response'].get('answers') if isinstance(r['response'],dict) else None
                answer=answers.get('action') if isinstance(answers,dict) else None
                if isinstance(answer,dict) and answer.get('type')=='choice' and isinstance(answer.get('choice'),str) and answer['choice'] in options:
                    return answer['choice'],r['id']
        return None


class Runner:
    def __init__(self,manifest,send=transport,key=None,wait=time.sleep):
        self.m=manifest; self.send=send; self.key=key; self.wait=wait
        self.stop=threading.Event(); self.gate=Gate(self.stop)
        self.journals={}; self.journal_users={}; self.journal_lock=threading.Lock(); self.state_lock=threading.RLock()
        self.batch=GAME/'output'/'records'/manifest['batch_id']
        self.state_path=self.batch/'status.json'
        self.state=json.loads(self.state_path.read_text(encoding='utf-8')) if self.state_path.exists() else {'matches':{},'phase':'planned'}
        self.started=time.monotonic(); self.last_save=0

    def journal(self,c):
        with self.journal_lock:
            if c['id'] not in self.journals: self.journals[c['id']]=ConditionJournal(condition_path(self.m,c),c)
            self.journal_users[c['id']]=self.journal_users.get(c['id'],0)+1
            return self.journals[c['id']]

    def status(self,match_id,status,**extra):
        with self.state_lock:
            self.state['matches'][match_id]=dict(status=status,updated=now(),**extra)
            if time.monotonic()-self.last_save>3: self.save()

    def save(self):
        with self.state_lock:
            self.state['updated']=now(); self.state['dependency']=self.gate.blocked
            self.state['api_concurrency']=self.gate.limit
            self.state['requests_this_process']=self.gate.total_requests
            self.state['counts']={s:sum(v['status']==s for v in self.state['matches'].values()) for s in ('complete','paused','dependency_blocked','incomplete')}
            self.state['not_started']=self.m['totals']['matches']-len(self.state['matches'])
            atomic(self.state_path,self.state); self.last_save=time.monotonic()

    def request(self,j,c,match_id,decision_id,payload,options):
        cached=j.model_choice(decision_id,options)
        if cached: return cached
        if self.key is None: self.key=credential()
        # A new scan may retry failed logical decisions. All prior attempts remain.
        for index in range(3):
            self.gate.enter()
            attempt_id=decision_id+'/a'+str(len(j.attempts.get(decision_id,[]))+1)
            try:
                j.event('request_started',match_id=match_id,decision_id=decision_id,attempt_id=attempt_id,payload_sha256=stable(payload),possible_remote_replay=any(a['attempt_id'] not in j.response_by_id for a in j.attempts.get(decision_id,[])))
            except BaseException:
                self.gate.leave(None)
                raise
            started=time.monotonic(); status=None; headers={}; raw=None; network=False
            try:
                status,raw,headers=self.send(payload,self.key,self.m['endpoint'])
                error=None
                try: response=loads(raw)
                except ValueError:
                    response=raw; error={'type':'invalid_json','message':'Response is not valid strict JSON'}
                if not 200<=status<300: error={'type':'http','status':status,'message':f'HTTP {status}'}
            except (OSError,HTTPException) as exc:
                network=True; response=None; error={'type':'network','message':str(exc).replace(self.key,'[REDACTED]')}
            finally:
                self.gate.leave(status,network)
            # Complete raw text lives in the attempt event; parsed response keeps
            # the exact pre-existing result schema and unique attempt IDs.
            if raw is not None: raw=raw.replace(self.key,'[REDACTED]')
            retry_value,retry_seconds=retry_after(headers)
            j.event('request_finished',match_id=match_id,decision_id=decision_id,attempt_id=attempt_id,http_status=status,elapsed_seconds=time.monotonic()-started,raw_text=raw,error=error,retry_after=retry_value,usage=response.get('usage') if isinstance(response,dict) else None)
            j.response(dict(id=attempt_id,response=response,error=error))
            if status==400 and isinstance(response,dict) and any(text in json.dumps(response).lower() for text in ('model not found','no endpoints','model is not available','unknown model','invalid model')):
                self.gate.blocked='Pinned model unavailable (HTTP 400)'
            if self.gate.blocked: raise DependencyBlocked(self.gate.blocked)
            if error is None:
                cached=j.model_choice(decision_id,options)
                if cached: return cached
                j.event('validation_failure',match_id=match_id,decision_id=decision_id,attempt_id=attempt_id,message='Missing or illegal answers.action choice/type')
                raise MatchPaused('Semantic response failure')
            transient=network or status==429 or status is not None and status>=500
            if not transient or index==2: raise MatchPaused(error['message'])
            if self.gate.circuit: raise MatchPaused('Global transient-failure circuit opened')
            delay=max((2,5)[index],retry_seconds)
            j.event('retry_wait',match_id=match_id,decision_id=decision_id,seconds=delay)
            self.wait(delay)
        raise AssertionError('unreachable')

    def play(self,c,match):
        if self.stop.is_set(): return
        j=self.journal(c)
        try:
            return self._play(c,match,j)
        finally:
            with self.journal_lock:
                self.journal_users[c['id']]-=1
                if not self.journal_users[c['id']]:
                    del self.journals[c['id']]
                    del self.journal_users[c['id']]

    def _play(self,c,match,j):
        match_id=c['id']+f'/m{match:03}'
        if self.stop.is_set(): return
        with j.lock:
            events=[e for e in j.events if e.get('match_id')==match_id]
        if any(e['kind']=='match_complete' for e in events):
            self.status(match_id,'complete',settled_rounds=next(e['settled_rounds'] for e in events if e['kind']=='match_complete')); return
        history=[e['record'] for e in events if e['kind']=='settlement']
        if [h['round'] for h in history]!=list(range(1,len(history)+1)): raise ValueError('Non-contiguous or duplicate settlement')
        totals=history[-1]['cumulative'][:] if history else [0]*len(c['players'])
        saved_actions={e['decision_id']:e for e in events if e['kind']=='action'}
        j.event('match_resumed' if events else 'match_started',match_id=match_id,seed=seed(c['id'],match),scan=self.state.get('scan',0))
        self.status(match_id,'incomplete',settled_rounds=len(history))
        try:
            if history and (len(history)==c['rounds'] or not continues(c,match,len(history))):
                j.event('match_complete',match_id=match_id,settled_rounds=len(history),cumulative=totals)
                self.status(match_id,'complete',settled_rounds=len(history)); return
            for r in range(len(history)+1,c['rounds']+1):
                if self.stop.is_set(): raise MatchPaused('Interrupted before next round')
                originals=[None]*len(c['players']); actions=[None]*len(c['players']); decision_ids=[]
                proposer=(r-1)%2
                order=[proposer,1-proposer] if c['scenario']=='ultimatum' else list(range(len(c['players'])))
                for player in order:
                    stage=('proposal' if player==proposer else 'response') if c['scenario']=='ultimatum' else 'simultaneous'
                    offer=int(actions[proposer].split('_')[1]) if stage=='response' else None
                    decision_id=f'{match_id}/r{r:03}/P{player+1}/{stage}'
                    decision_ids.append(decision_id)
                    if decision_id in saved_actions:
                        e=saved_actions[decision_id]; original=e['original']; actual=e['executed']
                    else:
                        # Only settled history enters simultaneous observations;
                        # originals/actions collected in this round never enter.
                        inp=observation(c,history,totals,player,r,stage,offer)
                        payload={'model':self.m['model'],**inp}
                        if c['players'][player]=='jev':
                            j.input(decision_id,payload,match_id=match_id,round=r,player=player,stage=stage)
                            original,attempt_id=self.request(j,c,match_id,decision_id,payload,legal(c['scenario'],stage))
                        else:
                            original=baseline(c,match,history,player,r,stage,offer); attempt_id=None
                        actual=execute(c,match,player,r,original)
                        e=j.event('action',match_id=match_id,decision_id=decision_id,round=r,player=player,stage=stage,strategy=c['players'][player],original=original,executed=actual,intervened=original!=actual,attempt_id=attempt_id)
                        saved_actions[decision_id]=e
                    originals[player]=original; actions[player]=actual
                rewards=payoff(c['scenario'],actions,proposer)
                totals=[round(a+b,10) for a,b in zip(totals,rewards)]
                record=dict(round=r,original=originals,actions=actions,payoffs=rewards,cumulative=totals[:],decision_ids=decision_ids,proposer=proposer if c['scenario']=='ultimatum' else None)
                j.event('settlement',match_id=match_id,settlement_id=f'{match_id}/r{r:03}',record=record)
                history.append(record)
                if not continues(c,match,r): break
            j.event('match_complete',match_id=match_id,settled_rounds=len(history),cumulative=totals)
            self.status(match_id,'complete',settled_rounds=len(history))
        except (MatchPaused,DependencyBlocked) as exc:
            blocked=isinstance(exc,DependencyBlocked) and self.gate.blocked is not None
            j.event('match_paused',match_id=match_id,reason=str(exc),dependency=blocked,settled_rounds=len(history))
            self.status(match_id,'dependency_blocked' if blocked else 'paused',reason=str(exc),settled_rounds=len(history))

    def dispatch(self,jobs,workers=8):
        iterator=iter(jobs)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            pending={}
            def fill():
                while len(pending)<workers and not self.stop.is_set():
                    try: c,n=next(iterator)
                    except StopIteration: break
                    if self.gate.blocked and 'jev' in c['players']: continue
                    pending[pool.submit(self.play,c,n)]=(c,n)
            fill()
            last=time.monotonic()
            while pending:
                done,_=concurrent.futures.wait(pending,timeout=1,return_when=concurrent.futures.FIRST_COMPLETED)
                for f in done:
                    pending.pop(f)
                    try:f.result()
                    except BaseException:
                        self.stop.set()
                        with self.gate.condition:self.gate.condition.notify_all()
                        raise
                # Let the coordinator drain in-flight calls before probing.
                if self.gate.circuit and self.gate.active==0:
                    self.recover_circuit()
                fill()
                if time.monotonic()-last>=20:
                    self.save(); print(json.dumps({'phase':self.state['phase'],'counts':self.state['counts'],'not_started':self.state['not_started'],'api_concurrency':self.gate.limit,'requests':self.gate.total_requests}),flush=True); last=time.monotonic()
        self.save()

    def recover_circuit(self):
        windows=self.state.get('circuit_windows',0)
        if windows>=2:
            self.gate.blocked='Persistent transient API failures after two recovery windows'
        else:
            self.state['circuit_windows']=windows+1
            append(self.batch/'events.jsonl',dict(kind='circuit_wait',time=now(),window=windows+1,seconds=300))
            self.save()
            # Wait interruptibly, then allow exactly one request until success.
            for _ in range(300):
                if self.stop.is_set(): break
                self.wait(1)
            self.gate.limit=1; self.gate.failure_streak=9
        with self.gate.condition:
            self.gate.circuit=False; self.gate.condition.notify_all()

    def run(self,rules_only=False):
        old_handler=None
        if threading.current_thread() is threading.main_thread():
            old_handler=signal.signal(signal.SIGINT,lambda *_: self.stop.set())
        try:
            with locked_output(self.batch/'batch.lock'):
                append(self.batch/'events.jsonl',dict(kind='process_started',time=now(),code_hashes={str(p.relative_to(ROOT)):stable(p.read_text(encoding='utf-8')) for p in Path(__file__).parent.glob('*.py')},resume=True))
                jobs=[(c,n) for c in self.m['conditions'] for n in range(1,c['matches']+1)]
                self.state['phase']='rules'; self.dispatch([(c,n) for c,n in jobs if 'jev' not in c['players']])
                if not rules_only and not self.stop.is_set():
                    self.state['phase']='smoke'
                    smoke=[]
                    for s in dict.fromkeys(c['scenario'] for c in self.m['conditions']):
                        c=next(c for c in self.m['conditions'] if c['scenario']==s and c['variant']=='base' and c['rounds']==1 and set(c['players'])=={'jev'})
                        smoke.append((c,1))
                    self.dispatch(smoke,workers=1)
                    smoke_ok=all(self.state['matches'].get(c['id']+'/m001',{}).get('status')=='complete' for c,_ in smoke)
                    if smoke_ok:
                        for scan in range(3):
                            self.state['scan']=scan; self.state['phase']='batch' if scan==0 else 'recovery'
                            remaining=[(c,n) for c,n in jobs if 'jev' in c['players'] and self.state['matches'].get(c['id']+f'/m{n:03}',{}).get('status')!='complete']
                            if not remaining or self.gate.blocked or self.stop.is_set(): break
                            self.dispatch(remaining)
                    else:
                        self.state['smoke_failure']=True
                        for c,n in jobs:
                            mid=c['id']+f'/m{n:03}'
                            if 'jev' in c['players'] and mid not in self.state['matches']:
                                self.status(mid,'incomplete',reason='Not submitted: real smoke gate did not pass',settled_rounds=0)
                self.state['phase']='interrupted' if self.stop.is_set() else 'dependency_blocked' if self.gate.blocked else 'finished_scan'
                if self.gate.blocked:
                    for c,n in jobs:
                        mid=c['id']+f'/m{n:03}'
                        if 'jev' in c['players'] and self.state['matches'].get(mid,{}).get('status')!='complete': self.status(mid,'dependency_blocked',reason=self.gate.blocked,settled_rounds=self.state['matches'].get(mid,{}).get('settled_rounds',0))
                self.save()
        finally:
            if old_handler is not None: signal.signal(signal.SIGINT,old_handler)
        return self.state
