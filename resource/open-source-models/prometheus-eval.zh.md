---
title: "Prometheus / Prometheus-Eval"
updated: 2026-10-09
---

# Prometheus / Prometheus-Eval

【定位】KAIST 牵头团队开发的开放权重评审（judge）模型家族——为其他模型的输出打分的模型——早于 Jev 发布。它以可复现的开源权重（而非封闭 API）对模型输出做结构化评估，是该范式的早期项目；该家族面向评测负载，并非 Jev 定义的类型化决策接口。

【功能】Prometheus 2 提供 7B 与 8x7B 两个规模的模型，支持 1–5 绝对评分与两个输出之间的成对比较；其中 7B 为本条目所列公开权重页对应的版本，8x7B 为更大的版本。项目报告与人类判断一致率为 72–85%（官方自报）；2025-04 又扩展出多语言版本 M-Prometheus（3B/7B/14B），语言覆盖超出此前的发布。

【特点】配套工具包括 prometheus-eval pip 包、训练脚本与 BiGGen-Bench 基准套件，构成覆盖打分与训练的完整评测工具链，而非单纯的模型发布。仓库仍在维护，但发布节奏已放缓。

【适用】适合对模型输出做自动评审、打分与成对比较的场景（LLM-as-judge 工作流）。Jev 的问题返回带校准概率的类型化答案，Prometheus 的运行返回生成式评分与文字判断，这是两者的关键差别：它不产生 noul/choice/score 类型化答案的校准概率分布，在类型化决策流程中是补充而非替代。

## Links

- [GitHub – prometheus-eval 评测库与训练代码](https://github.com/prometheus-eval/prometheus-eval)
- [HF – prometheus-7b-v2.0 权重](https://huggingface.co/prometheus-eval/prometheus-7b-v2.0)
