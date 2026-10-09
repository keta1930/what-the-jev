---
title: "Jebadiah (Frontier Infra)"
updated: 2026-10-09
---

# Jebadiah (Frontier Infra)

**Positioning** Jebadiah (Jeb) is Frontier Infra's open System One-style decision model: for each typed question it returns probabilities over option labels instead of generating text, so a caller receives a distribution over its own choices rather than a rephrased answer.

**What it does** It answers choice, noul, and score questions in one forward pass, and offers a TypeSafe-compatible `POST /v1/systemone`, AINode's `POST /v1/decide`, and a browser playground. The project includes a trainer, data construction, evaluation, and all run records, released together so the reported evaluations can be traced; weights are in the HF frontier-infra collection at 27B, 9B, and 4B. The browser playground lets a question schema be tried interactively before it is wired into an application.

**Characteristics** Under Apache-2.0, the backbones are the chat versions of Qwen3.8-27B, Qwen3.5-9B, and Qwen3.5-4B with thinking off, trained with LoRA rank 16 / alpha 32 on public data only. The project reports (self-reported) headline figures of 78.95 for 27B, 73.93 for 9B-v2, and 72.49 for 4B-v2, using its own set of evaluations that include Jevals subsets and Nimble 324. The 27B model needs about 56 GB in bf16. Adoption is early: the GitHub repository has 4 stars and 26 commits.

**When to use** Suited to teams that want the full pipeline — training code, data construction, evaluations, and run records — available alongside the weights, or that plan to fine-tune their own setup, with 27B, 9B, and 4B tiers to match hardware. The project is early with low adoption, so validate before production use and treat the headline numbers as vendor results; the 27B tier also needs roughly 56 GB in bf16. Not suited to tasks needing generated text.

## Links

- [GitHub – Source code and run records](https://github.com/getainode/jebadiah)
- [HF – jebadiah-27b weights](https://huggingface.co/frontier-infra/jebadiah-27b)
