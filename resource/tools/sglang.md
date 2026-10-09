---
title: "SGLang"
updated: 2026-10-09
---

# SGLang

**Positioning** Decision-model support in the SGLang serving framework: a `/v1/decisions` endpoint turns any generation model with a Jinja chat template into a decision model, alongside a System One-compatible `/v1/systemone` endpoint.

**What it does** `/v1/decisions` takes an input and typed questions (choice with 2-26 options, score with 2-10 levels, yes_no) and returns per-question probabilities over the options, the argmax choice or the probability-weighted score, and `label_mass`, the labels' full-vocabulary probability at the answer position. Questions are answered independently and scored together in one batch, the same server keeps serving chat traffic, and no special checkpoint is required. `/v1/systemone` exposes the same capability in the state-plus-noul/choice/score shape; the official TypeSafe SDK works after changing the base URL, choices go up to 255 options, and both endpoints accept image input with vision-capable models.

**Characteristics** Answers are read from next-token log-probabilities at the answer position (labels must be single tokens), with no text generated. The documentation states plainly that the returned probabilities are not calibrated and thresholds must be validated on labeled data. Qwen3.8-27B and Qwen3.5-35B-A3B are the validated models (one H200, BF16). A `prompt_format_version` field pins the prompt wording, and `/v1/score` can replay scored token ids. Decision checkpoints such as PPLX-Decider v1/v1.1 are served through `/v1/systemone` with their trained prompt, answer codes, and calibrated temperature. A nightly build is required as of review.

**When to use** Suits teams already running SGLang that want typed decisions from existing generation models, and self-hosting PPLX-Decider; not for tasks that depend on calibrated probabilities. Servers launched with `--enable-mis`, `--dllm-algorithm`, or a built-in conversation template refuse decision requests.

## Links

- [Docs – Decision models](https://docs.sglang.io/docs/supported-models/decision_models.md)
- [Docs – PPLX-Decider-v1.1-27B cookbook](https://docs.sglang.io/cookbook/autoregressive/Perplexity/PPLX-Decider-v1.1-27B.md)
- [GitHub – sgl-project/sglang](https://github.com/sgl-project/sglang)
