"""Rebuild the boston-housing report stats and figures from the datasets and responses."""

import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / 'report' / 'fig'

PROB_BINS = [
    (0.5, 0.7, '0.5–0.7'),
    (0.7, 0.9, '0.7–0.9'),
    (0.9, 0.99, '0.9–0.99'),
    (0.99, 1.001, '≥0.99'),
]

GAP_BUCKETS = [(2, 5), (5, 10), (10, 20), (20, 50)]

LABELS = {
    'en': {
        'variant_bars': ['rounded score\n(numeric)', 'top-probability band\n(numeric)', 'pairwise\ncomparison'],
        'variant_ylabel': 'correct (%)',
        'numeric_random': 'numeric random 10%',
        'pairwise_random': 'pairwise random 50%',
        'conf_xlabel': 'probability assigned to the chosen side',
        'conf_answers': 'answers',
        'conf_accuracy': 'accuracy (%)',
        'conf_random': 'coin flip 50%',
        'gap_xlabel': 'true price gap',
        'gap_ylabel': 'accuracy (%)',
        'gap_random': 'coin flip 50%',
    },
    'zh': {
        'variant_bars': ['评分取整\n（数值任务）', '概率最高档\n（数值任务）', '两两比较'],
        'variant_ylabel': '正确率（%）',
        'numeric_random': '数值随机水平 10%',
        'pairwise_random': '比较随机水平 50%',
        'conf_xlabel': '所选一方的概率',
        'conf_answers': '作答数',
        'conf_accuracy': '准确率（%）',
        'conf_random': '抛硬币 50%',
        'gap_xlabel': '真实价差',
        'gap_ylabel': '准确率（%）',
        'gap_random': '抛硬币 50%',
    },
}

CJK_FONTS = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback']


def load():
    """Return the references, criteria labels, metadata, and successful records of both tasks."""
    numeric_ds = json.loads((ROOT / 'data' / 'dataset.numeric.json').read_text())
    pairwise_ds = json.loads((ROOT / 'data' / 'dataset.pairwise.json').read_text())
    band_labels = numeric_ds['samples'][0]['input']['questions']['price_band']['criteria']
    numeric_ref = {s['id']: s['reference']['price_band']['score'] for s in numeric_ds['samples']}
    pairwise_ref = {s['id']: s['reference']['higher']['choice'] for s in pairwise_ds['samples']}
    pairwise_bucket = {s['id']: tuple(s['metadata']['gap_bucket']) for s in pairwise_ds['samples']}
    medvs = [s['metadata']['medv'] for s in numeric_ds['samples']]
    with (ROOT / 'result' / 'responses.score.numeric.jsonl').open() as file:
        numeric = [json.loads(line) for line in file]
    with (ROOT / 'result' / 'responses.choice.pairwise.jsonl').open() as file:
        pairwise = [json.loads(line) for line in file]
    numeric = [r for r in numeric if r['error'] is None]
    pairwise = [r for r in pairwise if r['error'] is None]
    return band_labels, numeric_ref, pairwise_ref, pairwise_bucket, medvs, numeric, pairwise


def numeric_stats(numeric_ref, records):
    """Return per-record numeric readings and the aggregate hit rates and errors."""
    rows = []
    for record in records:
        answer = record['response']['answers']['price_band']
        probs = {int(k): v for k, v in answer['probabilities'].items()}
        rows.append({
            'true': numeric_ref[record['id']],
            'score': answer['score'],
            'rounded': round(answer['score']),
            'top_band': max(probs, key=probs.get),
            'max_prob': max(probs.values()),
            'weighted': sum(k * v for k, v in probs.items()),
            'confidence': answer['confidence'],
        })
    return rows


def pairwise_stats(pairwise_ref, pairwise_bucket, records):
    """Return (selected probability, correct, gap bucket) per pairwise record."""
    rows = []
    for record in records:
        answer = record['response']['answers']['higher']
        prob = answer['probabilities'][answer['choice']]
        rows.append({
            'prob': prob,
            'correct': answer['choice'] == pairwise_ref[record['id']],
            'bucket': pairwise_bucket[record['id']],
        })
    return rows


def ci95(correct, total):
    """Return the 95% normal-approximation confidence interval of a proportion."""
    p = correct / total
    half = 1.96 * (p * (1 - p) / total) ** 0.5
    return 100 * (p - half), 100 * (p + half)


def variant_figure(round_rate, argmax_rate, pairwise_rate, lang):
    """Plot the three correctness readings with the two random levels."""
    text = LABELS[lang]
    values = [round_rate, argmax_rate, pairwise_rate]
    colors = ['#4b74a6', '#4b74a6', '#b34700']

    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(text['variant_bars'], values, color=colors, width=0.55)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 2, f'{value:.1f}',
                ha='center', fontsize=10)
    ax.axhline(10, ls='--', lw=1, color='#888888')
    ax.axhline(50, ls='--', lw=1, color='#888888')
    ax.set_xlim(-0.47, 3.6)
    ax.text(3.45, 12, text['numeric_random'], ha='right', fontsize=8, color='#888888')
    ax.text(3.45, 52, text['pairwise_random'], ha='right', fontsize=8, color='#888888')
    ax.set_ylabel(text['variant_ylabel'])
    ax.set_ylim(0, 100)
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'numeric-vs-pairwise.png', dpi=150)
    plt.close(fig)


def confidence_figure(bin_rows, lang):
    """Plot the answer distribution and accuracy per selected-probability bin."""
    text = LABELS[lang]
    labels = [label for _, _, label in PROB_BINS]
    counts = [row[0] for row in bin_rows]
    accuracies = [row[1] for row in bin_rows]
    x = list(range(len(PROB_BINS)))

    fig, ax1 = plt.subplots(figsize=(7, 4.2))
    ax1.bar(x, counts, color='#c9d7e8')
    for i, count in zip(x, counts):
        ax1.text(i, count / 2, str(count), ha='center', va='center', fontsize=9)
    ax1.set_xticks(x, labels)
    ax1.set_xlabel(text['conf_xlabel'])
    ax1.set_ylabel(text['conf_answers'])
    ax1.set_ylim(0, max(counts) * 1.18)

    ax2 = ax1.twinx()
    ax2.plot(x, accuracies, marker='o', color='#b34700')
    for i, accuracy in zip(x, accuracies):
        ax2.annotate(f'{accuracy:.1f}', (i, accuracy), textcoords='offset points',
                     xytext=(0, 9), ha='center', fontsize=9, color='#b34700')
    ax2.axhline(50, ls='--', lw=1, color='#888888')
    ax2.text(len(PROB_BINS) - 0.65, 51.5, text['conf_random'], ha='right', fontsize=8, color='#888888')
    ax2.set_ylabel(text['conf_accuracy'])
    ax2.set_ylim(0, 115)

    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'pairwise-confidence-accuracy.png', dpi=150)
    plt.close(fig)


def gap_figure(bucket_rows, lang):
    """Plot pairwise accuracy per true-price-gap bucket."""
    text = LABELS[lang]
    labels = [rf'${lo}k–${hi}k'.replace('$', r'\$') for lo, hi in GAP_BUCKETS]
    accuracies = [row[1] for row in bucket_rows]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(labels, accuracies, color='#4b74a6', width=0.55)
    for bar, accuracy in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width() / 2, accuracy + 2, f'{accuracy:.1f}',
                ha='center', fontsize=10)
    ax.axhline(50, ls='--', lw=1, color='#888888')
    ax.set_xlim(-0.6, 4.6)
    ax.text(4.45, 52, text['gap_random'], ha='right', fontsize=8, color='#888888')
    ax.set_xlabel(text['gap_xlabel'])
    ax.set_ylabel(text['gap_ylabel'])
    ax.set_ylim(0, 100)
    fig.tight_layout()
    fig.savefig(FIG_DIR / lang / 'pairwise-gap-accuracy.png', dpi=150)
    plt.close(fig)


def main():
    band_labels, numeric_ref, pairwise_ref, pairwise_bucket, medvs, numeric, pairwise = load()
    num = numeric_stats(numeric_ref, numeric)
    pair = pairwise_stats(pairwise_ref, pairwise_bucket, pairwise)

    n = len(num)
    round_hits = sum(r['rounded'] == r['true'] for r in num)
    argmax_hits = sum(r['top_band'] == r['true'] for r in num)
    mae_round = sum(abs(r['rounded'] - r['true']) for r in num) / n
    mae_argmax = sum(abs(r['top_band'] - r['true']) for r in num) / n
    round_rate = 100 * round_hits / n
    argmax_rate = 100 * argmax_hits / n
    print(f'numeric: n={n}, rounded-score hit {round_hits} ({round_rate:.2f}%, '
          f'95% CI {ci95(round_hits, n)[0]:.2f}–{ci95(round_hits, n)[1]:.2f}%)')
    print(f'numeric: top-probability band hit {argmax_hits} ({argmax_rate:.2f}%, '
          f'95% CI {ci95(argmax_hits, n)[0]:.2f}–{ci95(argmax_hits, n)[1]:.2f}%)')
    print(f'numeric: MAE rounded {mae_round:.2f} bands, top-band {mae_argmax:.2f} bands')
    print('numeric: per true band (label, n, rounded hit %, top-band hit %, top-band MAE)')
    for band, label in enumerate(band_labels):
        sub = [r for r in num if r['true'] == band]
        rh = sum(r['rounded'] == band for r in sub)
        ah = sum(r['top_band'] == band for r in sub)
        mae = sum(abs(r['top_band'] - band) for r in sub) / len(sub)
        print(f'  band {band} {label}: n={len(sub)}, rounded {100 * rh / len(sub):.1f}%, '
              f'top-band {100 * ah / len(sub):.1f}%, MAE {mae:.2f}')

    scores = [r['score'] for r in num]
    trues = [float(r['true']) for r in num]
    mean_s, mean_t = statistics.mean(scores), statistics.mean(trues)
    cov = sum((s - mean_s) * (t - mean_t) for s, t in zip(scores, trues))
    pearson = cov / (sum((s - mean_s) ** 2 for s in scores)
                     * sum((t - mean_t) ** 2 for t in trues)) ** 0.5
    print(f'numeric: score range {min(scores):.2f}–{max(scores):.2f}, '
          f'Pearson r(score, true band) {pearson:.3f}')
    print(f'numeric: max |score - weighted mean of probabilities| '
          f'{max(abs(r["score"] - r["weighted"]) for r in num):.2f}')
    confs = sorted(r['confidence'] for r in num)
    hit_conf = [r['confidence'] for r in num if r['rounded'] == r['true']]
    miss_conf = [r['confidence'] for r in num if r['rounded'] != r['true']]
    print(f'numeric confidence: <0.5 in {sum(c < 0.5 for c in confs)}/{n}, ==0 in '
          f'{sum(c == 0 for c in confs)}, median {confs[n // 2]:.2f}, max {confs[-1]:.2f}, '
          f'mean on hits {statistics.mean(hit_conf):.3f} vs misses {statistics.mean(miss_conf):.3f}')

    p = len(pair)
    correct = sum(r['correct'] for r in pair)
    pair_rate = 100 * correct / p
    print(f'pairwise: n={p}, correct {correct} ({pair_rate:.2f}%, '
          f'95% CI {ci95(correct, p)[0]:.2f}–{ci95(correct, p)[1]:.2f}%)')
    bucket_rows = []
    for bucket in GAP_BUCKETS:
        sub = [r['correct'] for r in pair if r['bucket'] == bucket]
        bucket_rows.append((len(sub), 100 * sum(sub) / len(sub)))
        print(f'pairwise bucket {bucket}: n={len(sub)}, accuracy {bucket_rows[-1][1]:.2f}%')
    bin_rows = []
    for lo, hi, label in PROB_BINS:
        sub = [r['correct'] for r in pair if lo <= r['prob'] < hi]
        bin_rows.append((len(sub), 100 * sum(sub) / len(sub)))
        print(f'pairwise prob bin {label}: n={len(sub)} ({100 * len(sub) / p:.1f}%), '
              f'accuracy {bin_rows[-1][1]:.2f}%')
    high = [r['correct'] for r in pair if r['prob'] >= 0.9]
    print(f'pairwise prob >=0.9: n={len(high)} ({100 * len(high) / p:.1f}%), '
          f'accuracy {100 * sum(high) / len(high):.2f}%')
    err_probs = sorted(r['prob'] for r in pair if not r['correct'])
    print(f'pairwise errors: n={len(err_probs)}, median selected prob '
          f'{err_probs[len(err_probs) // 2]:.2f}, at >=0.9: {sum(p_ >= 0.9 for p_ in err_probs)}')

    for name, records in (('numeric', numeric), ('pairwise', pairwise)):
        tin = sum(r['response']['usage']['input_tokens'] for r in records)
        tout = sum(r['response']['usage']['output_tokens'] for r in records)
        cost = sum(r['response']['usage']['cost'] for r in records)
        print(f'{name} usage: in {tin:,}, out {tout:,}, cost ${cost:.4f}')

    for lang in LABELS:
        if lang == 'zh':
            plt.rcParams['font.sans-serif'] = CJK_FONTS + plt.rcParams['font.sans-serif']
        (FIG_DIR / lang).mkdir(parents=True, exist_ok=True)
        variant_figure(round_rate, argmax_rate, pair_rate, lang)
        confidence_figure(bin_rows, lang)
        gap_figure(bucket_rows, lang)

    print(f'figures written to {FIG_DIR}')


if __name__ == '__main__':
    main()
