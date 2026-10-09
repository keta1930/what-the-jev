"""Rebuild the report figures from the dataset, responses, and leaderboard snapshot."""

import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

CONFIDENCE_BINS = [(0.0, 0.6, '<0.6'), (0.6, 0.85, '0.6–0.85'), (0.85, 1.01, '≥0.85')]
RANDOM_LEVEL = 10

CATEGORY_ZH = {
    'biology': '生物学',
    'business': '商业',
    'chemistry': '化学',
    'computer science': '计算机科学',
    'economics': '经济学',
    'engineering': '工程',
    'health': '健康',
    'history': '历史',
    'law': '法律',
    'math': '数学',
    'other': '其他',
    'philosophy': '哲学',
    'physics': '物理',
    'psychology': '心理学',
}

LABELS = {
    'en': {
        'cat_xlabel': 'accuracy (%)',
        'cat_title': 'Accuracy by category (14 categories)',
        'overall': 'overall {value:.2f}%',
        'random': 'random ~10%',
        'conf_xlabel': 'confidence',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
        'jev': 'JEV-1.13',
        'lb_xlabel': 'MMLU-Pro accuracy (%)',
        'lb_ylabel': 'models',
        'lb_title': 'HF MMLU-Pro leaderboard (141 entries) vs JEV',
        'lb_rank': 'JEV-1.13: {value:.2f} (rank {rank} of {total})',
    },
    'zh': {
        'cat_xlabel': '准确率（%）',
        'cat_title': '分类别准确率（14 类）',
        'overall': '整体 {value:.2f}%',
        'random': '随机约 10%',
        'conf_xlabel': '置信度',
        'answers': '题数',
        'accuracy': '准确率（%）',
        'jev': 'JEV-1.13',
        'lb_xlabel': 'MMLU-Pro 准确率（%）',
        'lb_ylabel': '模型数',
        'lb_title': 'HF MMLU-Pro 榜单（141 条）与 JEV 对比',
        'lb_rank': 'JEV-1.13：{value:.2f}（第 {rank}/{total} 名）',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the samples, successful records, and leaderboard entries."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    leaderboard = json.loads((ROOT / 'preparation' / 'raw' / 'leaderboard-latest.json').read_text())
    return dataset['samples'], [r for r in records if r['error'] is None], leaderboard


def category_stats(samples, records):
    """Return (category, count, accuracy) rows sorted by accuracy ascending."""
    reference = {s['id']: s['reference']['answer']['choice'] for s in samples}
    records_by_id = {r['id']: r for r in records}
    rows = []
    for name in sorted({s['metadata']['category'] for s in samples}):
        ids = [s['id'] for s in samples if s['metadata']['category'] == name]
        hits = sum(records_by_id[i]['response']['answers']['answer']['choice'] == reference[i]
                   for i in ids)
        rows.append((name, len(ids), 100 * hits / len(ids)))
    return sorted(rows, key=lambda row: row[2])


def confidence_stats(samples, records):
    """Return (count, accuracy) per confidence bin."""
    reference = {s['id']: s['reference']['answer']['choice'] for s in samples}
    stats = []
    for lo, hi, _ in CONFIDENCE_BINS:
        sub = [r for r in records
               if lo <= r['response']['answers']['answer']['confidence'] < hi]
        hits = sum(r['response']['answers']['answer']['choice'] == reference[r['id']] for r in sub)
        stats.append((len(sub), 100 * hits / len(sub)))
    return stats


def category_figure(rows, overall, lang):
    """Plot per-category accuracy bars with the overall and random references."""
    text = LABELS[lang]
    names = [CATEGORY_ZH[name] if lang == 'zh' else name for name, _, _ in rows]
    accuracies = [accuracy for _, _, accuracy in rows]

    fig, ax = plt.subplots(figsize=(7, 5.6))
    ax.barh(names, accuracies, color='#4b74a6')
    for index, accuracy in enumerate(accuracies):
        ax.text(accuracy + 0.6, index, f'{accuracy:.1f}', va='center', fontsize=8)
    ax.set_ylim(-0.6, len(rows) + 0.8)
    ax.axvline(overall, ls='--', lw=1, color='#b34700')
    ax.text(overall - 0.8, len(rows) + 0.3, text['overall'].format(value=overall),
            ha='right', va='center', fontsize=8, color='#b34700')
    ax.axvline(RANDOM_LEVEL, ls=':', lw=1, color='#888888')
    ax.text(RANDOM_LEVEL + 0.8, len(rows) + 0.3, text['random'],
            va='center', fontsize=8, color='#888888')
    ax.set_xlabel(text['cat_xlabel'])
    ax.set_xlim(0, 105)
    ax.set_title(text['cat_title'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'category-accuracy.png', dpi=150)
    plt.close(fig)


def confidence_figure(stats, lang):
    """Plot the answer distribution and accuracy per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in CONFIDENCE_BINS]
    counts = [count for count, _ in stats]
    accuracies = [accuracy for _, accuracy in stats]
    x = list(range(len(CONFIDENCE_BINS)))

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
    ax2.axhline(RANDOM_LEVEL, ls='--', lw=1, color='#888888')
    ax2.text(len(CONFIDENCE_BINS) - 1, RANDOM_LEVEL + 2, text['random'],
             ha='right', fontsize=8, color='#888888')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def leaderboard_figure(leaderboard, jev_accuracy, lang):
    """Plot the leaderboard score histogram with JEV's position marked."""
    text = LABELS[lang]
    values = [row['value'] for row in leaderboard]
    above = sum(value > jev_accuracy for value in values)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    counts, _, _ = ax.hist(values, bins=range(0, 95, 5), color='#4b74a6', edgecolor='white')
    ax.set_ylim(0, max(counts) * 1.28)
    ax.axvline(jev_accuracy, ls='--', lw=1.5, color='#b34700')
    ax.annotate(text['lb_rank'].format(value=jev_accuracy, rank=above + 1,
                                       total=len(values) + 1),
                (jev_accuracy, ax.get_ylim()[1]), textcoords='offset points',
                xytext=(-6, -14), ha='right', fontsize=9, color='#b34700')
    ax.set_xlabel(text['lb_xlabel'])
    ax.set_ylabel(text['lb_ylabel'])
    ax.set_xlim(0, 95)
    ax.set_title(text['lb_title'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'leaderboard-position.png', dpi=150)
    plt.close(fig)


def main():
    samples, records, leaderboard = load()
    reference = {s['id']: s['reference']['answer']['choice'] for s in samples}
    accuracy = 100 * sum(r['response']['answers']['answer']['choice'] == reference[r['id']]
                         for r in records) / len(records)
    categories = category_stats(samples, records)
    confidence = confidence_stats(samples, records)

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        category_figure(categories, accuracy, lang)
        confidence_figure(confidence, lang)
        leaderboard_figure(leaderboard, accuracy, lang)

    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
