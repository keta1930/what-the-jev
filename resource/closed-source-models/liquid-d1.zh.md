---
title: "Liquid d1（Liquid AI）"
updated: 2026-10-09
---

# Liquid d1（Liquid AI）

【定位】Liquid AI 于 2026 年 9 月 29 日发布的闭源决策模型族，采用与 Jev 相同的类型化决策接口：输入 state 加 Choice / Score / Noul 问题，输出带校准概率的类型化答案，零输出 token。整个系列与 Jev 的关系是接口级兼容，可在其既有位置替换使用。

【功能】系列实现 System One 端点契约，与 TypeSafe SDK 兼容，在已有工程中从 Jev 切换只需改 base URL、无需任何其他代码改动。共含三个托管模型：旗舰 d1 经 `api.liquid.ai/decisions/v1/systemone` 提供服务，设有名为 `d1:free` 的免费档；d1-3B 基于 LFM2.5-VL-3B 底座，接受文本与图像 state；d1-omni-600M 是三者中最小的，接受文本、图像与音频 state。

【特点】三个变体均闭源、仅限 Liquid AI 托管，权重未公开，也没有自托管路径。各变体模态覆盖不同，文本 / 图像 / 音频支持需逐模型确认。免费档之外的托管条款完全由 Liquid AI 单方面决定。

【适用】适合已使用 TypeSafe SDK、希望以最小改动更换决策模型的场景，以及 state 含图像或音频的任务。不适合自托管、权重私有化或需要自定托管条款的部署；图像与音频支持取决于所选变体，需逐模型核对。

## Links

- [决策模型 – Liquid AI 文档](https://docs.liquid.ai/lfm/models/decision-models) (Docs)
- [Liquid AI 发布 d1：零输出 token 的决策模型 – MarkTechPost](https://www.marktechpost.com/2026/09/29/liquid-ai-releases-d1-a-decision-model-that-returns-calibrated-probabilities-with-zero-output-tokens/) (News)
- [d1 – Vercel AI Gateway](https://vercel.com/ai-gateway/models/d1) (Docs)
