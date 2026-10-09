"""Rebuild the report figures and stats from the dataset and responses."""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

CATEGORIES = ['explain', 'evaluate', 'compare', 'synthesize', 'quantitative', 'design']

# confidence = probability on the side the model leans to, max(p, 1 - p)
BINS = [
    (0.5, 0.6, '0.5–0.6'),
    (0.6, 0.7, '0.6–0.7'),
    (0.7, 0.8, '0.7–0.8'),
    (0.8, 0.9, '0.8–0.9'),
    (0.9, 1.001, '0.9–1.0'),
]

LABELS = {
    'en': {
        'positive': 'fast-path questions',
        'groups_xlabel': 'accuracy (%)',
        'groups_title': 'routing accuracy by question group',
        'random': 'random 50%',
        'conf_xlabel': 'confidence = max(p, 1 − p)',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
    },
    'zh': {
        'positive': '快路径提问',
        'groups_xlabel': '准确率（%）',
        'groups_title': '分组路由准确率',
        'random': '随机 50%',
        'conf_xlabel': '置信度 = max(p, 1 − p)',
        'answers': '题数',
        'accuracy': '准确率（%）',
    },
}

CATEGORY_ZH = {
    'explain': '解释',
    'evaluate': '评估',
    'compare': '对比',
    'synthesize': '综合',
    'quantitative': '定量',
    'design': '设计',
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the samples by id and the successful records."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    samples = {s['id']: s for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    return samples, ok


def collect_rows(samples, records):
    """Return (id, p, reference, correct, group, confidence) per record."""
    rows = []
    for record in records:
        sample = samples[record['id']]
        reference = sample['reference']['use_fast_path']['noul']
        p = record['response']['answers']['use_fast_path']['noul']
        group = 'positive' if reference else sample['metadata']['category']
        correct = (p >= 0.5) == reference
        confidence = round(max(p, 1 - p), 2)  # round to kill float noise
        rows.append((record['id'], p, reference, correct, group, confidence))
    return rows


def wilson(correct, total):
    """Return the 95% Wilson interval of an accuracy in percent."""
    z, phat = 1.96, correct / total
    denom = 1 + z * z / total
    center = (phat + z * z / (2 * total)) / denom
    half = z * math.sqrt(phat * (1 - phat) / total + z * z / (4 * total * total)) / denom
    return 100 * (center - half), 100 * (center + half)


def group_stats(rows):
    """Return (count, correct) for positives, negatives, and each category."""
    stats = {'positive': [0, 0], 'negative': [0, 0]}
    stats.update({c: [0, 0] for c in CATEGORIES})
    for _, _, reference, correct, group, _ in rows:
        keys = ['positive'] if reference else ['negative', group]
        for name in keys:
            stats[name][0] += 1
            stats[name][1] += correct
    return stats


def bin_stats(rows):
    """Return (count, correct) per confidence bin; the first bin includes 0.6."""
    stats = []
    for index, (lo, hi, _) in enumerate(BINS):
        if index == 0:
            sub = [r for r in rows if lo <= r[5] <= hi]
        else:
            sub = [r for r in rows if lo < r[5] <= hi]
        stats.append((len(sub), sum(r[3] for r in sub)))
    return stats


def groups_figure(stats, lang):
    """Plot routing accuracy for positives and each negative category."""
    text = LABELS[lang]
    names = [text['positive']] + [
        CATEGORY_ZH[c] if lang == 'zh' else c for c in CATEGORIES
    ]
    keys = ['positive'] + CATEGORIES
    counts = [stats[k][0] for k in keys]
    accuracies = [100 * stats[k][1] / stats[k][0] for k in keys]
    labels = [f'{name} (n={count})' for name, count in zip(names, counts)]
    colors = ['#b34700' if key == 'quantitative' else '#4b74a6' for key in keys]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.barh(labels, accuracies, color=colors)
    for index, (accuracy, count, correct) in enumerate(
            zip(accuracies, counts, [stats[k][1] for k in keys])):
        ax.text(accuracy - 1.5, index, f'{correct}/{count}', va='center',
                ha='right', fontsize=9, color='white')
    ax.axvline(50, ls='--', lw=1, color='#888888')
    ax.set_ylim(len(labels) + 0.2, -0.6)  # inverted, with room below the last bar
    ax.text(51.5, len(labels) - 0.15, text['random'], ha='left', va='center',
            fontsize=8, color='#888888')
    ax.set_xlabel(text['groups_xlabel'])
    ax.set_xlim(0, 105)
    ax.set_title(text['groups_title'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'group-accuracy.png', dpi=150)
    plt.close(fig)


def confidence_figure(stats, lang):
    """Plot the answer distribution and accuracy per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in BINS]
    counts = [count for count, _ in stats]
    accuracies = [100 * correct / count for count, correct in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        if count >= 100:
            ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
        else:
            ax1.text(i, count + 6, str(count), ha='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['conf_xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    ax2.plot(x, accuracies, marker='o', color='#b34700')
    for i, accuracy in zip(x, accuracies):
        ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(50, ls='--', lw=1, color='#888888')
    ax2.text(1.5, 52, text['random'], ha='center', fontsize=8, color='#888888')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def main():
    samples, records = load()
    rows = collect_rows(samples, records)
    stats = group_stats(rows)
    bins = bin_stats(rows)

    papers = {}
    for sample in samples.values():
        reference = sample['reference']['use_fast_path']['noul']
        entry = papers.setdefault(sample['metadata']['paper'], [0, 0])
        entry[0 if reference else 1] += 1
    splits = {tuple(v) for v in papers.values()}
    print(f'dataset: {len(samples)} questions over {len(papers)} papers, '
          f'per-paper (fast, slow) splits {sorted(splits)}')

    example = next(r for r in records if r['id'] == 'hindsight-01')
    print('example hindsight-01:', json.dumps(example['response']['answers']),
          json.dumps(example['response']['usage']))

    total, correct = len(rows), sum(r[3] for r in rows)
    lo, hi = wilson(correct, total)
    print(f'answers {total}, correct {correct}, accuracy {100 * correct / total:.2f}% '
          f'(95% CI {lo:.2f}–{hi:.2f}%)')
    for key in ['positive', 'negative'] + CATEGORIES:
        count, group_correct = stats[key]
        print(f'  {key:12s} {group_correct}/{count} = {100 * group_correct / count:.2f}% '
              f'(share {100 * count / total:.1f}%)')

    errors = [r for r in rows if not r[3]]
    print(f'errors {len(errors)}, categories {sorted({r[4] for r in errors})}, '
          f'p range {min(r[1] for r in errors):.2f}–{max(r[1] for r in errors):.2f}')

    for (lo_, hi_, label), (count, bin_correct) in zip(BINS, bins):
        print(f'  confidence {label:8s} n={count:3d} share {100 * count / total:.1f}% '
              f'accuracy {100 * bin_correct / count:.2f}%')

    high = [r for r in rows if r[5] > 0.8]
    print(f'confidence >0.8: {len(high)}/{total} = {100 * len(high) / total:.1f}%, '
          f'all correct: {all(r[3] for r in high)}')
    pos_correct = [r[1] for r in rows if r[2] and r[3]]
    neg_correct = [r[1] for r in rows if not r[2] and r[3]]
    print(f'correct positives min p {min(pos_correct):.2f}, '
          f'correct negatives max p {max(neg_correct):.2f}')

    input_tokens = sum(r['response']['usage']['input_tokens'] for r in records)
    output_tokens = sum(r['response']['usage']['output_tokens'] for r in records)
    cost = sum(r['response']['usage']['cost'] for r in records)
    print(f'usage input {input_tokens:,} output {output_tokens:,} cost ${cost:.4f}')

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        groups_figure(stats, lang)
        confidence_figure(bins, lang)
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
