"""Rebuild the report figures and stats from the dataset, responses, and leaderboard snapshot."""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

BINS = [
    (0.0, 0.6, '<0.6'),
    (0.6, 0.85, '0.6–0.85'),
    (0.85, 1.01, '≥0.85'),
]

LABELS = {
    'en': {
        'xlabel': 'confidence',
        'answers': 'answers',
        'accuracy': 'accuracy (%)',
        'random': 'random guess 25%',
        'jev': 'JEV-1.13 (four-choice, single pass) 75.76',
        'lb_xlabel': 'model parameters (log scale)',
        'lb_ylabel': 'GPQA Diamond score (%)',
        'lb_title': 'HF GPQA leaderboard (Diamond, no tools) vs JEV',
    },
    'zh': {
        'xlabel': 'confidence',
        'answers': '题数',
        'accuracy': '准确率（%）',
        'random': '随机猜测 25%',
        'jev': 'JEV-1.13（四选一，单次作答）75.76',
        'lb_xlabel': '模型参数量（对数刻度）',
        'lb_ylabel': 'GPQA Diamond 成绩（%）',
        'lb_title': 'HF GPQA 榜单（Diamond 子集、无工具）与 JEV 对比',
    },
}

# A few recognizable entries are labeled in the scatter to orient the reader.
# pick selects which of a model's points carries the label, offset is in points.
ANNOTATE = {
    'FINAL-Bench/Darwin-180B-RSI': ('Darwin-180B-RSI', (5, 4), 'max'),
    'moonshotai/Kimi-K2.6': ('Kimi-K2.6', (5, 4), 'max'),
    'deepseek-ai/DeepSeek-R1-0528': ('DeepSeek-R1-0528', (5, 4), 'max'),
    'openai/gpt-oss-120b': ('gpt-oss-120b', (6, -9), 'min'),
    'meta-llama/Llama-3.2-1B-Instruct': ('Llama-3.2-1B', (5, 4), 'max'),
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the reference answers, successful records, and leaderboard entries."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    reference = {s['id']: s['reference']['choice']['choice'] for s in dataset['samples']}
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    ok = [r for r in records if r['error'] is None]
    leaderboard = json.loads((ROOT / 'preparation' / 'raw' / 'leaderboard-latest.json').read_text())
    return dataset['samples'], reference, records, ok, leaderboard


def answers(reference, records):
    """Return (confidence, correct, probabilities, choice) per record."""
    rows = []
    for record in records:
        answer = record['response']['answers']['choice']
        rows.append((answer['confidence'], answer['choice'] == reference[record['id']],
                     answer['probabilities'], answer['choice']))
    return rows


def bin_stats(rows):
    """Return (count, accuracy) per confidence bin."""
    stats = []
    for lo, hi, _ in BINS:
        sub = [correct for confidence, correct, _, _ in rows if lo <= confidence < hi]
        stats.append((len(sub), 100 * sum(sub) / len(sub)))
    return stats


def blemishes(rows):
    """Count probability sums below 1 and top-two ties."""
    bad_sum = 0
    tie = 0
    tie_bins = []
    for confidence, _, probabilities, choice in rows:
        if round(sum(probabilities.values()), 6) != 1.0:
            bad_sum += 1
        top = sorted(probabilities.values(), reverse=True)[:2]
        if abs(top[0] - top[1]) < 1e-9:
            assert choice in probabilities  # choice takes one of the tied options
            tie += 1
            tie_bins.append(confidence)
    return bad_sum, tie, tie_bins


def usage(records):
    """Sum token usage and cost over all records."""
    input_tokens = sum(r['response']['usage']['input_tokens'] for r in records)
    output_tokens = sum(r['response']['usage']['output_tokens'] for r in records)
    cost = sum(r['response']['usage']['cost'] for r in records)
    return input_tokens, output_tokens, cost


def wilson(correct, total):
    """Return the 95% Wilson interval for a proportion, in percent."""
    p = correct / total
    z = 1.959963985
    den = 1 + z * z / total
    center = p + z * z / (2 * total)
    spread = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total))
    return 100 * (center - spread) / den, 100 * (center + spread) / den


def diamond_entries(leaderboard):
    """Keep Diamond-subset results without tool use."""
    return [r for r in leaderboard
            if 'diamond' in r['filename'] and 'tools' not in r['filename']]


def confidence_figure(stats, lang):
    """Plot the answer distribution and accuracy per confidence bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in BINS]
    counts = [count for count, _ in stats]
    accuracies = [accuracy for _, accuracy in stats]
    x = list(range(len(BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        ax1.text(i, count + 3, str(count), ha='center', fontsize=9)
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


def leaderboard_figure(entries, jev_accuracy, lang):
    """Scatter leaderboard scores against model size with JEV's position marked."""
    text = LABELS[lang]
    points = [(r['num_parameters'], r['value'], r['modelId'])
              for r in entries if r.get('num_parameters')]

    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.scatter([p for p, _, _ in points], [v for _, v, _ in points],
               s=22, color='#4b74a6', alpha=0.75)
    labeled = {}
    for params, value, model_id in points:
        if model_id not in ANNOTATE:
            continue
        pick = ANNOTATE[model_id][2]
        current = labeled.get(model_id)
        if current is None or (pick == 'min') == (value < current[1]):
            labeled[model_id] = (params, value)
    for model_id, (params, value) in labeled.items():
        label, offset, _ = ANNOTATE[model_id]
        ax.annotate(label, (params, value), textcoords='offset points',
                    xytext=offset, fontsize=7, color='#333333')
    ax.axhline(jev_accuracy, ls='--', lw=1.2, color='#b34700')
    ax.text(1.1e9, jev_accuracy - 3.2, text['jev'], fontsize=8, color='#b34700')
    ax.set_xscale('log')
    ax.set_xlim(8e8, 5e12)
    ax.set_ylim(10, 100)
    ax.set_xlabel(text['lb_xlabel'])
    ax.set_ylabel(text['lb_ylabel'])
    ax.set_title(text['lb_title'], fontsize=10)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'leaderboard-position.png', dpi=150)
    plt.close(fig)


def main():
    samples, reference, records, ok, leaderboard = load()
    assert len(ok) == len(samples) == len(records)
    rows = answers(reference, records)
    total = len(rows)
    correct = sum(c for _, c, _, _ in rows)
    accuracy = 100 * correct / total
    lo, hi = wilson(correct, total)
    stats = bin_stats(rows)
    bad_sum, tie, tie_bins = blemishes(rows)
    input_tokens, output_tokens, cost = usage(records)
    entries = diamond_entries(leaderboard)
    better = sum(r['value'] > accuracy for r in entries)
    values = sorted(r['value'] for r in entries)
    median = (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2 \
        if len(values) % 2 == 0 else values[len(values) // 2]

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        confidence_figure(stats, lang)
        leaderboard_figure(entries, accuracy, lang)

    print(f'samples {len(samples)}, records {len(records)}, errors {len(records) - len(ok)}')
    print(f'accuracy {accuracy:.2f}% ({correct}/{total}), Wilson 95% CI {lo:.2f}–{hi:.2f}')
    for (bin_lo, bin_hi, label), (count, bin_accuracy) in zip(BINS, stats):
        print(f'  {label:8s} n={count:3d} share={100 * count / total:5.1f}% '
              f'accuracy {bin_accuracy:.2f}%')
    print(f'blemishes: prob sum != 1 -> {bad_sum} ({100 * bad_sum / total:.1f}%), '
          f'top-two tie -> {tie} ({100 * tie / total:.1f}%), tie confidences {tie_bins}')
    print(f'usage: input {input_tokens:,}, output {output_tokens:,}, cost ${cost:.6f}')
    print(f'leaderboard: {len(leaderboard)} entries, diamond no-tools {len(entries)} '
          f'from {len({r["modelId"] for r in entries})} models, '
          f'range {values[0]:.2f}–{values[-1]:.2f}, median {median:.2f}')
    print(f'JEV rank among diamond entries: {better + 1} of {len(entries)}')
    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
