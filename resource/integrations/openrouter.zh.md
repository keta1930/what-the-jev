---
title: "OpenRouter Jev Hub"
updated: 2026-10-09
---

# OpenRouter Jev Hub

【定位】OpenRouter 托管的 Jev（TypeSafe AI「System One」决策模型）入口，集中提供该模型的公开概念文档、官方教程与配套学习材料。

【功能】概念指南覆盖 Choice、Score、Noul 三种问题类型，说明 Jev 以校准概率返回类型化答案而非生成文本，并列出开发者可用的两个调用面：Decisions API（`POST /api/alpha/decisions`）与 System One API。官方教程从用 `curl` 发出第一次请求讲到如何解读响应中的概率，配有真实 API 响应示例。配套材料包括 SDK 指南、5 篇官方 cookbook，以及可在浏览器内交互体验的 Jev Lab。

【特点】文档内容更新至 2026-10-05。相关服务 Jev Router 用 Jev 本身为请求挑选模型与推理档位，支持最多 1M token 的上下文（官方文档数据）。

【适用】适合已通过 OpenRouter 调用其他模型、要在同一技术栈内接入 Jev 的团队，也适合首次接触 Jev 概念与 API 的开发者作为学习起点。文档为静态资料，反映 2026-10-05 时点的状态，此后的接口变化需以平台最新页面为准。

## Links

- [Docs – Jev 指南](https://openrouter.ai/docs/guides/community/jev)
- [Docs – Jev 教程](https://openrouter.ai/docs/guides/community/jev-tutorial)
- [Blog – What is Jev?](https://openrouter.ai/blog/insights/what-is-jev/)
