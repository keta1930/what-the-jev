---
title: "Decision Index"
updated: 2026-10-09
---

# Decision Index

【定位】Decision Index 是面向类型化决策引擎的第三方基准，与 TypeSafe AI 无关联。被测引擎接收 state 加一组类型化 questions（带显式 criteria 的 choice 或 noul），对每个问题返回一个答案及每个选项的概率。

【功能】其 GitHub 仓库是完整的复现套件：可从锁定的公开数据源重建冻结题集，用任意引擎跑分（HTTP 引擎按 /v1/systemone 线格式通信，transformers 引擎对现成因果 LLM 单次前向打分），再用榜单官方评分器出分。在线榜单为 0.3 版，公开套件覆盖五个领域——Knowledge & Reasoning、Language Understanding、Retrieval & Classification、Tools & Automation、Arts & Human Taste——的 37 个基准，共约 11 万条请求；parity 测试可复现榜单参赛者（含 Jev）已公开的逐基准结果。另有排名图像模型的 Vision 板，Reasoning 板在计划中。

【特点】主排名 Full score = 20% 公开基准 + 50% 同技能私有测试 + 30% 新领域私有决策任务，大部分分数来自无人能针对性训练的测试；每个基准经机会校正与覆盖率调整。edition 0.1–0.3 可并行复现，模型重跑后条目随之变化。

【适用】适合需要横向对比类型化决策引擎的读者；配套的 Hugging Face 追踪器（multimodalart）另行逐条登记开源 Jev 复刻动态。跑分前需经复现套件从锁定的公开数据源重建题集；引用任何排名前请核对 edition 与日期。

## Links

- [GitHub – Decision Index 复现套件（apolinario）](https://github.com/apolinario/decision-index)
- [HF Space – Jev 复现追踪器（multimodalart）](https://huggingface.co/spaces/multimodalart/jev-reproductions-tracker)
