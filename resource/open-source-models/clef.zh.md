---
title: "Clef / Clef-flash (Cloudflare)"
updated: 2026-10-09
---

# Clef / Clef-flash (Cloudflare)

【定位】Cloudflare Workers AI 团队自训的两个决策模型 Clef 与 Clef-flash，于 2026-10-01 Birthday Week 期间发布。Clef 为两者中较大者：27B，基于 Qwen3.8 底座；Clef-flash 为 9B，基于 Qwen3.5 底座。两个规模均提供两种获取方式：既可将 Apache-2.0 开源权重下载自托管，也可经 Workers AI 商业托管调用，托管线上跑的就是这两个开源模型。

【功能】两个模型共用同一套训练配方：冻结主干，叠加 LoRA 适配器与一个两阶段注意力路由头。内置视觉编码器，因此除文本外同样支持图片输入。上下文窗口 64K，是 Jev 32K 的两倍，并且与 Jev API 完全兼容。

【特点】Cloudflare 官方基准成绩属自报：称在 Jev Decision Index 上居首，并在 Jev 自有评测的四项中赢下三项。引用这类数字时应注明来源为官方自报，并核对对应的榜单版本。托管价格 $0.24/百万输入 token 来自第三方页面的标注，在 Cloudflare 自身材料中未见确认，属第三方转述数字。

【适用】适合需要图片输入、64K 上下文窗口，或需要自托管同时保持 Jev API 兼容的负载：开源权重让 Jev 用户以两倍上下文自托管一个兼容模型；托管路线则运行在 Workers AI 上，无需自建推理设施。与 Jev 的对比成绩均为厂商自报，与 Jev 或其他开源决策模型直接对比时，应逐一注明每个数字的来源。

## Links

- [Blog – 发布文章](https://blog.cloudflare.com/clef-decision-models/)
- [Docs – Workers AI 更新日志](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/)
