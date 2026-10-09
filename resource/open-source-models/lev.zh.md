---
title: "Lev (Interfaze AI)"
updated: 2026-10-09
---

# Lev (Interfaze AI)

【定位】Lev 是 Interfaze AI 的开源 System One 决策模型，并附带一套评测 harness。

【功能】它是基于 Qwen3.5-4B 的 LoRA 适配器，从已算出的 logits 直接读出概率，输出 token 数为零，在给定选项上返回校准概率。wire 协议为 TypeSafe 的 `/v1/systemone`，改 base URL 即可复用现有客户端。自带 levbench，测量准确率、log loss、Brier、ECE、选择性准确率、p50 延迟、成本与 schema 重试，并附 Snake 演示。

【特点】代码与权重为 Apache-2.0，部分训练数据集另有非商用条款。项目自报全部 13 个 S1Bench 子集上 68.9%，平均 ECE 0.115（Jev 为 0.091），在 13 个子集中有 5 个优于 Jev。引擎计算在 H100 上短请求 69ms，经 Modal 端到端 414–654ms。训练用 20 万条 × 3 epoch，H100 约 7.8 小时。llama.cpp 官方有 `ggml-org/lev-GGUF`（约 36ms/问，据 llama.cpp 官方博客）。采用度低：GitHub 16 stars，自 2026-09-24 起，资料完整。

【适用】适合需要概率输出与校准指标、并希望用同一套 harness 做同类比较的团队，也适合可接受小型早期项目的场景；TypeSafe 兼容端点意味着现有客户端只需改 base URL。采用度低且部分训练数据非商用，生产使用前应核对许可条款与项目成熟度。需要生成文本的任务不适用。

## Links

- [GitHub – 源码与 levbench](https://github.com/InterfazeAI/lev)
- [HF – 模型权重](https://huggingface.co/interfaze-ai/lev)
- [HF – ggml-org lev-GGUF](https://huggingface.co/ggml-org/lev-GGUF)
