---
title: "Cloudflare Workers AI: typesafe/jev"
updated: 2026-10-09
---

# Cloudflare Workers AI: typesafe/jev

【定位】Cloudflare Workers AI 模型目录中的 Jev 托管条目，模型直接运行在 Workers AI 内部，而非经外部网关接入。

【功能】接入只需一次 `env.AI.run()` 调用，直发 state 与 questions，无需另行接入网关或 API key；作为目录内置模型，它与 Workers AI 的其余模型并列，共享同一调用路径。模型页附四个完整的请求/响应示例，覆盖退款审核、部门路由、账户风险评分等场景，每个示例展示从请求体到类型化答案的完整往返，可直接当作起点而不必自行反推格式。

【特点】规格据 Cloudflare 模型页：32k 上下文窗口、零数据保留、输入价格 $0.042/1M token。注意区分：Cloudflare 另有自研开源决策模型 Clef（收录于另一条目），Workers AI 上的 `typesafe/jev` 是 Cloudflare 服务的 Jev，并非 Clef。

【适用】适合运行在 Cloudflare Workers 生态内、要在应用中直接获得决策能力的场景，页面示例可兼作请求格式参考。该路径绑定 Workers AI 的调用方式，其他环境的部署需另选接入渠道。

## Links

- [Docs – typesafe/jev 模型页](https://developers.cloudflare.com/ai/models/typesafe/jev/)
