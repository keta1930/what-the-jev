---
title: "jev-rerank-bench（anessbelbati）"
updated: 2026-10-09
---

# jev-rerank-bench（anessbelbati）

【定位】jev-rerank-bench 是 anessbelbati 关于 Jev 作重排器（reranker）的研究，覆盖 14 个数据集，对比 Cohere Rerank 4、ZeroEntropy zerank-2、chat 模型与多个开源模型。

【功能】各模型拿到相同的 BM25 top-30 候选（截断至 2000 字符），在候选列表中含标注相关段落的问句上计算 nDCG@10、Top-1、Recall@5、MRR@10。Jev 以八种问法参与：四级 rubric、批量 yes/no、单次 Choice、逐对 yes/no、锦标赛、级联、两两对决，以及反序对照。研究另含“无相关文档”测试、NevIR 否定对测试、校准曲线，以及重复请求、冷启动、批处理与顺序敏感性检查。全部原始响应均已保存；任何实现 System One 协议的服务都可提交排名。

【特点】在 8 个英文数据集、1617 个计分问句上，Jev 四级 rubric 的 nDCG@10 为 0.692，Cohere Rerank 4 Pro 为 0.691，95% 配对 bootstrap 区间为 −0.009 至 +0.012——研究自述这既未确立胜者、也未证明等价；若每个问句等权，则 Cohere 领先（0.756 对 0.738）。否定测试中 Jev rubric 在 NevIR 对上答对 71%，高于 Cohere Pro 的 67% 与 ZeroEntropy 的 61%。MIT 许可，2026-09-16 建库，主推于 2026-09-25。

【适用】适合判断决策模型在这条固定候选管线上的重排能力是否与专用重排器相当——其证据是保存的响应与 bootstrap 区间，而非单一数字。结果对应这条 BM25 管线与声明的数据集范围，不是官方全量基准分；引用须带版本与数据集范围，并注意同名仓库有多个，本条为 anessbelbati 版。

## Links

- [GitHub – anessbelbati/jev-rerank-bench 仓库](https://github.com/anessbelbati/jev-rerank-bench)
- [Blog – I gave Jev a reranker's job](https://anessbelbati.com/blog/i-gave-jev-a-rerankers-job)
