---
title: "Vercel AI Gateway & AI SDK"
updated: 2026-10-09
---

# Vercel AI Gateway & AI SDK

【定位】Vercel 平台对 Jev 的接入：AI Gateway 托管 `typesafe-ai/jev`，AI SDK 与 Vercel 自家 agent 框架提供上层调用与评估入口。

【功能】AI Gateway 以 `typesafe-ai/jev` 为 ID 提供 Jev，支持 Zero Data Retention。AI SDK 7 通过实验性的 `evaluate` API 暴露该模型，其中 Boolean 评估对应 Jev 的 Noul 问题类型。Vercel 的 agent 框架 eve 将 Jev 设为五项功能的默认评估器，用决策调用取代提示词式的 LLM 判断。changelog 条目记录了模型可用性与 Zero Data Retention 选项。

【特点】据 Vercel 官方博客（厂商自报、未经独立测量），Jev 是 AI Gateway 历史上被采用最快的模型，上线 24 小时内即有 13% 的付费团队在用。对已基于 AI SDK 构建的开发者，Jev 是原生选项而非额外依赖。

【适用】适合在 Vercel 平台或 AI SDK 生态内构建、需要以原生方式接入决策模型的团队，以及采用 eve 框架的 agent 项目。采用数据来自厂商自报；`evaluate` API 处于实验阶段，需关注其后续变化。

## Links

- [Docs – typesafe-ai/jev 上线 AI Gateway](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)
- [Blog – AI Gateway Jev 模型发布](https://vercel.com/blog/ai-gateway-jev-model-launch)
