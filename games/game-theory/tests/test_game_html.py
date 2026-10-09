"""Test offline pages, source fidelity and actual playback scripts."""
import json
from pathlib import Path
import pytest
from game_theory.html import match_page,page,write
from game_theory.html_check import check
from game_theory.plan import conditions,MODEL
from game_theory.rules import payoff
from game_theory.config import validate_files
from game_theory.storage import GAME

def test_fixed_configuration_files():
    assert validate_files(GAME)['model']==MODEL

def test_viewer_contains_all_jev_matches_and_no_rule_only_matches():
    from game_theory.html import presentation_manifest
    source=dict(conditions=conditions(),batch_id='unit-only')
    original=list(source['conditions'])
    view=presentation_manifest(source)
    assert all('jev' in c['players'] for c in view['conditions'])
    assert sum(c['matches'] for c in view['conditions'])==4864
    assert view['conditions']==[c for c in original if 'jev' in c['players']]
    assert source['conditions']==original and len(original)==5888

def test_full_builder_delivers_all_five_scenario_catalogs(tmp_path,monkeypatch):
    from game_theory import storage,html as renderer
    game=tmp_path/'source'
    monkeypatch.setattr(storage,'GAME',game)
    monkeypatch.setattr(renderer,'GAME',game)
    m=dict(batch_id='unit-empty-only',model=MODEL,conditions=[],totals=dict(conditions=0,matches=0))
    facts=dict(counts={},settled_rounds=0,cost_usd_returned=0,cost_missing_attempts=0)
    def empty_validation(manifest):
        storage.atomic(game/'output'/'records'/m['batch_id']/'summary.json',dict(matches=[]))
        return facts
    monkeypatch.setattr(renderer,'validate_batch',empty_validation)
    entry=Path(renderer.build(m))
    assert entry.exists()
    report=json.loads((entry.parent/'offline-check.json').read_text(encoding='utf-8'))
    assert report['valid'] and report['pages']==6
    for scenario in renderer.NAMES:
        text=(entry.parent/(scenario+'.html')).read_text(encoding='utf-8')
        assert '目前没有完整对局' in text and 'id="catalog"' in text

def test_empty_match_and_raw_links(tmp_path):
    c=next(c for c in conditions() if c['scenario']=='prisoner-dilemma' and c['players']==['jev','jev'] and c['rounds']==20 and c['variant']=='base')
    mid=c['id']+'/m001'
    match=dict(id=mid,number=1,status='incomplete',rounds=0,cumulative=[0,0],cost_usd_returned=0,cost_missing_attempts=0,reason=None,pending_actions=0,seed=2**64-1,returned_snapshots=[])
    match_page(tmp_path,dict(batch_id='unit-only',model=MODEL),c,match,dict(inputs=[],responses=[],events=[]))
    write(tmp_path/'index.html',page('test','test'))
    write(tmp_path/'prisoner-dilemma.html',page('test','<div id="'+c['id']+'"></div>'))
    result=check(tmp_path,expected_matches=1)
    assert result['valid']
    text=(tmp_path/'matches'/f"{c['id']}-m001.html").read_text(encoding='utf-8')
    assert '"seed":"18446744073709551615"' in text
    assert '"records":[]' in text
    assert 'id="next"' in text

def test_raw_escape_and_return_to_exact_round(tmp_path):
    c=next(c for c in conditions() if c['scenario']=='prisoner-dilemma' and c['players']==['cooperate','defect'] and c['rounds']==20)
    mid=c['id']+'/m001'; record=dict(round=1,actions=['cooperate','defect'],original=['cooperate','defect'],payoffs=[0,5],cumulative=[0,5])
    match=dict(id=mid,number=1,status='paused',rounds=1,cumulative=[0,5],cost_usd_returned=0,cost_missing_attempts=1,reason='</script><script>alert(1)</script>',pending_actions=0,seed=1,returned_snapshots=[])
    journals=dict(inputs=[],responses=[],events=[dict(kind='settlement',match_id=mid,record=record)])
    match_page(tmp_path,dict(batch_id='unit-only',model=MODEL),c,match,journals)
    raw=(tmp_path/'raw'/f"{c['id']}-m001-s1.html").read_text(encoding='utf-8')
    assert '#round=1' in raw and '返回对局第 1 轮 ↗' in raw
    assert '<script>alert(1)</script>' not in raw

def test_missing_external_and_oversize_rejected(tmp_path):
    write(tmp_path/'index.html',page('x','<a href="missing.html">missing</a>'))
    with pytest.raises(AssertionError,match='Missing linked file'):check(tmp_path)
    write(tmp_path/'index.html',page('x','<img src="https://example.com/a.png">'))
    with pytest.raises(AssertionError,match='External resource'):check(tmp_path)
    with pytest.raises(ValueError,match='exceeds 10 MiB'):write(tmp_path/'large.html','x'*(10*1024*1024+1))

def test_offline_check_distinguishes_raw_text_from_executable_network_calls(tmp_path):
    from game_theory.html import esc
    literal="<script>fetch('https://example.com')</script>"
    write(tmp_path/'index.html',page('raw','<pre>'+esc(literal)+'</pre>',data={'raw_text':literal}))
    assert check(tmp_path)['valid']
    write(tmp_path/'index.html',page('bad','',script="fetch('https://example.com')"))
    with pytest.raises(AssertionError,match='Runtime network dependency'):check(tmp_path)
    write(tmp_path/'index.html',page('bad','<style>body{background:url(https://example.com/a.png)}</style>'))
    with pytest.raises(AssertionError,match='Online CSS dependency'):check(tmp_path)

def test_dynamic_catalog_anchors_are_checked(tmp_path):
    write(tmp_path/'index.html',page('test','<a href="scenario.html#good">go</a>'))
    write(tmp_path/'scenario.html',page('test','',data={'items':[{'config':{'id':'good'}}]}))
    assert check(tmp_path)['valid']
    write(tmp_path/'index.html',page('test','<a href="scenario.html#missing">go</a>'))
    with pytest.raises(AssertionError,match='Missing anchor'):check(tmp_path)

def test_independent_fidelity_detects_changed_round_and_omitted_events(tmp_path,monkeypatch):
    from game_theory import storage,runner
    from game_theory.validate import inspect_condition
    from game_theory.html_check import fidelity_check
    from game_theory.html import esc,js
    from game_theory.plan import ENDPOINT,totals
    game=tmp_path/'source';monkeypatch.setattr(storage,'GAME',game);monkeypatch.setattr(runner,'GAME',game)
    c=dict(next(c for c in conditions() if c['scenario']=='prisoner-dilemma' and c['players']==['cooperate','defect'] and c['rounds']==1))
    c['matches']=1
    m=dict(batch_id='unit-only',conditions=[c],totals=totals([c]),model=MODEL,endpoint=ENDPOINT)
    runner.Runner(m,key='test-key').play(c,1)
    summary,journals=inspect_condition(m,c)
    storage.atomic(storage.condition_path(m,c)/'summary.json',summary)
    match={**summary['matches'][0],'condition_id':c['id'],'scenario':c['scenario']}
    out=tmp_path/'html';match_page(out,m,c,match,journals)
    assert fidelity_check(out,m)['events_checked']==5
    path=out/'matches'/f"{c['id']}-m001.html";original=path.read_text(encoding='utf-8')
    corrupted=original.replace('"payoffs":[0,5]','"payoffs":[99,5]')
    assert corrupted!=original
    path.write_text(corrupted,encoding='utf-8')
    with pytest.raises(AssertionError,match='HTML rounds differ'):fidelity_check(out,m)
    path.write_text(original,encoding='utf-8')
    raw=out/'raw'/f"{c['id']}-m001-s1.html";text=raw.read_text(encoding='utf-8')
    selected=[e for e in journals['events'] if e.get('round')==1 or e['kind']=='settlement']
    block=esc(json.dumps(selected,ensure_ascii=False,indent=2))
    assert block in text
    raw.write_text(text.replace(block,'[]'),encoding='utf-8')
    with pytest.raises(AssertionError,match='Raw event omitted'):fidelity_check(out,m)

def test_actual_script_reduced_motion_and_fast_navigation():
    import subprocess
    import shutil
    node=shutil.which('node')
    if node is None:pytest.skip('Node.js is required for the isolated classic-script test')
    result=subprocess.run([node,str(Path(__file__).with_name('game_dom.cjs'))],capture_output=True,text=True,encoding='utf-8',check=True)
    rows=json.loads(result.stdout)
    assert [x['reduced'] for x in rows]==[False,True]
    assert all(x['round']=='第 21 轮' for x in rows)

@pytest.mark.parametrize('huge_response',[False,True])
def test_raw_overflow_splits_without_losing_any_source_item(tmp_path,monkeypatch,huge_response):
    from game_theory import storage,runner,html as renderer
    from game_theory.validate import inspect_condition
    from game_theory.html_check import fidelity_check
    from game_theory.plan import ENDPOINT,totals
    game=tmp_path/'source';monkeypatch.setattr(storage,'GAME',game);monkeypatch.setattr(runner,'GAME',game)
    monkeypatch.setattr(renderer,'MAX_PAGE_BYTES',65536)
    players=['jev','cooperate'] if huge_response else ['cooperate','defect']
    rounds=1 if huge_response else 20
    c=dict(next(c for c in conditions() if c['scenario']=='prisoner-dilemma' and c['players']==players and c['rounds']==rounds and c['variant']=='base'));c['matches']=1
    m=dict(batch_id='unit-only',conditions=[c],totals=totals([c]),model=MODEL,endpoint=ENDPOINT)
    def send(*_):
        return 200,json.dumps({'model':MODEL,'provider':'test-double','answers':{'action':{'type':'choice','choice':'cooperate'}},'debug':'<bad>&'*30000,'usage':{'cost':.001}}),{}
    runner.Runner(m,send,key='test-key').play(c,1)
    source=storage.condition_path(m,c)
    if not huge_response:
        rows=storage.read(source/'events.jsonl')
        for row in rows:
            if row['kind']=='action':row['unit_test_padding']='x'*4000
        (source/'events.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows),encoding='utf-8')
    summary,journals=inspect_condition(m,c);storage.atomic(source/'summary.json',summary)
    match={**summary['matches'][0],'condition_id':c['id'],'scenario':c['scenario']}
    out=tmp_path/'html';renderer.match_page(out,m,c,match,journals)
    index=json.loads((out/'raw'/f"{c['id']}-m001-index.json").read_text(encoding='utf-8'))
    if huge_response:assert any(len(b['paths'])>1 for b in index['blobs'])
    else:assert len(index['segments'])>1
    assert all(p.stat().st_size<=65536 for p in out.rglob('*.html'))
    facts=fidelity_check(out,m)
    assert facts['matches_checked']==1 and facts['rounds_checked']==rounds
    if huge_response:
        blob=index['blobs'][0];p=out/'raw'/blob['paths'][0]
        text=p.read_text(encoding='utf-8');assert '&lt;bad&gt;' in text
        p.write_text(text.replace('&lt;bad&gt;','changed',1),encoding='utf-8')
        with pytest.raises(AssertionError,match='fragments differ'):fidelity_check(out,m)
