---
title: "jev-bench（PavelRavich）"
updated: 2026-10-09
---

# jev-bench（PavelRavich）

【定位】jev-bench 是 Pavel Ravich（GitHub: PavelRavich）个人完成的独立第三方基准，把 TypeSafe 的 Jev 决策模型与 GPT-6 Luna、GPT-6 Astra 放在决策式任务上对比；两个数据集均以 Jev 的类型化问题格式（Noul 与 Choice）呈现。

【功能】基准包含两个数据集、各 500 条样本：SMS Spam 以 Noul 二分类问题呈现，Banking77 以 77 类 Choice 任务呈现。每个"模型 × 数据集"组合都报告 accuracy、macro-F1、ECE、Brier、p50/p95 延迟和每千次调用成本，并全程附 bootstrap 置信区间；Medium 上的长文同步记录了方法论与作者对结果的解读。

【特点】整个评测只花费 $1.13，随机种子固定，仓库本身就是可复现存档。基准于 2026 年 9 月完成，此后作为存档存在而非持续开发，属于时间点快照：随着 Jev 与 GPT-6 系列模型演进，重跑公开代码才是检验其结论是否依然成立的方式。

【适用】适合需要小规模、低成本、指标口径完整的 Jev 与 GPT-6 对比数据的读者，也可作为自建评测的参考实现，沿用其固定种子与 bootstrap 置信区间的口径。注意它与本资源库另列的社区榜单 JevBench 是两个不同项目，两者仅名字相近；其结论对应 2026 年 9 月时的模型版本。

## Links

- [GitHub – jev-bench 仓库（代码、固定种子与结果）](https://github.com/PavelRavich/jev-bench)
- [Blog – 独立基准长文](https://medium.com/@pravvich/typesafes-jev-beyond-the-hype-an-independent-benchmark-8bdc1c99d000)
