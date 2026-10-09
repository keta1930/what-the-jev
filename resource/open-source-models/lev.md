---
title: "Lev (Interfaze AI)"
updated: 2026-10-09
---

# Lev (Interfaze AI)

**Positioning** Lev is an open-source System One decision model from Interfaze AI, released together with an evaluation harness.

**What it does** It is a LoRA adapter on top of Qwen3.5-4B that reads probabilities straight from already-computed logits, producing zero output tokens and returning calibrated probabilities over the given options. The wire protocol is TypeSafe's `/v1/systemone`, so existing clients work after changing the base URL. It ships with levbench, which measures accuracy, log loss, Brier score, ECE, selective accuracy, p50 latency, cost, and schema retries, plus a Snake demonstration.

**Characteristics** Code and weights are Apache-2.0, though some training datasets carry separate non-commercial terms. The project reports (self-reported) 68.9% across all 13 S1Bench subsets, with an average ECE of 0.115 against Jev's 0.091, and beats Jev on 5 of the 13 subsets. Engine computation is reported at 69 ms for short requests on an H100, while end-to-end through Modal is 414–654 ms. Training used 200,000 samples for 3 epochs, about 7.8 hours on an H100. llama.cpp ships `ggml-org/lev-GGUF` (about 36 ms per question, per the llama.cpp official blog). Adoption is low: the GitHub repository has 16 stars and dates from 2026-09-24, with documentation that is complete.

**When to use** Suited to teams that want probability outputs with calibration metrics and a like-for-like evaluation harness, and that can accept a small, early-stage project; the TypeSafe-compatible endpoint means existing clients need only a base-URL change. Because adoption is low and some training data is non-commercial, check the license terms and the project's maturity before production use. Not suited to tasks needing generated text.

## Links

- [GitHub – Source code and levbench](https://github.com/InterfazeAI/lev)
- [HF – Model weights](https://huggingface.co/interfaze-ai/lev)
- [HF – ggml-org lev-GGUF](https://huggingface.co/ggml-org/lev-GGUF)
