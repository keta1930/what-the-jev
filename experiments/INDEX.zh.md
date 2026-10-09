# 实验

*[English](INDEX.md) | 简体中文*

十三个实验，按考察对象分组；每条链接到该实验的报告。

## 一、LLM benchmark：学科能力

1. [gpqa-diamond](gpqa-diamond/report/REPORT.zh.md) — 探索 JEV 在 GPQA Diamond 研究生级科学题上的表现。
2. [gsm8k](gsm8k/report/REPORT.zh.md) — 探索 JEV 在 GSM8K 小学数学应用题上的表现。
3. [mmlu-pro](mmlu-pro/report/REPORT.zh.md) — 探索 JEV 在 MMLU-Pro 覆盖 14 个学科的大学水平题目上的表现。

## 二、LLM benchmark：社会常识与偏见

1. [bbq](bbq/report/REPORT.zh.md) — 探索 JEV 在 BBQ 偏见敏感问答题上的表现，以及是否会偏向刻板印象。
2. [socialiqa](socialiqa/report/REPORT.zh.md) — 探索 JEV 在 SocialIQA 社会常识题上的表现。

## 三、论文问答系统

1. [paper-classification](paper-classification/report/REPORT.zh.md) — 探索 JEV 能否按研究偏好判断一篇 arXiv 论文该不该收入论文库，并归入正确的主题。
2. [paper-qa](paper-qa/report/REPORT.zh.md) — 探索 JEV 能否基于原文回答关于该论文的问题。
3. [prompt-routing](prompt-routing/report/REPORT.zh.md) — 探索 JEV 能否仅凭提问文本，判断提问该走 JEV 快路径还是 LLM 慢路径。

## 四、经典机器学习预测：回归与分类

1. [boston-housing](boston-housing/report/REPORT.zh.md) — 探索 JEV 能否预测波士顿社区的房价，并比较不同社区的房价高低。
2. [titanic](titanic/report/REPORT.zh.md) — 探索 JEV 能否根据乘客记录预测乘客是否生还，并比较结构化字段与自然语言文本两种输入下的表现。

## 五、LLM 后训练标注

1. [dpo-jev-judge](dpo-jev-judge/report/REPORT.zh.md) — 探索 JEV 在 DPO 训练数据偏好标注上的表现。
2. [grpo-jev-judge](grpo-jev-judge/report/REPORT.zh.md) — 探索 JEV 在 GRPO 轨迹奖励分配上的表现。

## 六、技能路由

1. [skill-routing](skill-routing/report/REPORT.zh.md) — 探索 JEV 能否把用户任务路由到 126 个真实 Agent Skill 中的正确技能、技能组合或 none。
