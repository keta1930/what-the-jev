# Recompute cutoff estimates, sensitivity checks, and bilingual figures from the recorded experiment.

import argparse
from collections import Counter, defaultdict
from decimal import Decimal
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
import numpy as np

EXPERIMENT = Path(__file__).resolve().parents[2]
REPORT = EXPERIMENT / 'report'
MONTHS = [f'{2023 + i // 12}-{i % 12 + 1:02d}' for i in range(42)]
MODELS = ('jev', 'llm')
LANGUAGES = ('zh', 'en')
COLORS = {'jev': '#087F82', 'llm': '#7853B3'}
NAMES = {'jev': 'JEV', 'llm': 'GPT-4.1-mini'}


def read_jsonl(path):
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    if not rows or any(not isinstance(row, dict) for row in rows):
        raise ValueError(f'{path}: expected nonempty JSONL objects')
    return rows


def indexed(rows, label):
    result = {row['id']: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f'{label}: duplicate IDs')
    if any(row['error'] is not None for row in rows):
        raise ValueError(f'{label}: failed requests remain')
    return result


def observations():
    llm = indexed(read_jsonl(EXPERIMENT / 'preparation/raw/responses.gpt-4.1-mini.jsonl'), 'LLM')
    prompts = read_jsonl(EXPERIMENT / 'preparation/raw/prompts.gpt-4.1-mini.jsonl')
    prompt_index = {f'{row["language"]}:{row["id"]}': row for row in prompts}
    if set(llm) != set(prompt_index) or len(llm) != 1680:
        raise ValueError('LLM prompt/result IDs do not match the 1680 requests')
    rows, responses = [], {'jev': [], 'llm': []}
    for language in LANGUAGES:
        samples = json.loads((EXPERIMENT / f'data/dataset.{language}.json').read_text())['samples']
        jev = indexed(read_jsonl(EXPERIMENT / f'result/responses.mixed.{language}.jsonl'), language)
        if len(samples) != 840 or len(jev) != 840 or set(jev) != {sample['id'] for sample in samples}:
            raise ValueError(f'{language}: dataset/result IDs do not match 840 samples')
        for sample in samples:
            key = f'{language}:{sample["id"]}'
            prompt_input = json.loads(prompt_index[key]['body']['messages'][1]['content'])
            if prompt_input != sample['input']:
                raise ValueError(f'{key}: LLM and JEV model-facing questions differ')
            question = sample['input']['questions']['answer']
            for model in MODELS:
                response = (jev[sample['id']] if model == 'jev' else llm[key])['response']
                responses[model].append(response)
                if model == 'jev':
                    if response['model'] != 'typesafe/jev-1.13-20260917' or response['provider'] != 'TypeSafe':
                        raise ValueError('unexpected JEV model or provider')
                    answer = response['answers']['answer']
                else:
                    if response['model'] != 'openai/gpt-4.1-mini' or response['provider'] != 'OpenAI':
                        raise ValueError('unexpected LLM model or provider')
                    answer = json.loads(response['choices'][0]['message']['content'])
                row = {'model': model, 'language': language, 'id': sample['id'],
                       'pair_id': sample['metadata']['pair_id'], 'month': sample['metadata']['month'],
                       'kind': question['type'], 'N': sample['metadata']['concrete_option_count']}
                gold = sample['reference']['answer']
                if question['type'] == 'choice':
                    row.update(correct=answer['choice'] == gold['choice'], unknown=answer['choice'] == 'unknown',
                               confidence=answer['confidence'],
                               gold_p=answer['probabilities'][gold['choice']] if model == 'jev' else None)
                else:
                    p = answer['noul'] if model == 'jev' else answer['probability_true']
                    threshold_answer = True if p > 0.5 else False if p < 0.5 else None
                    prediction = threshold_answer if model == 'jev' else answer['answer']
                    row.update(correct=prediction == gold if prediction is not None else False,
                               prediction=prediction, probability_true=p, tie=p == 0.5,
                               probability_correct=threshold_answer == gold if threshold_answer is not None else False,
                               conflict=threshold_answer is not None and prediction != threshold_answer)
                rows.append(row)
    return rows, responses


def average(values):
    return sum(values) / len(values) if values else None


def summarize(rows):
    choice = [row for row in rows if row['kind'] == 'choice']
    noul = [row for row in rows if row['kind'] == 'noul']
    answered = [row for row in choice if not row['unknown']]
    pairs = defaultdict(list)
    for row in rows:
        pairs[(row['language'], row['pair_id'])].append(row)
    return {'choice_n': len(choice), 'choice_correct': sum(row['correct'] for row in choice),
            'choice_accuracy': average([row['correct'] for row in choice]),
            'unknown_n': sum(row['unknown'] for row in choice),
            'unknown_rate': average([row['unknown'] for row in choice]),
            'answered_accuracy': average([row['correct'] for row in answered]),
            'guess_baseline': average([1 / row['N'] for row in choice]),
            'noul_n': len(noul), 'noul_correct': sum(row['correct'] for row in noul),
            'noul_accuracy': average([row['correct'] for row in noul]),
            'noul_false': sum(row['prediction'] is False for row in noul),
            'noul_ties': sum(row['tie'] for row in noul),
            'noul_conflicts': sum(row['conflict'] for row in noul),
            'noul_probability_accuracy': average([row['probability_correct'] for row in noul]),
            'both_correct': sum(len(pair) == 2 and all(row['correct'] for row in pair) for pair in pairs.values()),
            'pair_n': len(pairs)}


def fit_cut(successes, totals):
    successes, totals = np.asarray(successes), np.asarray(totals)
    s, n = np.cumsum(successes, axis=-1), np.cumsum(totals, axis=-1)
    k = np.arange(3, len(MONTHS) - 2)
    left_s, left_n = s[..., k - 1], n[..., k - 1]
    right_s, right_n = s[..., -1, None] - left_s, n[..., -1, None] - left_n

    def log_likelihood(count, total):
        p = np.clip(count / total, 1e-12, 1 - 1e-12)
        return count * np.log(p) + (total - count) * np.log1p(-p)

    scores = log_likelihood(left_s, left_n) + log_likelihood(right_s, right_n)
    return k[np.argmax(scores, axis=-1)]


def boundary(k):
    return f'{MONTHS[int(k) - 1]} | {MONTHS[int(k)]}'


def change_points(rows, repetitions):
    rng = np.random.default_rng(20261015)
    estimates = {}
    for model in MODELS:
        for field in ('correct', 'unknown'):
            grid = np.zeros((42, 10, 2))
            four = np.zeros((42, 10), dtype=bool)
            for mi, month in enumerate(MONTHS):
                pairs = defaultdict(dict)
                for row in rows:
                    if row['model'] == model and row['kind'] == 'choice' and row['month'] == month:
                        pairs[row['pair_id']][row['language']] = row
                if len(pairs) != 10 or any(set(pair) != set(LANGUAGES) for pair in pairs.values()):
                    raise ValueError(f'{model}/{month}: expected ten bilingual facts')
                for ei, pair_id in enumerate(sorted(pairs)):
                    for li, language in enumerate(LANGUAGES):
                        grid[mi, ei, li] = pairs[pair_id][language][field]
                    four[mi, ei] = pairs[pair_id]['zh']['N'] == 4
            settings = {
                'pooled': (grid.sum(axis=(1, 2)), np.full(42, 20)),
                'zh': (grid[:, :, 0].sum(axis=1), np.full(42, 10)),
                'en': (grid[:, :, 1].sum(axis=1), np.full(42, 10)),
                'four_options_only': ((grid * four[:, :, None]).sum(axis=(1, 2)), four.sum(axis=1) * 2),
            }
            result = {name: {'boundary': boundary(fit_cut(s, n)), 'k': int(fit_cut(s, n))}
                      for name, (s, n) in settings.items()}
            # Keep both language versions together when resampling facts within each month.
            indices = rng.integers(0, 10, size=(repetitions, 42, 10))
            samples = grid[np.arange(42)[None, :, None], indices, :].sum(axis=(2, 3))
            cuts = fit_cut(samples, np.full_like(samples, 20))
            result['conditional_stability'] = {boundary(k): int((cuts == k).sum())
                                               for k in sorted(set(cuts))}
            estimates[f'{model}.{field}'] = result
    return estimates


def metrics(rows, responses, repetitions):
    output = {'overall': {}, 'monthly': {}, 'periods': {}, 'usage': {},
              'change_points': change_points(rows, repetitions),
              'resampling': {'seed': 20261015, 'repetitions': repetitions,
                             'unit': 'fact, paired languages, sampled within each month'}}
    for model in MODELS:
        for language in LANGUAGES:
            key = f'{model}.{language}'
            subset = [row for row in rows if row['model'] == model and row['language'] == language]
            output['overall'][key] = summarize(subset)
            output['monthly'][key] = {month: summarize([row for row in subset if row['month'] == month])
                                      for month in MONTHS}
        for label, start, end in [('2023-2024', '2023-01', '2024-12'),
                                  ('2025-01', '2025-01', '2025-01'),
                                  ('2025-02-03', '2025-02', '2025-03'),
                                  ('2025-04-onward', '2025-04', '2026-06')]:
            output['periods'][f'{model}.{label}'] = summarize([
                row for row in rows if row['model'] == model and start <= row['month'] <= end])
        usages = [response['usage'] for response in responses[model]]
        input_key, output_key = ('input_tokens', 'output_tokens') if model == 'jev' else ('prompt_tokens', 'completion_tokens')
        output['usage'][model] = {'samples': len(usages),
                                  'input_tokens': sum(usage[input_key] for usage in usages),
                                  'output_tokens': sum(usage[output_key] for usage in usages),
                                  'cost_usd': str(sum(Decimal(str(usage['cost'])) for usage in usages)),
                                  'models': dict(Counter(response['model'] for response in responses[model]))}
    return output


def draw(data, language, metric):
    chinese = language == 'zh'
    if chinese:
        names = {font.name for font in font_manager.fontManager.ttflist}
        family = next((name for name in ('Noto Sans CJK SC', 'Noto Sans CJK JP', 'WenQuanYi Zen Hei') if name in names), None)
        if family is None:
            raise ValueError('Chinese plots require a CJK font, such as Noto Sans CJK')
    else:
        family = 'DejaVu Sans'
    accuracy = metric == 'choice_accuracy'
    titles = {
        (True, True): 'JEV 的正确率断点比 GPT-4.1-mini 更晚',
        (True, False): '正确率下降的同时，“不知道”明显增加',
        (False, True): "JEV's accuracy drops later than GPT-4.1-mini's",
        (False, False): 'The decline comes with a sharp rise in “unknown” responses',
    }
    subtitle = ('2023 年 1 月—2026 年 6 月 · 每月 10 个新闻事实 · 每个点均为当月原始结果'
                if chinese else 'January 2023–June 2026 · 10 news facts per month · Every point is an observed monthly rate')
    estimate = data['change_points'][f'jev.{"correct" if accuracy else "unknown"}']
    cut_index = estimate['pooled']['k']
    candidates = [MONTHS.index(label.split(' | ')[0])
                  for label, count in estimate['conditional_stability'].items()
                  if count / data['resampling']['repetitions'] >= 0.05]
    cut_label = boundary(cut_index)
    with plt.rc_context({'font.family': family, 'font.size': 11, 'axes.unicode_minus': False,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.spines.left': False, 'axes.edgecolor': '#CBD5DC',
                         'text.color': '#192B39', 'axes.labelcolor': '#364B5A',
                         'xtick.color': '#526572', 'ytick.color': '#526572'}):
        fig, axes = plt.subplots(2, 1, figsize=(14.8, 9.3), sharex=True, sharey=True)
        fig.patch.set_facecolor('#FFFFFF')
        fig.subplots_adjust(left=0.075, right=0.97, top=0.79, bottom=0.15, hspace=0.38)
        fig.text(0.075, 0.955, titles[(chinese, accuracy)], fontsize=23 if chinese else 22,
                 weight='bold', ha='left', va='top')
        fig.text(0.075, 0.906, subtitle, fontsize=11, color='#526572', va='top')
        handles = [Line2D([0], [0], color=COLORS[model], marker='o' if model == 'jev' else 'D',
                          linewidth=2.2, markersize=5, label=NAMES[model]) for model in MODELS]
        if accuracy:
            handles.append(Line2D([0], [0], color='#89959F', linestyle=(0, (4, 3)), linewidth=1.2,
                                  label='按实际选项数均匀猜测' if chinese else 'Uniform concrete-choice baseline'))
        fig.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.068, 0.865),
                   frameon=False, ncol=len(handles), columnspacing=2.2)
        for ax, questions_language, letter in zip(axes, LANGUAGES, ('A', 'B')):
            ax.set_facecolor('#FFFFFF')
            ax.axvspan(16.5, 17.5, color=COLORS['llm'], alpha=0.095, zorder=0)
            ax.axvspan(min(candidates) - 0.5, max(candidates) + 0.5,
                       color=COLORS['jev'], alpha=0.085, zorder=0)
            ax.axvline(16.5, color=COLORS['llm'], linestyle=(0, (2, 3)), linewidth=1, alpha=0.65)
            ax.axvline(cut_index - 0.5, color=COLORS['jev'], linestyle=(0, (5, 3)), linewidth=1.5, alpha=0.8)
            ax.text(17.1, 1.025, 'GPT 官方截止：2024-06' if chinese else 'GPT official cutoff: 2024-06',
                    transform=ax.get_xaxis_transform(), ha='center', va='bottom',
                    color=COLORS['llm'], fontsize=10)
            ax.text(cut_index + 0.4, 1.025,
                    f'JEV 最佳转折：{cut_label}' if chinese else f'JEV best split: {cut_label}',
                    transform=ax.get_xaxis_transform(), ha='center', va='bottom',
                    color=COLORS['jev'], fontsize=10)
            panel = ('中文题' if questions_language == 'zh' else '英文题') if chinese else (
                'Chinese questions' if questions_language == 'zh' else 'English questions')
            ax.set_title(f'{letter}  {panel}', loc='left', fontsize=13, weight='bold', pad=14)
            if accuracy:
                baseline = [data['monthly'][f'jev.{questions_language}'][month]['guess_baseline'] for month in MONTHS]
                ax.plot(range(42), baseline, color='#89959F', linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
            for model in MODELS:
                values = [data['monthly'][f'{model}.{questions_language}'][month][metric] for month in MONTHS]
                ax.plot(range(42), values, color=COLORS[model], linewidth=2,
                        marker='o' if model == 'jev' else 'D', markersize=4.1,
                        markeredgewidth=0.8, markeredgecolor='white', zorder=3)
            ax.set_ylim(-0.045, 1.055)
            ax.set_xlim(-0.8, 41.8)
            ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
            ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
            ax.grid(axis='y', color='#E5EAF0', linewidth=0.8)
            ax.set_axisbelow(True)
            ax.tick_params(axis='both', length=0, pad=7)
            ax.set_ylabel(('选择题正确率' if accuracy else '“不知道”比例') if chinese else (
                'Choice accuracy' if accuracy else 'Unknown rate'), labelpad=12)
            ticks = [0, 6, 12, 18, 24, 30, 36, 41]
            ax.set_xticks(ticks, [MONTHS[index] for index in ticks])
            ax.tick_params(axis='x', labelbottom=True)
        if chinese:
            footers = [
                '紫色窄带：GPT 官方截止月份（2024-06-01）；青色虚线：JEV 合并最佳断点。',
                '青色浅带：复采样频率 ≥5% 的候选所涉月份，不是训练截止日期的置信区间。',
                '每种语言每月 n=10；两种语言对应同一批事实。' + (' 灰虚线按当月候选数计算，猜测时不选择“不知道”。' if accuracy else ''),
            ]
        else:
            footers = [
                'Purple band: official GPT cutoff month (2024-06-01). Teal dashed line: best pooled JEV split.',
                'Teal band: months preceding splits selected in ≥5% of conditional resamples; not a training-cutoff confidence interval.',
                'n=10 per language/month; both languages test the same facts.' + (' Gray baseline: uniform guessing over concrete options only.' if accuracy else ''),
            ]
        for index, footer in enumerate(footers):
            fig.text(0.075, 0.087 - index * 0.025, footer, fontsize=9.8, color='#526572')
        output = REPORT / 'fig' / language / ('monthly-accuracy.png' if accuracy else 'monthly-unknown.png')
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=220, facecolor=fig.get_facecolor(), metadata={'Software': 'knowledge-cutoff/report/scripts/analyze.py'})
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Recompute the saved experiment statistics and its two bilingual figures.')
    parser.add_argument('--bootstrap', type=int, default=2000, help='Conditional within-month fact resamples; default 2000')
    args = parser.parse_args()
    if args.bootstrap < 1:
        parser.error('--bootstrap must be positive')
    rows, responses = observations()
    data = metrics(rows, responses, args.bootstrap)
    for language in LANGUAGES:
        for metric in ('choice_accuracy', 'unknown_rate'):
            draw(data, language, metric)
    print(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
