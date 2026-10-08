---
title: "RouteLLM (lm-sys) (same-paradigm reference)"
updated: 2026-10-09
---

# RouteLLM (lm-sys) (same-paradigm reference)

**Positioning** RouteLLM, from lm-sys, is a framework for routing LLM traffic between stronger and weaker models by query difficulty: a request goes to the weaker, cheaper model unless the router judges it hard enough to need a stronger one. It predates Jev and is included here as a same-paradigm reference for the model-routing scenario — the scenario where Jev Choice is the typical Jev question type.

**What it does** It drops in as an OpenAI client replacement, intercepting an application's model calls in place of the usual client, or it runs as a compatible server front-ending model traffic. Its officially trained routers are claimed to save 85% of cost while retaining 95% of GPT-4-level quality; the figures are officially self-reported and were produced with the project's own evaluation framework, which ships alongside threshold-calibration tooling. The evaluation framework and the calibration tooling ship in the same repository.

**Characteristics** Model routing is also the typical scenario for Jev Choice, which makes RouteLLM the open-source baseline for it: where Jev makes a per-request decision with calibrated probabilities, RouteLLM routes with trained routers — a before-and-after comparison across the two approaches.

**When to use** For anyone studying decision layers for model routing, RouteLLM is the baseline to compare against Jev, and the two form a natural comparison across the approaches; for teams that just want cheaper inference, it is usable directly as a drop-in. Its evaluation and threshold-calibration tooling also make it a practical reference for how to measure and calibrate a router, not just how to build one. The 85%/95% figures are officially self-reported, so cite them with that provenance.

## Links

- [GitHub – lm-sys/RouteLLM repository](https://github.com/lm-sys/RouteLLM)
