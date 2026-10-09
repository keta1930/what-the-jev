---
title: "NeoHorse-Jev-4B (TokenRhythm)"
updated: 2026-10-09
---

# NeoHorse-Jev-4B (TokenRhythm)

**Positioning** NeoHorse-Jev-4B is a prefill-only decision model from TokenRhythm, the team behind the open NeoHorse framework, aimed at agent workflows that must route, select tools, or judge conditions rather than generate text.

**What it does** Given a state and caller-defined questions, it predicts decisions and probabilities without autoregressive generation, for routing requests, choosing tools, testing conditions, and grading results; it accepts text and a single image. It exposes a native `/v1/decision` endpoint and a System One-style `/v1/systemone`, so a client can use either protocol, plus `/health`; it deploys on vLLM, SGLang, or a local runtime, with GGUF and a ModelScope mirror also provided.

**Characteristics** Apache-2.0, on the NeoHorse-1-4B backbone (derived from Qwen3.5-4B), released 2026-09-23. The project reports (self-reported) 75.32% per-example accuracy and 100% valid output format on the 231 public JevBench questions; an average of 83.26% across Nimble, VitaminC, and MASSIVE, 11.50 percentage points above the base model; and 77.70 on a six-task text benchmark set, which the project says is the highest among open decision models with complete results from four vendors (the combined score is compiled by the vendor, so cross-model comparisons count as self-reported). Third-party coverage reports an average of 74.3 ms at 32 concurrent. The GitHub repository has 1.6k stars.

**When to use** Suited to agent pipelines that need to route, select tools, test conditions, or score outcomes in one pass without generated text, including deployments on vLLM or SGLang and local use through GGUF. Compare across models with care, since the headline combined score is vendor-compiled; validate on the target task before relying on it.

## Links

- [GitHub – NeoHorse framework and model](https://github.com/TokenRhythm/NeoHorse)
- [HF – NeoHorse-Jev-4B weights](https://huggingface.co/TokenRhythm/NeoHorse-Jev-4B)
