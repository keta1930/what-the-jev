---
title: "LangChain langchain-typesafe"
updated: 2026-10-09
---

# LangChain langchain-typesafe

【定位】这是一个 Agent 评估基准实验项目，测试决策模型 Jev 作为评测裁判，能否兼顾代码规则的可靠性与 LLM 裁判的开放性。

【功能】项目构建了带 Tavily 搜索的天气 Agent 并冻结五条运行轨迹；让各裁判对同一轨迹重复评测百次，量化二元准确率、评分方差、成本与延迟四项指标；以人工标注作为 oracle 校验准确率；支持本地运行与 LangSmith 实验上传，数据与图表完整可复现。LangChain 同步发布了 langchain-typesafe 集成包（含 TypeSafeClassifier 等）。

【特点】Jev 并非自回归 LLM，而是对结构化状态返回带概率的类型化判定（Noul、Score、Choice），决策优先设计带来更低方差与延迟。实验中其准确率达 100%，方差比 LLM 裁判低 92 至 913 倍，单次成本约 0.00035 美元、延迟 0.44 秒（以上数字为实验方自报，未经第三方验证），基于 Python 与 LangSmith 构建。

【适用】适合需要高频、低成本评测的 Agent 工程师与评估团队，可用于回归检测、轨迹反馈与开发迭代加速。注意实验仅基于五条运行轨迹和一位人工标注者，结论不宜推广为裁判通用排名，也不适合作为大规模通用评测基准。

## Links

- [Blog – Jev agent evals（LangSmith）](https://langchain.com/blog/jev-agent-evals-langsmith)
- [GitHub – danielgshea/jev-as-a-judge](https://github.com/danielgshea/jev-as-a-judge)
