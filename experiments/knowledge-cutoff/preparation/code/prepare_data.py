# Build bilingual headline probes for estimating JEV's knowledge cutoff date.

import argparse
from collections import Counter, deque
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from typing import Any, TypedDict
from urllib.parse import urlsplit

EXPERIMENT = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parents[4]
RAW = EXPERIMENT / 'preparation/raw/questions.jsonl'
MONTHS = tuple(f'{2023 + i // 12}-{i % 12 + 1:02d}' for i in range(42))
IDS = [f'knowledge-cutoff-{month}-{slot:02d}' for month in MONTHS for slot in range(1, 11)]
LANGUAGES = ('zh', 'en')
LETTERS = 'ABCD'
VARIANT = 'headline-v1'
CJK = re.compile(r'[\u2e80-\u9fff\uf900-\ufaff\U00020000-\U000323af]')
LEAK = re.compile(r'https?://|www\.|knowledge-cutoff-\d{4}-\d{2}', re.I)
sys.path.insert(0, str(ROOT / 'src'))

from decision_models.config import load_config
from decision_models.data import load_dataset
from decision_models.json_utils import loads, load_validator, validate


class Material(TypedDict):
    question: str
    options: list[str]
    statement_template: str


class Reuse(TypedDict):
    decision: str
    original_question: str
    reason: str


class Source(TypedDict):
    url: str
    title: str
    publisher: str
    published_date: str | None
    supports: str
    access: str


class Salience(TypedDict):
    rationale: str
    independent_publishers: list[str]


class Review(TypedDict):
    reviewer: str
    status: str
    note: str


class Event(TypedDict):
    base_id: str
    month: str
    event_date: str
    category: str
    event: str
    reuse: Reuse
    zh: Material
    en: Material
    sources: list[Source]
    salience: Salience
    temporal_novelty: str
    distractor_rationales: list[str]
    review: Review


class Plan(TypedDict):
    permutation: list[int]
    assertion_slot: int


TEXT = {
    'zh': {
        'choice': '选择state中历史知识题唯一正确的具体选项；无法确定时选择unknown。',
        'noul': '判断state中的陈述是否符合历史事实。',
        'unknown': '无法确定／不知道',
        'true': '陈述符合历史事实。', 'false': '陈述不符合历史事实。',
    },
    'en': {
        'choice': 'Choose the only correct concrete option for the historical knowledge question '
                  'in state; choose unknown if unsure.',
        'noul': 'Determine whether the statement in state is historically true.',
        'unknown': 'Cannot determine / do not know',
        'true': 'The statement is historically true.', 'false': 'The statement is historically false.',
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def shape(value: Any, definition: type, label: str) -> None:
    require(isinstance(value, dict) and set(value) == set(definition.__annotations__),
            f'{label} must have exactly these fields: {sorted(definition.__annotations__)}')


def iso_date(value: Any, label: str) -> date:
    require(isinstance(value, str), f'{label} must be an ISO date')
    parsed = date.fromisoformat(value)
    require(parsed.isoformat() == value, f'{label} must be an ISO date')
    return parsed


def read_jsonl(path: Path) -> list[Any]:
    rows = []
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        require(bool(line.strip()), f'{path} has a blank line: {number}')
        rows.append(loads(line))
    return rows


def validate_bank(rows: list[Event]) -> None:
    require(len(rows) == 420, f'headline bank must have 420 events, got {len(rows)}')
    seen_questions = {language: set() for language in LANGUAGES}
    seen_events = set()
    seen_reviews = set()
    for expected_id, row in zip(IDS, rows, strict=True):
        shape(row, Event, expected_id)
        require(row['base_id'] == expected_id, f'expected chronological slot {expected_id}')
        label = row['base_id']
        require(row['month'] == label[17:24], f'{label} month does not match its slot')
        iso_date(row['event_date'], f'{label} event_date')
        require(row['event_date'][:7] == row['month'], f'{label} event_date has the wrong month')
        require(all(text(row[key]) for key in ('category', 'event', 'temporal_novelty')),
                f'{label} needs category, event and temporal novelty')
        identity = (row['month'], row['event'].strip().casefold())
        require(identity not in seen_events, f'{label} repeats an event within its month')
        seen_events.add(identity)
        reuse = row['reuse']
        shape(reuse, Reuse, f'{label} reuse')
        require(reuse['decision'] in ('reuse', 'rewrite', 'replace') and text(reuse['reason'])
                and text(reuse['original_question']),
                f'{label} has invalid reuse evidence or missing original-question provenance')
        for language in LANGUAGES:
            item = row[language]
            shape(item, Material, f'{label} {language}')
            require(text(item['question']) and text(item['statement_template']),
                    f'{label} {language} needs a question and assertion template')
            options = item['options']
            require(isinstance(options, list) and 2 <= len(options) <= 4
                    and all(text(option) for option in options)
                    and len({option.strip().casefold() for option in options}) == len(options),
                    f'{label} {language} needs 2 to 4 distinct concrete options')
            require(not any(option.strip().casefold() in
                            ('unknown', '无法确定／不知道', 'cannot determine / do not know')
                            for option in options), f'{label} {language} has a nonconcrete option')
            template = item['statement_template']
            remainder = template.replace('{answer}', '')
            require(template.count('{answer}') == 1 and '{' not in remainder and '}' not in remainder,
                    f'{label} {language} template needs exactly one literal {{answer}}')
            material = [item['question'], template, *options]
            require(not any(LEAK.search(value) for value in material),
                    f'{label} {language} leaks a URL or sample ID into model material')
            require(language != 'en' or not any(CJK.search(value) for value in material),
                    f'{label} English model material contains CJK text')
            question = item['question'].strip().casefold()
            require(question not in seen_questions[language], f'{label} repeats a {language} question')
            seen_questions[language].add(question)
        count = len(row['zh']['options'])
        require(count == len(row['en']['options']), f'{label} languages have different option counts')
        rationales = row['distractor_rationales']
        require(isinstance(rationales, list) and len(rationales) == count - 1
                and all(text(note) for note in rationales)
                and len(set(rationales)) == count - 1, f'{label} needs distinct distractor rationales')
        sources = row['sources']
        require(isinstance(sources, list) and len(sources) >= 2, f'{label} needs two news sources')
        urls, publishers = set(), set()
        contemporaneous = False
        for source in sources:
            shape(source, Source, f'{label} source')
            require(all(text(source[key]) for key in ('url', 'title', 'publisher', 'supports')),
                    f'{label} has an empty source field')
            parsed = urlsplit(source['url'])
            require(parsed.scheme in ('http', 'https') and bool(parsed.hostname)
                    and '.' in parsed.hostname and not parsed.username and not parsed.password
                    and not parsed.fragment and source['url'] not in urls,
                    f'{label} has an invalid or duplicate source URL')
            urls.add(source['url'])
            publishers.add(source['publisher'])
            require(source['access'] in ('opened', 'search_snippet'), f'{label} has invalid source access')
            if source['published_date'] is not None:
                iso_date(source['published_date'], f'{label} source published_date')
                contemporaneous |= source['published_date'][:7] == row['month']
        salience = row['salience']
        shape(salience, Salience, f'{label} salience')
        independent = salience['independent_publishers']
        require(text(salience['rationale']) and isinstance(independent, list)
                and all(text(publisher) for publisher in independent)
                and len(independent) >= 2 and len(set(independent)) == len(independent)
                and set(independent) <= publishers,
                f'{label} needs two distinct source publishers supporting salience')
        require(contemporaneous, f'{label} needs a dated same-month news source')
        review = row['review']
        shape(review, Review, f'{label} review')
        require(review['status'] == 'accepted' and text(review['reviewer']) and text(review['note'])
                and review['note'] not in seen_reviews, f'{label} needs a specific accepted review')
        seen_reviews.add(review['note'])


def rank(domain: str, value: str) -> str:
    return sha256(f'{VARIANT}|{domain}|{value}'.encode()).hexdigest()


def circulation(edges: list[tuple[str, str, int, int]]) -> list[int] | None:
    graph: dict[str, list[list[Any]]] = {}
    balance: Counter = Counter()

    def add(start: str, end: str, capacity: int) -> list[Any]:
        graph.setdefault(start, [])
        graph.setdefault(end, [])
        forward = [end, capacity, len(graph[end])]
        backward = [start, 0, len(graph[start])]
        graph[start].append(forward)
        graph[end].append(backward)
        return forward

    tracked = []
    for start, end, lower, upper in edges:
        tracked.append(add(start, end, upper - lower))
        balance[start] -= lower
        balance[end] += lower
    needed = 0
    for node, amount in balance.items():
        if amount > 0:
            add('@source', node, amount)
            needed += amount
        elif amount < 0:
            add(node, '@sink', -amount)
    delivered = 0
    while delivered < needed:
        parents: dict[str, tuple[str, int] | None] = {'@source': None}
        queue = deque(['@source'])
        while queue and '@sink' not in parents:
            node = queue.popleft()
            for index, (end, capacity, _) in enumerate(graph[node]):
                if capacity > 0 and end not in parents:
                    parents[end] = (node, index)
                    queue.append(end)
        if '@sink' not in parents:
            return None
        node = '@sink'
        amount = needed - delivered
        while parents[node] is not None:
            start, index = parents[node]
            amount = min(amount, graph[start][index][1])
            node = start
        node = '@sink'
        while parents[node] is not None:
            start, index = parents[node]
            edge = graph[start][index]
            edge[1] -= amount
            graph[node][edge[2]][1] += amount
            node = start
        delivered += amount
    return [upper - edge[1] for (_, _, _, upper), edge in zip(edges, tracked, strict=True)]


def balanced_slots(rows: list[Event]) -> tuple[dict[str, int], str]:
    total = len(rows)
    slots = range(4)
    for mode in ('monthly-and-global', 'global', 'available-options'):
        edges = [('sink', 'source', total, total)]
        choices = []
        for row in sorted(rows, key=lambda item: rank('allocation', item['base_id'])):
            base_id = row['base_id']
            edges.append(('source', base_id, 1, 1))
            available = range(len(row['zh']['options']))
            for slot in sorted(available, key=lambda value: rank('slot', f'{base_id}|{value}')):
                choices.append((len(edges), base_id, slot))
                edges.append((base_id, f'{row["month"]}:{slot}', 0, 1))
        for month in MONTHS:
            for slot in slots:
                lower, upper = (2, 3) if mode == 'monthly-and-global' else (0, 10)
                edges.append((f'{month}:{slot}', f'slot:{slot}', lower, upper))
        for slot in slots:
            target = total // len(slots)
            lower, upper = (0, total) if mode == 'available-options' else (target, target)
            edges.append((f'slot:{slot}', 'sink', lower, upper))
        flow = circulation(edges)
        if flow is not None:
            return {base_id: slot for index, base_id, slot in choices if flow[index]}, mode
    raise ValueError('no valid concrete-slot allocation exists')


def false_assignments(rows: list[Event]) -> tuple[dict[str, int], str]:
    for mode in ('global', 'available-options'):
        edges = [('sink', 'source', 210, 210)]
        choices = []
        for month in MONTHS:
            edges.append(('source', month, 5, 5))
            cohort = [row for row in rows if row['month'] == month]
            for row in sorted(cohort, key=lambda item: rank('truth', item['base_id'])):
                base_id = row['base_id']
                edges.append((month, base_id, 0, 1))
                available = range(1, len(row['zh']['options']))
                for slot in sorted(available, key=lambda value: rank('false-slot', f'{base_id}|{value}')):
                    choices.append((len(edges), base_id, slot))
                    edges.append((base_id, f'slot:{slot}', 0, 1))
        for slot in (1, 2, 3):
            lower, upper = (70, 70) if mode == 'global' else (0, 210)
            edges.append((f'slot:{slot}', 'sink', lower, upper))
        flow = circulation(edges)
        if flow is not None:
            return {base_id: slot for index, base_id, slot in choices if flow[index]}, mode
    raise ValueError('no assignment can select five valid false assertions per month')


def assignments(rows: list[Event]) -> tuple[dict[str, Plan], dict[str, str]]:
    positions, position_mode = balanced_slots(rows)
    false_slots, false_mode = false_assignments(rows)
    plans = {}
    for row in rows:
        base_id = row['base_id']
        order = sorted(range(1, len(row['zh']['options'])),
                       key=lambda slot: rank('permutation', f'{base_id}|{slot}'))
        order.insert(positions[base_id], 0)
        plans[base_id] = {'permutation': order,
                          'assertion_slot': false_slots.get(base_id, 0)}
    return plans, {'choice_positions': position_mode, 'false_slots': false_mode}


def sample_for(row: Event, language: str, kind: str, plan: Plan) -> dict[str, Any]:
    item = row[language]
    options = item['options']
    slot = plan['assertion_slot']
    assertion = item['statement_template'].format(answer=options[slot])
    pair_id = f'{row["base_id"]}-{VARIANT}'
    if kind == 'choice':
        criteria = {LETTERS[index]: options[original] for index, original in enumerate(plan['permutation'])}
        criteria['unknown'] = TEXT[language]['unknown']
        state = item['question']
        answer = {'choice': LETTERS[plan['permutation'].index(0)]}
    else:
        criteria = {key: TEXT[language][key] for key in ('true', 'false')}
        state = assertion
        answer = slot == 0
    metadata = {key: row[key] for key in ('month', 'event_date', 'category', 'event')}
    metadata.update({
        'pair_id': pair_id, 'language': language, 'concrete_option_count': len(options),
    })
    return {'id': f'{pair_id}-{kind}',
            'input': {'state': state, 'questions': {'answer': {
                'type': kind, 'instructions': TEXT[language][kind], 'criteria': criteria}}},
            'reference': {'answer': answer}, 'metadata': metadata}


def validate_datasets(datasets: dict[str, Any], rows: list[Event]) -> None:
    validate_bank(rows)
    plans, _ = assignments(rows)
    schema = load_validator(ROOT / 'schema/dataset.schema.json')
    for language in LANGUAGES:
        dataset = datasets[language]
        validate(dataset, schema, f'invalid {language} dataset')
        samples = dataset['samples']
        require(len(samples) == 840, f'{language} dataset must contain 840 samples')
        monthly: dict[str, Counter] = {month: Counter() for month in MONTHS}
        cross = Counter()
        for index, row in enumerate(rows):
            permutation = plans[row['base_id']]['permutation']
            for offset, kind in enumerate(('choice', 'noul')):
                sample = samples[2 * index + offset]
                expected = sample_for(row, language, kind, plans[row['base_id']])
                require(type(sample['metadata'].get('concrete_option_count')) is int,
                        f'{sample["id"]} needs a strict integer option count')
                require(kind != 'noul' or type(sample['reference'].get('answer')) is bool,
                        f'{sample["id"]} needs an exact boolean assertion reference')
                require(sample == expected, f'{sample["id"]} differs from its complete raw reconstruction')
                material = json.dumps(sample['input'], ensure_ascii=False)
                require(not LEAK.search(material) and (language != 'en' or not CJK.search(material)),
                        f'{sample["id"]} leaks provenance or contains CJK English material')
                counts = monthly[row['month']]
                counts[kind] += 1
                if kind == 'noul':
                    counts[sample['reference']['answer']] += 1
                    gold = LETTERS[permutation.index(0)]
                    cross[(gold, sample['reference']['answer'])] += 1
        require(all(counts == Counter({'choice': 10, 'noul': 10, True: 5, False: 5})
                    for counts in monthly.values()), f'{language} monthly types or truth counts differ')
        for letter in LETTERS:
            count = cross[(letter, True)] + cross[(letter, False)]
            require(count < 2 or (cross[(letter, True)] > 0 and cross[(letter, False)] > 0),
                    f'{language} assertion truth is determined by gold letter {letter}')
    for zh, en in zip(datasets['zh']['samples'], datasets['en']['samples'], strict=True):
        require(zh['id'] == en['id'] and zh['reference'] == en['reference']
                and zh['metadata']['pair_id'] == en['metadata']['pair_id']
                and zh['metadata']['concrete_option_count'] == en['metadata']['concrete_option_count'],
                'languages differ in paired IDs, references or option counts')


def build_datasets(rows: list[Event]) -> dict[str, Any]:
    validate_bank(rows)
    plans, _ = assignments(rows)
    datasets = {language: {'schema_version': 1, 'samples': [
        sample_for(row, language, kind, plans[row['base_id']])
        for row in rows for kind in ('choice', 'noul')]} for language in LANGUAGES}
    validate_datasets(datasets, rows)
    return datasets


def serialized(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def validate_config() -> None:
    config = load_config(EXPERIMENT / 'config.yaml')
    require(config['data'] == [f'data/dataset.{language}.json' for language in LANGUAGES]
            and config['output'] == [f'result/responses.mixed.{language}.jsonl' for language in LANGUAGES],
            'config must use matching bilingual dataset and result paths')


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build 840 independent headline probes per language to estimate JEV's knowledge cutoff date.")
    parser.add_argument('--check', action='store_true', help='Validate generated bytes without writing files')
    args = parser.parse_args()
    validate_config()
    rows = read_jsonl(RAW)
    datasets = build_datasets(rows)
    outputs = {language: (EXPERIMENT / f'data/dataset.{language}.json', serialized(dataset))
               for language, dataset in datasets.items()}
    if not args.check:
        config = load_config(EXPERIMENT / 'config.yaml')
        existing_results = [EXPERIMENT / name for name in config['output']
                            if (EXPERIMENT / name).exists()]
        changed = [path for path, expected in outputs.values()
                   if not path.is_file() or path.read_bytes() != expected]
        require(not existing_results or not changed,
                f'cannot create or change headline datasets while results exist: {existing_results}')
    for language, dataset in datasets.items():
        path, expected = outputs[language]
        if args.check:
            require(path.is_file() and path.read_bytes() == expected, f'{path} differs from the reviewed bank')
            validate_datasets({**datasets, language: loads(path.read_text(encoding='utf-8'))}, rows)
        else:
            path.write_bytes(expected)
        load_dataset(path)
        print(f'{"Checked" if args.check else "Built"} 840 {language} samples; SHA256 {sha256(expected).hexdigest()}')
    plans, modes = assignments(rows)
    labels = Counter(LETTERS[plan['permutation'].index(0)] for plan in plans.values())
    false_slots = Counter(plan['assertion_slot'] for plan in plans.values() if plan['assertion_slot'])
    print(f'42 months; each month 10 choice, 5 true and 5 false; allocation: {modes}')
    print(f'Correct letters: {dict(sorted(labels.items()))}; false original slots: {dict(sorted(false_slots.items()))}')
    print(f'Concrete option counts: {dict(sorted(Counter(len(row["zh"]["options"]) for row in rows).items()))}')
    print(f'Reuse decisions: {dict(Counter(row["reuse"]["decision"] for row in rows))}')
    print(f'Accepted reviews: {len(rows)}; source entries: {sum(len(row["sources"]) for row in rows)}')


if __name__ == '__main__':
    main()
