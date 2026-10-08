---
title: "jev-reranker (hotchpotch)"
updated: 2026-10-09
---

# jev-reranker (hotchpotch)

**Positioning** jev-reranker is a Python library, published on PyPI, that applies Jev to two adjacent retrieval tasks: reranking the candidates a RAG pipeline retrieves, and filtering those candidates by relevance to the query. Its author is Yuichi Tateno, a LlamaIndex contributor, and it installs from PyPI as jev-reranker.

**What it does** The core function, relevance_rerank(), is tuned so that documents that merely overlap with the query in topic are pushed toward the low end of the score range. That makes a downstream threshold a workable cut — genuinely relevant items stay above it while topically adjacent noise falls below — instead of every document sliding along one smooth gradient where a cutoff has nowhere to land. The same scores serve the filtering task as well, so both tasks run on one score scale. Judging runs in two modes, listwise and pointwise: in the first, a candidate list is judged together in context; in the second, each item is judged on its own.

**Characteristics** Long candidate lists are split automatically into batches before they are judged. Requests are handled concurrently, with automatic retries when a single request fails. Every execution returns a full audit in the detail field of the result.

**When to use** It suits RAG pipelines that rerank retrieved candidates or filter them against a fixed score threshold. Since Jev is a decision model rather than an embedding model, ranking quality depends heavily on how the question and criteria are phrased. The library's defaults encode one opinion on that phrasing, and a corpus different from the author's may call for retuning them against the new corpus.

## Links

- [GitHub – hotchpotch/jev-reranker](https://github.com/hotchpotch/jev-reranker)
- [PyPI – jev-reranker](https://pypi.org/project/jev-reranker/)
