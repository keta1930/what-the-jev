---
title: "Vercel AI Gateway & AI SDK"
updated: 2026-10-09
---

# Vercel AI Gateway & AI SDK

**Positioning** Vercel's access path for Jev runs through the AI Gateway, which hosts the model under `typesafe-ai/jev`, while the AI SDK and Vercel's own agent framework provide the upper-level calling and evaluation surfaces on top of it.

**What it does** The AI Gateway serves Jev under the model ID `typesafe-ai/jev`, with Zero Data Retention available for teams that need it. AI SDK 7 exposes the model through its experimental `evaluate` API, in which a Boolean evaluation maps onto Jev's Noul question type. Vercel's agent framework eve goes further: it sets Jev as the default evaluator for five of its features, replacing prompted LLM judgments with decision calls. A changelog entry documents the model's availability and the Zero Data Retention option. The changelog entry lists the model ID and the retention option.

**Characteristics** By Vercel's own account in its launch blog — a vendor-reported figure rather than an independently measured one — Jev is the fastest-adopted model in AI Gateway's history, with 13% of paid teams using it within 24 hours of launch, a figure the company says indicates how quickly decision-model workloads moved onto the platform. For developers already building on the AI SDK, Jev is a native option rather than an extra dependency.

**When to use** Suits teams building on Vercel or inside the AI SDK ecosystem that want decision-model calls as a native option, and agent projects on the eve framework, which get Jev-backed evaluation on five features by default. The adoption figure is vendor-reported, and the `evaluate` API is experimental, so watch for changes when relying on it in production setups.

## Links

- [Docs – typesafe-ai/jev now available on AI Gateway](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)
- [Blog – AI Gateway Jev model launch](https://vercel.com/blog/ai-gateway-jev-model-launch)
