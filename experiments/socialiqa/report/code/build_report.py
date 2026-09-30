"""Build bilingual Markdown and standalone LaTeX reports from aggregate results.

No model calls. PDF export uses an existing XeLaTeX installation with --pdf.
"""
from pathlib import Path
import argparse, json, re, subprocess
ROOT = Path(__file__).resolve().parents[4]
NAMES = ('socialiqa',)
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
    d['title'] = t('Jev 在 SocialIQA 社会常识选择题上的表现', 'Jev on SocialIQA: Social Commonsense Decisions')
    d['abstract'] = t(f"在 SocialIQA v1.4 的 {number(s['n'])} 道英语测试题中，Jev 答对 {number(s['correct'])} 道，准确率为 {pct(s['accuracy'])}，按重复题目聚类的 95% 区间为 {ci(s['cluster_bootstrap95'])}。九个官方来源分组的准确率为 78.11%–84.66%。结果反映对日常人物动机、情绪和行动后果的选择判断表现。", f"Jev answered {number(s['correct'])} of {number(s['n'])} English SocialIQA v1.4 test questions correctly, achieving {pct(s['accuracy'])} accuracy with a duplicate-question cluster 95% interval of {ci(s['cluster_bootstrap95'])}. Accuracy across the nine official source groups ranges from 78.11% to 84.66%. These results describe selection judgments about everyday motives, emotions and consequences.")
    d['scene'] = [t('材料为作者发布的 v1.4 test 全部 2,224 行，每题包含英语情境、问题及三个选项。每题独立作答，按公开参考标签评分。模型版本为 ' + MODEL + '。', 'The material contains all 2,224 rows of the authors’ v1.4 test release. Each item contains an English context, a question and three options. Each is answered independently and scored against the released reference label. Model snapshot: ' + MODEL + '.'), t('九个分组使用官方 promptDim 字段。该字段记录 ATOMIC 问题生成来源，人工改写后的问题可能偏离原始维度，因此分组不作为九种独立心理能力的测量。材料为长期公开的英语选择题；本次成绩描述这一题集上的表现。', 'The nine groups use the official promptDim field, which records the ATOMIC question-generation source. Rewritten questions can depart from that source, so these groups are not treated as nine independent psychological abilities. The evaluation concerns a long-public English multiple-choice dataset.')]
    d['sections'].append(section(t('整体结果', 'Overall results'), para(t('以数据集提供的答案为判据。全部正式题均获得有效响应，随机三选一参照为 33.33%。', 'The dataset labels are the scoring criterion. Every formal item has a valid response. Uniform random three-option selection has an expected accuracy of 33.33%.')), table(t(['指标', '结果'], ['Measure', 'Result']), [[t('正式题数', 'Formal items'), number(s['n'])], [t('答对题数', 'Correct'), number(s['correct'])], [t('准确率', 'Accuracy'), pct(s['accuracy'])], [t('题目聚类 95% 区间', 'Question-cluster 95% interval'), ci(s['cluster_bootstrap95'])], [t('不同完整题目数', 'Distinct complete questions'), s['unique_first_occurrence']['n']], [t('不同完整题目准确率', 'Distinct-question accuracy'), pct(s['unique_first_occurrence']['accuracy'])]])))
    labels = {'oEffect': ('对他人的影响', 'Effect on others'), 'oReact': ('他人情绪反应', 'Others’ reactions'), 'oWant': ('他人后续意愿', 'Others’ wants'), 'xAttr': ('主角属性', 'Actor attributes'), 'xEffect': ('对主角的影响', 'Effect on actor'), 'xIntent': ('主角动机', 'Actor intent'), 'xNeed': ('主角事前需要', 'Actor prerequisites'), 'xReact': ('主角情绪反应', 'Actor reactions'), 'xWant': ('主角后续意愿', 'Actor wants')}
    d['sections'].append(section(t('官方来源分组', 'Official source groups'), table(t(['分组', '题数', '答对', '准确率'], ['Group', 'Items', 'Correct', 'Accuracy']), [[f'{k} ({t(*labels[k])})', v['n'], v['correct'], pct(v['accuracy'])] for k, v in s['groups'].items()]), para(t('xWant 分组最高，xAttr 分组最低。各组题量不同，排序仅描述本题集，不构成稳定能力等级。', 'The xWant group has the highest accuracy and xAttr the lowest. Group sizes differ; this ordering describes the dataset rather than a stable hierarchy of abilities.'))))
    cost = s['cost']
    d['cost'] = [cost['test']['input_tokens'], cost['test']['output_tokens'], cost['test']['reported_usd']]
    d['cost_note'] = t(f"正式评测已报告费用为 {dec(cost['test']['reported_usd'])} 美元。另有 12 道接口调试题；含调试的已报告总费用为 {dec(sum((x['reported_usd'] for x in cost.values())))} 美元，共 855,948 输入 token、84,968 输出 token。一次技术失败未报告费用，历史账本另保留 0.01 美元预留；预留不计作已结算费用。", f"Reported formal-evaluation cost is USD {dec(cost['test']['reported_usd'])}. Twelve separate interface-debugging items bring the reported total to USD {dec(sum((x['reported_usd'] for x in cost.values())))}, with 855,948 input tokens and 84,968 output tokens. One technical failure has unknown billing; the historical ledger retains USD 0.01 as a reservation, not a settled charge.")
    d['conclusion'] = t(f"Jev 在这份英语社会常识题集上达到 {pct(s['accuracy'])} 准确率，能够对多数人物动机、情绪和行动后果作出符合参考答案的选择。仍有 {s['n'] - s['correct']} 题未选中参考答案。该表现可作为社会情境理解的基线，分数的解释限于本次选择题条件，不等同于情感体验或助人意愿。", f"Jev achieves {pct(s['accuracy'])} accuracy on this English social-commonsense dataset, selecting the reference answer for most questions about motives, emotions and consequences. It misses {s['n'] - s['correct']} reference answers. The result provides a baseline for social-situation understanding under the tested selection format; it does not measure emotional experience or willingness to help.")
    d['refs'] = [('Sap et al. (2019). Social IQa: Commonsense Reasoning about Social Interactions. EMNLP-IJCNLP.', 'https://aclanthology.org/D19-1454/'), ('SocialIQA v1.4: authors’ dataset release, CC BY 4.0.', 'https://maartensap.com/social-iqa/')]
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
