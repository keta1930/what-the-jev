"""Bounded readable raw pages, with lossless overflow fragments."""
import json
from .display import NAMES
from .plan import stable
from .storage import atomic


def raw_pages(out,c,match,records,journals):
    from .html import esc,page,write,MAX_PAGE_BYTES
    mid=match['id'];slug=c['id']+f"-m{match['number']:03}"
    inputs=[x for x in journals['inputs'] if x['match_id']==mid]
    events=[e for e in journals['events'] if e['match_id']==mid]
    attempt_ids={e['attempt_id'] for e in events if e['kind']=='request_started'}
    responses={r['id']:r for r in journals['responses'] if r['id'] in attempt_ids}
    max_round=max([match['rounds'],*[x['round'] for x in inputs],*[e.get('round',0) for e in events],1])
    ranges=[(r,min(r+19,max_round)) for r in range(1,max_round+1,20)]
    compact=set();blobs={}
    # Keep an individual fragment comfortably below the cap after escaping.
    frame=page('完整 JSON 文本段','<h1>完整记录文本段</h1><pre></pre>',prefix='../')
    budget=min(1024*1024,MAX_PAGE_BYTES-len(frame.encode('utf-8'))-4096)
    if budget<=0:raise ValueError('HTML size cap is smaller than the raw-page frame')

    def blocks(value,r,force=False):
        text=json.dumps(value,ensure_ascii=False,indent=2)
        escaped=esc(text)
        if not force and len(escaped.encode('utf-8'))<=budget:
            return '<pre>'+escaped+'</pre>',set()
        digest=stable(value);key=digest[:20]
        if key not in blobs:
            fragments=[];remaining=text
            while remaining:
                low=1;high=len(remaining)
                while low<high:
                    take=(low+high+1)//2
                    if len(esc(remaining[:take]).encode('utf-8'))<=budget:low=take
                    else:high=take-1
                fragments.append(remaining[:low]);remaining=remaining[low:]
            blobs[key]=dict(id=key,sha256_json=digest,round=r,text_parts=fragments,
                            paths=[f'{slug}-json-{key}-p{i+1}.html' for i in range(len(fragments))])
        b=blobs[key]
        body='<p class="notice">此 JSON 记录分为 '+str(len(b['paths']))+' 个连续文本段，完整内容未删减。</p><div class="raw-navigation">'
        body+=' '.join('<a href="'+p+'">文本段 '+str(i+1)+'</a>' for i,p in enumerate(b['paths']))+'</div>'
        return body,{key}

    def render(start,end,segments):
        used=set()
        def pre(value,r,force=False):
            text,refs=blocks(value,r,force);used.update(refs);return text
        body='<nav class="crumb"><a href="../matches/'+slug+'.html#round='+str(start)+'">← 返回对局第 '+str(start)+' 轮</a></nav><p class="eyebrow">完整英文请求 / 原始响应 / 事件</p><h1>'+esc(NAMES[c['scenario']])+' · 第 '+str(match['number'])+' 场</h1><p class="muted">逻辑决策 ID 与每次 attempt ID 分开保存。候选概率与 confidence 保持原值；缺失不补造。</p>'
        body+='<div class="raw-navigation">'+' '.join('<a href="'+s['path']+'">'+str(s['start'])+'–'+str(s['end'])+'</a>' for s in segments)+'</div>'
        for r in range(start,end+1):
            force=r in compact
            body+=f'<section class="raw-round" id="r{r}"><h2>第 {r} 轮</h2><a href="../matches/{slug}.html#round={r}">返回对局第 {r} 轮 ↗</a>'
            selected=[x for x in inputs if x['round']==r]
            for x in selected:
                body+='<h3>'+esc(x['id'])+'</h3><h4>实际发送输入</h4>'+pre(x,r,force)
                attempts=[e for e in events if e.get('decision_id')==x['id'] and e['kind']=='request_started']
                for a in attempts:
                    aid=a['attempt_id'];body+='<h4>'+esc(aid)+'</h4>'
                    if aid in responses:body+=pre(responses[aid],r,force)
                    else:body+='<p>尚无已持久化响应；可能发生远端响应后本地未落盘的窗口。</p>'
                    for e in events:
                        if e.get('attempt_id')==aid and e['kind']=='request_finished':
                            body+='<details><summary>HTTP、耗时、usage 与完整传输文本</summary>'+pre(e,r,force)+'</details>'
            decision_ids={x['id'] for x in selected}
            round_events=[e for e in events if e['kind']!='request_finished' and (e.get('round')==r or e.get('decision_id') in decision_ids or e['kind']=='settlement' and e['record']['round']==r)]
            body+='<details><summary>行动、请求关联与结算事件 · '+str(len(round_events))+' 条</summary>'+pre(round_events,r,force)+'</details></section>'
        lifecycle=[e for e in events if e['kind'] in ('match_started','match_resumed','match_paused','match_complete')]
        body+='<details><summary>对局状态事件与冻结配置</summary>'+pre(dict(config=c,match=match,events=lifecycle),start,start in compact)+'</details>'
        return page('完整记录',body,prefix='../'),used

    # Bisect by settled round, preserving all individual items. If a single
    # round remains oversized, its JSON blocks become lossless fragment links.
    while True:
        segments=[dict(start=a,end=b,path=f'{slug}-s{i+1}.html') for i,(a,b) in enumerate(ranges)]
        rendered=[];changed=False
        for i,(start,end) in enumerate(ranges):
            text,used=render(start,end,segments)
            if len(text.encode('utf-8'))>MAX_PAGE_BYTES:
                if start<end:
                    middle=(start+end)//2
                    ranges[i:i+1]=[(start,middle),(middle+1,end)]
                elif start not in compact:compact.add(start)
                else:raise ValueError('Raw navigation frame exceeds the HTML page cap')
                changed=True;break
            rendered.append((text,used))
        if not changed:break
    used_blobs=set()
    for segment,(text,used) in zip(segments,rendered):
        write(out/'raw'/segment['path'],text);used_blobs.update(used)
    index_blobs=[]
    for key in sorted(used_blobs):
        b=blobs[key]
        source=next(s for s in segments if s['start']<=b['round']<=s['end'])
        for i,(text,path) in enumerate(zip(b['text_parts'],b['paths'])):
            body='<nav class="crumb"><a href="'+source['path']+'#r'+str(b['round'])+'">← 返回第 '+str(b['round'])+' 轮完整记录</a></nav><h1>完整 JSON · 文本段 '+str(i+1)+' / '+str(len(b['paths']))+'</h1><p class="muted">按编号顺序连接全部文本段，得到原 JSON 记录；这里不省略原始文本。</p><div class="raw-navigation">'+' '.join('<a href="'+p+'">'+str(j+1)+'</a>' for j,p in enumerate(b['paths']))+'</div><pre class="json-fragment">'+esc(text)+'</pre>'
            write(out/'raw'/path,page('完整记录文本段',body,prefix='../'))
        index_blobs.append({k:v for k,v in b.items() if k!='text_parts'})
    atomic(out/'raw'/f'{slug}-index.json',dict(format_version=2,match_id=mid,max_round=max_round,segments=segments,blobs=index_blobs))
    return segments
