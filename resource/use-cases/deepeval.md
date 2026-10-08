---
title: "DeepEval (confident-ai)"
updated: 2026-10-09
---

# DeepEval (confident-ai)

**Positioning** DeepEval, by confident-ai, is an open-source LLM evaluation framework built like pytest: metrics such as G-Eval, faithfulness, and agent-trajectory evaluation run as tests over an LLM application's outputs — each metric is a test that receives the outputs and returns a score. The project is very actively developed, and full documentation, including the metric catalog, is available on the project site.

**What it does** It supports Jev natively through the JevEval custom metric. Where a metric needs a judgment about an output, JevEval delegates the scoring to Jev, which returns calibrated probabilities instead of a generated judgment. The substitution is surgical: JevEval slots into the existing metric interface rather than adding a parallel evaluation path, so Jev-backed scoring runs next to the framework's other metrics in the same test suite.

**Characteristics** For evaluation workloads, JevEval replaces some LLM-as-judge calls — asking a generative model for a verdict — with a typed decision. What gets replaced is the text verdict a generative model would otherwise produce. The calibration of that decision doubles as a confidence signal on the score.

**When to use** Suits teams already running DeepEval who want judgment calls handled by Jev, particularly metrics where the score benefits from an attached confidence signal — run it wherever a metric already asks a generative model for a verdict. It is also a case of adoption at the evaluation layer: a mainstream framework using Jev as a backend for judgment calls rather than merely another text generator to be graded. The substitution covers part of the LLM-as-judge calls, not all of them; generation-based metrics keep their original path.

## Links

- [GitHub – confident-ai/deepeval repository](https://github.com/confident-ai/deepeval)
- [Docs – DeepEval documentation](https://deepeval.com/docs)
