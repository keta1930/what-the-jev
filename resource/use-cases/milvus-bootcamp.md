---
title: "Milvus bootcamp: Search with Jev"
updated: 2026-10-09
---

# Milvus bootcamp: Search with Jev

**Positioning** This entry points to a subdirectory of Milvus's official bootcamp repository, bootcamp/RAG/search_with_jev: nine notebooks on retrieval-augmented search in which Jev supplies the judgment calls. The bootcamp is the project's tutorial repository, and pymilvus is its companion Python package. Together the notebooks form a practical cookbook for the pattern, one recipe per decision point.

**What it does** The notebooks cover reranking, context filtering, deciding when to stop searching, graph-relationship reranking, query routing, cache reuse, pre-indexing selection, injection screening, and evidence review — the decision points inside a RAG pipeline where a calibrated judgment is an alternative to generation. The collection spans the retrieval flow end to end, from pre-indexing selection through query routing to evidence review. In each, Jev's role is the judgment call rather than generating text. Together the notebooks form a complete, runnable pipeline combining Gemini embeddings with Jev judgments, usable both as tutorials and as copy-paste starting points. The runnable pipeline combines Gemini embeddings with Jev judgments end to end.

**Characteristics** The JevRerankFunction integration has been merged into pymilvus[model], so Jev-based reranking is available directly to pymilvus users without extra integration work. As official vendor tutorial material, each of the nine decision points comes with runnable code.

**When to use** For developers adding decision points to a RAG pipeline: read the notebooks as tutorials or lift the code as a starting point. It is also vendor documentation of Jev being used as a component in a retrieval stack. The material is organized around the Milvus and pymilvus stack, so porting it to another retrieval stack means adapting the code yourself.

## Links

- [GitHub – bootcamp/RAG/search_with_jev subdirectory](https://github.com/milvus-io/bootcamp/tree/master/bootcamp/RAG/search_with_jev)
