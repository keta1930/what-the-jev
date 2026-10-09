---
title: "Span-01 (Respan)"
updated: 2026-10-09
---

# Span-01 (Respan)

**Positioning** Span-01 is a proprietary reasoning classifier from Respan (formerly Keywords AI), announced on September 24, 2026. It is aimed at behavior detection over AI agent traces, that is, deciding whether behaviors described in natural language appear in a trace (official blog).

**What it does** For each behavior defined in natural language, the model returns, in one call, probabilities for present, absent, and not_observable, covering a set of behaviors over the same trace, with one probability per behavior. At inference it runs as a true single forward pass rather than token-by-token generation, so the three probabilities come back directly in one response. On training, general classification reasoning is first built with RLAIF and then specialized, and hybrid attention is used to preserve that reasoning across long traces (official). Pricing is $0.02 per million input tokens with free output tokens, and a variant, Span-01 Lite, is provided free of charge (official). No weights, license, or repository are published.

**Characteristics** Respan reports an overall behavior F1 of 84.3 for Span-01, against 81.5 for GPT-6 Luna and 71.5 for Jev 1.13.0. On production behaviors it reports an overall score of 0.806, against 0.716 for Jev, 0.719 for Sonnet 5, and 0.885 for GPT-6 Sol, the highest among the models compared. These figures are Respan's own.

**When to use** Suited to replacing LLM-as-a-judge for safety, reliability, grounding, and response-quality checks on production traces, where each behavior is defined in natural language and answered with a probability rather than a generated label. The material is recent, and the model is at an early stage.

## Links

- [Introducing Span-01 – Respan blog](https://www.respan.ai/blog/introducing-span-1) (Blog)
- [Span-01 – OpenRouter](https://openrouter.ai/respan/span-01) (Gateway)
