---
title: "Semantic Router (aurelio-labs) (same-paradigm reference)"
updated: 2026-10-09
---

# Semantic Router (aurelio-labs) (same-paradigm reference)

**Positioning** Semantic Router, by aurelio-labs, is an open-source project that describes itself as a superfast decision layer for LLMs. It predates Jev by a generation and is included here as a same-paradigm reference: the same goal — low-latency decisions for LLM applications — approached with embeddings and similarity rather than typed probabilistic answers. Where Jev would answer typed questions with calibrated probabilities, Semantic Router matches inputs to routes by encoder similarity. It is the closest open-source counterpart to Jev's positioning as a low-latency decision layer from the generation before Jev.

**What it does** Routing and tool decisions are made in a semantic vector space rather than by having an LLM generate text: an input is compared against the defined routes through an encoder, and the matching route is returned without generating anything. You define Routes, choose an Encoder, and a RouteLayer then returns a matching route in tens of milliseconds (project-reported). The routes, the encoder, and the match threshold are all defined in application code. Local models, multimodal inputs, and threshold optimization — for deciding when a route counts as a match — are supported out of the box.

**Characteristics** The project is currently being rewritten for its 1.x release, so some churn in its public APIs is to be expected before that lands.

**When to use** For latency-sensitive routing and tool-selection workloads, it is the pre-Jev point of comparison when benchmarking a decision layer, and reading it alongside Jev frames the design space of decision layers. Because the 1.x rewrite is in progress, integrations that need stable APIs should account for the expected churn.

## Links

- [GitHub – aurelio-labs/semantic-router repository](https://github.com/aurelio-labs/semantic-router)
- [Docs – Semantic Router on aurelio.ai](https://aurelio.ai/semantic-router)
