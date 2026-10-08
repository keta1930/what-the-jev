---
title: "LEAPERone Decisions API"
updated: 2026-10-09
---

# LEAPERone Decisions API

【定位】LEAPERone 是一个 OpenRouter 兼容网关，定位面向国内用户；其 Decisions API 将决策请求透传给上游的 Jev 模型。

【功能】Decisions API 提供 `POST /v1/decisions`，并保留 `/api/alpha/decisions` 作为别名，请求在别名 `~typesafe/jev-latest` 下透传给 Jev，按上游 usage 原价结算。端点路径与 OpenRouter 保持一致，把现有集成中的 `openrouter.ai` 换成 `api.leaper.one` 即可完成迁移，请求体无需改动。由于网关与 OpenRouter 兼容，为 OpenRouter Decisions API 编写的客户端库可以继续使用。

【特点】作为第三方网关，它位于客户端与上游模型之间，相比直连 OpenRouter 多一次转发。文档目前仅中文页面有效，英文页返回 404，非中文读者需借助翻译。

【适用】适合直连 openrouter.ai 不方便的国内团队作为直接替代，已按 OpenRouter 接口编写的集成与客户端库可低成本迁移。能直连 OpenRouter 时是否经此多一跳，需按网络与运维情况权衡。

## Links

- [Docs – Decisions API 参考（中文）](https://leaper.one/zh/docs/api-reference/decisions)
