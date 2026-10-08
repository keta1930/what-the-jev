---
title: "JevK5 (allebee)"
updated: 2026-10-09
---

# JevK5 (allebee)

【定位】allebee 项目的开源决策模型，将蒸馏 LoRA 与 SemIf 式选项字母 logit 读取结合，回答过程零生成 token。代码与权重均为 Apache-2.0，并明确致谢读取方法源自 SemIf。

【功能】在 Qwen3.5-4B/9B 上进行蒸馏 LoRA 训练，适配器已合并进发布的权重。答案从选项字母的 logit 单次前向读出；校准采用两级温度，超过 16 个选项的菜单经 knockout 多轮机制处理，而非对全部候选做一次 softmax。

【特点】JevBench v1.4 榜单上列全部 76 个系统第 2、开源模型第 1（62.04，Jev 为 63.29），为当时该榜上排名最高的开源模型，上述名次与分数均出自该版榜单。另有独立的轻量版 JevK5-Lite（437M，基于 DeBERTa 单独训练，并非 Qwen 权重的量化版）面向低算力场景的校准，并提供 GGUF 量化版本用于本地推理。逐题结果与覆盖全部训练数据的许可清单随权重一并公开，便于复现与审计。

【适用】适合本地与低算力的类型化决策部署——GGUF 构建与 Lite 版共同覆盖从低算力到本地部署的区间——以及需要评测披露可复核、可审计的用法。其榜单成绩来自 JevBench v1.4，在该版上比较开源条目的团队会看到它位列开源第一；超过 16 个选项的场景走 knockout 多轮机制，与单次 softmax 的行为不同。

## Links

- [GitHub – 源码](https://github.com/allebee/jevk5)
- [HF – JevK5 权重](https://huggingface.co/aliboserikbay/JevK5)
- [HF – JevK5-GGUF 量化版](https://huggingface.co/aliboserikbay/JevK5-GGUF)
