---
title: "Tev1 (Together AI)"
updated: 2026-10-09
---

# Tev1 (Together AI)

【定位】Together AI 的开源决策权重：基于 Qwen3.5 的 4B 与 0.8B LoRA 适配器，随官方博客文章《Train your own Jev for $17》一并发布，权重与教程出自同一公告。以 17 美元的训练成本复现最小 Jev 式系统是其核心主张。

【功能】范围有意收窄：仅支持 choice 型决策，从 2 至 24 个候选中选出一个选项，不覆盖 score 与 noul 两类问题，这一点与 Jev 及本目录中其他开源替代不同。4B 与 0.8B 两个规模覆盖小规模硬件区间。除自托管开源权重外，也在 Together 的 serverless 平台提供托管服务，托管价格 $0.042/百万 token。

【特点】配套博客记录了从小底座训练决策模型的完整过程与逐项成本构成，$17 为复现最小可用系统的训练开销。对混合负载而言，约束在狭窄的接口能力而非成本。它可作为自训决策模型的参考配方与成本演示，而非 Jev 的直接替代品。

【适用】适合想以小底座起步、自行训练决策模型并核算训练预算的团队，可按博客流程对照复做；serverless 路线可用来估算这些适配器在 Together 的托管成本。问题类型仅 choice 一种，混合 choice/score/noul 的负载无法直接用其替代 Jev。

## Links

- [GitHub – 权重与训练配方](https://github.com/togethercomputer/tev1)
- [Blog – Train your own Jev for $17](https://www.together.ai/blog/how-to-train-your-own-jev)
