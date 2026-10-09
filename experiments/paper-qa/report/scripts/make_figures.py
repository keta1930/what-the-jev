"""Rebuild the report figures and stats from the dataset, responses, and paper list."""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

BINS = [
    (0.0, 0.2, '<0.2'),
    (0.2, 0.4, '0.2–0.4'),
    (0.4, 0.6, '0.4–0.6'),
    (0.6, 0.8, '0.6–0.8'),
    (0.8, 1.01, '≥0.8'),
]

LABELS = {
    'en': {
        'xlabel': 'noul output value',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
        'random': 'random guess 50%',
        'dom_xlabel': 'accuracy (%)',
        'dom_title': 'Accuracy by domain (30 questions each)',
        'domains': {},
    },
    'zh': {
        'xlabel': 'noul 输出值',
        'answers': '题数',
        'accuracy': '准确率（%）',
        'random': '随机猜测 50%',
        'dom_xlabel': '准确率（%）',
        'dom_title': '分主题域准确率（每域 30 题）',
        'domains': {
            'agent': '智能体',
            'behavior-simulation': '行为模拟',
            'interpretability-alignment': '可解释性与对齐',
            'memory': '记忆',
            'prompt-injection': '提示注入',
            'reasoning': '推理',
            'self-evolution': '自我进化',
            'training': '训练',
        },
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the samples, successful records, and paper domain map."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    samples = {s['id']: s for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    papers = json.loads((ROOT / 'preparation' / 'raw' / 'papers.json').read_text())
    domains = {p['slug']: p['domain'] for p in papers['papers']}
    return samples, ok, domains


def collect_rows(samples, records, domains):
    """Return (id, domain, reference, noul value, correct) per record."""
    rows = []
    for record in records:
        sample = samples[record['id']]
        name = next(iter(sample['input']['questions']))
        reference = sample['reference'][name]['noul']
        value = record['response']['answers'][name]['noul']
        correct = (value >= 0.5) == reference
        rows.append((record['id'], domains[sample['metadata']['paper']], reference, value, correct))
    return rows


def wilson(correct, total):
    """Return the 95% Wilson score interval in percent."""
    phat = correct / total
    z = 1.959964
    den = 1 + z * z / total
    center = (phat + z * z / (2 * total)) / den
    half = z * math.sqrt(phat * (1 - phat) / total + z * z / (4 * total * total)) / den
    return 100 * (center - half), 100 * (center + half)


def bin_stats(rows):
    """Return (count, accuracy) per noul value bin; accuracy is None when empty."""
    stats = []
    for lo, hi, _ in BINS:
        sub = [correct for _, _, _, value, correct in rows if lo <= value < hi]
        stats.append((len(sub), 100 * sum(sub) / len(sub) if sub else None))
    return stats


def confidence_figure(stats, lang):
    """Plot the answer distribution and accuracy per noul value bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in BINS]
    counts = [count for count, _ in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        if count >= 100:
            ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
        elif count > 0:
            ax1.text(i, count + 6, str(count), ha='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    xs = [i for i, (_, accuracy) in zip(x, stats) if accuracy is not None]
    ys = [accuracy for _, accuracy in stats if accuracy is not None]
    ax2.plot(xs, ys, marker='o', color='#b34700')
    for i, accuracy in zip(xs, ys):
        if accuracy == 0:
            ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                         xytext=(10, 6), ha='left', fontsize=9, color='#b34700')
        else:
            ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                         xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(50, ls='--', lw=1, color='#888888')
    ax2.text(1.2, 41, text['random'], ha='right', fontsize=8, color='#888888')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def domain_figure(domain_stats, lang):
    """Plot per-domain accuracy as horizontal bars."""
    text = LABELS[lang]
    names = sorted(domain_stats)
    labels = [text['domains'].get(name, name) for name in names]
    accuracies = [100 * domain_stats[name][0] / domain_stats[name][1] for name in names]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.barh(labels, accuracies, color='#4b74a6')
    for index, (accuracy, name) in enumerate(zip(accuracies, names)):
        correct, total = domain_stats[name]
        ax.text(accuracy - 1, index, f'{accuracy:.1f} ({correct}/{total})',
                va='center', ha='right', fontsize=8, color='white')
    ax.set_xlabel(text['dom_xlabel'])
    ax.set_xlim(0, 105)
    ax.set_title(text['dom_title'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'domain-accuracy.png', dpi=150)
    plt.close(fig)


def main():
    samples, records, domains = load()
    rows = collect_rows(samples, records, domains)
    total = len(rows)
    correct = sum(row[4] for row in rows)
    lo, hi = wilson(correct, total)
    print(f'records {len(records)}, answers {total}, accuracy {100 * correct / total:.2f}% '
          f'({correct}/{total}), 95% CI {lo:.2f}–{hi:.2f}')

    reference_true = sum(1 for row in rows if row[2])
    print(f'reference: supported {reference_true}, refuted {total - reference_true}')

    errors = [row for row in rows if not row[4]]
    for row in errors:
        print(f'error: {row[0]} domain={row[1]} reference={row[2]} noul={row[3]}')

    domain_stats = {}
    for _, domain, _, _, is_correct in rows:
        stat = domain_stats.setdefault(domain, [0, 0])
        stat[0] += is_correct
        stat[1] += 1
    for name in sorted(domain_stats):
        c, n = domain_stats[name]
        print(f'domain {name}: {c}/{n} = {100 * c / n:.1f}%')

    stats = bin_stats(rows)
    for (_, _, label), (count, accuracy) in zip(BINS, stats):
        rendered = f'{accuracy:.2f}%' if accuracy is not None else 'n/a'
        print(f'noul {label:8s} n={count:4d} accuracy {rendered}')

    extreme = [row for row in rows if row[3] < 0.1 or row[3] > 0.9]
    middle = [row for row in rows if 0.4 < row[3] < 0.6]
    print(f'extreme (<0.1 or >0.9): {len(extreme)} ({100 * len(extreme) / total:.1f}%), '
          f'middle (0.4–0.6): {len(middle)}')
    low_ref_true = min(row[3] for row in rows if row[2])
    high_ref_false = max(row[3] for row in rows if not row[2])
    print(f'reference true: min noul {low_ref_true}; reference false: max noul {high_ref_false}')

    input_tokens = sum(r['response']['usage']['input_tokens'] for r in records)
    output_tokens = sum(r['response']['usage']['output_tokens'] for r in records)
    cost = sum(r['response']['usage']['cost'] for r in records)
    print(f'usage: input {input_tokens:,}, output {output_tokens:,}, cost ${cost:.4f}')

    sizes = [len(s['input']['state']['paper_excerpt'].encode()) for s in samples.values()]
    print(f'excerpt bytes: {min(sizes):,}–{max(sizes):,}')

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(stats, lang)
        domain_figure(domain_stats, lang)
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
