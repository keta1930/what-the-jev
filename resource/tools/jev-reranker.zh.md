---
title: "jev-reranker（hotchpotch）"
updated: 2026-10-09
---

# jev-reranker（hotchpotch）

【定位】jev-reranker 是发布在 PyPI 上的 Python 库，把 Jev 用于两个相邻的检索任务：RAG 候选重排与相关性过滤。作者是 LlamaIndex 贡献者 Yuichi Tateno。

【功能】核心函数 relevance_rerank() 对候选文档做重排，取向是把与查询仅主题重叠的文档压向分数区间的低端，使下游阈值能够有效切分——真正相关的条目留在阈值之上，仅主题相邻的噪声落在阈值之下，而不是所有文档沿一条平滑梯度排开、阈值难以落在有效位置。同一套分数可直接用于相关性过滤。支持 listwise 与 pointwise 两种模式：结合上下文判定整个候选列表，或对每条候选独立判定。

【特点】长候选列表自动切分后分批判定。请求并发执行，失败自动重试。每次运行都会在结果的 detail 字段返回完整的执行审计。

【适用】适合 RAG 管线中按阈值重排候选、或按分数过滤候选的场景。Jev 是决策模型而非嵌入模型，排序质量高度依赖问题与 criteria 的措辞；库内默认值只代表作者的一种措辞取法，更换语料时可能需要重新调校。

## Links

- [GitHub – hotchpotch/jev-reranker](https://github.com/hotchpotch/jev-reranker)
- [PyPI – jev-reranker](https://pypi.org/project/jev-reranker/)
