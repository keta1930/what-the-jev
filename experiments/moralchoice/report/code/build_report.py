"""Build bilingual Markdown and standalone LaTeX reports from aggregate results.

No model calls. PDF export uses an existing XeLaTeX installation with --pdf.
"""
from pathlib import Path
import argparse, json, re, subprocess
ROOT = Path(__file__).resolve().parents[4]
NAMES = ('moralchoice',)
MODEL = 'typesafe/jev-1.13-20260917'

def pct(x):
    return f'{100 * x:.2f}%'

def ci(x):
    return f'{pct(x[0])}–{pct(x[1])}'

def number(x):
    return f'{x:,}'

def dec(x):
    return f'{float(x):.9f}'.rstrip('0').rstrip('.')

def para(text):
    return {'kind': 'paragraph', 'text': text}

def table(headers, rows):
    return {'kind': 'table', 'headers': headers, 'rows': [[str(c) for c in r] for r in rows]}

def section(title, *blocks):
    return {'title': title, 'blocks': list(blocks)}

def document(name, zh):
    s = json.loads((ROOT / f'experiments/{name}/report/generated/summary.json').read_text(encoding='utf-8'))

    def t(c, e):
        return c if zh else e
    d = {'lang': 'zh' if zh else 'en', 'name': name, 'sections': []}
    lo = s['low']
    hi = s['high']
    d['title'] = t('Jev 在 MoralChoice 中的道德选择与稳定性', 'Jev on MoralChoice: Moral Choices and Response Stability')
    d['abstract'] = t(f"在 MoralChoice 的 1,367 个英语情境中，每个情境包含六个结构化判断。687 个低歧义情境的六种变体全部选择参考行动。680 个高歧义情境中，{pct(hi['all_decisions_action1']['rate'])} 的判断选择 action1，{pct(hi['six_variant']['unanimous_underlying_action']['rate'])} 的情境在六种变体下选择同一行动。高歧义情境的选择通常稳定，但对提问形式和顺序仍有敏感性。", f"Each of 1,367 English MoralChoice scenarios receives six structured judgments. All six variants select the reference action in every one of the 687 low-ambiguity scenarios. In the 680 high-ambiguity scenarios, {pct(hi['all_decisions_action1']['rate'])} of judgments select action1 and {pct(hi['six_variant']['unanimous_underlying_action']['rate'])} of scenarios retain the same underlying action across all variants. High-ambiguity choices are usually stable, with remaining sensitivity to form and order.")
    d['scene'] = [t('发布数据包含 687 个低歧义和 680 个高歧义情境。低歧义情境以 action1 为参考行动，高歧义情境不设统一正确答案。每个情境包括 ab、repeat、compare 三种形式及各自的正逆序，共 8,202 个判断。模型版本为 ' + MODEL + '。', 'The release contains 687 low-ambiguity and 680 high-ambiguity scenarios. The reference action is action1 for low-ambiguity scenarios; no universal correct action is assigned to high-ambiguity scenarios. Each scenario has ab, repeat and compare forms in both orders, yielding 8,202 judgments. Model snapshot: ' + MODEL + '.'), t('形式和顺序沿用原研究设计，输出改为 Jev 的结构化二选一。同一情境六个问题在一次请求中回答；repeat 不再测试逐字文本复述。顺序及跨形式稳定性为本次适配的分析指标，六个判断不作为六个独立情境。', 'Forms and order swaps follow the original design, while output is adapted to Jev’s structured binary choice. Six questions are answered in one request per scenario; repeat does not test verbatim text repetition. Order and cross-form stability are analysis measures for this adaptation, and six judgments are not counted as six independent scenarios.')]
    d['sections'].append(section(t('整体结果', 'Overall results'), para(t('低歧义以发布数据的参考行动为判据，随机二选一参照为 50%。高歧义仅描述选择分布，不计算正确率。', 'Low-ambiguity judgments use the released reference action, with a 50% uniform binary-choice baseline. High-ambiguity results describe choices rather than accuracy.')), table(t(['指标', '低歧义', '高歧义'], ['Measure', 'Low ambiguity', 'High ambiguity']), [[t('情境数', 'Scenarios'), lo['scenarios'], hi['scenarios']], [t('判断数', 'Judgments'), lo['questions'], hi['questions']], [t('action1 选择比例', 'Share selecting action1'), pct(lo['all_decisions_action1']['rate']), pct(hi['all_decisions_action1']['rate'])], [t('六种变体选择同一行动', 'Same action across all six'), pct(lo['six_variant']['unanimous_underlying_action']['rate']), pct(hi['six_variant']['unanimous_underlying_action']['rate'])], [t('平均 P(action1)', 'Mean P(action1)'), pct(lo['all_p_action1']['mean']), pct(hi['all_p_action1']['mean'])]]), para(t('低歧义的情境级全部选择参考行动比例为 100%，Wilson 95% 区间为 99.44%–100%。高歧义的 action1 比例受发布数据中行动内容的排列影响，不等于首位选项偏好。', 'Every low-ambiguity scenario selects the reference action in all variants: 100%, with a scenario-level Wilson 95% interval of 99.44%–100%. The high-ambiguity action1 share depends on the content arrangement in the release; it is not a first-position preference.'))))
    rows = []
    for form, r in hi['order_stability'].items():
        a = r['hard_choice_agreement']
        rows.append([form, f"{a['numerator']} / {a['denominator']}", pct(a['rate']), pct(r['absolute_p_action1_change']['mean']), pct(r['first_presented_option_choice']['rate'])])
    d['sections'].append(section(t('高歧义稳定性', 'High-ambiguity stability'), table(t(['形式', '正逆序一致', '一致率', '平均概率变化', '首位选择率'], ['Form', 'Order agreement', 'Rate', 'Mean probability change', 'First-position share']), rows), para(t('616/680 个情境的六种变体选择相同。compare 的正逆序一致率最低，表明是／否比较形式更容易随顺序改变底层选择。六种概率的情境内平均极差为 10.75 个百分点。', 'All six variants agree in 616 of 680 scenarios. The compare form has the lowest order agreement, indicating greater sensitivity of yes/no comparisons to order. The mean within-scenario probability range across six variants is 10.75 percentage points.'))))
    d['sections'].append(section(t('辅助规则分组', 'Auxiliary rule groups'), para(t('辅助规则标签来自发布数据，并可能相互重叠。仅比较一个行动被标为违反、另一个明确标为不违反该规则的情境。完整聚合表保存在机器可读汇总中。', 'Auxiliary rule labels come from the release and may overlap. Comparisons use scenarios where one action is marked as violating a rule and the other explicitly is not. Full aggregate tables are retained in the machine-readable summary.'))))
    d['sections'][-1]['blocks'].append(table(t(['规则标签', '高歧义情境数', '选择不违反该规则', '六种变体均不违反'], ['Rule label', 'High-ambiguity scenarios', 'Nonviolating choice share', 'All six nonviolating']), [[r['rule_label'], r['contrast_scenarios'], pct(r['nonviolating_action_choice']['rate']), pct(r['six_variant_unanimous_nonviolating']['rate'])] for r in s['high_auxiliary_rule_contrasts']]))
    c = s['cost']
    d['cost'] = [c['input_tokens'], c['output_tokens'], c['actual_cost_usd']]
    d['cost_note'] = t('1,367 次请求全部成功，无重试或未知费用。', 'All 1,367 requests succeeded, with no retries or unknown charges.')
    d['conclusion'] = t('Jev 在低歧义情境下与参考选择完全一致。高歧义情境没有统一正确答案，约九成情境的底层行动在六种形式和顺序组合中保持一致；其余变化主要集中在比较形式。此结果描述结构化选择及其稳定性，不将集中的选择概率解释为道德正确性或人类意见比例。', 'Jev fully agrees with the reference choices in low-ambiguity scenarios. High-ambiguity scenarios have no universal correct answer; about nine in ten retain the same underlying action across the six form/order combinations, with more changes in the comparison form. The result describes structured choices and their stability, without equating concentrated probabilities with moral correctness or human opinion shares.')
    d['refs'] = [('Scherrer et al. (2023). Evaluating the Moral Beliefs Encoded in LLMs. NeurIPS.', 'https://proceedings.neurips.cc/paper_files/paper/2023/file/a2cf225ba392627529efef14dc857e22-Paper-Conference.pdf'), ('MoralChoice data release, commit 89c0fe7b158b5ade5d10e0644c1aa20ab4c78cbe; CC BY 4.0.', 'https://huggingface.co/datasets/ninoscherrer/moralchoice')]
    cost = d['cost']
    d['sections'].append(section(t('调用成本', 'Call costs'), table(t(['输入 token', '输出 token', '已报告费用（美元）'], ['Input tokens', 'Output tokens', 'Reported cost (USD)']), [[number(cost[0]), number(cost[1]), dec(cost[2])]]), para(d['cost_note'])))
    return d

def markdown(d):
    zh = d['lang'] == 'zh'
    text = [f"# {d['title']}", '', '## ' + ('摘要' if zh else 'Abstract'), '', d['abstract'], '', '## 1 ' + ('数据集' if zh else 'Dataset'), ''] + sum(([x, ''] for x in d['scene']), [])
    text += ['## 2 ' + ('结果' if zh else 'Results'), '']
    for i, s in enumerate(d['sections'], 1):
        text += [f"### 2.{i} {s['title']}", '']
        for b in s['blocks']:
            if b['kind'] == 'paragraph':
                text += [b['text'], '']
            else:
                text += ['| ' + ' | '.join(b['headers']) + ' |', '| ' + ' | '.join(['---'] * len(b['headers'])) + ' |']
                text += ['| ' + ' | '.join(row) + ' |' for row in b['rows']] + ['']
    text += ['## 3 ' + ('结论' if zh else 'Conclusion'), '', d['conclusion'], '', '## ' + ('参考文献' if zh else 'References'), '']
    text += [f'{i}. [{label}]({url})' for i, (label, url) in enumerate(d['refs'], 1)]
    return '\n'.join(text) + '\n'

def escape(s):
    return re.sub('[\\\\&%$#_{}~^]', lambda m: {'\\': '\\textbackslash{}', '&': '\\&', '%': '\\%', '$': '\\$', '#': '\\#', '_': '\\_', '{': '\\{', '}': '\\}', '~': '\\textasciitilde{}', '^': '\\textasciicircum{}'}[m[0]], str(s))

def latex(d):
    zh = d['lang'] == 'zh'
    header = '\\documentclass[10pt,a4paper,fontset=fandol]{ctexart}' if zh else '\\documentclass[10pt,a4paper]{article}'
    lines = [header, '\\usepackage[margin=2cm]{geometry}', '\\usepackage{fontspec,booktabs,longtable,array,xcolor,hyperref}', '\\setmainfont{TeX Gyre Pagella}', '\\setsansfont{TeX Gyre Heros}', '\\definecolor{reportblue}{HTML}{244D65}', '\\hypersetup{colorlinks=true,urlcolor=reportblue,linkcolor=reportblue}', '\\setlength{\\parindent}{0pt}', '\\setlength{\\parskip}{5pt}', '\\renewcommand{\\arraystretch}{1.18}', '\\setlength{\\tabcolsep}{5pt}', '\\emergencystretch=2em', '\\urlstyle{same}', '\\pagestyle{plain}', '\\title{\\sffamily ' + escape(d['title']) + '}', '\\author{}', '\\date{' + ('2026 年 9 月 30 日' if zh else 'September 30, 2026') + '}', '\\begin{document}', '\\maketitle', '\\section*{' + ('摘要' if zh else 'Abstract') + '}', escape(d['abstract']), '\\section{' + ('数据集' if zh else 'Dataset') + '}']
    lines.insert(2, '\\usepackage{needspace}')
    if zh:
        lines.insert(3, '\\ctexset{section={format=\\large\\sffamily\\bfseries,beforeskip=14pt,afterskip=7pt},subsection={format=\\normalsize\\sffamily\\bfseries,beforeskip=10pt,afterskip=5pt}}')
    title_index = lines.index('\\maketitle')
    date = '2026 年 9 月 30 日' if zh else 'September 30, 2026'
    lines[title_index] = '\\begin{center}{\\sffamily\\LARGE ' + escape(d['title']) + '\\par}\\vspace{8pt}{\\small ' + date + '}\\end{center}\\vspace{6pt}'
    lines.extend((escape(x) + '\n' for x in d['scene']))
    lines.append('\\section{' + ('结果' if zh else 'Results') + '}')
    for index, sec in enumerate(d['sections']):
        if d['name'] == 'socialiqa' and index == 1:
            lines.append('\\newpage')
        else:
            lines.append('\\Needspace{8\\baselineskip}')
        lines.append('\\subsection{' + escape(sec['title']) + '}')
        for block in sec['blocks']:
            if block['kind'] == 'paragraph':
                lines.append(escape(block['text']) + '\n')
                continue
            n = len(block['headers'])
            first = 0.4 if n == 2 else 0.32 if n == 4 else 0.24
            remain = (1 - first) / (n - 1)
            fractions = [first] + [remain] * (n - 1)
            widths = [f'>{{\\raggedright\\arraybackslash}}p{{\\dimexpr {f:.4f}\\textwidth-2\\tabcolsep\\relax}}' for f in fractions]
            lines += ['{\\small', '\\begin{longtable}{@{}' + ''.join(widths) + '@{}}', '\\toprule', ' & '.join(('\\textbf{' + escape(h) + '}' for h in block['headers'])) + '\\\\', '\\midrule', '\\endfirsthead', '\\toprule', ' & '.join(('\\textbf{' + escape(h) + '}' for h in block['headers'])) + '\\\\', '\\midrule', '\\endhead']
            lines += [' & '.join((escape(c) for c in row)) + '\\\\' for row in block['rows']]
            lines += ['\\bottomrule', '\\end{longtable}', '}']
    lines += ['\\Needspace{8\\baselineskip}', '\\section{' + ('结论' if zh else 'Conclusion') + '}', escape(d['conclusion']), '\\Needspace{5\\baselineskip}', '\\section*{' + ('参考文献' if zh else 'References') + '}', '\\begin{enumerate}']
    lines += ['\\item ' + escape(label) + ' ' + '\\url{' + url + '}' for label, url in d['refs']]
    lines += ['\\end{enumerate}', '\\end{document}']
    return '\n'.join(lines) + '\n'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--experiment', choices=NAMES)
    p.add_argument('--pdf', action='store_true')
    args = p.parse_args()
    for name in [args.experiment] if args.experiment else NAMES:
        out = ROOT / f'experiments/{name}/report'
        for lang in ['zh', 'en']:
            d = document(name, lang == 'zh')
            (out / f'report_{lang}.md').write_text(markdown(d), encoding='utf-8', newline='\n')
            tex = out / f'report_{lang}.tex'
            tex.write_text(latex(d), encoding='utf-8', newline='\n')
            if args.pdf:
                for _ in range(2):
                    run = subprocess.run(['xelatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', tex.name], cwd=out, capture_output=True, text=True, encoding='utf-8', errors='replace')
                    if run.returncode:
                        raise RuntimeError(f'{name}/{tex.name}: ' + run.stdout[-3500:])
                print(f'Exported {name}/report_{lang}.pdf', flush=True)
        print(f'Built bilingual report sources: {name}', flush=True)
if __name__ == '__main__':
    main()
