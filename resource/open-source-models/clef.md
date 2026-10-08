---
title: "Clef / Clef-flash (Cloudflare)"
updated: 2026-10-09
---

# Clef / Clef-flash (Cloudflare)

**Positioning** Clef and Clef-flash are decision models trained in-house by Cloudflare's Workers AI team, announced on 2026-10-01 during Birthday Week. Clef is the larger of the two at 27B on a Qwen3.8 base, while Clef-flash is the 9B model on a Qwen3.5 base. The weights are open-sourced under Apache-2.0, and the same two models are also served commercially through Workers AI, so each of the two sizes is available both as Apache-2.0 weights to self-host and as a commercial endpoint.

**What it does** Both models share one recipe: a frozen backbone with LoRA adapters and a two-stage attention routing head. They include a vision encoder, so image input is supported alongside text. They offer a 64K context — twice Jev's 32K — and are fully compatible with the Jev API.

**Characteristics** Cloudflare's official benchmarks report first place on the Jev Decision Index and three wins out of four on Jev's own evaluations; all of these figures are self-reported. On pricing, a third-party page lists hosted access at $0.24 per million input tokens — a reported figure, not confirmed in Cloudflare's own materials here.

**When to use** For workloads that need image input, a 64K context window, or a self-hosted model that stays compatible with the Jev API: the open weights let Jev users self-host a compatible model with double the context, while the hosted route runs on Workers AI with no inference infrastructure of one's own. The benchmark comparison with Jev is vendor-reported, so note the source of each number when comparing the models directly against Jev or against other open decision models.

## Links

- [Blog – Announcement post](https://blog.cloudflare.com/clef-decision-models/)
- [Docs – Workers AI changelog](https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/)
