"""Rebuild the report figures and stats from the dataset and responses."""

import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

CONF_BINS = [
    (0.0, 0.7, '<0.7'),
    (0.7, 0.9, '0.7–0.9'),
    (0.9, 0.99, '0.9–0.99'),
    (0.99, 1.01, '≥0.99'),
]

LABELS = {
    'en': {
        'xlabel': 'confidence',
        'tasks': 'tasks',
        'accuracy': 'strict accuracy (%)',
        'group_overall': 'overall 97.6%',
        'panel_ngold': 'by gold skills per task',
        'panel_style': 'by style',
        'panel_prefix': 'by task group (id prefix)',
        'formal': 'formal',
        'casual': 'casual',
    },
    'zh': {
        'xlabel': 'confidence',
        'tasks': '题数',
        'accuracy': '严格准确率（%）',
        'group_overall': '整体 97.6%',
        'panel_ngold': '按标准技能数',
        'panel_style': '按语体',
        'panel_prefix': '按题组（id 前缀）',
        'formal': '正式',
        'casual': '口语',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the samples by id and the successful records."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    samples = {s['id']: s for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    return samples, records, ok


def verdicts(samples, records):
    """Return (strict, loose, confidence) per record."""
    rows = []
    for record in records:
        sample = samples[record['id']]
        answer = record['response']['answers']['skill']
        reference = sample['reference']['skill']
        strict = answer['choice'] == reference['choice']
        loose = strict or answer['choice'] in reference.get('acceptable', [])
        rows.append((strict, loose, answer['confidence']))
    return rows


def wilson(correct, total):
    """Return the 95% Wilson interval for a proportion, in percent."""
    p = correct / total
    z = 1.959964
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return 100 * (center - half), 100 * (center + half)


def group_stats(samples, records, key):
    """Return {group: (strict, loose, total)} for a metadata key or id prefix."""
    stats = defaultdict(lambda: [0, 0, 0])
    for record in records:
        sample = samples[record['id']]
        group = sample['id'][0] if key == 'prefix' else sample['metadata'][key]
        answer = record['response']['answers']['skill']
        reference = sample['reference']['skill']
        strict = answer['choice'] == reference['choice']
        loose = strict or answer['choice'] in reference.get('acceptable', [])
        stats[group][0] += strict
        stats[group][1] += loose
        stats[group][2] += 1
    return stats


def confidence_bins(rows):
    """Return (count, strict accuracy) per confidence bin."""
    stats = []
    for lo, hi, _ in CONF_BINS:
        sub = [(strict, loose) for strict, loose, conf in rows if lo <= conf < hi]
        stats.append((len(sub), 100 * sum(s for s, _ in sub) / len(sub)))
    return stats


def confidence_figure(stats, lang):
    """Plot the answer distribution and strict accuracy per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in CONF_BINS]
    counts = [count for count, _ in stats]
    accuracies = [accuracy for _, accuracy in stats]
    x = list(range(len(CONF_BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['xlabel'])
    ax1.set_ylabel(text['tasks'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    ax2.plot(x, accuracies, marker='o', color='#b34700')
    for i, accuracy in zip(x, accuracies):
        ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.set_ylabel(text['accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'confidence-accuracy.png', dpi=150)
    plt.close(fig)


def group_figure(by_ngold, by_style, by_prefix, overall, lang):
    """Plot strict accuracy per group in three panels."""
    text = LABELS[lang]
    panels = [
        (text['panel_ngold'], [str(k) for k in sorted(by_ngold)],
         [by_ngold[k] for k in sorted(by_ngold)]),
        (text['panel_style'], [text['formal'], text['casual']],
         [by_style['formal'], by_style['casual']]),
        (text['panel_prefix'], list('OMLAN'), [by_prefix[k] for k in 'OMLAN']),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
    for ax, (title, names, groups) in zip(axes, panels):
        values = [100 * strict / total for strict, _, total in groups]
        labels = [f'{name}\n(n={total})' for name, (_, _, total) in zip(names, groups)]
        x = list(range(len(groups)))
        ax.bar(x, values, color='#4b74a6')
        for i, value in zip(x, values):
            ax.text(i, value + 0.4, f'{value:.1f}', ha='center', fontsize=9)
        ax.axhline(overall, ls='--', lw=1, color='#888888')
        ax.set_xticks(x, labels, fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.set_ylim(88, 102)
        ax.set_yticks([90, 95, 100])
    axes[0].set_ylabel(LABELS[lang]['accuracy'])
    axes[-1].text(2, overall + 0.9, text['group_overall'],
                  ha='center', fontsize=8, color='#888888')

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'group-accuracy.png', dpi=150)
    plt.close(fig)


def main():
    samples, records, ok = load()
    rows = verdicts(samples, ok)
    total = len(rows)
    strict = sum(s for s, _, _ in rows)
    loose = sum(l for _, l, _ in rows)
    lo_ci, hi_ci = wilson(strict, total)

    print(f'records {len(records)}, failed {len(records) - len(ok)}')
    print(f'strict {strict}/{total} = {100 * strict / total:.2f}%  (95% CI {lo_ci:.2f}–{hi_ci:.2f}%)')
    print(f'loose  {loose}/{total} = {100 * loose / total:.2f}%')

    by_ngold = group_stats(samples, ok, 'n_gold')
    by_style = group_stats(samples, ok, 'style')
    by_prefix = group_stats(samples, ok, 'prefix')
    for name, stats in [('n_gold', by_ngold), ('style', by_style), ('prefix', by_prefix)]:
        for group in sorted(stats, key=str):
            s, l, n = stats[group]
            print(f'  {name}={group}: strict {s}/{n} = {100 * s / n:.2f}%, loose {l}/{n} = {100 * l / n:.2f}%')

    stats = confidence_bins(rows)
    for (lo, hi, label), (count, accuracy) in zip(CONF_BINS, stats):
        print(f'  conf {label:8s} n={count:4d} ({100 * count / total:.1f}%)  strict accuracy {accuracy:.2f}%')
    hi_conf = [(s, l) for s, l, c in rows if c >= 0.8]
    print(f'  conf>=0.8: n={len(hi_conf)}, strict-correct {sum(s for s, _ in hi_conf)}, '
          f'loose-correct {sum(l for _, l in hi_conf)}')

    # Error patterns, aggregated
    subset = none_to_skill = wrong_single = 0
    for record in ok:
        sample = samples[record['id']]
        answer = record['response']['answers']['skill']
        reference = sample['reference']['skill']
        if answer['choice'] == reference['choice']:
            continue
        gold = sample['metadata']['gold_skills']
        chosen = set(answer['choice'].split(' + ')) if answer['choice'] != 'none' else set()
        if not gold:
            none_to_skill += 1
        elif len(gold) >= 2 and chosen < set(gold):
            subset += 1
        else:
            wrong_single += 1
    print(f'  errors: combo->subset {subset}, none->specific {none_to_skill}, single->wrong {wrong_single}')

    bad_sum = sum(1 for r in ok
                  if abs(sum(r['response']['answers']['skill']['probabilities'].values()) - 1) > 1e-6)
    below_max = tied_max = 0
    for record in ok:
        answer = record['response']['answers']['skill']
        probabilities = answer['probabilities']
        top = max(probabilities.values())
        if probabilities[answer['choice']] < top:
            below_max += 1
        elif list(probabilities.values()).count(top) > 1:
            tied_max += 1
    print(f'  prob sum != 1: {bad_sum}, choice below max: {below_max}, '
          f'choice tied at max: {tied_max}')

    big = [(s, l) for (s, l, _), r in zip(rows, ok) if samples[r['id']]['metadata']['n_options'] == 127]
    small = [(s, l) for (s, l, _), r in zip(rows, ok) if samples[r['id']]['metadata']['n_options'] != 127]
    print(f'  127-option tasks: strict {sum(s for s, _ in big)}/{len(big)} = '
          f'{100 * sum(s for s, _ in big) / len(big):.2f}%')
    print(f'  5–15-option tasks: strict {sum(s for s, _ in small)}/{len(small)} = '
          f'{100 * sum(s for s, _ in small) / len(small):.2f}%')

    input_tokens = sum(r['response']['usage']['input_tokens'] for r in ok)
    output_tokens = sum(r['response']['usage']['output_tokens'] for r in ok)
    cost = sum(r['response']['usage']['cost'] for r in ok)
    print(f'usage: input {input_tokens:,}, output {output_tokens:,}, cost ${cost:.4f}')

    overall = 100 * strict / total
    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(stats, lang)
        group_figure(by_ngold, by_style, by_prefix, overall, lang)
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
