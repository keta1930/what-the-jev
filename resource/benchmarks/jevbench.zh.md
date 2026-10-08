---
title: "JevBench（Benchmark Heaven）"
updated: 2026-10-09
---

# JevBench（Benchmark Heaven）

【定位】JevBench 是 Benchmark Heaven 自有的 Jev 级决策模型榜单（独立第三方来源），与 TypeSafe AI 无关联、亦无背书，Jev 只是被测系统之一。

【功能】评测形式为给模型一段 state 和一组有界选项，模型返回类型化答案，理想情况下附带每个选项的概率。榜单迭代很快：截至本次核查为 v1.0 至 v1.4.x，另已发布冻结的 v1.5 方法索引，共收录 95 个系统（91 个参与排名）；v1.4.2.2 版榜首为 Imajev-4B 67.37、Plumb-4B 65.84、decider-4b v2 64.13、Jev 1.13.0 63.29、JevK5 v0.2.0 62.04。

【特点】JevBench Score 由四个等权轴——机会校正的 Intelligence、Calibration、Speed、Cost——经几何平均合成，成本按每 1,000 次决策而非每 1,000 token 计价。题目在任何系统运行前冻结并哈希，保留私有不公开的 hard 层，封闭集只发布聚合统计，成本修正有日志和测试，转售他人模型的服务只列榜不排名；MIT 许可的评测框架可端到端复现，项目为个人自费维护。

【适用】适合跟踪 Jev 级决策模型横向排名、或想用其 MIT 框架自行复现评测的读者。引用任何排名必须连同版本号——上述数字对应 v1.4.2.2；另注意它与本资源库另列的 PavelRavich jev-bench 是两个不同项目，请勿混淆。

## Links

- [GitHub – JevBench 仓库](https://github.com/fstandhartinger/jevbench)
- [Website – 实时榜单](https://benchmarkheaven.com/jev-models)
