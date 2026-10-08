---
title: "OpenAI Decisions API（GPT-6 Luna）"
updated: 2026-10-09
---

# OpenAI Decisions API（GPT-6 Luna）

【定位】Decisions API 是 OpenAI 进军类型化决策推理的产品，DevDay 2026 预览，2026 年 10 月 6 日进入公开 beta。它沿用 Jev 开创的“state + 类型化问题输入、结构化决策输出”范式，是本目录中与 Jev 最直接对应的大厂产品。

【功能】服务只暴露一个端点 `POST /v1/decisions`，目前唯一的模型是 `gpt-6-luna`。请求中的 state 可同时混合文本与图像，API 返回结构化决策而非自由文本，不提供自由生成模式。模型另以 `gpt-6-luna-decisions` 之名上架 OpenRouter，与 Jev 的 `typesafe/jev-1.13` 并列。

【特点】闭源，仅提供托管服务，无自托管路径。输入定价为每百万 token $0.10，是 Jev 输入价的两倍以上。OpenAI 官方称类型化决策比通用模型调用快至 10 倍，并表示正式版（GA）将在“数周内”上线；这两个数字与时间表均为厂商说法，此处未经独立验证。

【适用】适合已在 OpenAI 生态内、希望获取结构化决策输出的团队，尤其是 state 需要同时混合文本与图像的请求。不适合需要自托管、权重私有化或多模型可选的部署；服务仍处公开 beta、目前只有一个模型，正式版时间表以厂商口径为准。

## Links

- [Decisions API 公开 beta 公告 – OpenAI Community](https://community.openai.com/t/decisions-api-is-now-available-in-public-beta/1403877) (Official announcement)
- [gpt-6-luna-decisions – OpenRouter](https://openrouter.ai/openai/gpt-6-luna-decisions) (Docs)
- [OpenAI 上线 Decisions API 公开 beta – AI Weekly](https://aiweekly.co/alerts/openai-launches-decisions-api-public-beta-on-gpt-6-luna) (News)
