---
title: "StartLux-Decision (StartLux Labs)"
updated: 2026-10-10
---

# StartLux-Decision (StartLux Labs)

**Positioning** StartLux Labs' family of typed decision models: five dense sizes from 0.8B to 27B plus a 35B-A3B mixture of experts, each reading a text, JSON, or image state with typed questions and returning a probability per option in a single forward pass. Nothing is generated — answers are read from the option letters — and requests use the TypeSafe `/v1/systemone` format, so existing Jev clients work unchanged.

**What it does** Every size takes a 262,144-token state and answers `choice`, `noul`, and `score` questions; a long state is read once in chunks and each question branches off it. Shipped runtimes cover CUDA, where the `flash-linear-attention` and `causal-conv1d` kernels are required, Apple Silicon through MLX, and GGUF under llama.cpp, the last two reading text only. The project self-reports a Decision Index 0.2.1 score of 63.88 for the 27B against 57.91 for Jev 1.13, 210 correct of 231 public JevBench items for the 35B-A3B, and 12.2 ms to 102.3 ms per request across the ladder on one H200. Inference code is Apache-2.0; weights are CC BY-NC 4.0, free for non-commercial use with attribution and otherwise needing a separate license.

**Characteristics** Weights sit on Hugging Face and ModelScope, with BF16, Q8_0, and Q4_K_M GGUF builds for the dense sizes; measured on the same 231 JevBench items they return the original answer 99-100% of the time, while Q4_K_M changes more answers at 0.8B and 2B, where Q8_0 is recommended. The 35B-A3B has no GGUF. Training data includes the public train splits of 14 of the 38 Decision Index benchmarks, with the matching test items filtered out, and the repository adds LoRA fine-tuning and temperature calibration. Decision Index runs were not submitted to the public board, so those figures are project-run.

**When to use** Suited to deploying Jev-compatible decisions locally at a chosen size, including image and very long inputs on CUDA. Not suited to commercial use without a separate license, nor to the MLX and GGUF paths when images are needed.

## Links

- [GitHub – Repository](https://github.com/StartLuxLabs/StartLux-Decision)
- [HF – Model collection](https://huggingface.co/collections/startlux-models/startlux-decision-6abba92b301b573fa154d493)
- [HF – StartLux-Decision-27B weights](https://huggingface.co/startlux-models/StartLux-Decision-27B)
