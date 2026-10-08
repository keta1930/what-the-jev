---
title: "OpenAI Decisions API (GPT-6 Luna)"
updated: 2026-10-09
---

# OpenAI Decisions API (GPT-6 Luna)

**Positioning** The Decisions API is OpenAI's move into typed decision inference, previewed at DevDay 2026 and opened to public beta on October 6, 2026. It follows the pattern Jev introduced — a state plus typed questions in, structured decisions out — which makes it, among the entries in this directory, the most direct large-vendor counterpart to Jev.

**What it does** The service exposes a single endpoint, `POST /v1/decisions`, and the public beta is currently served by exactly one model, `gpt-6-luna`. A request carries a state that can combine text and images, and in return the API sends structured decisions instead of free-form text. There is no free-form generation mode: every response is a structured decision. The model is also listed on OpenRouter as `gpt-6-luna-decisions`, alongside `typesafe/jev-1.13`.

**Characteristics** The service is closed-source and hosted only by OpenAI; there is no self-hosting path. Input is priced at $0.10 per million tokens, which is more than double Jev's input price. OpenAI claims typed decisions can be up to 10× faster than general-purpose model calls and says general availability is "weeks" away; both the speed figure and the timeline are vendor claims and have not been independently verified here.

**When to use** Suited to teams that already work inside the OpenAI ecosystem and want structured decision output, particularly when the state needs to combine text and images in one request. Not suited to deployments that require self-hosting, private weights, or a choice of models. The API is in public beta with a single endpoint and a single model, and the general-availability timeline remains a vendor statement rather than a committed date.

## Links

- [Decisions API public beta announcement – OpenAI Community](https://community.openai.com/t/decisions-api-is-now-available-in-public-beta/1403877) (Official announcement)
- [gpt-6-luna-decisions – OpenRouter](https://openrouter.ai/openai/gpt-6-luna-decisions) (Docs)
- [OpenAI launches Decisions API public beta on GPT-6 Luna – AI Weekly](https://aiweekly.co/alerts/openai-launches-decisions-api-public-beta-on-gpt-6-luna) (News)
