---
title: "Semantic Router (aurelio-labs)（同范式对照）"
updated: 2026-10-09
---

# Semantic Router (aurelio-labs)（同范式对照）

【定位】Semantic Router 是 aurelio-labs 的开源项目，自称"LLM 的超快决策层"，早于 Jev 一代，作为同范式对照条目收录：目标同为给 LLM 应用提供低延迟决策，路径是嵌入与相似度，而非类型化概率答案。在 Jev 以校准概率回答类型化问题之处，Semantic Router 以编码器相似度将输入匹配到对应路由。它是与 Jev 低延迟决策层定位最接近的开源对照实现。

【功能】路由与工具决策在语义向量空间中完成，而非让 LLM 生成文本。用法是定义 Route、选择 Encoder，RouteLayer 在几十毫秒内返回匹配的路由（项目自报）。开箱支持本地模型、多模态输入与阈值优化。

【特点】项目当前正进行 1.x 重写，API 可预期出现一定变动。

【适用】适合延迟敏感的路由与工具选择负载，可作为评估决策层时"Jev 之前"的对照点；与 Jev 对照阅读可框出决策层的设计空间。项目处于 1.x 重写期，对 API 稳定性有要求的接入需注意变动风险。

## Links

- [GitHub – aurelio-labs/semantic-router 仓库](https://github.com/aurelio-labs/semantic-router)
- [Docs – aurelio.ai 上的 Semantic Router 文档](https://aurelio.ai/semantic-router)
