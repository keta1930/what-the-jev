---
title: "JevK5 (allebee)"
updated: 2026-10-09
---

# JevK5 (allebee)

**Positioning** JevK5 is an open-source decision model from the allebee project that combines distilled LoRA training with a SemIf-style option-letter logit readout, so answering generates zero tokens. Both code and weights are Apache-2.0, and the readout approach is explicitly acknowledged to derive from SemIf.

**What it does** Distilled LoRA training runs on Qwen3.5-4B and 9B, and the adapters are already merged into the released weights; answers are read from option-letter logits in a single forward pass. Calibration is handled with two levels of temperature, and menus with more than 16 options go through a knockout multi-round mechanism rather than a single softmax over all candidates.

**Characteristics** On the JevBench v1.4 leaderboard it ranked 2nd among all 76 systems and 1st among open-source models, scoring 62.04 against Jev's 63.29 — the top open-source entry on that leaderboard at the time; both figures come from that leaderboard version. A separate CPU variant, JevK5-Lite (DeBERTa, 437M), targets calibration at low compute — a separate DeBERTa model, not a quantization of the Qwen checkpoints — and GGUF quantizations are available for local inference. Per-question results and a license list covering all training data are published alongside the weights, which makes reproduction and audit straightforward.

**When to use** For typed-decision deployments that must run locally or on low-compute hardware — the GGUF builds and the DeBERTa-based Lite variant cover that range — and for uses that need reproducible, auditable evaluation disclosure. Teams comparing open-source entries on that version of the leaderboard will find it ranked first among them, while menus beyond 16 options take the knockout path rather than one softmax.

## Links

- [GitHub – Source code](https://github.com/allebee/jevk5)
- [HF – JevK5 weights](https://huggingface.co/aliboserikbay/JevK5)
- [HF – JevK5-GGUF quantizations](https://huggingface.co/aliboserikbay/JevK5-GGUF)
