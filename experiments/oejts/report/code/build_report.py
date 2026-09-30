"""Build bilingual Markdown and standalone LaTeX reports from aggregate results.

No model calls. PDF export uses an existing XeLaTeX installation with --pdf.
"""
from pathlib import Path
import argparse, json, re, subprocess
ROOT = Path(__file__).resolve().parents[4]
NAMES = ('oejts',)
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
    d['title'] = t('Jev 在 OEJTS 开放类型量表上的回答倾向与重复稳定性', 'Jev on OEJTS: Response Tendencies and Repeat Stability')
    d['abstract'] = t(f"对 OEJTS 1.2 的 32 道英语五级选择题进行十轮独立施测，得到 {s['completed_answers']} 个有效回答。按该量表计分，十轮均得到 ISTJ；SN 维度最接近分类分界点，十轮中有两轮恰在分界点。{s['fully_stable_questions']}/32 道题在十轮中始终选择同一位置。结果描述固定措辞下的回答与计分稳定性。", f"Ten rounds of the 32 English five-position OEJTS 1.2 items yield {s['completed_answers']} valid responses. The scale’s scoring rule yields ISTJ in all ten rounds. SN lies closest to its classification boundary and falls exactly on it in two rounds. {s['fully_stable_questions']} of 32 items retain the same position in every round. Results describe response and scoring stability under fixed wording.")
    d['scene'] = [t('OEJTS 1.2 是 Eric Jorgenson 发布的开放替代量表，不是官方 MBTI。每题以两端描述和五个位置呈现，使用固定的模型自评说明，每题独立请求，连续完成十轮。模型版本为 ' + MODEL + '。', 'OEJTS 1.2 is an open alternative scale released by Eric Jorgenson, not the official MBTI. Each item presents two endpoint descriptions and five positions under a fixed model-self-description instruction. Items are requested independently across ten rounds. Model snapshot: ' + MODEL + '.'), t('四维 IE、SN、FT、JP 的计分及分界沿用该量表。题目含有人类生活经历描述，因而本实验将其作为模型回答倾向的探索性适配。类型次数表示本次计分结果的重复次数，不表示人格概率。', 'The scale’s scoring and boundaries are used for IE, SN, FT and JP. Because items include human lived-experience descriptions, this is an exploratory adaptation of model response tendencies. Type counts are repeated scoring outcomes, not personality probabilities.')]
    d['sections'].append(section(t('整体结果', 'Overall results'), para(t('判据为原量表的数值计分规则，没有正确答案准确率。全选中间位置的四维分数均为 24，按原分类规则得到 ISFJ，可作为分界参照。', 'The criterion is the scale’s numerical scoring rule; there is no correct-answer accuracy. Selecting the middle position on every item gives 24 on each dimension and ISFJ under the original classification rule, providing a boundary reference.')), table(t(['指标', '结果'], ['Measure', 'Result']), [[t('独立题目', 'Distinct items'), 32], [t('完整轮次', 'Complete rounds'), 10], [t('有效回答', 'Valid responses'), s['completed_answers']], [t('类型次数', 'Type counts'), 'ISTJ: 10'], [t('十轮完全一致的题目', 'Items unchanged across ten rounds'), f"{s['fully_stable_questions']} / 32"]])))
    d['sections'].append(section(t('各维度稳定性', 'Dimension stability'), table(t(['维度', '均值', '最小值', '最大值', '平均距 24', '分界点轮数'], ['Dimension', 'Mean', 'Minimum', 'Maximum', 'Mean distance from 24', 'Boundary rounds']), [[a, f"{r['mean']:.2f}", r['min'], r['max'], f"{r['mean_distance_from_24']:.2f}", r['boundary_rounds']] for a, r in s['dimensions'].items()]), para(t('SN 的平均距分界点为 1.60，明显小于其余维度。十轮类型相同并不表示每道题的答案都相同，也不表示所有维度都远离分界。', 'SN has a mean boundary distance of 1.60, smaller than the other dimensions. An identical type across ten rounds does not imply identical item answers or that every dimension is far from its boundary.'))))
    d['sections'].append(section(t('逐轮计分', 'Scores by round'), table(t(['轮次', '类型', 'IE', 'SN', 'FT', 'JP', '分界维度'], ['Round', 'Type', 'IE', 'SN', 'FT', 'JP', 'Boundary']), [[r['round'], r['type'], *[r['scores'][a] for a in ('IE', 'SN', 'FT', 'JP')], ', '.join(r['boundary_axes']) or '-'] for r in s['rounds']])))
    d['cost'] = [s['input_tokens'], s['output_tokens'], s['known_cost_usd']]
    d['cost_note'] = t('320 次请求均有有效响应和计费记录，没有未知费用。官方 MBTI 没有施测结果。', 'All 320 requests have valid responses and billing records, with no unknown charges. There are no results from the official MBTI.')
    d['conclusion'] = t('Jev 在固定说明、英语题目与位置顺序下呈现较高的重复稳定性，十轮按 OEJTS 规则均得到 ISTJ。SN 维度接近分界，部分题目仍会改变选择。这一结论针对本次量表回答与计分，不能作为已验证的模型人格测量。', 'Jev shows high repeat stability under the fixed instruction, English wording and position order, yielding ISTJ under OEJTS rules in every round. SN lies near the boundary and some item choices vary. This finding concerns questionnaire responses and scoring, not a validated measurement of model personality.')
    d['refs'] = [('Eric Jorgenson (2015). Open Extended Jungian Type Scales 1.2. Original items: CC BY-NC-SA 4.0. Questionnaire text is not redistributed here.', 'https://openpsychometrics.org/tests/OJTS/development/OEJTS1.2.pdf')]
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
