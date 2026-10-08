---
title: "Laya (ConvAI Innovations)"
updated: 2026-10-09
---

# Laya (ConvAI Innovations)

**Positioning** A multilingual, non-autoregressive decision engine that outputs typed decisions (classification, scoring, yes/no judgment) for a text state in a single forward pass, replacing generative LLMs with fast, deterministic inference — an answer comes back as a typed decision rather than generated text.

**What it does** Decision needs are specified as typed questions over the input state; a single forward pass returns the answer with a calibrated confidence, with no text generation and no hallucination. A router detects language and script in sub-millisecond time and automatically routes among three checkpoints, covering 100+ languages across those checkpoints. The project reports (self-reported) that fine-tuning on your own decision data lifts accuracy on its benchmark from 0.362 to 0.766. It also ships a Jev-compatible HTTP server, MCP and LangChain integrations, a CLI, and a web playground, so the same engine can be reached from an agent stack, a shell, or a browser.

**Characteristics** Built on ModernBERT and mmBERT encoders, trained with reinforcement learning under a strictly proper scoring rule; project-reported latency is about 33 ms per question on a T4, or 7.2 ms per question in batch. Long documents up to 8192 tokens are supported, with optional ONNX and TileLang GPU acceleration paths and Docker and NixOS deployment recipes.

**When to use** Suited to high-throughput structured decisions such as ticket triage, email routing, content moderation, and churn early warning, especially multilingual production environments — where the router picks the checkpoint per input — and business that cannot tolerate hallucination. Not suited to open-ended text generation, multi-step complex reasoning, or deep-comprehension needs beyond its long-document limits.

## Links

- [Website – Project homepage](https://laya.convaiinnovations.com/)
- [GitHub – Source code and laya-serve](https://github.com/NandakishorM/laya)
- [HF – Model checkpoints](https://huggingface.co/convaiinnovations/laya)
- [PyPI – laya package](https://pypi.org/project/laya/)
