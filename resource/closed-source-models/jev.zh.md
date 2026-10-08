---
title: "Jev（TypeSafe AI）"
updated: 2026-10-09
---

# Jev（TypeSafe AI）

【定位】TypeSafe AI 的旗舰闭源决策模型，2026 年 9 月 15 日发布，也是“System One”品类的开创者，并作为本仓库实验的参考模型。它不做文本生成：输入 state 与类型化问题，输出带校准概率的类型化答案，零输出 token。

【功能】请求由一个 state 加类型化问题组成，问题限 Choice / Score / Noul 三种原语（分别对应选择、评分与无选项判断），模型返回对应的类型化答案与校准概率，不产生任何文本。接入以 OpenRouter 为主，模型 ID 为 `typesafe/jev-1.13`，另有移动别名 `~typesafe/jev-latest`；直连 API `api.typesafe.ai/v1/systemone` 于 2026 年 9 月 27 日重新开放注册，另经 Vercel AI Gateway 与 Cloudflare Workers AI 分发。

【特点】训练方法为 RLCD（Reinforcement Learning for Calibrated Decisions），权重专有、未发布。定价为每百万输入 token $0.042，输出免费，上下文窗口 32K。同门产品 Jev Router 用 Jev 选择模型与推理力度，提供 1M token 上下文。

【适用】适合需要类型化、可校准的结构化决策而无须文本生成的场景，如选择、评分、无选项判断类任务，可经 OpenRouter 等既有渠道接入。不适合开放式文本生成任务；只回答三种原语之上的类型化问题；32K 上下文限制了单次请求可携带的 state 规模。

## Links

- [TypeSafe AI 官网](https://typesafe.ai/) (Website)
- [System One 概念 – TypeSafe 文档](https://docs.typesafe.ai/concepts/system-one) (Docs)
- [Introducing System One models and Jev – TypeSafe 博客](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (Blog)
- [Jev 使用指南 – OpenRouter 文档](https://openrouter.ai/docs/guides/community/jev) (Docs)
