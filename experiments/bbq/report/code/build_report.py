"""Build bilingual Markdown and standalone LaTeX reports from aggregate results.

No model calls. PDF export uses an existing XeLaTeX installation with --pdf.
"""
from pathlib import Path
import argparse, json, re, subprocess
ROOT = Path(__file__).resolve().parents[4]
NAMES = ('bbq',)
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
    a = s['groups']['all/ambig']
    b = s['groups']['all/disambig']
    d['title'] = t('Jev 在 BBQ 上的证据使用与社会偏见', 'Jev on BBQ: Evidence Use and Social Bias')
    d['abstract'] = t(f"在 BBQ 的 58,492 道英语题中，Jev 在信息不足情境下的准确率为 {pct(a['accuracy'])}，在信息充分情境下为 {pct(b['accuracy'])}。信息不足时的大多数回答正确保留为未知；其 {a['nonunknown_denominator']} 次具体对象回答中，{a['biased_count']} 次符合预设刻板印象方向。信息充分时仍有 {pct(b['unknown_rate'])} 的回答选择未知。", f"Across 58,492 English BBQ items, Jev achieves {pct(a['accuracy'])} accuracy with insufficient information and {pct(b['accuracy'])} with sufficient information. Most under-informative cases are correctly left unknown; {a['biased_count']} of the {a['nonunknown_denominator']} concrete-person answers follow the predefined stereotype direction. With sufficient information, {pct(b['unknown_rate'])} of answers remain unknown.")
    d['scene'] = [t('材料来自固定版本 BBQ 的全部 11 个数据文件，覆盖九个基础社会维度与两个交叉类别，语境为美国英语社会。14,623 个四题组各包含信息不足／充分与负向／非负向设问的组合。题目英文和选项顺序保留原样，模型版本为 ' + MODEL + '。', 'The fixed BBQ release contains 11 files covering nine base social dimensions and two intersectional categories in U.S. English-speaking contexts. Its 14,623 quartets combine insufficient/sufficient information with negative/non-negative questions. English wording and option order are preserved. Model snapshot: ' + MODEL + '.'), t('社会类别和偏见方向取自官方标注。用于区间估计的 342 个模板家族由本次分析依来源模板补充分组，同模板扩展题共同计入；这不是新增的社会类别。', 'Social categories and stereotype directions come from official annotations. The 342 template families used for interval estimation are an additional grouping defined in this analysis from source templates; expansions of a template stay together. They are not new social categories.')]
    rows = []
    for label, key, g in [(t('信息不足', 'Insufficient'), 'ambig', a), (t('信息充分', 'Sufficient'), 'disambig', b)]:
        rows.append([label, number(g['n']), pct(g['accuracy']), ci(s['cluster_bootstrap']['all/' + key]['intervals']['accuracy']), pct(g['unknown_rate']), f"{100 * g['bias_score']:+.2f}"])
    d['sections'].append(section(t('整体结果', 'Overall results'), para(t('准确率以官方答案为判据。偏见分数采用官方方向，以下按 -100 至 100 标度报告，正值表示净方向符合预设刻板印象。三选一随机准确率参照为 33.33%。', 'Accuracy uses official answer labels. Bias scores use the official stereotype direction and are reported on a -100 to 100 scale; positive values indicate net alignment with the predefined stereotype. The uniform three-option accuracy baseline is 33.33%.')), table(t(['情境', '题数', '准确率', '95% 区间', '未知率', '偏见分数'], ['Context', 'Items', 'Accuracy', '95% interval', 'Unknown', 'Bias score']), rows), para(t('始终选择未知的模型在信息不足题上准确率为 100%，在信息充分题上为 0%。因此，两个情境及未知率需要同时阅读。接近零的净偏见分数也可能来自相反方向的错误抵消。', 'An always-unknown model scores 100% on insufficient-information items and 0% on sufficient-information items. The two conditions and unknown rates must therefore be read together. Opposite-direction errors can also cancel in a near-zero net bias score.'))))
    cats = [('Age', '年龄'), ('Disability_status', '残障状态'), ('Gender_identity', '性别认同'), ('Nationality', '国籍'), ('Physical_appearance', '外貌'), ('Race_ethnicity', '种族／族裔'), ('Religion', '宗教'), ('SES', '社会经济地位'), ('Sexual_orientation', '性取向'), ('Race_x_gender', '种族 × 性别'), ('Race_x_SES', '种族 × 经济地位')]
    rows = []
    for key, label in cats:
        x = s['groups'][f'category/{key}/ambig']
        y = s['groups'][f'category/{key}/disambig']
        rows.append([t(label, key.replace('_', ' ')), number(x['n']), pct(x['accuracy']), pct(y['accuracy']), pct(y['unknown_rate'])])
    d['sections'].append(section(t('社会类别', 'Social categories'), table(t(['类别', '每种情境题数', '不足：准确率', '充分：准确率', '充分：未知率'], ['Category', 'Items per condition', 'Insufficient accuracy', 'Sufficient accuracy', 'Sufficient unknown']), rows), para(t('信息不足时，宗教和年龄类别准确率较低；信息充分时，外貌与社会经济地位类别准确率较低。基础类别和交叉类别题数不同，总体成绩不是类别等权平均。', 'Religion and age have lower accuracy under insufficient information. Physical appearance and socioeconomic status have lower accuracy under sufficient information. Category sizes differ, so the overall result is not a category-balanced mean.'))))
    d['sections'].append(section(t('回答方向与证据', 'Answer direction and evidence'), table(t(['行为', '次数／比例'], ['Behavior', 'Count / rate']), [[t('不足：具体对象回答', 'Insufficient: concrete-person answers'), a['nonunknown_denominator']], [t('其中符合刻板印象方向', 'Of those: stereotype-aligned'), f"{a['biased_count']} / {a['nonunknown_denominator']} ({pct(a['biased_count'] / a['nonunknown_denominator'])})"], [t('充分：选择未知', 'Sufficient: unknown'), b['unknown_count']], [t('充分：选择错误对象', 'Sufficient: incorrect person'), b['n'] - b['correct'] - b['unknown_count']], [t('充分：证据符合刻板印象时准确率', 'Sufficient: stereotype-aligned evidence accuracy'), pct(b['aligned_accuracy'])], [t('充分：证据相反时准确率', 'Sufficient: opposing evidence accuracy'), pct(b['opposed_accuracy'])]]), para(t('偏见标注齐全的子集用于偏见分数；全量题目用于准确率。充分信息题的正确答案方向并非严格平衡，即使全答对，官方全量偏见分数也约为 +0.54，不能把偏离零全部解释为模型错误。', 'Bias scores use the subset with complete target annotations; accuracy uses all items. Correct-answer directions in sufficient-information items are not exactly balanced: even perfect answers score about +0.54 on the official overall bias metric. A nonzero score cannot therefore be attributed entirely to model error.'))))
    c = s['billing']
    d['cost'] = [c['input_tokens'], c['output_tokens'], c['reported_usd']]
    d['cost_note'] = t('费用含全部有计费结果的尝试。一次技术失败没有返回费用，另有 0.002 美元历史预留，未计作已结算金额。全部 58,492 题最终均有有效响应。', 'Costs cover every attempt with reported billing. One technical failure has no reported cost; a separate historical USD 0.002 reservation is not treated as a settled charge. All 58,492 items ultimately have valid responses.')
    d['conclusion'] = t('Jev 在多数题目上能够区分证据不足与充分的情境。剩余问题包括信息不足时少量、但方向集中的刻板印象推断，以及信息充分时仍选择未知。总体高准确率与低净偏见分数需要结合这些具体回答行为解读，结论对应本次美国英语题集。', 'Jev distinguishes insufficient from sufficient evidence on most items. Remaining issues include infrequent but directionally concentrated stereotypical inferences without enough information, and unknown answers despite sufficient information. High overall accuracy and low net bias scores should be interpreted alongside these behaviors in this U.S. English dataset.')
    d['refs'] = [('Parrish et al. (2022). BBQ: A Hand-Built Bias Benchmark for Question Answering. Findings of ACL.', 'https://aclanthology.org/2022.findings-acl.165/'), ('BBQ official release, commit bea11bd97d79217245b5871acd247b9d6eb24598; CC BY 4.0.', 'https://github.com/nyu-mll/BBQ')]
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
