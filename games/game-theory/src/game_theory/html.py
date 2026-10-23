"""Self-contained file-compatible pages rebuilt from validated journals."""
import html
import json
import uuid
from collections import Counter
from pathlib import Path
from .storage import GAME, ROOT, now, atomic, condition_path
from .validate import validate_batch, inspect_condition
from .display import NAMES, TAGLINES, RULES_ZH, STRATEGY_ZH, ACTION_ZH, VARIANTS, STATUS, strategy_definitions

from .raw_html import raw_pages

MAX_PAGE_BYTES=10*1024*1024
ASSETS=Path(__file__).with_name('assets')

def esc(value): return html.escape(str(value),quote=True)
def js(value): return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def page(title,body,data=None,script='',prefix=''):
    css=(ASSETS/'style.css').read_text(encoding='utf-8')
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' · 博弈记录册</title><style>'+css+'</style><body><div class="shell"><header class="site-header"><a class="brand" href="'+prefix+'index.html">◈ 博弈记录册</a><span>真实行动 · 逐轮留存</span></header><main>'+body+'</main><footer>所有 Jev 的目标：最大化自己整场累计收益。模型只知道对方编号，不知道对手策略身份。</footer></div>'+(('<script>const DATA='+js(data)+';</script>') if data is not None else '')+('<script>'+script+'</script>' if script else '')+'</body></html>'

def write(path,text):
    size=len(text.encode('utf-8'))
    if size>MAX_PAGE_BYTES: raise ValueError(f'HTML exceeds {MAX_PAGE_BYTES/1024**2:g} MiB; split required: {path}')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')
    return size

def match_page(out,m,c,match,journals):
    mid=match['id']; slug=c['id']+f"-m{match['number']:03}"
    records=[e['record'] for e in journals['events'] if e.get('match_id')==mid and e['kind']=='settlement']
    raw_segments=raw_pages(out,c,match,records,journals)
    body='<nav class="crumb"><a href="../'+c['scenario']+'.html#'+c['id']+'">← 返回场景与组合</a><span>'+esc(VARIANTS[c['variant']])+'</span></nav><p class="eyebrow">'+esc(NAMES[c['scenario']])+' / 第 '+str(match['number'])+' 场</p><div class="title-row"><h1>对局观察台</h1><span class="badge">'+esc(STATUS[match['status']])+'</span></div><p class="muted">观众可见真实策略身份；模型请求中仅提供玩家编号。每场独立重置策略状态。</p>'
    body+='<div class="observer"><div id="roster" class="roster" aria-label="本场固定玩家策略"></div><div class="observer-grid"><section class="round-panel"><div class="round-heading"><div><span class="eyebrow">当前轮次</span><h2 id="round-title"></h2></div><p id="round-context"></p></div><div id="scene" class="scene '+c['scenario']+'" aria-live="polite"></div></section><aside class="trend-panel"><section><h2>累计收益 <small id="trend-stage"></small></h2><div id="trend"></div></section><section><h2>逐轮选择 <small>图形为策略身份，色块为实际行动</small></h2><div id="choices"></div></section><p class="muted">点击曲线或色块可定位已揭示轮次。未来记录随播放展开。</p></aside></div><div class="transport"><button id="play" type="button" aria-pressed="false">▶ 播放</button><button id="previous" type="button">← 上一轮</button><span id="position" role="status"></span><button id="next" type="button">下一轮 →</button><label class="speed-label">速度<select id="speed"><option value="3000">慢</option><option value="1800" selected>标准</option><option value="1000">快</option></select></label><label class="scrub-label">定位轮次<input id="scrub" type="range" min="1" max="1" value="1" aria-label="定位轮次"></label></div><nav class="round-picker" aria-label="选择轮次"><button id="previous-group" type="button">上一组</button><div id="round-grid"></div><button id="next-group" type="button">下一组</button></nav></div>'
    body+='<div class="below"><details><summary>规则与本场条件</summary><p>'+esc(RULES_ZH[c['scenario']])+'</p><p>所有 Jev 目标：最大化自己整场累计收益。历史窗口 '+str(c['history_window'])+' 轮；自身累计收益始终可见。'+('总轮数已告知。' if c['horizon']=='known' else '公开每轮后 0.9 继续概率，未公开 100 轮硬上限。' if c['horizon']=='geometric' else '未告知总轮数；实际最多 '+str(c['rounds'])+' 轮。')+'</p><p>执行翻转概率：'+str(c['noise'])+'。'+('第 10 轮仅翻转 P1；执行前不公开触发轮次，仅说明可能有外部干预。' if c['intervention'] else '')+'</p><dl>'
    for i,p in enumerate(c['players']): body+='<dt>P'+str(i+1)+' · '+esc(STRATEGY_ZH[p])+'</dt><dd>'+esc(strategy_definitions(c['scenario'])[p])+(' 起始相位 '+str(c['phases'][i])+'。' if p=='cycle' else '')+'</dd>'
    body+='</dl></details><details><summary>本场状态与整场最终概况</summary><div id="final-summary"></div></details><details><summary>批次、模型与费用</summary><div id="batch-details"></div></details><a class="raw-link" id="raw-link" href="../raw/'+slug+'-s1.html">查看本轮完整英文输入、响应与事件 ↗</a></div>'
    data=dict(batch_id=m['batch_id'],model=m['model'],generated=now(),config=c,match={**match,'seed':str(match['seed'])},records=records,raw_segments=raw_segments,slug=slug,names=STRATEGY_ZH,actions=ACTION_ZH)
    write(out/'matches'/f'{slug}.html',page('逐轮记录',body,data,(ASSETS/'identity.js').read_text(encoding='utf-8')+(ASSETS/'match.js').read_text(encoding='utf-8'),prefix='../'))

def scenario_page(out,m,s,items):
    complete=[(c,match) for c,matches in items for match in matches if match['status']=='complete']
    preferred=next(((c,x) for c,x in complete if c['variant']=='base' and c['rounds']==20 and set(c['players'])=={'jev'} and (s!='public-goods' or len(c['players'])==4)),None)
    default=preferred or (complete[0] if complete else None)
    body='<nav class="crumb"><a href="index.html">← 五种场景</a></nav><p class="eyebrow">'+esc(s)+'</p><h1>'+esc(NAMES[s])+'</h1><p class="intro">'+esc(TAGLINES[s])+'</p><div class="rule-box">'+esc(RULES_ZH[s])+'</div>'
    if default:
        c,x=default; body+='<a class="primary-link" href="matches/'+c['id']+f'-m{x["number"]:03}.html">打开默认对局 →</a>'
    else: body+='<p class="notice">目前没有完整对局。下方保留全部条件与未完成状态。</p>'
    body+='<p class="muted">默认选取：基础 20 轮全 Jev 的首场完整对局，公共物品优先 4 人；否则按清单顺序取首场完整对局，不按收益筛选。</p><details><summary>规则策略的精确定义</summary><dl>'
    for p,definition in strategy_definitions(s).items(): body+='<dt>'+esc(STRATEGY_ZH[p])+' · '+esc(p)+'</dt><dd>'+esc(definition)+'</dd>'
    body+='</dl><p>规则策略与 Jev 使用相同可见历史。零历史时，针锋相对和赢留输换按首次规则行动；自身累计收益仍可见。循环使用公开轮次或角色次数。每场重置状态。</p></details><section class="catalog"><h2>完整条件与对局</h2><div class="filters"><label>策略或条件 ID<input id="search" type="search" placeholder="例如 Jev、随机、condition ID"></label><label>轮数<select id="round-filter"><option value="">全部</option><option>1</option><option>20</option><option>100</option></select></label><label>状态<select id="status-filter"><option value="">全部</option>' + ''.join('<option value="'+k+'">'+v+'</option>' for k,v in STATUS.items())+'</select></label><label>条件<select id="variant-filter"><option value="">全部</option>'+''.join('<option value="'+k+'">'+v+'</option>' for k,v in VARIANTS.items())+'</select></label></div><p id="catalog-count" class="muted"></p><div id="catalog"></div><div class="controls"><button id="catalog-prev">上一页</button><span id="catalog-page"></span><button id="catalog-next">下一页</button></div></section>'
    data=dict(scenario=s,names=STRATEGY_ZH,variants=VARIANTS,status=STATUS,items=[dict(config=c,matches=[{k:x[k] for k in ('id','number','status','rounds')} for x in matches]) for c,matches in items])
    body=body.replace('<h2>完整条件与对局</h2>','<h2>选择玩家阵容</h2><p class="muted">图标表示整场固定策略；P 编号表示座位。先选阵容，再看轮数与条件。</p><div id="strategy-legend" class="strategy-legend"></div><div id="lineup-filter" class="lineup-filter" aria-label="阵容筛选"></div>')
    write(out/(s+'.html'),page(NAMES[s],body,data,(ASSETS/'identity.js').read_text(encoding='utf-8')+(ASSETS/'catalog.js').read_text(encoding='utf-8')))

def presentation_manifest(m):
    """Viewer scope; the immutable experiment manifest is never rewritten."""
    return {**m,'conditions':[c for c in m['conditions'] if 'jev' in c['players']],
            'display_scope':'at-least-one-jev'}

def build(m):
    facts=validate_batch(m)
    view=presentation_manifest(m)
    visible=view['conditions']
    build_id=uuid.uuid4().hex[:12]
    out=GAME/'output'/('.html-build-'+build_id); out.mkdir(parents=True,exist_ok=False)
    summary=json.loads((GAME/'output'/'records'/m['batch_id']/'summary.json').read_text(encoding='utf-8'))
    by_condition={}
    for x in summary['matches']: by_condition.setdefault(x['condition_id'],[]).append(x)
    scenes={s:[] for s in NAMES}; page_count=0
    for c in visible:
        _,journals=inspect_condition(m,c)
        matches=by_condition[c['id']]
        for x in matches: match_page(out,m,c,x,journals); page_count+=1
        scenes[c['scenario']].append((c,matches))
    for s,items in scenes.items():
        scenario_page(out,m,s,items)
    body='<p class="eyebrow">JEV / GAME THEORY / LOCAL RECORDS</p><h1 class="home-title">每一个选择，<br>都有它的下一轮。</h1><p class="intro">五种博弈，一本可以逐轮翻看的互动记录册。<br>从实际行动出发，看清规则、选择和收益。</p><div class="scenario-cards">'
    for i,(s,items) in enumerate(scenes.items(),1):
        ms=[x for _,matches in items for x in matches]; complete=sum(x['status']=='complete' for x in ms)
        state='已有完整对局' if complete else '记录尚未完整'
        body+='<a class="scenario-card" href="'+s+'.html"><span class="card-number">0'+str(i)+'</span><div class="card-drawing drawing-'+s+'" aria-hidden="true">'+['▯ ↔ ▯','♧ ⤨ ♧','◁ ◇ ▷','○ ＋ ○','▰ ▱'][i-1]+'</div><h2>'+esc(NAMES[s])+'</h2><p>'+esc(TAGLINES[s])+'</p><span class="card-status">'+state+' <span>↗</span></span></a>'
    body+='<p class="display-scope">仅展示至少有一位 Jev 参与的 '+str(page_count)+' 场对局。纯规则对局不在展示范围内。</p></div><details class="batch-facts"><summary>原始批次记录与真实费用</summary><p>批次 '+esc(m['batch_id'])+'；固定模型 '+esc(m['model'])+'。</p><p>生成时间 '+esc(now())+'（UTC）。中文展示说明独立于英文请求。</p><p>'+str(m['totals']['conditions'])+' 个条件 / '+str(m['totals']['matches'])+' 场；已完成 '+str(facts['counts'].get('complete',0))+' 场，已结算 '+str(facts['settled_rounds'])+' 轮。</p><p>已返回费用 USD '+format(facts['cost_usd_returned'],'.8f')+'；'+str(facts['cost_missing_attempts'])+' 次尝试费用未返回。缺失费用不当作零。</p><p>全部状态：'+esc(json.dumps(facts['counts'],ensure_ascii=False))+'</p><p>展示范围内的全部条件、失败和不完整项均保留。上述批次总量包含历史纯规则记录，未删除原始数据。这里的次数与收益只描述已经发生的记录，不代表模型能力评分。</p></details>'
    write(out/'index.html',page('五种场景',body))
    atomic(out/'build-manifest.json',dict(batch_id=m['batch_id'],generated=now(),match_pages=page_count,display_scope='at-least-one-jev',display_conditions=len(visible),excluded_rule_matches=m['totals']['matches']-page_count,validation=facts,entry='index.html'))
    from .html_check import check
    check(out,expected_matches=page_count,manifest=view)
    final=GAME/'output'/'html'
    archive=GAME/'output'/'html-archive'/(m['batch_id']+'-'+build_id)
    for target in (out,final,archive):
        if target.is_symlink() or not target.resolve().is_relative_to(GAME.resolve()):
            raise ValueError('Unsafe HTML output path')
    if final.exists():
        archive.parent.mkdir(parents=True,exist_ok=True)
        final.rename(archive)
    out.rename(final)
    return str(final/'index.html')
