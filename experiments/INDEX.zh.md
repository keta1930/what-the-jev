# 实验

*[English](INDEX.md) | 简体中文*

十三个实验，按考察对象分组；每条链接到该实验的报告。

## 一、LLM benchmark：学科能力

1. [gpqa-diamond](gpqa-diamond/report/REPORT.zh.md) — 【研究生级科学题】测试 JEV 模型能否以四选一形式解答 GPQA Diamond 研究生级科学题。
2. [gsm8k](gsm8k/report/REPORT.zh.md) — 【小学数学】测试 JEV 模型能否以四选一形式解答 GSM8K 小学数学应用题。
3. [mmlu-pro](mmlu-pro/report/REPORT.zh.md) — 【多学科知识】测试 JEV 模型能否以十选一为主的选择题形式解答 MMLU-Pro 覆盖 14 个学科的题目。

## 二、LLM benchmark：社会常识与偏见

1. [bbq](bbq/report/REPORT.zh.md) — 【偏见敏感问答】测试 JEV 能否答对 BBQ 偏见敏感三选一问答题，且不偏向刻板印象方向选项。
2. [socialiqa](socialiqa/report/REPORT.zh.md) — 【社会常识】测试 JEV 能否以三选一形式解答 SocialIQA 社会常识题，并检验其 confidence 能否标记可信作答。

## 三、论文问答系统

1. [paper-classification](paper-classification/report/REPORT.zh.md) — 【论文库管理】测试 JEV 能否判断一篇 arXiv 论文该不该收入遵循研究偏好的论文库，并归入正确的主题。
2. [paper-qa](paper-qa/report/REPORT.zh.md) — 【论文问答】测试 JEV 作为论文问答系统的快路径，判断论文片段是否支持某陈述的准确率。
3. [prompt-routing](prompt-routing/report/REPORT.zh.md) — 【入口路由】测试 JEV 能否仅凭提问文本，判断读者的提问该走 JEV 快路径还是 LLM 慢路径。

## 四、经典机器学习预测：回归与分类

1. [boston-housing](boston-housing/report/REPORT.zh.md) — 【房价估计】测试 JEV 能否把波士顿社区房价钉在绝对刻度上（价格档评分），以及能否可靠地排出相对高低（两两比较）。
2. [titanic](titanic/report/REPORT.zh.md) — 【二分类】测试 JEV 能否根据乘客记录判断泰坦尼克号乘客是否生还，并对比结构化字段与自然语言文本两种输入表示的准确率、成本与置信行为。

## 五、LLM 后训练标注

1. [dpo-jev-judge](dpo-jev-judge/report/REPORT.zh.md) — 【裁判一致性】测试 JEV 能否在两条同题思考中选出与 LLM 裁判偏好相同的一条。
2. [grpo-jev-judge](grpo-jev-judge/report/REPORT.zh.md) — 【裁判一致性】测试 JEV 能否在同一题目的八条思考中选出与 LLM 裁判相同的最优者。

## 六、技能路由

1. [skill-routing](skill-routing/report/REPORT.zh.md) — 【技能路由】测试 JEV 能否把用户任务路由到 126 个真实 Agent Skill 中的正确技能、技能组合或 none。
