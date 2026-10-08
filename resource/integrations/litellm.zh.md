---
title: "LiteLLM Jev Support"
updated: 2026-10-09
---

# LiteLLM Jev Support

【定位】LiteLLM 网关对 Jev 的集成，把直接决策调用与请求链路内的上下文管理放进同一个代理。

【功能】自 v1.103.0-rc 起，一个 pass-through 端点将请求代理到 `/typesafe/v1/systemone`，已以 LiteLLM 为网关的部署无需新增基础设施即可调用 Jev；经此路由的请求自动继承网关的日志、预算与成本追踪能力，Jev 用量按模型 ID `typesafe/jev-1.13.0` 记账。另一项「相关性压缩」guardrail 由 Jev 判定对话中哪些工具结果已经过期，并用一段简短提示替换，在上下文送入模型之前完成裁剪；它与 LiteLLM 其余 proxy guardrail 一起配置。

【特点】pass-through 文档覆盖端点配置，博客文章宣布并说明这项集成。决策调用与 guardrail 共用同一代理，Jev 开销与其他 provider 在同一位置可见。

【适用】适合已部署 LiteLLM、要把 Jev 纳入统一日志与成本治理的团队，以及需要在推理前裁剪过期工具结果的对话管线。未使用 LiteLLM 的部署需先引入该网关，才能获得上述接入路径。

## Links

- [Blog – TypeSafe Jev 支持](https://docs.litellm.ai/blog/typesafe_jev)
- [Docs – TypeSafe pass-through 端点](https://docs.litellm.ai/docs/pass_through/typesafe)
- [Docs – TypeSafe guardrail](https://docs.litellm.ai/docs/proxy/guardrails/typesafe)
