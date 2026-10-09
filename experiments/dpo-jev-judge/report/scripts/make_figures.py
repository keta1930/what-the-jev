"""Rebuild the report figures and stats from the dataset and responses."""

import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

QUESTION = 'better'
TYPES = ['causal', 'diagnosis', 'tradeoff']
RANDOM = 50.0

LAYOUTS = [
    ('standard', 'result/responses.jsonl'),
    ('criteria-text', 'result/responses.choice.criteria-text.jsonl'),
]

BINS = [
    (0.0, 0.2, '<0.2'),
    (0.2, 0.4, '0.2–0.4'),
    (0.4, 0.6, '0.4–0.6'),
    (0.6, 0.8, '0.6–0.8'),
    (0.8, 1.01, '≥0.8'),
]

LABELS = {
    'en': {
        'xlabel': 'confidence of the answer',
        'answers': 'pairs',
        'agree': 'agreement with the judge (%)',
        'random': 'random pick 50%',
    },
    'zh': {
        'xlabel': '作答的 confidence',
        'answers': '对数',
        'agree': '与判官一致率（%）',
        'random': '随机选择 50%',
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
    """Return the judge preferences and per-layout successful records."""
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
    """Return (count, agreement) per confidence bin."""
    stats = []
    for lo, hi, _ in BINS:
        sub = [choice == reference[pid] for pid, choice, conf, _ in rows if lo <= conf < hi]
        stats.append((len(sub), 100 * sum(sub) / len(sub)))
    return stats


def confidence_figure(stats, lang):
    """Plot the answer distribution and agreement per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in BINS]
    counts = [count for count, _ in stats]
    agrees = [agree for _, agree in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.2)

    ax2 = ax1.twinx()
    ax2.plot(x, agrees, marker='o', color='#b34700')
    for i, agree in zip(x, agrees):
        ax2.annotate(f'{agree:.1f}', (i, agree), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(RANDOM, ls='--', lw=1, color='#888888')
    ax2.text(len(BINS) - 1, RANDOM + 2, text['random'], ha='right', fontsize=8, color='#888888')
    ax2.set_ylabel(text['agree'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-agreement.png', dpi=150)
    plt.close(fig)


def main():
    reference, layouts = load()
    placement = Counter(reference.values())

    per_layout = {}
    for name, records in layouts.items():
        rows = answers_of(records)
        agree = sum(choice == reference[pid] for pid, choice, _, _ in rows)
        lo, hi = wilson(agree, len(rows))
        picks = Counter(choice for _, choice, _, _ in rows)
        by_type = {}
        for t in TYPES:
            sub = [(pid, choice) for pid, choice, _, _ in rows if pid.split('-')[1] == t]
            by_type[t] = (len(sub), sum(choice == reference[pid] for pid, choice in sub))
        by_position = {}
        for pos in ('A', 'B'):
            sub = [(pid, choice) for pid, choice, _, _ in rows if reference[pid] == pos]
            by_position[pos] = (len(sub), sum(choice == pos for pid, choice in sub))
        conf_agree = [conf for pid, choice, conf, _ in rows if choice == reference[pid]]
        conf_disagree = [conf for pid, choice, conf, _ in rows if choice != reference[pid]]
        confs = sorted(conf for _, _, conf, _ in rows)
        usage = [u for *_, u in rows]
        flaws = sum(
            1 for r in records
            if max(r['response']['answers'][QUESTION]['probabilities'],
                   key=r['response']['answers'][QUESTION]['probabilities'].get)
            != r['response']['answers'][QUESTION]['choice']
        )
        per_layout[name] = {
            'rows': rows, 'agree': agree, 'ci': (lo, hi), 'picks': picks, 'by_type': by_type,
            'by_position': by_position, 'conf_agree': conf_agree, 'conf_disagree': conf_disagree,
            'median_conf': confs[len(confs) // 2],
            'in_tokens': sum(u['input_tokens'] for u in usage),
            'out_tokens': sum(u['output_tokens'] for u in usage),
            'cost': sum(u['cost'] for u in usage), 'flaws': flaws,
        }

    standard = per_layout['standard']
    stats = bin_stats(standard['rows'], reference)

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(stats, lang)

    print(f"reference placement: A {placement['A']}, B {placement['B']}")
    for name in ('standard', 'criteria-text'):
        d = per_layout[name]
        n = len(d['rows'])
        print(f"[{name}] n={n} agree={d['agree']} agreement {100 * d['agree'] / n:.1f}% "
              f"(95% CI {d['ci'][0]:.1f}–{d['ci'][1]:.1f}%), random {RANDOM:.0f}%")
        print(f"  by type: " + '; '.join(
            f"{t} {k}/{m} ({100 * k / m:.1f}%)" for t, (m, k) in d['by_type'].items()))
        print(f"  picks: A {d['picks']['A']} ({100 * d['picks']['A'] / n:.1f}%), "
              f"B {d['picks']['B']} ({100 * d['picks']['B'] / n:.1f}%)")
        print(f"  agreement by reference position: " + '; '.join(
            f"{pos} {k}/{m} ({100 * k / m:.1f}%)" for pos, (m, k) in d['by_position'].items()))
        print(f"  confidence mean agree={sum(d['conf_agree']) / len(d['conf_agree']):.3f} "
              f"disagree={sum(d['conf_disagree']) / len(d['conf_disagree']):.3f}, median {d['median_conf']:.2f}")
        print(f"  argmax!=choice: {d['flaws']}")
        print(f"  usage: in={d['in_tokens']:,} out={d['out_tokens']:,} cost=${d['cost']:.4f}")
    print('[standard] confidence bins:')
    for (lo, hi, label), (count, agree) in zip(BINS, stats):
        print(f'  {label:8s} n={count:3d} agree {agree:.1f}%')
    ct_stats = bin_stats(per_layout['criteria-text']['rows'], reference)
    print('[criteria-text] confidence bins:')
    for (lo, hi, label), (count, agree) in zip(BINS, ct_stats):
        print(f'  {label:8s} n={count:3d} agree {agree:.1f}%')
    print(f"figures written to {FIG_DIR}")


if __name__ == '__main__':
    main()
