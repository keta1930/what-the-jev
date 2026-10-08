---
title: "LiteLLM Jev Support"
updated: 2026-10-09
---

# LiteLLM Jev Support

**Positioning** LiteLLM's gateway integration for Jev comes in two parts — direct decision calls through a pass-through endpoint, and a guardrail that puts Jev inside the request path — with both running behind the same proxy and sharing its controls.

**What it does** Since v1.103.0-rc, a pass-through endpoint proxies requests to `/typesafe/v1/systemone`, so a deployment that already standardizes on LiteLLM can start calling Jev without standing up any new infrastructure. Calls routed this way inherit the gateway's usual controls — logging, budgets, and cost tracking — with Jev usage billed under the model ID `typesafe/jev-1.13.0`. The second integration, the "relevance compression" guardrail, has Jev judge which tool results in a conversation have gone stale and replaces each one with a short hint, trimming the context before it reaches the model. It is configured alongside LiteLLM's other proxy guardrails.

**Characteristics** The pass-through documentation covers the endpoint's configuration, and a blog post announces and explains both parts of the integration. The guardrail runs on the same proxy as the pass-through endpoint. Together, the two pieces keep gateway-side access to Jev — both calling it and letting it shape the context — in one place, with Jev spend visible where every other provider's is.

**When to use** Suits teams already running LiteLLM that want Jev under the gateway's unified logging, budget, and cost governance, as well as conversational pipelines that need stale tool results trimmed from the context before it reaches the model. Deployments not using LiteLLM would have to adopt the gateway first to gain either of these two access paths; budgets and cost reports then cover Jev together with every other provider.

## Links

- [Blog – TypeSafe Jev support](https://docs.litellm.ai/blog/typesafe_jev)
- [Docs – TypeSafe pass-through endpoint](https://docs.litellm.ai/docs/pass_through/typesafe)
- [Docs – TypeSafe guardrail](https://docs.litellm.ai/docs/proxy/guardrails/typesafe)
