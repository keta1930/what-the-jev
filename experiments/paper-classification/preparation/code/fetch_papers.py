"""抓取 arXiv 论文候选元数据，写入 raw/papers.json —— 只运行一次。

产出是带抓取日期的元数据快照：raw/papers.json 里的 fetched_on 就是这份快照的
版本标签，之后所有数据集都由它构造（见 build_dataset.py），不再回访 arXiv。
所以本脚本的运行结果不需要也无法复现。

重跑会覆盖 raw/papers.json 并得到不同的候选集：arXiv 的相关度排序与索引随时间
变化，检索窗口又跟着运行日期移动。那等于换了一个版本，需要重新走一遍人工复核。

用法：
    python fetch_papers.py
"""

import json
import re
from datetime import date, timedelta
from pathlib import Path

import arxiv

PREPARATION = Path(__file__).resolve().parents[1]
RAW_PATH = PREPARATION / 'raw' / 'papers.json'

LOOKBACK_DAYS = 365
PER_QUERY = 40
MIN_ABSTRACT_CHARS = 500

QUERIES = {
    'memory': [
        'abs:"agent memory"',
        'abs:"long-term memory" AND abs:agent AND abs:LLM',
        'abs:"memory" AND abs:"LLM agent"',
        'abs:"episodic memory" AND abs:agent',
        'ti:memory AND abs:"large language model"',
        'abs:"memory management" AND abs:agent',
        'abs:"memory" AND abs:agent AND abs:benchmark',
    ],
    'self_evolution': [
        'abs:"self-evolving agent"',
        'abs:"self-evolving" AND abs:LLM',
        'abs:"self-improving agent"',
        'abs:"self-improvement" AND abs:agent',
        'abs:"self-evolution" AND abs:"large language model"',
        'abs:"lifelong learning" AND abs:agent',
        'abs:"continual learning" AND abs:agent AND abs:LLM',
    ],
    'agent_other': [
        'abs:"LLM agent" AND abs:planning',
        'abs:"tool use" AND abs:"LLM agent"',
        'abs:"multi-agent" AND abs:"large language model"',
        'abs:"computer-use agent"',
        'abs:"GUI agent"',
        'abs:"web agent" AND abs:benchmark',
        'abs:"agent" AND abs:"reinforcement learning"',
    ],
    'off_topic': [
        'cat:cs.CV AND abs:"video generation"',
        'cat:cs.CV AND abs:"3D reconstruction"',
        'abs:"medical image segmentation"',
        'abs:"speech recognition" AND cat:eess.AS',
        'cat:q-bio.BM AND abs:protein',
        'cat:cs.RO AND abs:manipulation',
        'abs:"recommender system" AND abs:"graph neural network"',
        'cat:cs.LG AND abs:"optimization theory"',
    ],
}

# 与分组定位不符的候选在抓取阶段就丢弃
RELEVANT_TITLE = re.compile(
    r'(memory|memor|self-evolv|self-improv|self-refin|self-train|evolution|'
    r'lifelong|continual)',
    re.IGNORECASE,
)


def arxiv_id(entry_id: str) -> str:
    """从 entry_id URL 取出不带版本号的 arXiv ID。"""
    tail = entry_id.rstrip('/').rsplit('/', 1)[-1]
    return re.sub(r'v\d+$', '', tail)


def is_candidate(group: str, paper) -> bool:
    """过滤掉与分组定位不符的候选。"""
    if len(paper.summary) < MIN_ABSTRACT_CHARS:
        return False
    title = paper.title
    if group in ('memory', 'self_evolution'):
        return 'agent' in (title + paper.summary).lower()
    if group == 'agent_other':
        return 'agent' in title.lower() and not RELEVANT_TITLE.search(title)
    return 'agent' not in title.lower()


def window_query(query: str, start: date, end: date) -> str:
    """给检索式加上提交日期窗口。"""
    lo = start.strftime('%Y%m%d') + '0000'
    hi = end.strftime('%Y%m%d') + '2359'
    return f'{query} AND submittedDate:[{lo} TO {hi}]'


def to_record(group: str, paper) -> dict:
    """把 arXiv 结果转成候选记录；只存抓下来的字段，判定值一律不存。"""
    aid = arxiv_id(paper.entry_id)
    return {
        'id': aid,
        'group': group,
        'title': paper.title.strip(),
        'authors': [a.name for a in paper.authors],
        'published': paper.published.strftime('%Y-%m-%d'),
        'primary_category': paper.primary_category,
        'categories': paper.categories,
        'comment': (paper.comment or '').strip(),
        'abstract': paper.summary.replace('\n', ' ').strip(),
        'pdf_url': paper.pdf_url,
        'abs_url': f'https://arxiv.org/abs/{aid}',
    }


def fetch_all(client, start: date, end: date) -> dict[str, dict]:
    """按分组抓取候选，跨分组按 arXiv ID 去重，先扫描的分组优先认领。"""
    found: dict[str, dict] = {}
    for group, queries in QUERIES.items():
        print(f'[{group}]')
        for query in queries:
            search = arxiv.Search(
                query=window_query(query, start, end),
                max_results=PER_QUERY,
                sort_by=arxiv.SortCriterion.Relevance,
            )
            try:
                results = list(client.results(search))
            except Exception as exc:
                print(f'  ! {query}: {exc}')
                continue
            kept = 0
            for paper in results:
                if not is_candidate(group, paper):
                    continue
                aid = arxiv_id(paper.entry_id)
                if aid in found:
                    continue
                kept += 1
                found[aid] = to_record(group, paper)
            print(f'  {query}: {len(results)} 命中，保留 {kept}')
    return found


def main() -> None:
    today = date.today()
    start = today - timedelta(days=LOOKBACK_DAYS)
    client = arxiv.Client(page_size=50, delay_seconds=3.0, num_retries=5)
    found = fetch_all(client, start, today)

    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(
        json.dumps(
            {
                'fetched_on': today.isoformat(),
                'window_start': start.isoformat(),
                'queries': QUERIES,
                'candidates': list(found.values()),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding='utf-8',
    )
    print(f'snapshot {today.isoformat()}, window from {start.isoformat()}')
    print(f'{len(found)} candidates -> {RAW_PATH}')


if __name__ == '__main__':
    main()
