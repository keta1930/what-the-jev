---
title: "Tev1 (Together AI)"
updated: 2026-10-09
---

# Tev1 (Together AI)

**Positioning** Tev1 is Together AI's open-source decision-model offering: LoRA adapters on Qwen3.5 at 4B and 0.8B, released together with an official blog post explaining how to "train your own Jev for $17". The weights and the walkthrough shipped as a single announcement. Reproducing a minimal Jev-style system at that training cost is the project's central claim.

**What it does** Its scope is deliberately narrow: Tev1 supports only choice-type decisions, picking one option from 2 to 24 candidates, and score and noul questions fall outside its interface, unlike Jev and several other open alternatives in this directory. The two model sizes, 4B and 0.8B, bracket small-scale hardware. Beyond self-hosting the open weights, Tev1 is served through Together's serverless platform at $0.042 per million tokens.

**Characteristics** The accompanying blog post records the full pipeline and cost breakdown for training a decision model from a small base; the $17 figure is the training cost of reproducing a minimal usable system, which is what the walkthrough documents. For mixed workloads the narrow interface is the binding constraint, not the cost. Read the project as a recipe and a cost demonstration rather than a drop-in Jev replacement.

**When to use** For teams that want to bootstrap their own decision model from a small base and study the training budget — the walkthrough is the practical value, and it can be followed step by step; the $17 figure is the training cost that walkthrough documents. The serverless route shows what hosted serving of these adapters costs at Together. With choice-only support, mixed choice/score/noul workloads cannot route to it directly as a stand-in for Jev.

## Links

- [GitHub – Weights and training recipe](https://github.com/togethercomputer/tev1)
- [Blog – Train your own Jev for $17](https://www.together.ai/blog/how-to-train-your-own-jev)
