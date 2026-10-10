---
title: "chinese-laya (yanqiangmiffy)"
updated: 2026-10-10
---

# chinese-laya (yanqiangmiffy)

**Positioning** A Chinese-language adaptation of Laya's multilingual decision checkpoint: an experiment and engineering record that machine-translates the natural-language fields of a public English typed-decision dataset into Simplified Chinese and fine-tunes the model's encoder and decision head on the result. It is a single-experiment record, not an official Laya trainer, Chinese model, or benchmark, and the trained weights are not published.

**What it does** The repository holds the translation and fine-tuning scripts, the Chinese data splits, baseline and evaluation reports, and a local React plus FastAPI demo with 9 scenarios and 27 reference samples. On its 2,000-question Chinese test set, the author reports calibrated target-class agreement of 34.05% for the original multilingual checkpoint, 74.95% after a 4-epoch fine-tune, and 76.25% for the best epoch of a 10-epoch run; over the same three checkpoints Soft-target NLL falls from 1.2374 to 0.8706 and score expected-value MAE from 0.7172 to 0.2358, while ECE rises from 0.0764 to about 0.15. The author reads that rise as a reason not to claim across-the-board improvement.

**Characteristics** The source data is LocalLLaMA/typed-decisions (Apache-2.0), four synthetic workflows — `agent_trace_observability`, `customer_service`, `invoice_processing`, `security_incidents` — translated field by field through an OpenAI-compatible API with `Ternary-Bonsai-2-27B`, keeping case IDs, candidate order, enum values, and gold probabilities unchanged. The splits hold 960/120/120/400 cases, that is 4,800/600/600/2,000 questions of type `choice`, `score`, and `noul`, five per case. Training starts from the 322M-parameter `convaiinnovations/laya-multilingual` checkpoint on a single A800 80 GB, with a loss of soft-target cross-entropy plus an RLCD-style policy term. The repository is Apache-2.0; weights and training directories are kept out of it.

**When to use** Suited to readers who want a Chinese-language reference for fine-tuning a decision model, or a base to reproduce and extend. Not a measure of real Chinese business accuracy: the author states the results reflect fitting a machine-translated benchmark, the translations were not reviewed by experts, the targets come from the original English dataset, and the figures are single runs without confidence intervals.

## Links

- [GitHub – Repository](https://github.com/yanqiangmiffy/chinese-laya)
- [HF – Base checkpoint laya-multilingual](https://huggingface.co/convaiinnovations/laya-multilingual)
- [HF – Source dataset typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions)
