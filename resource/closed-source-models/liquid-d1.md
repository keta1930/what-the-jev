---
title: "Liquid d1 (Liquid AI)"
updated: 2026-10-09
---

# Liquid d1 (Liquid AI)

**Positioning** Liquid d1 is a family of decision models released by Liquid AI on September 29, 2026, built around the same typed-decision interface that Jev established: a state plus Choice, Score, or Noul questions in, typed answers with calibrated probabilities and zero output tokens out. Every variant is closed-source and served only as a hosted service.

**What it does** The family implements the System One endpoint contract and is compatible with the TypeSafe SDK, so switching from Jev requires only a base-URL change and no other code modifications. Three hosted variants make up the line: the flagship d1 is served at `api.liquid.ai/decisions/v1/systemone` and has a free tier under the name `d1:free`; d1-3B builds on the LFM2.5-VL-3B backbone and accepts text and image states; d1-omni-600M is the smallest of the three and takes text, image, and audio states. No variant generates text; every response is a typed answer with a calibrated probability.

**Characteristics** No weights have been published for any of the three variants, and there is no self-hosting or private-deployment path. Multimodal coverage differs across the variants, so text, image, or audio support must be checked per model. Hosting terms beyond the `d1:free` tier are set solely by Liquid AI.

**When to use** Suited to existing TypeSafe SDK setups that want to replace their decision model with only an endpoint change, and to tasks whose states include images or audio. Not suited to self-hosted or weight-private deployments, nor to buyers who need to control their own hosting terms. Image and audio support depends on the variant chosen — d1-3B covers text and images, while d1-omni-600M adds audio.

## Links

- [Decision models – Liquid AI docs](https://docs.liquid.ai/lfm/models/decision-models) (Docs)
- [Liquid AI releases d1, a decision model with zero output tokens – MarkTechPost](https://www.marktechpost.com/2026/09/29/liquid-ai-releases-d1-a-decision-model-that-returns-calibrated-probabilities-with-zero-output-tokens/) (News)
- [d1 – Vercel AI Gateway](https://vercel.com/ai-gateway/models/d1) (Docs)
