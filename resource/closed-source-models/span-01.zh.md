---
title: "Span-01（Respan）"
updated: 2026-10-09
---

# Span-01（Respan）

【定位】Respan（原 Keywords AI）的专有推理分类器，2026 年 9 月 24 日发布，面向 AI agent traces 的行为检测，即判断以自然语言描述的行为是否出现在某条 trace 中（官方博客）。

【功能】对每个用自然语言定义的行为，模型一次性返回 present / absent / not_observable 三类概率，覆盖同一 trace 上的多个行为，每个行为一个概率：present 表示行为出现，absent 表示未出现，not_observable 表示在该 trace 中无法判断。它是真实单次前向传播，而非逐 token 生成，概率由该次传播直接给出；训练上先用 RLAIF 训练通用分类推理再专化，并使用混合注意力以在长 trace 中保留推理（官方）。定价为输入 $0.02/1M tokens、输出免费；变体 Span-01 Lite 免费（官方）。无权重、无 license、无仓库。

【特点】官方自报：Overall behavior F1 为 84.3，对比 GPT-6 Luna 的 81.5、Jev 1.13.0 的 71.5；Production behavior 综合 0.806，对比 Jev 的 0.716、Sonnet 5 的 0.719、GPT-6 Sol 的 0.885，后者为四者中最高。

【适用】适合替换 LLM-as-a-judge，用于生产 trace 的安全、可靠性、grounding、响应质量检测，且每个行为以自然语言定义、需要以概率而非生成标签作答；资料较新，属较早阶段。

## Links

- [Introducing Span-01 – Respan 博客](https://www.respan.ai/blog/introducing-span-1) (Blog)
- [Span-01 – OpenRouter](https://openrouter.ai/respan/span-01) (Gateway)
