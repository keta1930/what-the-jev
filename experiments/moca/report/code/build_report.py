"""Build bilingual Markdown and standalone LaTeX reports from aggregate results.

No model calls. PDF export uses an existing XeLaTeX installation with --pdf.
"""
from pathlib import Path
import argparse, json, re, subprocess
ROOT = Path(__file__).resolve().parents[4]
NAMES = ('moca',)
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
    m = s['metrics']
    d['title'] = t('Jev 在 MoCa 因果与道德判断中的人类一致性', 'Jev on MoCa: Agreement with Human Causal and Moral Judgments')
    d['abstract'] = t(f"在 MoCa 的 206 个英语故事上，Jev 与每题 25 人聚合判断的三类一致率为 {pct(m['overall']['three_class_agreement'])}。因果题为 {pct(m['causal']['three_class_agreement'])}，道德题为 {pct(m['moral']['three_class_agreement'])}。Jev 能区分人类明确肯定与否定的题目，但对人类分歧较大的因果故事较少落入模糊区间。", f"Across 206 English MoCa stories, Jev’s three-class agreement with the aggregated judgments of 25 human respondents per item is {pct(m['overall']['three_class_agreement'])}. Agreement is {pct(m['causal']['three_class_agreement'])} for causal items and {pct(m['moral']['three_class_agreement'])} for moral items. Jev distinguishes clear human yes/no judgments but rarely places human-ambiguous causal stories in the ambiguous interval.")
    d['scene'] = [t('材料包括 144 个因果故事与 62 个道德许可故事。参照为数据集每题的 25 个人类二元判断。三类为 Yes、No 和 Ambiguous，沿用 0.4／0.6 边界；Jev 的第三类由二选一概率派生。模型版本为 ' + MODEL + '。', 'The dataset includes 144 causal stories and 62 moral-permissibility stories, each with 25 binary human judgments. The classes are Yes, No and Ambiguous, using the 0.4/0.6 boundaries; Jev’s third class is derived from its binary-choice probability. Model snapshot: ' + MODEL + '.'), t('因素名称沿用来源中的专家标注，同一故事可以包含多个因素。人类比例与 Jev 结构化选择概率具有不同含义，本文报告它们在这组故事上的一致性与数值差异。', 'Factor names follow the source’s expert annotations, and factors may overlap within a story. Human response proportions and Jev’s structured-choice probabilities have different meanings; this report describes their agreement and numerical differences on these stories.')]
    rows = []
    for key, label in [('overall', t('全部', 'All')), ('causal', t('因果', 'Causal')), ('moral', t('道德', 'Moral'))]:
        r = m[key]
        rows.append([label, r['n'], pct(r['three_class_agreement']), ci(r['three_class_agreement_ci95']), f"{r['auroc_human_unambiguous']:.3f}", f"{r['yes_probability_mae']:.3f}"])
    d['sections'].append(section(t('整体结果', 'Overall results'), para(t('以数据集的人类聚合标签为一致性判据，不将人类多数判断称为道德正确答案。三类均匀随机参照为 33.33%，总体多数类参照为 36.41%。AUROC 只使用人类非模糊题。', 'Agreement is judged against the dataset’s aggregated human labels, without treating majority judgments as moral truth. Uniform three-class chance is 33.33%; the overall majority-class baseline is 36.41%. AUROC uses only human-unambiguous items.')), table(t(['范围', '题数', '一致率', '95% 区间', 'AUROC', '概率 MAE'], ['Subset', 'Items', 'Agreement', '95% interval', 'AUROC', 'Probability MAE']), rows)))
    rows = []
    for key, label in [('causal', t('因果', 'Causal')), ('moral', t('道德', 'Moral'))]:
        for k, label2 in [('human_label_counts', t('人类', 'Human')), ('jev_label_counts', 'Jev')]:
            r = m[key][k]
            rows.append([label, label2, r.get('Yes', 0), r.get('No', 0), r.get('Ambiguous', 0)])
    d['sections'].append(section(t('判断分布', 'Judgment distributions'), table(t(['范围', '来源', 'Yes', 'No', 'Ambiguous'], ['Subset', 'Source', 'Yes', 'No', 'Ambiguous']), rows), para(t('46 个被人类归为模糊的因果题中，Jev 只有 1 题同样归为模糊；道德题相应为 12/29。因果题中 Jev 的肯定判断明显更多，说明三类一致率较低主要涉及判断分布及边界差异。', 'Only 1 of 46 human-ambiguous causal items is also classified as ambiguous by Jev; the corresponding count is 12 of 29 moral items. Jev gives substantially more affirmative causal judgments, showing that lower three-class agreement involves distribution and boundary differences.'))))
    labels = {'action_omission': ('行动 → 不作为', 'Action to omission'), 'agent_awareness': ('知情 → 不知情', 'Aware to unaware'), 'causal_structure': ('合取 → 析取', 'Conjunctive to disjunctive'), 'event_normality': ('异常 → 正常', 'Abnormal to normal'), 'beneficiary': ('他人受益 → 自己受益', 'Other to self beneficiary'), 'causal_role': ('意外 → 工具性', 'Accidental to instrumental'), 'evitability': ('可避免 → 不可避免', 'Avoidable to inevitable'), 'personal_force': ('非个人施力 → 个人施力', 'Impersonal to personal force')}
    rows = [[t(*labels[r['dimension']]), f"{r['n_a']} / {r['n_b']}", f"{r['human_delta_b_minus_a']:+.3f}", f"{r['jev_delta_b_minus_a']:+.3f}"] for r in s['factor_contrasts'] if r['dimension'] in labels]
    d['sections'].append(section(t('因素分组的平均差异', 'Mean differences across factor groups'), table(t(['分组变化', '两组题数', '人类差值', 'Jev 差值'], ['Group transition', 'Group sizes', 'Human difference', 'Jev difference']), rows), para(t('差值描述后一组相对前一组的平均肯定比例／概率变化。因素相互重叠，故事内容也随组变化，因此这些结果为描述性关联，不是单个因素的独立因果效应。', 'Differences describe changes in mean affirmative share/probability from the first group to the second. Factors overlap and story content changes across groups; these are descriptive associations, not isolated causal effects.'))))
    c = s['cost']
    d['cost'] = [c['input_tokens'], c['output_tokens'], c['actual_cost_usd']]
    d['cost_note'] = t('206 次请求全部一次成功，没有未知费用或重试。', 'All 206 requests succeeded on the first attempt, with no unknown charges or retries.')
    d['conclusion'] = t('Jev 与人类聚合判断呈现部分相似性，道德题的一致性高于因果题。对人类明确肯定与否定的区分能力，并未转化为对人类模糊判断的同等识别。因素分组的部分平均方向相同，另一些方向不同；这些结果描述相同故事上的判断关系。', 'Jev shows partial agreement with aggregated human judgments, with higher agreement on moral than causal items. Its ability to distinguish clear human yes/no judgments does not translate into comparable identification of human ambiguity. Some factor-group mean directions match and others differ; the findings describe judgments on the same stories.')
    d['refs'] = [('Nie et al. (2023). MoCa: Measuring Human-Language Model Alignment on Causal and Moral Judgment Tasks. NeurIPS.', 'https://arxiv.org/abs/2310.19677'), ('MoCa official repository, commit 1b61a20294247480d64675ceb19751ef4e1e878f.', 'https://github.com/cicl-stanford/moca')]
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
