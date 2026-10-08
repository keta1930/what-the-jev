---
title: "decider (Mapika)"
updated: 2026-10-09
---

# decider (Mapika)

【定位】Mapika 推出的 System One 式开源决策模型家族，代码、权重与完整训练配方公开，许可证为 Apache-2.0。问题类型与 Jev 一致，覆盖 choice、score、noul 三类，即 Jev 所回答的三种类型。

【功能】模型单次前向传播即可输出 Choice/Score/Noul 三类答案的概率分布。RL 阶段直接以对数评分（log scoring）优化校准，校准温度作为独立体系维护，而非并入模型权重。训练配方为 95 个公开数据集的混合，完整公开，可按配方复现训练。

【特点】家族规模从 0.8B 到 35B-A3B，包含 Gemma-4-12B 与 Gemma-4-31B 变体，并提供随主检查点一同发布的 GGUF、NVFP4 与 NPU 移植版本，把同一家族延伸到占用更小的硬件。据项目公布结果（官方自报）：JevBench v1.5.2 上 decider-4b v2 列 #7/99（Jev 本体为 #3），Decision Index 上 decider-chat-gemma4-31b 列 #2/70（ECE 0.047）；基准结果表保存在仓库的 RESULTS.md。项目仍在持续开发，2026-10-07 仍在发版。

【适用】适合需要自托管、问题类型与 Jev 一致、且要覆盖多种硬件目标（含量化与 NPU 部署）的团队。其在 JevBench v1.5.2 上的成绩位居 99 名中的前十，但仍低于 Jev 本体（#3），以该榜为选型基准时需注意。

## Links

- [GitHub – 源码与训练配方](https://github.com/Mapika/decider)
- [HF – decider-4b 权重](https://huggingface.co/Mapika/decider-4b)
- [Docs – RESULTS.md 基准结果表](https://github.com/Mapika/decider/blob/main/docs/RESULTS.md)
