---
title: "NeoHorse-Jev-4B (TokenRhythm)"
updated: 2026-10-09
---

# NeoHorse-Jev-4B (TokenRhythm)

【定位】NeoHorse-Jev-4B 是 TokenRhythm（开源框架 NeoHorse 团队）的 prefill-only 决策模型，面向需要决策而非生成文本的 agent 工作流。

【功能】给定 state 与调用方定义的问题，它不做自回归生成，直接预测决策与概率，用于路由请求、选工具、判条件、评结果；支持文本与单张图片输入。提供原生端点 `/v1/decision`、System One 风格端点 `/v1/systemone` 与 `/health`，可在 vLLM、SGLang 或本地 runtime 部署，也提供 GGUF 与 ModelScope 镜像。

【特点】Apache-2.0；底座为 NeoHorse-1-4B（Qwen3.5-4B 派生），2026-09-23 发布。项目自报 JevBench 公开 231 题 75.32% 逐例准确率、100% 合法输出格式；Nimble、VitaminC、MASSIVE 三项均值 83.26%，比基座高 11.50 个百分点；六项文本基准组 77.70，官方称在四家完整结果的开源决策模型中最高（综合分由厂商汇总，跨模型对比按自报对待）。第三方报道称 32 并发下平均 74.3ms。GitHub 1.6k stars。

【适用】适合需要在一次前向内完成路由、工具选择、条件判断或结果评分、且不生成文本的 agent 流水线，包括在 vLLM、SGLang 上部署以及通过 GGUF 本地使用。由于 head 综合分由厂商汇总，跨模型对比需谨慎，依赖前应在目标任务上验证。

## Links

- [GitHub – NeoHorse 框架与模型](https://github.com/TokenRhythm/NeoHorse)
- [HF – NeoHorse-Jev-4B 权重](https://huggingface.co/TokenRhythm/NeoHorse-Jev-4B)
