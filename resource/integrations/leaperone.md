---
title: "LEAPERone Decisions API"
updated: 2026-10-09
---

# LEAPERone Decisions API

**Positioning** LEAPERone is an OpenRouter-compatible gateway positioned for users in mainland China; its Decisions API takes decision requests from clients and passes them through to the Jev model hosted upstream.

**What it does** The Decisions API exposes `POST /v1/decisions` and keeps `/api/alpha/decisions` as an alias, so endpoint paths written for OpenRouter continue to work. Both the primary path and the alias accept the same request bodies. Requests pass through to Jev under the alias `~typesafe/jev-latest`, and usage is settled at the upstream's original price. Migration from OpenRouter is deliberately cheap: the endpoint paths mirror OpenRouter's, so swapping the `openrouter.ai` host for `api.leaper.one` in an existing integration is all it takes, with request bodies unchanged. Because the gateway is OpenRouter-compatible, client libraries built for the OpenRouter Decisions API keep working against it, and the API reference documents the endpoint and its request format.

**Characteristics** As a third-party gateway, it sits between the client and the upstream model, which adds one forwarding hop compared with calling OpenRouter directly. For documentation, only the Chinese page currently works — the English page returns 404 — so non-Chinese readers currently need translation help.

**When to use** It works as a drop-in alternative for teams in mainland China that find direct access to openrouter.ai inconvenient, and for them the migration of an existing OpenRouter integration comes down to swapping one domain for another in the request URL. Non-Chinese readers will need translation for the documentation, and where direct OpenRouter access already works, whether to take the extra hop is a trade-off each team has to weigh on its own.

## Links

- [Docs – Decisions API reference (Chinese)](https://leaper.one/zh/docs/api-reference/decisions)
