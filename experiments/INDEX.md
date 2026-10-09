# Experiments

*English | [简体中文](INDEX.zh.md)*

Thirteen experiments on the JEV decision model, grouped by what they probe. Each entry links to its report.

## 1. LLM Benchmarks: Academic Ability

1. [gpqa-diamond](gpqa-diamond/report/REPORT.md) — Explore JEV's performance on GPQA Diamond graduate-level science questions.
2. [gsm8k](gsm8k/report/REPORT.md) — Explore JEV's performance on GSM8K grade-school math word problems.
3. [mmlu-pro](mmlu-pro/report/REPORT.md) — Explore JEV's performance on MMLU-Pro college-level questions across 14 disciplines.

## 2. LLM Benchmarks: Social Commonsense and Bias

1. [bbq](bbq/report/REPORT.md) — Explore JEV's performance on BBQ's bias-sensitive questions, and whether it leans toward stereotypes.
2. [socialiqa](socialiqa/report/REPORT.md) — Explore JEV's performance on SocialIQA social commonsense questions.

## 3. Paper QA System

1. [paper-classification](paper-classification/report/REPORT.md) — Explore whether JEV can decide, based on a research preference, whether an arXiv paper belongs in a paper library, and which topic it falls under.
2. [paper-qa](paper-qa/report/REPORT.md) — Explore whether JEV can answer questions about a paper based on its own text.
3. [prompt-routing](prompt-routing/report/REPORT.md) — Explore whether JEV can decide from the question text alone whether a question in paper QA goes to the JEV fast path or the LLM slow path.

## 4. Classical Machine Learning Prediction: Regression and Classification

1. [boston-housing](boston-housing/report/REPORT.md) — Explore whether JEV can predict Boston suburb housing prices, and compare price levels across suburbs.
2. [titanic](titanic/report/REPORT.md) — Explore whether JEV can predict whether a Titanic passenger survived from the passenger record, and compare structured fields with prose text.

## 5. LLM Post-Training Annotation

1. [dpo-jev-judge](dpo-jev-judge/report/REPORT.md) — Explore JEV's performance on preference annotation for DPO training data.
2. [grpo-jev-judge](grpo-jev-judge/report/REPORT.md) — Explore JEV's performance on GRPO trajectory reward assignment.

## 6. Skill Routing

1. [skill-routing](skill-routing/report/REPORT.md) — Explore whether JEV can route user tasks to the right skill, skill set, or none, among 126 real agent skills.
