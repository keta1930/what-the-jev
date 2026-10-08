---
title: "Kev (Jared Palmer)"
updated: 2026-10-09
---

# Kev (Jared Palmer)

**Positioning** Kev is a family of small decision models built on Qwen backbones that you can train yourself on your own labeled data and deploy locally, serving as an open-source alternative to TypeSafe's Jev for text judgments, classification, and scoring decisions.

**What it does** A single request supports yes/no, multiple-choice, and scoring questions, with strict isolation between questions so the answer to one never interferes with another. Default outputs are temperature-calibrated probabilities, making it easy to set confidence thresholds for automatic routing, with each answer carrying its calibrated probability. The model can be fine-tuned on your own labeled data, and a coding agent can run the whole pipeline from question discovery to deployment on Modal. One command deploys an HTTPS endpoint that scales to zero cost when idle, so a deployment that stops receiving traffic stops costing money. Alongside self-hosting, kev-4b is also available through a hosted OpenRouter entry point.

**Characteristics** The stack is a Qwen3.5/3.8 backbone plus rank-16 LoRA adapters and a pointer head, with strict question isolation implemented via attention masks or an independent-row mechanism. Four size tiers from 0.8B to 27B cover laptops through data-center GPUs, so the same stack can be sized to the hardware at hand, with CUDA, ROCm, and Apple MLX support, under Apache-2.0.

**When to use** For developers who need to run text decision models locally or in private environments; typical cases include support-ticket routing, urgency triage, and customer sentiment scoring. Not for tasks that demand top-tier knowledge QA — smaller models also lose accuracy on long documents, where the 27B version is the recommended choice.

## Links

- [Blog – Introducing Kev](https://jaredpalmer.com/blog/introducing-kev)
- [GitHub – Source code](https://github.com/jaredpalmer/kev)
- [HF – kev-4b weights](https://huggingface.co/jaredpalmer/kev-4b)
- [Docs – OpenRouter hosting of kev-4b](https://openrouter.ai/jaredpalmer/kev-4b)
