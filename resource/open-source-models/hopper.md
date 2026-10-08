---
title: "Hopper (hopit-ai)"
updated: 2026-10-09
---

# Hopper (hopit-ai)

**Positioning** Hopper is a single-forward-pass decision server from hopit-ai. It was released alongside five models; the server code is open source, while adapter licensing varies by tier and needs checking before adoption.

**What it does** The lineup covers two general-purpose lines of Qwen3.5-4B LoRA adapters — Hopper and Hopper-G — plus Gemma-4-12B-it in both frozen and fine-tuned variants, a 12B tier alongside the 4B adapters — a larger-model option than the LoRA-only lineups elsewhere in this directory. The frozen and fine-tuned 12B variants give a choice between the base model and an adapted one. Answers are produced with a letter softmax, over the option letters, and then mapped through per-answer-type temperatures for calibration, so each answer type gets its own temperature. Long menus with more than 26 options are handled by a two-stage tournament/embedding approach rather than one softmax over all candidates.

**Characteristics** On the JevBench v1.5.5 leaderboard the system scores 67.5 overall (#16) with 87.9 on the calibration axis; both figures come from that leaderboard. Licensing splits by tier: the server code is Apache-2.0; the Hopper and Hopper-G adapters are restricted to research and demonstration use because their training involves RACE data terms; only the Hopper 12B (trained) adapters carry Apache-2.0.

**When to use** Suited to evaluation and research use — comparing decision servers or reproducing the benchmark — and to production deployments that stay entirely on the Apache-2.0 12B trained adapters. The 4B Hopper and Hopper-G adapters cannot serve production workloads under their license terms, so confirm which adapter tier a deployment uses before putting the server in front of business traffic.

## Links

- [GitHub – Decision server and adapters source](https://github.com/hopit-ai/hopper)
- [HF – Hopper adapters](https://huggingface.co/HopitAI/hopper)
- [HF – Hopper-G adapters](https://huggingface.co/HopitAI/hopper-g)
