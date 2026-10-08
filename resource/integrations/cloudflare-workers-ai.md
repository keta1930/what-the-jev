---
title: "Cloudflare Workers AI: typesafe/jev"
updated: 2026-10-09
---

# Cloudflare Workers AI: typesafe/jev

**Positioning** Jev as listed in the Cloudflare Workers AI model catalog: the model is served directly inside Workers AI rather than being reached through an external gateway, and it appears alongside the catalog's other models.

**What it does** Integration is a single `env.AI.run()` call that sends the state and questions directly to the model, with no separate gateway or API key to wire up. As a catalog model, it shares the same invocation path as the rest of Workers AI. The model page carries four complete request/response examples covering scenarios such as refund review, department routing, and account risk scoring, among others; each shows the full round trip from request body to typed answer, so the examples can serve as starting points rather than something to reverse-engineer. Each example shows the request body, the questions, and the typed answer for its scenario.

**Characteristics** Specs per the Cloudflare model page: a 32k context window, zero data retention, and input pricing of $0.042 per million tokens. One distinction to keep in mind: Cloudflare also maintains Clef, its own open-source decision model, which is covered in a separate entry in this collection — `typesafe/jev` on Workers AI is the Jev model as served by Cloudflare, not Clef.

**When to use** Fits applications already running inside the Cloudflare Workers ecosystem — a Worker calls the model the same way it calls the catalog's other models — and the worked examples double as references for putting the request format together. The access path is tied to Workers AI's invocation style, so deployments outside that environment need a different route to Jev.

## Links

- [Docs – typesafe/jev model page](https://developers.cloudflare.com/ai/models/typesafe/jev/)
