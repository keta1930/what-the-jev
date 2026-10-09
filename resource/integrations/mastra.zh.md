---
title: "Mastra Classifier"
updated: 2026-10-09
---

# Mastra Classifier

【定位】Mastra 的 Classifier 原语（`@mastra/core/classifier`），对任意 AI SDK 评测模型提出固定域问题并返回带概率的类型化答案；官方以 Jev 为核心示例（`@ai-sdk/typesafe-ai`）（Mastra 博客与文档）。它面向无需解析生成文本即可采取行动的判断。

【功能】在共享 state 上定义多个具名 choice/score/boolean 问题并一次性求值，所有问题对同一 state 求值，答案按问题名索引。配套组件有 `createClassifierScorer()`（把某问题映射为 0-1 scorer 分数并保留证据）、`ClassifierProcessor`（输入/输出内容护栏）、`ModelSelectionProcessor`（cost routing）与 workflow 的 `.classifier()` 步骤（官方 release 与文档）。经 `Mastra({ classifiers })` 注册，按 ID 引用。Classifier 只返回证据，阈值与阻断策略由应用持有（官方）。

【特点】时间线（第三方整理）：Classifier 2026-09-22 合入（#24458）、注册 #24738、ClassifierProcessor 2026-09-23（#24768）、`createClassifierScorer()` 见 `@mastra/core@1.70.0`（#24792）。官方自测：用 Jev 分类 78 条开源 issue（标题加正文），约 10 条与其人工判断一致，官方明示不适合需取证或多步推理的任务，可由 agent 先收集证据（官方自报）。

【适用】适合 Mastra agent 的 workflow 分支、tool approval、内容护栏与 evals（classifier-as-judge）；需要取证或多步推理的任务，宜先由 agent 收集证据再交 Classifier 求值。

## Links

- [Docs – Classifier reference](https://mastra.ai/reference/classifier/classifier)
- [Blog – Introducing classifiers with Jev](https://mastra.ai/blog/introducing-classifiers-with-jev)
- [Docs – Jev](https://mastra.ai/articles/jev)
