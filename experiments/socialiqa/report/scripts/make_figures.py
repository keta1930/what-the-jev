"""Rebuild the report figures and stats from the dataset and responses."""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

CONF_BINS = [
    (0.0, 0.6, '<0.6'),
    (0.6, 0.85, '0.6–0.85'),
    (0.85, 1.01, '≥0.85'),
]

DIM_GLOSS = {
    'en': {
        'xIntent': 'why the person acted',
        'xNeed': 'what the person needed before',
        'xAttr': 'how to describe the person',
        'xReact': 'how the person feels after',
        'xEffect': 'what happens to the person',
        'xWant': 'what the person wants next',
        'oReact': 'how others feel after',
        'oEffect': 'what happens to others',
        'oWant': 'what others want next',
    },
    'zh': {
        'xIntent': '当事人为何这样做',
        'xNeed': '当事人事先需要什么',
        'xAttr': '如何描述当事人',
        'xReact': '当事人事后感受',
        'xEffect': '对当事人的影响',
        'xWant': '当事人想做什么',
        'oReact': '他人的感受',
        'oEffect': '对他人的影响',
        'oWant': '他人想做什么',
    },
}

LABELS = {
    'en': {
        'conf_xlabel': 'confidence reported with the answer',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
        'random': 'random guess 33.3%',
        'dim_xlabel': 'accuracy (%)',
        'overall': 'overall 80.6%',
        'dim_title': 'Accuracy by ATOMIC dimension',
    },
    'zh': {
        'conf_xlabel': '作答给出的 confidence',
        'answers': '题数',
        'accuracy': '准确率（%）',
        'random': '随机猜测 33.3%',
        'dim_xlabel': '准确率（%）',
        'overall': '整体 80.6%',
        'dim_title': '按 ATOMIC 维度分组的准确率',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the reference answers, dimension labels, and successful records."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    reference = {s['id']: s['reference']['answer']['choice'] for s in dataset['samples']}
    dims = {s['id']: s['metadata']['promptDim'] for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    return reference, dims, ok


def collect_rows(reference, dims, records):
    """Return one dict per record with choice, confidence, correctness, and usage."""
    rows = []
    for record in records:
        answer = record['response']['answers']['answer']
        rows.append({
            'id': record['id'],
            'dim': dims[record['id']],
            'choice': answer['choice'],
            'confidence': answer['confidence'],
            'probabilities': answer['probabilities'],
            'correct': answer['choice'] == reference[record['id']],
            'usage': record['response']['usage'],
        })
    return rows


def confidence_figure(bin_stats, lang):
    """Plot the answer distribution and accuracy per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in CONF_BINS]
    counts = [count for count, _ in bin_stats]
    accuracies = [accuracy for _, accuracy in bin_stats]
    x = list(range(len(CONF_BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8', width=0.55)
    for i, count in zip(x, counts):
        ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['conf_xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    ax2.plot(x, accuracies, marker='o', color='#b34700')
    for i, accuracy in zip(x, accuracies):
        ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(100 / 3, ls='--', lw=1, color='#888888')
    ax2.text(len(CONF_BINS) - 1, 35.5, text['random'], ha='right', fontsize=8, color='#888888')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def dimension_figure(dim_stats, overall_accuracy, lang):
    """Plot per-dimension accuracy with the overall level marked."""
    text = LABELS[lang]
    entries = sorted(dim_stats, key=lambda entry: entry[2])
    names = [f"{dim} · {DIM_GLOSS[lang][dim]}" for dim, _, _ in entries]
    values = [accuracy for _, _, accuracy in entries]

    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.barh(names, values, color='#4b74a6', height=0.62)
    for index, value in enumerate(values):
        ax.text(value + 0.6, index, f'{value:.1f}', va='center', fontsize=8)
    ax.axvline(overall_accuracy, ls='--', lw=1, color='#b34700')
    ax.text(overall_accuracy, -0.75, text['overall'], ha='center', va='center',
            fontsize=8, color='#b34700')
    ax.axvline(100 / 3, ls=':', lw=1, color='#888888')
    ax.text(100 / 3, -0.75, text['random'], ha='center', va='center', fontsize=8, color='#888888')
    ax.set_ylim(-1.1, len(entries) - 0.5 + 0.1)
    ax.set_xlabel(text['dim_xlabel'])
    ax.set_xlim(0, 100)
    ax.set_title(text['dim_title'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'dimension-accuracy.png', dpi=150)
    plt.close(fig)


def main():
    reference, dims, records = load()
    rows = collect_rows(reference, dims, records)
    n = len(rows)
    positions = {letter: sum(1 for choice in reference.values() if choice == letter)
                 for letter in 'ABC'}
    correct = sum(row['correct'] for row in rows)
    accuracy = 100 * correct / n
    p = correct / n
    ci = 100 * 1.96 * math.sqrt(p * (1 - p) / n)

    bin_stats = []
    for lo, hi, _ in CONF_BINS:
        sub = [row['correct'] for row in rows if lo <= row['confidence'] < hi]
        bin_stats.append((len(sub), 100 * sum(sub) / len(sub)))

    dim_stats = []
    for dim in sorted({row['dim'] for row in rows}):
        sub = [row['correct'] for row in rows if row['dim'] == dim]
        dim_stats.append((dim, len(sub), 100 * sum(sub) / len(sub)))

    bad_sum = [row for row in rows if abs(sum(row['probabilities'].values()) - 1) > 1e-6]
    bad_argmax = [row for row in rows
                  if max(row['probabilities'], key=row['probabilities'].get) != row['choice']]
    input_tokens = sum(row['usage']['input_tokens'] for row in rows)
    output_tokens = sum(row['usage']['output_tokens'] for row in rows)
    cost = sum(row['usage']['cost'] for row in rows)
    mean_confidence = sum(row['confidence'] for row in rows) / n

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(bin_stats, lang)
        dimension_figure(dim_stats, accuracy, lang)

    print(f'reference positions: {positions}')
    print(f'answers {n}, correct {correct}, accuracy {accuracy:.2f}% (95% CI {accuracy - ci:.2f}–{accuracy + ci:.2f})')
    print(f'mean confidence {mean_confidence:.3f}')
    for (lo, hi, label), (count, bin_accuracy) in zip(CONF_BINS, bin_stats):
        print(f'  confidence {label:9s} n={count:4d} share={100 * count / n:5.1f}% accuracy {bin_accuracy:.2f}%')
    for dim, count, dim_accuracy in sorted(dim_stats, key=lambda entry: -entry[2]):
        print(f'  {dim:8s} n={count:4d} accuracy {dim_accuracy:.2f}%')
    print(f'blemishes: prob sum != 1: {len(bad_sum)}, choice != argmax: {len(bad_argmax)}')
    print(f'usage: input {input_tokens:,} output {output_tokens:,} cost ${cost:.4f}')
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
