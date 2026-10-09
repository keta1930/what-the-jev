---
title: "Solar Decide（Upstage）"
updated: 2026-10-09
---

# Solar Decide（Upstage）

【定位】Upstage 于 2026 年 9 月 22 日发布 Beta 的结构化决策模型，以 System One 端点形式提供，构建在 Solar Mini 4 之上（官方）。它属于 Jev 开创的 System One 品类，与 Jev 使用同一 `/v1/systemone` 请求 schema，输入 state 与类型化问题，返回 choice、score 或 yes/no 答案。

【功能】模型返回的答案只有 choice、score、yes/no 三类，每个答案都带直接取自模型的校准概率，而不是写成文本；模型不生成散文，每个决策只做一次前向传播，输出 token 免费。上下文窗口为 512K，整份文档可作 state，并承接 Solar Mini 4 的韩语能力（官方）。定价以 Upstage Console 为准：输入 $0.1/1M tokens、缓存输入 $0.1/1M、输出免费；OpenRouter 路由显示输入 $0.05/1M、输出 $0（网关自报）。另有更快的变体 Solar Decide Flash，OpenRouter 记录其发布日期为 2026-10-08。

【特点】权重闭源，仅经 Upstage Console 一个平台提供服务，没有其他托管渠道；该 API 的隐私标注为 Data not collected（官方）。

【适用】适合 routing、classification、policy checks，以及 state 为长文档或韩文的场景；不适合需要生成自由文本的任务，因为模型只返回 choice、score、yes/no 三类类型化答案。

## Links

- [Solar Decide – Upstage Console 文档](https://console.upstage.ai/docs/models/solar-decide) (Docs)
- [Upstage 模型 – OpenRouter](https://openrouter.ai/upstage) (Gateway)
- [Rate limits – Upstage Console 文档](https://console.upstage.ai/docs/guides/rate-limits) (Docs)
