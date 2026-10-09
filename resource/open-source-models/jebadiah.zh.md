---
title: "Jebadiah (Frontier Infra)"
updated: 2026-10-09
---

# Jebadiah (Frontier Infra)

【定位】Jebadiah（Jeb）是 Frontier Infra 的开源 System One 风格决策模型：对每个类型化问题返回选项标签上的概率而非生成文本，调用方拿到的是自身选项上的分布，而不是改写后的回答。

【功能】一次前向传播回答 choice、noul、score 三类问题，提供 TypeSafe 兼容的 `POST /v1/systemone`、AINode 的 `POST /v1/decide` 与浏览器 playground。项目把 trainer、数据构造、评测与全部 run record 一并发布，便于追溯其评测结果；权重在 HF frontier-infra 集合，分为 27B、9B、4B 三档。

【特点】Apache-2.0；底座为 Qwen3.8-27B、Qwen3.5-9B、Qwen3.5-4B 的 chat 版（thinking 关闭），用 LoRA rank 16 / alpha 32 仅以公开数据训练。项目自报 headline 为 27B 78.95、9B-v2 73.93、4B-v2 72.49，评测为自建多套，含 Jevals 子集与 Nimble 324。27B 在 bf16 下需约 56 GB。采用尚早：GitHub 4 stars、26 commits。

【适用】适合希望连同权重一起拿到完整流水线（训练代码、数据构造、评测与 run record），或计划自行微调的团队，27B、9B、4B 三档可按硬件选择。项目处于早期、采用度低，用于生产前应先验证，并把 headline 数字视为厂商结果；27B 档还需约 56 GB 的 bf16 内存。需要生成文本的任务不适用。

## Links

- [GitHub – 源码与 run record](https://github.com/getainode/jebadiah)
- [HF – jebadiah-27b 权重](https://huggingface.co/frontier-infra/jebadiah-27b)
