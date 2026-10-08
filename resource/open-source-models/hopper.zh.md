---
title: "Hopper (hopit-ai)"
updated: 2026-10-09
---

# Hopper (hopit-ai)

【定位】hopit-ai 推出的单次前向传播决策服务器，配套发布 5 个模型。服务器代码开源，适配器许可按档位区分，采用前需先确认所用档位。

【功能】配套模型包括 Qwen3.5-4B LoRA 适配器的两条通用线（Hopper 与 Hopper-G），以及 Gemma-4-12B-it 的冻结、微调两个变体；12B 档与 4B 适配器并列，是比本目录中纯 LoRA 阵容更大的模型选项，冻结与微调两个变体分别对应原始底座与适配后的模型。答案先对选项字母做 softmax，再按答案类型逐个温度映射完成校准，使每种答案类型有各自的温度；超过 26 个选项的长菜单采用 tournament/embedding 两阶段方案，而非对所有候选一次 softmax。

【特点】JevBench v1.5.5 榜单上总分 67.5（#16）、校准轴 87.9，两个数字均出自该版榜单。许可证分档：服务器代码为 Apache-2.0；Hopper 与 Hopper-G 适配器因训练涉及 RACE 数据条款，仅限研究与演示用途；只有 Hopper 12B (trained) 适配器为 Apache-2.0。

【适用】适合评估与研究用途——如对比决策服务器或复现该基准——以及仅使用 12B trained 适配器的生产场景。受许可条款限制，Hopper/Hopper-G 的 4B 适配器不能用于生产业务；把服务器接入业务流量前，应先确认部署所用的是哪一个适配器档位。

## Links

- [GitHub – 决策服务器与适配器源码](https://github.com/hopit-ai/hopper)
- [HF – Hopper 适配器](https://huggingface.co/HopitAI/hopper)
- [HF – Hopper-G 适配器](https://huggingface.co/HopitAI/hopper-g)
