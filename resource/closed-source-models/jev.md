---
title: "Jev (TypeSafe AI)"
updated: 2026-10-09
---

# Jev (TypeSafe AI)

**Positioning** Jev is the flagship closed-source decision model from TypeSafe AI, released on September 15, 2026, and the model that created the "System One" category. It is also the reference model for this repository's experiments. Rather than generating text, it takes a state plus typed questions and returns typed answers with calibrated probabilities, consuming zero output tokens.

**What it does** A request carries a state plus typed questions over three primitives — Choice, Score, and Noul — and the model returns the corresponding typed answers with calibrated probabilities. It accepts no free-form prompts and produces no prose. Access runs primarily through OpenRouter under the model ID `typesafe/jev-1.13`, with a moving alias `~typesafe/jev-latest`. A direct API at `api.typesafe.ai/v1/systemone` reopened registration on September 27, 2026, and the model is also distributed through the Vercel AI Gateway and Cloudflare Workers AI.

**Characteristics** Trained with RLCD (Reinforcement Learning for Calibrated Decisions); the weights are proprietary and have not been released. Input costs $0.042 per million tokens, output is free, and the context window is 32K. A sibling product, Jev Router, uses Jev to select models and reasoning effort for incoming requests, and offers a 1M-token context.

**When to use** Suited to scenarios that need typed, calibrated structured decisions rather than text generation, particularly where requests already run through OpenRouter, the Vercel AI Gateway, or Cloudflare Workers AI. Not suited to open-ended text generation or any workload that expects prose output. Jev answers only typed questions over the three primitives, and the 32K context bounds how much state a single request can carry, so very large states do not fit in one request.

## Links

- [TypeSafe AI – official website](https://typesafe.ai/) (Website)
- [System One concept – TypeSafe docs](https://docs.typesafe.ai/concepts/system-one) (Docs)
- [Introducing System One models and Jev – TypeSafe blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (Blog)
- [Jev guide – OpenRouter docs](https://openrouter.ai/docs/guides/community/jev) (Docs)
