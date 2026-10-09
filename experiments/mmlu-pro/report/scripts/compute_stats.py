"""Recompute every number cited in the report from the dataset, responses, and leaderboard snapshot."""

import json
import math
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIDENCE_BINS = [(0.0, 0.6, '<0.6'), (0.6, 0.85, '0.6–0.85'), (0.85, 1.01, '≥0.85')]
SUM_TOLERANCE = 1e-6


def load():
    """Return the samples and the successful response records."""
    dataset = json.loads((ROOT / 'data' / 'dataset.json').read_text())
    with (ROOT / 'result' / 'responses.jsonl').open() as file:
        records = [json.loads(line) for line in file]
    return dataset['samples'], [r for r in records if r['error'] is None]


def main():
    samples, records = load()
    reference = {s['id']: s['reference']['answer']['choice'] for s in samples}
    option_counts = Counter(len(s['input']['questions']['answer']['criteria']) for s in samples)

    total = len(records)
    correct = sum(r['response']['answers']['answer']['choice'] == reference[r['id']] for r in records)
    accuracy = correct / total
    half_width = 1.96 * math.sqrt(accuracy * (1 - accuracy) / total)

    print(f'answers {total}, correct {correct}, accuracy {100 * accuracy:.2f}%')
    print(f'95% CI {100 * (accuracy - half_width):.2f}–{100 * (accuracy + half_width):.2f}')
    print('option counts:', ', '.join(f'{k} options: {v} ({100 * v / total:.2f}%)'
                                      for k, v in sorted(option_counts.items())))

    print('per-category:')
    categories = sorted({s['metadata']['category'] for s in samples})
    records_by_id = {r['id']: r for r in records}
    rows = []
    for name in categories:
        ids = [s['id'] for s in samples if s['metadata']['category'] == name]
        hits = sum(records_by_id[i]['response']['answers']['answer']['choice'] == reference[i]
                   for i in ids)
        rows.append((name, len(ids), hits, 100 * hits / len(ids)))
    for name, n, hits, acc in sorted(rows, key=lambda row: -row[3]):
        print(f'  {name:16s} n={n:5d} correct={hits:5d} accuracy {acc:.2f}%')

    print('confidence bins:')
    conf_rows = []
    for lo, hi, label in CONFIDENCE_BINS:
        sub = [r for r in records
               if lo <= r['response']['answers']['answer']['confidence'] < hi]
        hits = sum(r['response']['answers']['answer']['choice'] == reference[r['id']] for r in sub)
        conf_rows.append((label, len(sub), hits))
        print(f'  {label:10s} n={len(sub):5d} ({100 * len(sub) / total:.2f}%) '
              f'correct={hits:5d} accuracy {100 * hits / len(sub):.2f}%')
    errors_low = conf_rows[0][1] - conf_rows[0][2]
    print(f'  errors in <0.6 bin: {errors_low} of {total - correct} '
          f'({100 * errors_low / (total - correct):.2f}%)')

    bad_sum = 0
    bad_argmax = 0
    input_tokens = output_tokens = 0
    cost = 0.0
    for r in records:
        answer = r['response']['answers']['answer']
        if abs(sum(answer['probabilities'].values()) - 1) > SUM_TOLERANCE:
            bad_sum += 1
        top = max(answer['probabilities'].items(), key=lambda item: item[1])
        if top[0] != answer['choice']:
            bad_argmax += 1
        usage = r['response']['usage']
        input_tokens += usage['input_tokens']
        output_tokens += usage['output_tokens']
        cost += usage['cost']
    print(f'probabilities sum != 1: {bad_sum} ({100 * bad_sum / total:.2f}%)')
    print(f'choice != argmax: {bad_argmax} ({100 * bad_argmax / total:.2f}%)')
    print(f'usage: input {input_tokens:,}, output {output_tokens:,}, cost ${cost:.4f}')

    leaderboard = json.loads((ROOT / 'preparation' / 'raw' / 'leaderboard-latest.json').read_text())
    values = [row['value'] for row in leaderboard]
    above = sum(value > 100 * accuracy for value in values)
    print(f'leaderboard entries {len(values)}, range {min(values):.2f}–{max(values):.2f}, '
          f'median {statistics.median(values):.2f}')
    print(f'JEV {100 * accuracy:.2f}: {above} entries higher, rank {above + 1} of {len(values) + 1}')


if __name__ == '__main__':
    main()
