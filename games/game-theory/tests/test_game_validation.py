"""Test recomputation and source corruption detection."""
import copy
import json
import pytest
from game_theory import runner,storage,validate as checks
from game_theory.plan import conditions,totals,MODEL,ENDPOINT
from game_theory.rules import baseline,legal
from game_theory.html import js,esc

def test_full_journal_recomputation_and_corruption_detection(tmp_path,monkeypatch):
    game=tmp_path/'games'/'game-theory'
    for mod in (runner,storage,checks): monkeypatch.setattr(mod,'GAME',game)
    c=copy.deepcopy(next(c for c in conditions() if c['scenario']=='public-goods' and c['players']==['jev','cooperate','defect'] and c['rounds']==20 and c['variant']=='base'))
    c['matches']=1
    m=dict(batch_id='check',model=MODEL,endpoint=ENDPOINT,conditions=[c],totals=totals([c]))
    def send(payload,*_): return 200,json.dumps({'model':MODEL,'answers':{'action':{'type':'choice','choice':'contribute'}},'usage':{'cost':.01}}),{}
    r=runner.Runner(m,send,key='test-key');r.play(c,1)
    summary,journals=checks.inspect_condition(m,c)
    assert summary['matches'][0]['status']=='complete'
    assert summary['matches'][0]['rounds']==20
    assert summary['matches'][0]['cost_usd_returned']==pytest.approx(.2)
    p=storage.condition_path(m,c)/'events.jsonl'
    rows=storage.read(p)
    settlement=next(x for x in rows if x['kind']=='settlement')
    settlement['record']['cumulative'][0]+=1
    p.write_text('\n'.join(json.dumps(x) for x in rows)+'\n',encoding='utf-8')
    with pytest.raises(AssertionError,match='Cumulative payoff mismatch'): checks.inspect_condition(m,c)

def test_strategy_phase_and_role_definitions():
    base=next(c for c in conditions() if c['scenario']=='ultimatum' and c['players']==['cycle','cycle'] and c['rounds']==20 and c['phases']==[0,1])
    assert [baseline(base,1,[],0,r,'proposal') for r in (1,3,5,7)]==['offer_0','offer_10','offer_0','offer_10']
    assert [baseline(base,1,[],1,r,'response',2) for r in (1,3,5,7)]==['reject','accept','reject','accept']
    c=copy.deepcopy(base);c['players']=['tit_for_tat','defect']
    h=[dict(round=1,actions=['offer_5','accept'],original=['offer_5','accept'],payoffs=[5,5]),dict(round=2,actions=['accept','offer_2'],original=['accept','offer_2'],payoffs=[2,8])]
    assert baseline(c,1,h,0,3,'proposal')=='offer_2'
    assert baseline(c,1,h,0,4,'response',0)=='reject'
    c['players'][0]='win_stay_lose_shift'
    assert baseline(c,1,h,0,3,'proposal')=='offer_5'
    assert baseline(c,1,h,0,4,'response',10)=='reject'
    c['history_window']=0
    assert baseline(c,1,h,0,4,'response',0)=='accept'

def test_public_goods_tft_ties_and_wsls():
    c=copy.deepcopy(next(c for c in conditions() if c['scenario']=='public-goods' and c['players']==['tit_for_tat']*3 and c['rounds']==20))
    h=[dict(round=1,actions=['contribute','keep','contribute'],original=['contribute','keep','contribute'],payoffs=[10.6666666667,20.6666666667,10.6666666667])]
    assert baseline(c,1,h,0,2,'simultaneous')=='contribute'
    c['players'][0]='win_stay_lose_shift'
    assert baseline(c,1,h,0,2,'simultaneous')=='contribute'
    h[0]['payoffs'][0]=0
    assert baseline(c,1,h,0,2,'simultaneous')=='keep'

def test_safe_html_serialization():
    hostile='</script><script>alert("x")</script>\u2028 & <img src=x onerror=alert(1)>'
    embedded=js({'text':hostile})
    assert '</script>' not in embedded and '<img' not in embedded
    assert json.loads(embedded)['text']==hostile
    assert '<script>' not in esc(hostile)
