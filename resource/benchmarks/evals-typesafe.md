---
title: "evals.typesafe.ai"
updated: 2026-10-09
---

# evals.typesafe.ai

**Positioning** evals.typesafe.ai is TypeSafe's official interactive site for its "workflow evals": multi-step decision workflows rendered step by step, with a reimbursement-approval workflow shown as the site's worked example. It is a vendor-run showcase rather than an independent benchmark.

**What it does** Visitors can watch how the model behaves at each step inside a realistic process, a format closer to how decision models are deployed than isolated single questions. Unlike single-question benchmarks, workflow evals measure behavior across a whole chain of steps rather than one decision at a time. The site shipped alongside a launch blog that presents the evaluation numbers.

**Characteristics** The blog's headline figures include 193.6x and 444.6x improvements, and these are official, self-reported numbers with real limitations: the evaluation setup consists of TypeSafe's own workflow definitions scored against model-generated reference answers, so the multipliers should be treated as vendor claims rather than established results; both multipliers come from that same self-reported setup. Measuring a chain of steps is also what makes workflow evals harder to verify independently. The mitigating factor is transparency — the workflow code behind the evals is open-sourced in the typesafe-ai GitHub organization, so third parties can audit exactly what was measured.

**When to use** Suited to readers who want to observe how Jev behaves inside multi-step workflows, or to audit what the official evaluation measures by reading the open-sourced workflow code in the typesafe-ai organization. Treat the published multipliers as vendor claims, not verified results; for an outside view of Jev's standing, the independent leaderboards and benchmarks listed elsewhere in this collection are the better starting point.

## Links

- [Website – official workflow evals](https://evals.typesafe.ai/)
- [GitHub – typesafe-ai organization (open-sourced workflow code)](https://github.com/typesafe-ai)
