"""Rebuild the report stats and figures from the datasets, responses, and raw Titanic CSV."""

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

VARIANTS = ['fields', 'text']
SEL_BINS = [
    (0.5, 0.6, '0.5–0.6'),
    (0.6, 0.7, '0.6–0.7'),
    (0.7, 0.8, '0.7–0.8'),
    (0.8, 1.01, '≥0.8'),
]
CONF_BINS = [
    (0.0, 0.3, '<0.3'),
    (0.3, 0.5, '0.3–0.5'),
    (0.5, 0.7, '0.5–0.7'),
    (0.7, 0.9, '0.7–0.9'),
    (0.9, 1.01, '≥0.9'),
]
DIMENSIONS = [('Sex', ['female', 'male']), ('Pclass', ['1', '2', '3'])]

COLORS = {'fields': '#4b74a6', 'text': '#b34700', 'bar': '#c9d7e8', 'marker': '#666666'}

LABELS = {
    'en': {
        'fields': 'fields', 'text': 'text',
        'fields_title': 'structured fields', 'text_title': 'natural-language text',
        'answers': 'answers', 'accuracy': 'accuracy (%)',
        'sel_x': 'selected probability', 'conf_x': 'confidence',
        'random': 'random 50%', 'majority': 'always-died baseline 61.6%',
        'tokens': 'input tokens', 'variant_accuracy': 'accuracy by variant',
        'groups': ['female', 'male', '1st class', '2nd class', '3rd class'],
        'survived_share': 'share of survivors',
        'sex_dim': 'sex', 'class_dim': 'ticket class',
    },
    'zh': {
        'fields': '字段版', 'text': '文本版',
        'fields_title': '结构化字段', 'text_title': '自然语言文本',
        'answers': '作答数', 'accuracy': '准确率（%）',
        'sel_x': '所选概率', 'conf_x': 'confidence',
        'random': '随机 50%', 'majority': '全猜死亡 61.6%',
        'tokens': '输入 token', 'variant_accuracy': '两版准确率',
        'groups': ['女性', '男性', '一等舱', '二等舱', '三等舱'],
        'survived_share': '生还者占比',
        'sex_dim': '性别', 'class_dim': '舱位',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback', 'Droid Sans Fallback Full']


def register_cjk_fonts():
    """Register the system CJK font files so the zh figures render Chinese."""
    for path in (
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
    ):
        try:
            fm.fontManager.addfont(path)
        except Exception:
            pass


def load():
    """Return the references, per-variant answer rows, and raw CSV attributes."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    reference = {s['id']: s['reference']['survived']['choice'] for s in dataset['samples']}
    passenger_id = {s['id']: s['metadata']['passenger_id'] for s in dataset['samples']}
    rows = {}
    for name in VARIANTS:
        path = ROOT / 'result' / f'responses.choice.{name}.jsonl'
        records = [json.loads(line) for line in path.open()]
        ok = [r for r in records if r['error'] is None]
        variant_rows = []
        for record in ok:
            answer = record['response']['answers']['survived']
            usage = record['response']['usage']
            variant_rows.append({
                'id': record['id'],
                'choice': answer['choice'],
                'probs': answer['probabilities'],
                'sel': answer['probabilities'][answer['choice']],
                'conf': answer['confidence'],
                'correct': answer['choice'] == reference[record['id']],
                'in_tok': usage['input_tokens'],
                'out_tok': usage['output_tokens'],
                'cost': usage['cost'],
            })
        rows[name] = variant_rows
    with (ROOT / 'preparation' / 'raw' / 'titanic.csv').open(newline='') as file:
        raw = {int(r['PassengerId']): r for r in csv.DictReader(file)}
    groups = {s['id']: {dim: raw[pid][dim] for dim, _ in DIMENSIONS}
              for s in dataset['samples'] for pid in [passenger_id[s['id']]]}
    return reference, rows, groups


def confidence_interval(correct, total):
    """Return the 95% normal-approximation interval of an accuracy in percent."""
    p = correct / total
    half = 1.96 * (p * (1 - p) / total) ** 0.5
    return 100 * (p - half), 100 * (p + half)


def bin_stats(rows, bins, key):
    """Return (count, accuracy in percent) per bin of the given measurement."""
    stats = []
    for lo, hi, _ in bins:
        sub = [r['correct'] for r in rows if lo <= r[key] < hi]
        stats.append((len(sub), 100 * sum(sub) / len(sub) if sub else None))
    return stats


def measurement_figure(rows_by_variant, bins, key, filename, lang):
    """Plot the answer distribution and accuracy per bin for both variants side by side."""
    text = LABELS[lang]
    labels = [label for _, _, label in bins]
    x = list(range(len(bins)))
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2))
    twins = []
    for axis, name in zip(axes, VARIANTS):
        stats = bin_stats(rows_by_variant[name], bins, key)
        counts = [count for count, _ in stats]
        accuracies = [accuracy for _, accuracy in stats]
        axis.bar(x, counts, color=COLORS['bar'])
        for i, count in zip(x, counts):
            if count >= 40:
                axis.text(i, max(counts) * 0.04, str(count), ha='center', va='bottom', fontsize=9)
            else:
                axis.text(i, count + max(counts) * 0.02, str(count), ha='center', fontsize=9)
        axis.set_xticks(x, labels)
        axis.set_xlabel(text[f'{key}_x'])
        axis.set_ylim(0, max(counts) * 1.18)
        axis.set_title(text[f'{name}_title'], fontsize=10)
        twin = axis.twinx()
        twin.plot(x, accuracies, marker='o', color=COLORS['text'])
        for i, accuracy in enumerate(accuracies):
            twin.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                          xytext=(0, 9), ha='center', fontsize=8, color=COLORS['text'])
        twin.axhline(50, ls='--', lw=1, color='#888888')
        twin.set_ylim(0, 112)
        twins.append(twin)
    axes[0].set_ylabel(text['answers'])
    axes[1].axes.yaxis.set_visible(False)
    twins[0].axes.yaxis.set_visible(False)
    twins[1].set_ylabel(text['accuracy'])
    twins[1].text(len(bins) - 1, 51.5, text['random'], ha='right', fontsize=8, color='#888888')
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / filename, dpi=150)
    plt.close(fig)


def variant_figure(rows_by_variant, majority, lang):
    """Plot accuracy and input tokens per variant."""
    text = LABELS[lang]
    names = [text[name] for name in VARIANTS]
    accuracies = [100 * sum(r['correct'] for r in rows_by_variant[name]) / len(rows_by_variant[name])
                  for name in VARIANTS]
    tokens = [sum(r['in_tok'] for r in rows_by_variant[name]) for name in VARIANTS]
    colors = [COLORS[name] for name in VARIANTS]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.0))
    bars = ax1.bar(names, accuracies, color=colors, width=0.5)
    for bar, accuracy in zip(bars, accuracies):
        ax1.text(bar.get_x() + bar.get_width() / 2, accuracy + 1.5, f'{accuracy:.2f}',
                 ha='center', fontsize=9)
    random_line = ax1.axhline(50, ls='--', lw=1, color='#888888')
    majority_line = ax1.axhline(majority, ls=':', lw=1, color='#888888')
    ax1.legend([random_line, majority_line], [text['random'], text['majority']],
               loc='upper right', fontsize=8)
    ax1.set_ylim(0, 100)
    ax1.set_ylabel(text['accuracy'])
    ax1.set_title(text['variant_accuracy'], fontsize=10)

    bars = ax2.bar(names, tokens, color=colors, width=0.5)
    for bar, value in zip(bars, tokens):
        ax2.text(bar.get_x() + bar.get_width() / 2, value + max(tokens) * 0.02,
                 f'{value:,}', ha='center', fontsize=9)
    ax2.set_ylim(0, max(tokens) * 1.15)
    ax2.set_ylabel(text['tokens'])
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'variant-comparison.png', dpi=150)
    plt.close(fig)


def group_figure(rows_by_variant, reference, groups, lang):
    """Plot accuracy per group for both variants with the group survivor share."""
    text = LABELS[lang]
    group_keys = [value for _, values in DIMENSIONS for value in values]
    dim_of = {value: dim for dim, values in DIMENSIONS for value in values}
    names = text['groups']
    x = list(range(len(group_keys)))
    width = 0.36

    fig, axis = plt.subplots(figsize=(8.6, 4.2))
    for offset, name in [(-width / 2, 'fields'), (width / 2, 'text')]:
        accuracies = []
        for key in group_keys:
            ids = [i for i, g in groups.items() if g[dim_of[key]] == key]
            by_id = {r['id']: r for r in rows_by_variant[name]}
            accuracies.append(100 * sum(by_id[i]['correct'] for i in ids) / len(ids))
        bars = axis.bar([i + offset for i in x], accuracies, width,
                        color=COLORS[name], label=text[name])
        for bar, accuracy in zip(bars, accuracies):
            axis.text(bar.get_x() + bar.get_width() / 2, accuracy + 1.5, f'{accuracy:.1f}',
                      ha='center', fontsize=8)
    shares = []
    for key in group_keys:
        ids = [i for i, g in groups.items() if g[dim_of[key]] == key]
        shares.append(100 * sum(1 for i in ids if reference[i] == 'A') / len(ids))
    axis.plot(x, shares, marker='D', ls='', color=COLORS['marker'], label=text['survived_share'])
    axis.set_xticks(x, names)
    axis.set_ylim(0, 100)
    axis.set_ylabel(text['accuracy'])
    axis.axvline(1.5, ls=':', lw=1, color='#bbbbbb')
    axis.text(0.5, 96, text['sex_dim'], ha='center', fontsize=9, color='#666666')
    axis.text(2.65, 96, text['class_dim'], ha='center', fontsize=9, color='#666666')
    axis.legend(loc='upper right', fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'group-accuracy.png', dpi=150)
    plt.close(fig)


def print_stats(reference, rows_by_variant, groups):
    """Print every number quoted in the report."""
    total = len(reference)
    survived = sum(1 for choice in reference.values() if choice == 'A')
    majority = 100 * (total - survived) / total
    print(f'passengers {total}, reference survived {survived} / died {total - survived}')
    print(f'baselines: random 50%, always-died {majority:.2f}%')
    for name in VARIANTS:
        rows = rows_by_variant[name]
        correct = sum(r['correct'] for r in rows)
        lo, hi = confidence_interval(correct, len(rows))
        accuracy = 100 * correct / len(rows)
        in_tok = sum(r['in_tok'] for r in rows)
        out_tok = sum(r['out_tok'] for r in rows)
        cost = sum(r['cost'] for r in rows)
        ties = sum(1 for r in rows if len(set(r['probs'].values())) == 1)
        bad_sum = sum(1 for r in rows if abs(sum(r['probs'].values()) - 1) > 1e-6)
        chose_b = sum(1 for r in rows if r['choice'] == 'B')
        low_conf = sum(1 for r in rows if r['conf'] < 0.5)
        high_conf = sum(1 for r in rows if r['conf'] >= 0.7)
        high_sel = [r for r in rows if r['sel'] >= 0.9]
        print(f'\n[{name}] valid {len(rows)}/{total}, correct {correct}, '
              f'accuracy {accuracy:.2f}% (95% CI {lo:.2f}–{hi:.2f})')
        print(f'  tokens in {in_tok:,} / out {out_tok:,}, cost ${cost:.4f}')
        print(f'  chose died {chose_b} ({100 * chose_b / len(rows):.1f}%), '
              f'prob sums != 1: {bad_sum}, 0.5/0.5 ties: {ties}')
        print(f'  confidence <0.5: {low_conf} ({100 * low_conf / len(rows):.1f}%), >=0.7: {high_conf}')
        print(f'  selected prob >=0.9: {len(high_sel)} answers, '
              f'accuracy {100 * sum(r["correct"] for r in high_sel) / len(high_sel):.1f}%')
        for key, bins, title in [('sel', SEL_BINS, 'selected probability'),
                                 ('conf', CONF_BINS, 'confidence')]:
            print(f'  {title} bins:')
            for (lo_, hi_, label), (count, acc) in zip(bins, bin_stats(rows, bins, key)):
                acc_text = f'{acc:.2f}%' if acc is not None else 'n/a'
                print(f'    {label:8s} n={count:4d} ({100 * count / len(rows):5.1f}%) accuracy {acc_text}')
    saving = 1 - sum(r['in_tok'] for r in rows_by_variant['text']) / \
        sum(r['in_tok'] for r in rows_by_variant['fields'])
    total_cost = sum(r['cost'] for name in VARIANTS for r in rows_by_variant[name])
    print(f'\ninput-token saving of text vs fields {100 * saving:.1f}%, total cost ${total_cost:.4f}')
    f_by_id = {r['id']: r for r in rows_by_variant['fields']}
    t_by_id = {r['id']: r for r in rows_by_variant['text']}
    ids = sorted(f_by_id)
    agree = sum(1 for i in ids if f_by_id[i]['choice'] == t_by_id[i]['choice'])
    both_wrong = sum(1 for i in ids if not f_by_id[i]['correct'] and not t_by_id[i]['correct'])
    print(f'variant agreement {agree}/{total} ({100 * agree / total:.1f}%), both wrong {both_wrong}')
    print('\ngroups:')
    for dim, values in DIMENSIONS:
        for value in values:
            ids_g = [i for i, g in groups.items() if g[dim] == value]
            share = 100 * sum(1 for i in ids_g if reference[i] == 'A') / len(ids_g)
            parts = []
            for name in VARIANTS:
                by_id = {r['id']: r for r in rows_by_variant[name]}
                acc = 100 * sum(by_id[i]['correct'] for i in ids_g) / len(ids_g)
                parts.append(f'{name} {acc:.2f}%')
            print(f'  {dim}={value}: n={len(ids_g)}, survivor share {share:.1f}%, ' + ', '.join(parts))


def main():
    register_cjk_fonts()
    reference, rows_by_variant, groups = load()
    majority = 100 * sum(1 for c in reference.values() if c == 'B') / len(reference)
    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        measurement_figure(rows_by_variant, SEL_BINS, 'sel', 'selected-probability.png', lang)
        measurement_figure(rows_by_variant, CONF_BINS, 'conf', 'confidence.png', lang)
        variant_figure(rows_by_variant, majority, lang)
        group_figure(rows_by_variant, reference, groups, lang)
    print_stats(reference, rows_by_variant, groups)
    print(f'\nfigures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
