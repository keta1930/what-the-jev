---
title: "Hanzo Kai"
updated: 2026-10-09
---

# Hanzo Kai

**Positioning** Hanzo Kai is a decision model from Hanzo, released on September 28, 2026. Its weights are closed, and it is offered only through the Hanzo API rather than as downloadable weights, so there is no self-hosting path (official).

**What it does** A request sends the facts of a situation together with a question that lists options, and the model returns four kinds of typed answer: Choice, Score, Predicate (yes/no), and Defer, which hands the call to a person or a rule when confidence is low. Every option listed carries a probability, and the answer is bounded to these types, so there is no prose to parse. The model is designed for mixed evidence (text, images, or sensor readings), for resolving several dependent decisions in one pass, and for replay: each decision records the program version, evidence fingerprints, model revision, the full probability distribution, and the approval and execution trace (official). The endpoint is `POST https://api.hanzo.ai/v1/decisions`, priced at $0.021 per million input tokens with free output tokens (official).

**Characteristics** Hanzo reports a mean accuracy of 86.2% against Jev's 77.2% across 12 tasks on its website (hanzo.ai/kai, Decision Index v2), while the release blog states 85.7% against 78.0%. Hanzo also states that accuracy approaches zero at 1,000 or more options.

**When to use** Suited to model or tool selection inside agents, stop decisions, and when-to-hand-off calls such as when to ask a human, to lead scoring, intent detection, and escalation in business workflows, and to physical systems that decide on sensor data. Not suited to very large option sets, negated yes/no questions, or dependent multi-question programs.

## Links

- [Kai – Hanzo](https://hanzo.ai/kai) (Website)
- [Introducing Kai – Hanzo blog](https://hanzo.blog/blog/2026-09-28-introducing-kai/) (Blog)
