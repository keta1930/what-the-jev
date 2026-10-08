---
title: "LangChain langchain-typesafe"
updated: 2026-10-09
---

# LangChain langchain-typesafe

**Positioning** This is an agent-evaluation benchmark experiment project, testing whether the decision model Jev, when used as an evaluation judge for agent trajectories, can combine the reliability of code-based rules with the openness of an LLM judge.

**What it does** The project built a weather agent with Tavily search and froze five run traces from it. Each judge then evaluated the same traces one hundred times over, quantifying four metrics across the runs: binary accuracy, score variance, cost, and latency. Human annotation served as the oracle for verifying accuracy. The project supports both running locally and uploading experiments to LangSmith, with data and charts fully reproducible. Alongside the experiment, LangChain also released the langchain-typesafe integration package (including TypeSafeClassifier and other components).

**Characteristics** Jev is not an autoregressive LLM: it returns typed, probability-carrying judgments (Noul, Score, Choice) over structured states, and its decision-first design brings lower variance and latency. In the experiment it reached 100% accuracy, showed variance 92 to 913 times lower than the LLM judges, and cost about $0.00035 per judgment, with latency of 0.44 seconds per judgment — figures as reported by the experiment's authors, not third-party verified. The experiment stack is built on Python and LangSmith.

**When to use** Suits agent engineers and evaluation teams that need high-frequency, low-cost evaluation — for regression detection, trace feedback, and speeding up development iteration. Note that the experiment rests on only five run traces and a single human annotator, so its conclusions should not be generalized into an overall ranking of judges, nor used as a large-scale, general-purpose evaluation benchmark.

## Links

- [Blog – Jev agent evals with LangSmith](https://langchain.com/blog/jev-agent-evals-langsmith)
- [GitHub – danielgshea/jev-as-a-judge](https://github.com/danielgshea/jev-as-a-judge)
