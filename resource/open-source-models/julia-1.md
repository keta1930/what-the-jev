---
title: "Julia-1 (Supersonic Labs)"
updated: 2026-10-09
---

# Julia-1 (Supersonic Labs)

**Positioning** Julia-1 is a compact decision model from Supersonic Labs that runs on CPU as well as accelerators, covering classification, routing, ordered scoring, and boolean judgment through one interface.

**What it does** A single call handles choice, score, and noul questions and returns a full softmax probability distribution in the order of the caller's options, without generating text, so each value maps onto a supplied option. A hierarchical Router handles larger choice lists that exceed the native call, which covers 2 to 20 options per request. `SupersonicLabs/Julia-1-ONNX` provides an ONNX plus WebGPU version that runs in the browser.

**Characteristics** At 144.3M parameters, it pairs a JHU CLSP mmBERT-small multilingual encoder with a decision head, under Apache-2.0; FP32 weights are about 550.5 MiB and the runtime caps at 8,192 tokens. The project reports (self-reported, 2026-09-24, H200 BF16) 73.15% on typed decisions (1,463/2,000, against a Jev reference of 72.70%), 94% on AG News, 86% on DAIR Emotion, and 71.50% on MASSIVE across 52 locales, but only 64% on Banking77 (Jev reference 87%). Third-party coverage reports a median latency of 33 ms on an M4. llama.cpp ships `ggml-org/Julia-1-GGUF` (about 3 ms per question, per the llama.cpp official blog). Total training cost was about $104.

**When to use** Suited to CPU-only or in-browser environments and to high-throughput typed decisions where a small footprint matters, including multilingual classification and routing. Accuracy trails larger models on some single-domain sets such as Banking77, so benchmark on the target task first and route hard cases elsewhere if needed. Not suited to open-ended text generation or multi-step reasoning.

## Links

- [HF – Julia-1 model](https://huggingface.co/SupersonicLabs/Julia-1)
- [HF – ggml-org Julia-1-GGUF](https://huggingface.co/ggml-org/Julia-1-GGUF)
- [News – Release coverage](https://www.marktechpost.com/2026/09/26/supersonic-labs-releases-julia-1-a-144-3m-parameter-open-decision-model-that-runs-on-a-cpu)
