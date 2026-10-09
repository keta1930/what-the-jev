---
title: "Nimble (Bespoke Labs)"
updated: 2026-10-09
---

# Nimble (Bespoke Labs)

【定位】Nimble 是 Bespoke Labs 推出的开放 Jev 替代，数据、模型与训练配方一并公开，属于一步式类型化文本决策模型。

【功能】单次请求给出 state 与由 enum、布尔字段构成的问题 schema，模型直接对候选答案 token 打分，返回所选答案及每个选项的概率，不产生推理输出。提示上限 8,192 token，choice 与 score 问题支持 2 至 26 个选项。项目提供 Jev 兼容的 `/v1/systemone` 服务，并公开数据与评测脚本；Nimble 也是 Ollama 0.35 首批发布的决策模型之一，用 `ollama pull nimble` 安装（Q8_0 约 9.53 GB）。

【特点】基于 Qwen3.5-9B 加 LoRA。项目自报在 324 条留出样本上与参考标签一致率 90.12%（292/324），基座为 66.36%，Jev 1.13.0 为 93.21%；Ollama 官方示例称 M5 Max 上平均每次决策 91ms（官方自报）。JevBench v1.2.8 列有 Bespoke Nimble 9B 一行。许可证按版本区分：Bespoke-Nimble-9B 为 Apache-2.0，Bespoke-Nimble-9B-v3 为 CC BY-NC 4.0（非商用）。GitHub 2.1k stars，最近提交 2026-10-05。

【适用】适合希望完整掌握数据、权重与训练配方，并在本地或自有服务上运行类型化决策的团队，Ollama 构建可降低部署成本。v3 权重为非商用许可，商业部署需先确认所用版本。模型只返回选项与概率、不生成解释，需要说明理由的任务不适用。

## Links

- [GitHub – 源码](https://github.com/bespokelabsai/nimble)
- [HF – Bespoke-Nimble-9B 权重](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B)
- [Blog – Ollama 支持 Jev 风格决策模型](https://ollama.com/blog/ollama-now-supports-jev-style-decision-models)
