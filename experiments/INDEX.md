# Experiments

*English | [简体中文](INDEX.zh.md)*

Thirteen experiments on the JEV decision model, grouped by what they probe. Each entry links to its report.

## 1. LLM Benchmarks: Academic Ability

1. [gpqa-diamond](gpqa-diamond/report/REPORT.md) — 【Graduate-Level Science】Can JEV answer GPQA Diamond graduate-level science questions in four-choice form?
2. [gsm8k](gsm8k/report/REPORT.md) — 【Grade-School Math】Can JEV solve GSM8K grade-school math word problems posed as four-choice questions?
3. [mmlu-pro](mmlu-pro/report/REPORT.md) — 【Multi-Discipline Knowledge】Can JEV answer MMLU-Pro college-level questions across 14 disciplines, mostly in ten-choice form?

## 2. LLM Benchmarks: Social Commonsense and Bias

1. [bbq](bbq/report/REPORT.md) — 【Bias-Sensitive QA】Does JEV answer BBQ's bias-sensitive three-choice questions correctly without leaning toward stereotype-aligned options?
2. [socialiqa](socialiqa/report/REPORT.md) — 【Social Commonsense】Can JEV answer SocialIQA social commonsense questions in three-choice form, and does its confidence mark trustworthy answers?

## 3. Paper QA System

1. [paper-classification](paper-classification/report/REPORT.md) — 【Paper Library Management】Can JEV decide whether an arXiv paper belongs in a personal research library and which topic of the research preference it falls under?
2. [paper-qa](paper-qa/report/REPORT.md) — 【Paper QA】Can JEV, as the fast path of a paper-QA system, judge whether a paper excerpt supports a statement?
3. [prompt-routing](prompt-routing/report/REPORT.md) — 【Prompt Routing】Can JEV decide from the question text alone whether a reader's question should go to the JEV fast path or the LLM slow path?

## 4. Classical Machine Learning Prediction: Regression and Classification

1. [boston-housing](boston-housing/report/REPORT.md) — 【Housing Prices】Tests whether JEV can place Boston suburb housing prices on an absolute scale (price-band scoring) versus order them relatively (pairwise comparison).
2. [titanic](titanic/report/REPORT.md) — 【Binary Classification】Can JEV judge whether a Titanic passenger survived, and does rendering the record as prose instead of structured fields change accuracy, cost, or confidence behavior?

## 5. LLM Post-Training Annotation

1. [dpo-jev-judge](dpo-jev-judge/report/REPORT.md) — 【Judge Agreement】Can JEV pick the better of two thinking traces, matching an LLM judge's preference?
2. [grpo-jev-judge](grpo-jev-judge/report/REPORT.md) — 【Judge Agreement】Can JEV pick the same best thinking trace as an LLM judge among eight rollouts of one open-ended reasoning question?

## 6. Skill Routing

1. [skill-routing](skill-routing/report/REPORT.md) — 【Skill Routing】Can JEV route user tasks to the right skill, skill set, or none, among 126 real agent skills?
