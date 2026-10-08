---
title: "Perplexity Decisions API (pplx-decider-v1-27b)"
updated: 2026-10-09
---

# Perplexity Decisions API (pplx-decider-v1-27b)

【定位】Perplexity 推出的多模态决策模型（模型 ID pplx-decider-v1-27b），2026-10-01 上线 api.perplexity.ai/v1/decisions，基于 Qwen3.8-27B 微调。权重以 Apache-2.0 开源，同时提供商业托管 API，两条路线为同一微调版本。

【功能】请求携带 state（文本或图片）与最多 128 个问题，全部问题在同一次调用内作答，262K 长上下文可容纳长文档。开源权重发布于 Hugging Face，可自托管、可审计，不必只作为端点调用；v1.1（约 2026-10-05 发布）将输入价格从 $0.04 降至 $0.02/百万 token，此前版本的调用按较高价格计费。

【特点】官方自报评测：在一个 11 项测试的面板上得 85.71%，Jev 为 84.51%，两者差距不足一个百分点，发布报道即以这一差距作为标题结论。发布材料未引用第三方复现，对比数字需按官方自报对待。

【适用】适合需要多模态输入（含图片）、262K 长上下文且希望自托管权重的决策场景，也适合单次调用问题数多（最多 128 个）的负载。托管与自托管为同一微调版本，选择改变的是运维方式而非模型，也可两者并行运行对比。若以与 Jev 的对比数字为选型依据，需注意其来源为官方自报、且未获第三方复现，差距也不足一分。

## Links

- [Docs – OpenRouter 模型页](https://openrouter.ai/perplexity/pplx-decider-v1-27b)
- [Docs – 概览与用法](https://vercel.com/i/what-is-perplexity-decisions-api)
- [News – 发布报道](https://aiweekly.co/alerts/perplexity-open-sources-27b-decider-edges-jev-on-11-test-panel)
