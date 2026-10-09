---
title: "Solar Decide (Upstage)"
updated: 2026-10-09
---

# Solar Decide (Upstage)

**Positioning** Solar Decide is a structured decision model from Upstage, released in Beta on September 22, 2026 (official). It is served as a System One endpoint built on Solar Mini 4, so a single request carries a state with typed questions and receives typed answers back. It uses the same `/v1/systemone` request schema as Jev.

**What it does** A request sends a state and typed questions, and the model returns a choice, a score, or a yes/no answer, each with a calibrated probability taken directly from the model rather than written out as text. It generates no prose, so every decision is a single forward pass and output tokens are free. The context window is 512K, which lets a whole document serve as the state, and the model carries Solar Mini 4's Korean-language capability (official). Pricing listed on the Upstage Console is $0.1 per million input tokens, $0.1 per million cached input tokens, and free output tokens. On OpenRouter, routing for the model lists $0.05 per million input tokens and $0 output tokens (gateway listing). A faster variant, Solar Decide Flash, is recorded on OpenRouter with a release date of October 8, 2026.

**Characteristics** The weights are closed, and the model is served on a single platform, the Upstage Console. Its API entry is marked Data not collected (official).

**When to use** Suited to routing, classification, and policy checks, and to tasks whose state is a long document or is in Korean, since the 512K context can hold a full document and the model keeps Solar Mini 4's Korean ability. Not suited to tasks that need free-form text generation.

## Links

- [Solar Decide – Upstage Console docs](https://console.upstage.ai/docs/models/solar-decide) (Docs)
- [Upstage models – OpenRouter](https://openrouter.ai/upstage) (Gateway)
- [Rate limits – Upstage Console docs](https://console.upstage.ai/docs/guides/rate-limits) (Docs)
