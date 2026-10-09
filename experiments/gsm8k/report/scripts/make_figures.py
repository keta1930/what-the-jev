"""Rebuild the report figures and stats from the dataset, responses, and leaderboard snapshot."""

import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

BINS = [
    (0.0, 0.3, '<0.3'),
    (0.3, 0.5, '0.3–0.5'),
    (0.5, 0.7, '0.5–0.7'),
    (0.7, 0.9, '0.7–0.9'),
    (0.9, 0.99, '0.9–0.99'),
    (0.99, 1.01, '≥0.99'),
]

LABELS = {
    'en': {
        'xlabel': 'probability assigned to the chosen option',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
        'random': 'random guess 25%',
        'jev': 'JEV-1.13 (four-choice)',
        'lb_xlabel': 'GSM8K accuracy (%)',
        'lb_title': 'HF GSM8K leaderboard (≤32B) vs JEV',
    },
    'zh': {
        'xlabel': '所选选项的概率',
        'answers': '题数',
        'accuracy': '准确率（%）',
        'random': '随机猜测 25%',
        'jev': 'JEV-1.13（四选一）',
        'lb_xlabel': 'GSM8K 准确率（%）',
        'lb_title': 'HF GSM8K 榜单（≤32B）与 JEV 对比',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the reference answers, successful records, and leaderboard entries."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    reference = {s['id']: s['reference']['answer']['choice'] for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    leaderboard = json.loads((ROOT / 'preparation' / 'raw' / 'leaderboard-latest.json').read_text())
    return reference, ok, leaderboard


def selected_probabilities(reference, records):
    """Return (selected probability, correct) per record."""
    rows = []
    for record in records:
        answer = record['response']['answers']['answer']
        prob = answer['probabilities'][answer['choice']]
        rows.append((prob, answer['choice'] == reference[record['id']]))
    return rows


def bin_stats(rows):
    """Return (count, accuracy) per probability bin."""
    stats = []
    for lo, hi, _ in BINS:
        sub = [correct for prob, correct in rows if lo <= prob < hi]
        stats.append((len(sub), 100 * sum(sub) / len(sub)))
    return stats


def confidence_figure(stats, lang):
    """Plot the answer distribution and accuracy per probability bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in BINS]
    counts = [count for count, _ in stats]
    accuracies = [accuracy for _, accuracy in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        if count >= 100:
            ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
        else:
            ax1.text(i, count + 8, str(count), ha='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['xlabel'])
    ax1.set_ylabel(text['answers'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    ax2.plot(x, accuracies, marker='o', color='#b34700')
    for i, accuracy in zip(x, accuracies):
        ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(25, ls='--', lw=1, color='#888888')
    ax2.text(len(BINS) - 1, 26.5, text['random'], ha='right', fontsize=8, color='#888888')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def leaderboard_figure(leaderboard, jev_accuracy, lang):
    """Plot leaderboard scores with JEV's position highlighted."""
    text = LABELS[lang]
    entries = [(row['modelId'].split('/')[-1], row['value']) for row in leaderboard]
    entries.append((text['jev'], jev_accuracy))
    entries.sort(key=lambda entry: entry[1])
    names = [name for name, _ in entries]
    values = [value for _, value in entries]
    colors = ['#b34700' if name == text['jev'] else '#4b74a6' for name in names]

    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.barh(names, values, color=colors)
    for index, value in enumerate(values):
        ax.text(value + 0.4, index, f'{value:.2f}', va='center', fontsize=8)
    ax.set_xlabel(text['lb_xlabel'])
    ax.set_xlim(0, 105)
    ax.set_title(text['lb_title'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'leaderboard-position.png', dpi=150)
    plt.close(fig)


def main():
    reference, records, leaderboard = load()
    rows = selected_probabilities(reference, records)
    accuracy = 100 * sum(correct for _, correct in rows) / len(rows)
    stats = bin_stats(rows)

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(stats, lang)
        leaderboard_figure(leaderboard, accuracy, lang)

    print(f'answers {len(rows)}, accuracy {accuracy:.2f}%')
    for (lo, hi, label), (count, bin_accuracy) in zip(BINS, stats):
        print(f'  {label:8s} n={count:4d} accuracy {bin_accuracy:.2f}%')
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
