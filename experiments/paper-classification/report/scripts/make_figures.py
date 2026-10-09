"""Rebuild the report figures and stats from the dataset and responses."""

import json
import math
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

CONDITIONS = ['full_crit', 'min_crit', 'full_nocrit', 'min_nocrit']
QUESTIONS = ['decision', 'topic']

# Confidence bins: high >0.9, mid 0.6-0.9 inclusive, low <0.6.
BINS = [
    (lambda cf: cf < 0.6, '<0.6'),
    (lambda cf: 0.6 <= cf <= 0.9, '0.6–0.9'),
    (lambda cf: cf > 0.9, '>0.9'),
]

LABELS = {
    'en': {
        'conditions': ['full state\n+ criteria', 'min state\n+ criteria',
                       'full state\nno criteria', 'min state\nno criteria'],
        'decision': 'decision', 'topic': 'topic',
        'cond_ylabel': 'accuracy (%)',
        'xlabel': 'confidence per question answer',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
        'random': 'random 33%',
    },
    'zh': {
        'conditions': ['完整材料\n有标准', '精简材料\n有标准',
                       '完整材料\n无标准', '精简材料\n无标准'],
        'decision': 'decision 题', 'topic': 'topic 题',
        'cond_ylabel': '准确率（%）',
        'xlabel': '每题作答的 confidence',
        'answers': '作答数',
        'accuracy': '准确率（%）',
        'random': '随机 33%',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the references, metadata, and successful records."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    reference = {s['id']: s['reference'] for s in dataset['samples']}
    metadata = {s['id']: s['metadata'] for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    return reference, metadata, records, ok


def correct(record, reference, question):
    """Return whether one question answer matches the reference."""
    return record['response']['answers'][question]['choice'] == reference[record['id']][question]


def accuracy(records, reference, question):
    """Return the accuracy of one question over the given records."""
    hits = sum(1 for r in records if correct(r, reference, question))
    return hits, 100 * hits / len(records)


def wald_interval(hits, n):
    """Return the 95% Wald confidence interval of an accuracy, in percent."""
    p = hits / n
    half = 1.959964 * math.sqrt(p * (1 - p) / n)
    return 100 * (p - half), 100 * (p + half)


def bin_stats(rows):
    """Return (count, accuracy) per confidence bin."""
    stats = []
    for in_bin, _ in BINS:
        sub = [hit for confidence, hit in rows if in_bin(confidence)]
        stats.append((len(sub), 100 * sum(sub) / len(sub)))
    return stats


def condition_figure(cond_accuracy, lang):
    """Plot decision and topic accuracy per condition."""
    text = LABELS[lang]
    x = list(range(len(CONDITIONS)))
    width = 0.36
    series = [
        ([cond_accuracy[c][q] for c in CONDITIONS], text[q], color)
        for q, color in [('decision', '#4b74a6'), ('topic', '#b34700')]
    ]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    for offset, (values, name, color) in zip([-width / 2, width / 2], series):
        bars = ax.bar([i + offset for i in x], values, width, label=name, color=color)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.5, f'{value:.0f}',
                    ha='center', fontsize=9)
    ax.set_xticks(x, text['conditions'], fontsize=9)
    ax.set_ylabel(text['cond_ylabel'])
    ax.set_ylim(75, 100)
    ax.legend(loc='upper right', fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'condition-accuracy.png', dpi=150)
    plt.close(fig)


def confidence_figure(stats, lang):
    """Plot the answer distribution and accuracy per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, label in BINS]
    counts = [count for count, _ in stats]
    accuracies = [accuracy for _, accuracy in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        if count >= 100:
            ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
        else:
            ax1.text(i, count + 12, str(count), ha='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    ax2.plot(x, accuracies, marker='o', color='#b34700')
    for i, accuracy in zip(x, accuracies):
        ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(100 / 3, ls='--', lw=1, color='#888888')
    ax2.text(0, 35.5, text['random'], ha='left', fontsize=8, color='#888888')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def main():
    reference, metadata, records, ok = load()

    # Overall accuracy per question, with 95% Wald intervals.
    print(f'records {len(records)}, failed {len(records) - len(ok)}')
    for q in QUESTIONS:
        hits, acc = accuracy(ok, reference, q)
        lo, hi = wald_interval(hits, len(ok))
        print(f'{q}: {hits}/{len(ok)} = {acc:.2f}% (95% CI {lo:.2f}-{hi:.2f})')
    both = sum(1 for r in ok
               if all(correct(r, reference, q) for q in QUESTIONS))
    print(f'both correct: {both}/{len(ok)} = {100 * both / len(ok):.2f}%')

    # Accuracy and cost per condition.
    cond_accuracy = {}
    for cond in CONDITIONS:
        sub = [r for r in ok if metadata[r['id']]['condition'] == cond]
        cond_accuracy[cond] = {}
        line = f'condition {cond}:'
        for q in QUESTIONS:
            hits, acc = accuracy(sub, reference, q)
            cond_accuracy[cond][q] = acc
            line += f' {q} {hits}/{len(sub)} = {acc:.1f}%'
        tokens_in = sum(r['response']['usage']['input_tokens'] for r in sub)
        tokens_out = sum(r['response']['usage']['output_tokens'] for r in sub)
        cost = sum(r['response']['usage']['cost'] for r in sub)
        print(f'{line} | in {tokens_in:,} out {tokens_out:,} ${cost:.4f}')

    # Marginal ablation effects, averaged over the other factor.
    crit = [c for c in CONDITIONS if c.endswith('_crit')]
    nocrit = [c for c in CONDITIONS if c.endswith('_nocrit')]
    full = [c for c in CONDITIONS if c.startswith('full')]
    min_ = [c for c in CONDITIONS if c.startswith('min')]
    for q in QUESTIONS:
        crit_acc = sum(cond_accuracy[c][q] for c in crit) / 2
        nocrit_acc = sum(cond_accuracy[c][q] for c in nocrit) / 2
        full_acc = sum(cond_accuracy[c][q] for c in full) / 2
        min_acc = sum(cond_accuracy[c][q] for c in min_) / 2
        print(f'{q}: criteria {crit_acc:.2f} vs no criteria {nocrit_acc:.2f};'
              f' full state {full_acc:.2f} vs min state {min_acc:.2f}')

    # Marginal input-token cost of each factor, averaged over the other factor.
    cond_in = {c: sum(r['response']['usage']['input_tokens']
                      for r in ok if metadata[r['id']]['condition'] == c)
               for c in CONDITIONS}
    crit_in = sum(cond_in[c] for c in crit) / 2
    nocrit_in = sum(cond_in[c] for c in nocrit) / 2
    full_in = sum(cond_in[c] for c in full) / 2
    min_in = sum(cond_in[c] for c in min_) / 2
    print(f'input tokens: criteria {crit_in:,.0f} vs no criteria {nocrit_in:,.0f};'
          f' full state {full_in:,.0f} vs min state {min_in:,.0f}')

    # Accuracy per selection group and venue acceptance.
    for group in ['memory', 'self_evolution', 'agent_other', 'off_topic']:
        sub = [r for r in ok if metadata[r['id']]['selection_group'] == group]
        line = f'selection_group {group} (n={len(sub)}):'
        for q in QUESTIONS:
            _, acc = accuracy(sub, reference, q)
            line += f' {q} {acc:.1f}%'
        print(line)
    for flag in [True, False]:
        sub = [r for r in ok if metadata[r['id']]['venue_accepted'] == flag]
        line = f'venue_accepted {flag} (n={len(sub)}):'
        for q in QUESTIONS:
            _, acc = accuracy(sub, reference, q)
            line += f' {q} {acc:.2f}%'
        print(line)

    # Confidence bins over the 800 per-question answers.
    rows = [(r['response']['answers'][q]['confidence'], correct(r, reference, q))
            for r in ok for q in QUESTIONS]
    stats = bin_stats(rows)
    print(f'confidence bins over {len(rows)} answers:')
    for (_, label), (count, acc) in zip(BINS, stats):
        print(f'  {label:8s} n={count:4d} ({100 * count / len(rows):.1f}%) accuracy {acc:.2f}%')
    for q in QUESTIONS:
        qrows = [(r['response']['answers'][q]['confidence'], correct(r, reference, q))
                 for r in ok]
        qstats = bin_stats(qrows)
        line = f'  {q}:'
        for (_, label), (count, acc) in zip(BINS, qstats):
            line += f' {label} n={count} acc {acc:.1f}% |'
        print(line)

    # Error directions and choice distribution.
    for q in QUESTIONS:
        errors = Counter((reference[r['id']][q], r['response']['answers'][q]['choice'])
                         for r in ok if not correct(r, reference, q))
        choices = Counter(r['response']['answers'][q]['choice'] for r in ok)
        print(f'{q} choices {dict(choices)}; errors {dict(errors)}')
    unsure_probs = [r['response']['answers']['decision']['probabilities'].get('unsure', 0)
                    for r in ok]
    print(f'unsure chosen 0 times; max unsure probability {max(unsure_probs):.2f}')

    # Error concentration across papers and cross-condition consistency.
    for q in QUESTIONS:
        error_papers = Counter(r['id'].split('__')[0] for r in ok
                               if not correct(r, reference, q))
        always = sum(1 for n in error_papers.values() if n == 4)
        print(f'{q} errors on {len(error_papers)} papers, {always} wrong in all 4 conditions')
    by_paper = {}
    for r in ok:
        pid = r['id'].split('__')[0]
        by_paper.setdefault(pid, {})[metadata[r['id']]['condition']] = r
    for q in QUESTIONS:
        same = sum(1 for p in by_paper.values()
                   if len({r['response']['answers'][q]['choice'] for r in p.values()}) == 1)
        print(f'papers with identical {q} across conditions: {same}/{len(by_paper)}')

    # Output quirks: probability sums and choice-probability agreement.
    bad_sum = 0
    mismatch = 0
    for r in ok:
        for q in QUESTIONS:
            answer = r['response']['answers'][q]
            if abs(sum(answer['probabilities'].values()) - 1) > 1e-6:
                bad_sum += 1
            if max(answer['probabilities'], key=answer['probabilities'].get) != answer['choice']:
                mismatch += 1
    print(f'probability sums != 1: {bad_sum}/800; choice != top probability: {mismatch}/800')

    # Token and cost totals.
    tokens_in = sum(r['response']['usage']['input_tokens'] for r in ok)
    tokens_out = sum(r['response']['usage']['output_tokens'] for r in ok)
    cost = sum(r['response']['usage']['cost'] for r in ok)
    print(f'usage: in {tokens_in:,}, out {tokens_out:,}, ${cost:.4f}')

    # Figures, one set per language.
    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        condition_figure(cond_accuracy, lang)
        confidence_figure(stats, lang)
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
