---
title: "jev-rerank-bench (anessbelbati)"
updated: 2026-10-09
---

# jev-rerank-bench (anessbelbati)

**Positioning** jev-rerank-bench, by anessbelbati, is a study of Jev as a reranker across 14 datasets, comparing it with Cohere Rerank 4, ZeroEntropy zerank-2, chat models, and several open models.

**What it does** Models receive the same BM25 top-30 candidates, truncated to 2,000 characters, and are scored on ranking metrics (nDCG@10, Top-1, Recall@5, MRR@10) over questions whose candidate list holds a labelled relevant passage. Jev is asked in eight ways — a four-level rubric, batched yes/no, one Choice, per-pair yes/no, tournament, cascade, and duel, plus a reversed-order control. The study also runs a "nothing relevant" test, a negation test on NevIR pairs, calibration curves, and repeat, cold-start, batching, and order-sensitivity checks. All raw responses are saved, and any model served over the System One protocol can be submitted for a row.

**Characteristics** On the eight English datasets and 1,617 scored questions, Jev's four-level rubric reaches nDCG@10 0.692 against Cohere Rerank 4 Pro at 0.691, with a 95% paired-bootstrap interval of −0.009 to +0.012 — the study states this establishes neither a winner nor equivalence; weighting each query equally puts Cohere ahead (0.756 vs 0.738). On the negation test Jev's rubric is right on 71% of NevIR pairs, ahead of Cohere Pro at 67% and ZeroEntropy at 61%. MIT-licensed; created 2026-09-16, with the main run on 2026-09-25.

**When to use** Suited to judging whether a decision model is competitive with dedicated rerankers on a fixed candidate pipeline, from saved evidence and bootstrap intervals rather than a single number. The results cover this BM25 pipeline and a stated dataset set, not official full-benchmark scores; cite them with the version and dataset scope, and note that several same-named repositories exist — this entry is the anessbelbati one.

## Links

- [GitHub – anessbelbati/jev-rerank-bench repository](https://github.com/anessbelbati/jev-rerank-bench)
- [Blog – I gave Jev a reranker's job](https://anessbelbati.com/blog/i-gave-jev-a-rerankers-job)
