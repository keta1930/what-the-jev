---
title: "Milvus bootcamp: Search with Jev"
updated: 2026-10-09
---

# Milvus bootcamp: Search with Jev

【定位】本条目指向 Milvus 官方教程仓库的子目录 bootcamp/RAG/search_with_jev：九个 Notebook 演示检索增强搜索中由 Jev 出判断的环节。

【功能】覆盖重排、上下文过滤、搜索停止时机、图关系重排、查询路由、缓存复用、索引前筛选、注入筛查与证据评审，即 RAG 管线中可用校准判断替代生成的决策点。Notebook 共同构成 Gemini 嵌入加 Jev 判定的完整可运行管线，可当教程读，也可直接复制作为起点。

【特点】JevRerankFunction 集成已合并进 pymilvus[model]，pymilvus 用户可直接使用 Jev 重排。作为厂商官方教程，九个决策点各有可运行代码。

【适用】适合在 RAG 管线中引入决策点的开发者学习与取码，也是 Jev 用于检索栈的官方教程材料。内容围绕 Milvus 与 pymilvus 技术栈组织，用于其他检索栈时代码需自行改写。

## Links

- [GitHub – bootcamp/RAG/search_with_jev 子目录](https://github.com/milvus-io/bootcamp/tree/master/bootcamp/RAG/search_with_jev)
