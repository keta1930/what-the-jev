"""Rebuild the report figures and stats from the dataset and responses."""

import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

QUESTION = 'winner_overall'
POSITIONS = [f'R{i}' for i in range(1, 9)]
TYPES = ['causal', 'diagnosis', 'tradeoff']
RANDOM = 100 / len(POSITIONS)

LAYOUTS = [
    ('standard', 'result/responses.jsonl'),
    ('criteria-text', 'result/responses.choice.criteria-text.jsonl'),
]

BINS = [
    (0.0, 0.2, '<0.2'),
    (0.2, 0.3, '0.2–0.3'),
    (0.3, 0.4, '0.3–0.4'),
    (0.4, 0.5, '0.4–0.5'),
    (0.5, 1.01, '≥0.5'),
]

LABELS = {
    'en': {
        'xlabel': 'confidence of the answer',
        'answers': 'answers',
        'hit': 'hit rate (%)',
        'random': 'random pick 12.5%',
        'pos_xlabel': 'option position',
        'pos_ylabel': 'questions',
        'judge': 'LLM judge winners',
        'jev': 'JEV picks',
    },
    'zh': {
        'xlabel': '作答的 confidence',
        'answers': '题数',
        'hit': '命中率（%）',
        'random': '随机选择 12.5%',
        'pos_xlabel': '选项位置',
        'pos_ylabel': '题数',
        'judge': 'LLM 判官所选',
        'jev': 'JEV 所选',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def wilson(hits, n, z=1.96):
    """Return the Wilson 95% confidence interval bounds in percent."""
    p = hits / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / (1 + z * z / n)
    return 100 * (center - half), 100 * (center + half)


def load():
    """Return the judge choices and per-layout successful records."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    reference = {s['id']: s['reference'][QUESTION]['choice'] for s in dataset['samples']}
    layouts = {}
    for name, rel in LAYOUTS:
        with (ROOT / rel).open() as file:
            layouts[name] = [r for r in (json.loads(line) for line in file) if r['error'] is None]
    return reference, layouts


def answers_of(records):
    """Return (id, choice, confidence, usage) per record."""
    return [
        (r['id'], r['response']['answers'][QUESTION]['choice'],
         r['response']['answers'][QUESTION]['confidence'], r['response']['usage'])
        for r in records
    ]


def bin_stats(rows, reference):
    """Return (count, hit rate) per confidence bin."""
    stats = []
    for lo, hi, _ in BINS:
        sub = [choice == reference[pid] for pid, choice, conf, _ in rows if lo <= conf < hi]
        stats.append((len(sub), 100 * sum(sub) / len(sub)))
    return stats


def confidence_figure(stats, lang):
    """Plot the answer distribution and hit rate per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in BINS]
    counts = [count for count, _ in stats]
    hits = [hit for _, hit in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        ax1.text(i, count + 1, str(count), ha='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.2)

    ax2 = ax1.twinx()
    ax2.plot(x, hits, marker='o', color='#b34700')
    for i, hit in zip(x, hits):
        ax2.annotate(f'{hit:.1f}', (i, hit), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(RANDOM, ls='--', lw=1, color='#888888')
    ax2.text(0, RANDOM + 2, text['random'], ha='left', fontsize=8, color='#888888')
    ax2.set_ylabel(text['hit'])
    ax2.set_ylim(0, 100)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-hit.png', dpi=150)
    plt.close(fig)


def position_figure(judge_picks, jev_picks, lang):
    """Plot judge winners and JEV picks per option position."""
    text = LABELS[lang]
    x = list(range(len(POSITIONS)))
    width = 0.38

    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars1 = ax.bar([i - width / 2 for i in x], judge_picks, width, color='#8a8a8a', label=text['judge'])
    bars2 = ax.bar([i + width / 2 for i in x], jev_picks, width, color='#b34700', label=text['jev'])
    for bars in (bars1, bars2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.6,
                    f'{bar.get_height():.0f}', ha='center', fontsize=8)
    ax.set_xticks(x, POSITIONS)
    ax.set_xlabel(text['pos_xlabel'])
    ax.set_ylabel(text['pos_ylabel'])
    ax.set_ylim(0, max(jev_picks) * 1.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'position-distribution.png', dpi=150)
    plt.close(fig)


def main():
    reference, layouts = load()
    judge_picks = [Counter(reference.values())[p] for p in POSITIONS]

    per_layout = {}
    for name, records in layouts.items():
        rows = answers_of(records)
        hits = sum(choice == reference[pid] for pid, choice, _, _ in rows)
        lo, hi = wilson(hits, len(rows))
        picks = Counter(choice for _, choice, _, _ in rows)
        by_type = {}
        for t in TYPES:
            sub = [(pid, choice) for pid, choice, _, _ in rows if pid.split('-')[1] == t]
            by_type[t] = (len(sub), sum(choice == reference[pid] for pid, choice in sub))
        conf_hit = [conf for pid, choice, conf, _ in rows if choice == reference[pid]]
        conf_miss = [conf for pid, choice, conf, _ in rows if choice != reference[pid]]
        confs = sorted(conf for _, _, conf, _ in rows)
        usage = [u for *_, u in rows]
        below_max = tied_max = prob_sum_off = 0
        for r in records:
            answer = r['response']['answers'][QUESTION]
            probs = answer['probabilities']
            top = max(probs.values())
            if probs[answer['choice']] < top:
                below_max += 1
            elif list(probs.values()).count(top) > 1:
                tied_max += 1
            if round(sum(probs.values()), 6) != 1:
                prob_sum_off += 1
        per_layout[name] = {
            'rows': rows, 'hits': hits, 'ci': (lo, hi), 'picks': picks, 'by_type': by_type,
            'conf_hit': conf_hit, 'conf_miss': conf_miss, 'median_conf': confs[len(confs) // 2],
            'in_tokens': sum(u['input_tokens'] for u in usage),
            'out_tokens': sum(u['output_tokens'] for u in usage),
            'cost': sum(u['cost'] for u in usage),
            'below_max': below_max, 'tied_max': tied_max, 'prob_sum_off': prob_sum_off,
        }

    standard = per_layout['standard']
    stats = bin_stats(standard['rows'], reference)
    pos_hit = {p: [0, 0] for p in POSITIONS}
    for pid, choice, _, _ in standard['rows']:
        pos_hit[reference[pid]][1] += 1
        if choice == reference[pid]:
            pos_hit[reference[pid]][0] += 1

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(stats, lang)
        position_figure(judge_picks, [standard['picks'][p] for p in POSITIONS], lang)

    for name in ('standard', 'criteria-text'):
        d = per_layout[name]
        n = len(d['rows'])
        print(f"[{name}] n={n} hits={d['hits']} hit rate {100 * d['hits'] / n:.1f}% "
              f"(95% CI {d['ci'][0]:.1f}–{d['ci'][1]:.1f}%), random {RANDOM:.1f}%")
        print(f"  by type: " + '; '.join(
            f"{t} {k}/{m} ({100 * k / m:.1f}%)" for t, (m, k) in d['by_type'].items()))
        print(f"  picks: " + ', '.join(f"{p} {d['picks'][p]} ({100 * d['picks'][p] / n:.1f}%)" for p in POSITIONS))
        print(f"  confidence mean hit={sum(d['conf_hit']) / len(d['conf_hit']):.3f} "
              f"miss={sum(d['conf_miss']) / len(d['conf_miss']):.3f}, median {d['median_conf']:.2f}")
        print(f"  choice strictly below max prob: {d['below_max']} ({100 * d['below_max'] / n:.1f}%); "
              f"tied at max: {d['tied_max']} ({100 * d['tied_max'] / n:.1f}%); "
              f"prob sum != 1: {d['prob_sum_off']} ({100 * d['prob_sum_off'] / n:.1f}%)")
        print(f"  usage: in={d['in_tokens']:,} out={d['out_tokens']:,} cost=${d['cost']:.4f}")
    print('judge winners: ' + ', '.join(f'{p} {c} ({100 * c / 150:.1f}%)' for p, c in zip(POSITIONS, judge_picks)))
    print('[standard] confidence bins:')
    for (lo, hi, label), (count, hit) in zip(BINS, stats):
        print(f'  {label:8s} n={count:3d} hit {hit:.1f}%')
    print('[standard] hit by judge winner position: ' + '; '.join(
        f'{p} {k}/{m}' for p, (k, m) in pos_hit.items()))
    print(f"figures written to {FIG_DIR}")


if __name__ == '__main__':
    main()
