"""Offline resource, navigation and embedded-record verification."""
from html.parser import HTMLParser
import json
import re
from urllib.parse import urlsplit,unquote
from .storage import atomic,now
from .storage import condition_path,read
from .plan import stable

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set();self.external=[];self.modules=[];self.scripts=[];self.styles=[];self.capture=None;self.parts=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        for key in ('href','src'):
            if key in attrs:
                value=attrs[key];self.links.append(value)
                if urlsplit(value).scheme or value.startswith('//'):self.external.append(value)
        if tag=='script' and attrs.get('type')=='module':self.modules.append(attrs)
        if tag in ('script','style'):self.capture=tag;self.parts=[]
    def handle_data(self,text):
        if self.capture:self.parts.append(text)
    def handle_endtag(self,tag):
        if tag==self.capture:
            (self.scripts if tag=='script' else self.styles).append(''.join(self.parts));self.capture=None

class PreBlocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.blocks=[];self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=='pre':self.current=[]
    def handle_data(self,text):
        if self.current is not None:self.current.append(text)
    def handle_endtag(self,tag):
        if tag=='pre' and self.current is not None:
            self.blocks.append(''.join(self.current));self.current=None

def fidelity_check(out,m):
    """Compare every embedded round and readable raw item to its source journal.

    This is deliberately independent of the renderer's intermediate objects.
    A structurally valid page must still fail if an action, payoff, request,
    response, retry or lifecycle event was changed or omitted by the renderer.
    """
    matches_checked=0;rounds_checked=0;inputs_checked=0;responses_checked=0;events_checked=0
    for c in m['conditions']:
        source=condition_path(m,c)
        inputs=read(source/'inputs.jsonl');responses=read(source/'responses.jsonl');events=read(source/'events.jsonl')
        summary_path=source/'summary.json'
        summaries={x['id']:x for x in json.loads(summary_path.read_text(encoding='utf-8'))['matches']} if summary_path.exists() else {}
        for number in range(1,c['matches']+1):
            mid=c['id']+f'/m{number:03}';slug=c['id']+f'-m{number:03}'
            text=(out/'matches'/f'{slug}.html').read_text(encoding='utf-8')
            embedded=re.search(r'<script>const DATA=(.*?);</script>',text,re.S)
            assert embedded,f'Missing embedded match data: {slug}'
            data=json.loads(embedded.group(1))
            selected_events=[e for e in events if e['match_id']==mid]
            expected_records=[e['record'] for e in selected_events if e['kind']=='settlement']
            assert data['records']==expected_records,f'HTML rounds differ from source: {slug}'
            assert data['config']==c and data['batch_id']==m['batch_id'] and data['model']==m['model']
            assert data['match']['id']==mid and data['match']['number']==number
            if mid in summaries:
                expected={**summaries[mid],'condition_id':c['id'],'scenario':c['scenario']}
                expected['seed']=str(expected['seed'])
                assert data['match']==expected,f'HTML match facts differ from summary: {slug}'
            elif not selected_events:
                assert not data['records'] and data['match']['status']!='complete'
            selected_inputs={x['id']:x for x in inputs if x['match_id']==mid}
            attempts={e['attempt_id'] for e in selected_events if e['kind']=='request_started'}
            selected_responses={x['id']:x for x in responses if x['id'] in attempts}
            seen_inputs={};seen_responses={};seen_events=set()
            def collect(value):
                if isinstance(value,list):
                    for x in value:collect(x)
                elif isinstance(value,dict):
                    if 'id' in value and 'payload' in value:
                        assert value['id'] in selected_inputs and value==selected_inputs[value['id']],f'Raw input differs: {slug}'
                        seen_inputs[value['id']]=value
                    elif set(value)=={'id','response','error'}:
                        assert value['id'] in selected_responses and value==selected_responses[value['id']],f'Raw response differs: {slug}'
                        seen_responses[value['id']]=value
                    elif 'kind' in value and 'match_id' in value:seen_events.add(stable(value))
                    elif 'events' in value:collect(value['events'])
            max_round=max([len(expected_records),*[x['round'] for x in selected_inputs.values()],*[e.get('round',0) for e in selected_events],1])
            raw_index=json.loads((out/'raw'/f'{slug}-index.json').read_text(encoding='utf-8'))
            assert raw_index['match_id']==mid and raw_index['max_round']==max_round
            segments=raw_index['segments']
            assert data['raw_segments']==segments
            assert [s['path'] for s in segments]==[f'{slug}-s{i+1}.html' for i in range(len(segments))],'Unsafe raw segment path'
            assert [r for segment in segments for r in range(segment['start'],segment['end']+1)]==list(range(1,max_round+1)),'Raw round segments have a gap or overlap'
            assert all(segment['end']-segment['start']<20 for segment in segments)
            raw_paths=[out/'raw'/segment['path'] for segment in segments]
            assert all(p.exists() for p in raw_paths),f'Missing raw pages: {slug}'
            for raw_path in raw_paths:
                parser=PreBlocks();parser.feed(raw_path.read_text(encoding='utf-8'))
                for block in parser.blocks:collect(json.loads(block))
            for blob in raw_index['blobs']:
                assert blob['id']==blob['sha256_json'][:20]
                assert blob['paths']==[f'{slug}-json-{blob["id"]}-p{i+1}.html' for i in range(len(blob['paths']))],'Unsafe raw fragment path'
                fragments=[]
                for name in blob['paths']:
                    parser=PreBlocks();parser.feed((out/'raw'/name).read_text(encoding='utf-8'))
                    assert len(parser.blocks)==1,'Raw JSON fragment page has ambiguous contents'
                    fragments.append(parser.blocks[0])
                value=json.loads(''.join(fragments))
                assert stable(value)==blob['sha256_json'],'Raw JSON fragments differ from source hash'
                collect(value)
            assert set(seen_inputs)==set(selected_inputs),f'Raw input omitted: {slug}'
            assert set(seen_responses)==set(selected_responses),f'Raw response omitted: {slug}'
            expected_events={stable(e) for e in selected_events}
            assert seen_events==expected_events,f'Raw event omitted or changed: {slug}'
            matches_checked+=1;rounds_checked+=len(expected_records)
            inputs_checked+=len(seen_inputs);responses_checked+=len(seen_responses);events_checked+=len(expected_events)
    # Full builds also prove that each scenario's dynamic catalog contains
    # every frozen condition and every match, with the source-derived status.
    from .storage import GAME
    batch_summary=GAME/'output'/'records'/m['batch_id']/'summary.json'
    catalogs_checked=0
    if batch_summary.exists():
        source_matches=json.loads(batch_summary.read_text(encoding='utf-8'))['matches']
        by_condition={}
        for x in source_matches:by_condition.setdefault(x['condition_id'],[]).append(x)
        for scenario in dict.fromkeys(c['scenario'] for c in m['conditions']):
            text=(out/(scenario+'.html')).read_text(encoding='utf-8')
            embedded=re.search(r'<script>const DATA=(.*?);</script>',text,re.S)
            assert embedded,'Missing scenario catalog data'
            data=json.loads(embedded.group(1));expected=[]
            for c in m['conditions']:
                if c['scenario']==scenario:
                    expected.append(dict(config=c,matches=[{k:x[k] for k in ('id','number','status','rounds')} for x in by_condition[c['id']]]))
            assert data['items']==expected,'Scenario catalog differs from complete source index'
            catalogs_checked+=1
    result=dict(checked_at=now(),valid=True,matches_checked=matches_checked,rounds_checked=rounds_checked,inputs_checked=inputs_checked,responses_checked=responses_checked,events_checked=events_checked,catalogs_checked=catalogs_checked,all_embedded_rounds_equal_source=True,all_raw_items_equal_source=True)
    atomic(out/'fidelity-check.json',result)
    return result

def check(out,expected_matches=None,manifest=None):
    pages={};max_bytes=0;embedded=0;links=0
    for path in out.rglob('*.html'):
        text=path.read_text(encoding='utf-8');size=path.stat().st_size;max_bytes=max(max_bytes,size)
        assert size<=10*1024*1024,f'Oversized page: {path}'
        parser=Links();parser.feed(text)
        assert not parser.external,f'External resource/link: {path}'
        assert not parser.modules,f'Module script: {path}'
        for script in parser.scripts:
            if not script.startswith('const DATA='):
                assert not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(',script),f'Runtime network dependency: {path}'
        for style in parser.styles:
            assert not re.search(r'(?:url\s*\(|@import\s+)[\s\"\']*(?:https?:|//)',style,re.I),f'Online CSS dependency: {path}'
        assert not re.search(r'sk-or-v1-[A-Za-z0-9_-]{16,}',text),f'Credential-like text in HTML: {path}'
        pages[path.resolve()]=parser
        match=re.search(r'<script>const DATA=(.*?);</script>',text,re.S)
        if match:
            data=json.loads(match.group(1))
            if 'items' in data:parser.ids.update(x['config']['id'] for x in data['items'])
            if 'records' in data:
                embedded+=1
                assert data['match']['rounds']==len(data['records'])
                assert [h['round'] for h in data['records']]==list(range(1,len(data['records'])+1))
                if data['records']: assert data['match']['cumulative']==data['records'][-1]['cumulative']
                slug=data['slug']
                # JavaScript builds these links, so verify them explicitly.
                assert data['raw_segments']
                for segment in data['raw_segments']:
                    assert (out/'raw'/segment['path']).exists()
    for path,parser in pages.items():
        for href in parser.links:
            part=urlsplit(href);target=(path.parent/unquote(part.path)).resolve() if part.path else path
            assert target.is_relative_to(out.resolve()),f'Link escapes package: {path}: {href}'
            assert target.exists(),f'Missing linked file: {path}: {href}'
            # Round hashes are route state, not DOM IDs.
            if part.fragment and not part.fragment.startswith('round='):
                assert target in pages and unquote(part.fragment) in pages[target].ids,f'Missing anchor: {path}: {href}'
            links+=1
    if expected_matches is not None: assert embedded==expected_matches
    result=dict(checked_at=now(),pages=len(pages),embedded_matches=embedded,links=links,max_page_bytes=max_bytes,no_external_resources=True,no_fetch_or_modules=True,valid=True,file_protocol_runtime_verified=False)
    atomic(out/'offline-check.json',result)
    if manifest is not None:fidelity_check(out,manifest)
    return result
