---
title: "llama.cpp"
updated: 2026-10-09
---

# llama.cpp

**Positioning** The local inference engine llama.cpp natively supports decision models since PR #29818 was merged on 2026-10-02: `llama-server` exposes a `/v1/systemone` endpoint that serves typed decisions in the request and response shape of Jev's System One API.

**What it does** Clients written for Jev, including the official TypeSafe SDKs, work by pointing their base URL at a local `llama-server`. Five pre-converted GGUFs are published under the `ggml-org` organization — OpenJev (27B, with vision input), Kev-4B, Laya, Lev, and Julia-1 — and `llama-server -hf ggml-org/Kev-4B-GGUF` starts a server in one command.

**Characteristics** The implementation treats decision models as wrappers around embedding models (BERT/Qwen and similar), switching input and output handling on the `{arch}.decision.type` GGUF metadata, which keeps the libllama changes minimal. The conversion script handles the new tensors and metadata, so further decision checkpoints can be converted the same way. The pull request includes per-question probability comparisons against the reference implementations, with the worst probability difference between 8.4e-4 and 2.2e-2 across models, plus an OpenJev tiny model used for testing. Parallel shared-prompt-prefix support, documentation, developer docs, and vision input landed in the same pull request, and support for Cloudflare's Clef is listed as a follow-up. The semantic release v0.5.0 predates the merge, so a recent build that contains the endpoint is required.

**When to use** Suits running a System One-compatible decision service at no cost on private hardware; the path does not involve Jev's proprietary weights. The OpenJev GGUF carries vision input, so decisions over images also run locally. Confirm the build in use contains the endpoint, and validate model outputs against business thresholds before relying on them.

## Links

- [GitHub – PR #29818: add /v1/systemone API](https://github.com/ggml-org/llama.cpp/pull/29818)
- [GitHub – llama.cpp repository](https://github.com/ggml-org/llama.cpp)
