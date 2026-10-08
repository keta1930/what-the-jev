---
title: "Perplexity Decisions API (pplx-decider-v1-27b)"
updated: 2026-10-09
---

# Perplexity Decisions API (pplx-decider-v1-27b)

**Positioning** Perplexity's Decisions API (model id pplx-decider-v1-27b) is a multimodal decision model fine-tuned from Qwen3.8-27B, launched on 2026-10-01 at api.perplexity.ai/v1/decisions. The weights are open-sourced under Apache-2.0 on Hugging Face while the hosted API is commercial; both routes expose the same fine-tune, which is why the entry appears in this open-source category with that caveat attached.

**What it does** Requests carry a state — text or image — plus up to 128 questions, all answered within one call inside a 262K context window that fits long documents. The open weights can be self-hosted and audited rather than consumed only as an endpoint. Version 1.1, released around 2026-10-05, cut input pricing from $0.04 to $0.02 per million tokens; calls before that version priced at the higher rate.

**Characteristics** Perplexity's own evaluation reports 85.71% versus Jev's 84.51% on an 11-test panel, a margin of under one point that the release coverage highlighted as the headline result. The figures are self-reported, and the announcement materials cite no third-party replication, so treat the comparison accordingly.

**When to use** For decision workloads that need multimodal input (including images), a 262K context, or many questions per call — up to 128 in a single request — and for teams that want the option to self-host and audit the weights instead of depending on a commercial endpoint, or to run both and compare. Since both routes expose the same fine-tune, choosing hosted versus self-hosted changes the operations, not the model. When selecting against Jev on the published numbers, note that they are vendor-reported, carry a sub-one-point margin, and lack third-party replication.

## Links

- [Docs – OpenRouter model page](https://openrouter.ai/perplexity/pplx-decider-v1-27b)
- [Docs – Overview and usage](https://vercel.com/i/what-is-perplexity-decisions-api)
- [News – Release coverage](https://aiweekly.co/alerts/perplexity-open-sources-27b-decider-edges-jev-on-11-test-panel)
