---
title: "Spring AI TypeSafe (Spring AI Community)"
updated: 2026-10-09
---

# Spring AI TypeSafe (Spring AI Community)

**Positioning** A Spring-ecosystem integration for Jev: it is maintained by Christian Tzolov, hosted under the spring-ai-community organization, and developed as a community project outside core Spring AI.

**What it does** At its center is a `TypeSafeClient`, and around it sits a set of adapters that map Jev onto Spring AI idioms: `JevJudge`, `JevSelfRefineAdvisor`, `JevGuardrailAdvisor`, a `JevDocumentFilter`/Reranker, `JevToolIndex`, and `JevEvaluator`. The six adapters implement Spring AI's own SPI rather than porting the interface of some other framework. From v0.3.0 onward, the same client can also be pointed at local decision engines such as Laya or Ollama, so an application can switch between hosted Jev and a local engine without changing its call sites, and the Jev-specific abstractions stay stable across those backends.

**Characteristics** The project shipped three releases, 0.1.0 through 0.3.0, within two weeks. The launch blog post, dated 2026-09-21, walks through each of the components and shows how the individual advisors fit into a Spring AI pipeline. The blog post and the repository cover setup and component usage. As a community-maintained project, it follows its own release cadence rather than Spring AI's.

**When to use** Suits teams building Java applications on Spring AI that need judging, guardrails, document filtering and reranking, tool indexing, and evaluation capabilities in their pipelines, as well as deployments that want the option of a local decision engine such as Laya or Ollama alongside hosted Jev. Both kinds of backend sit behind the same client. Because the project is community-maintained and releases on its own cadence, track version and compatibility changes when adopting it for production use.

## Links

- [Blog – Spring AI TypeSafe: structured judgment](https://spring.io/blog/2026/09/21/spring-ai-typesafe-structured-judgment)
- [GitHub – spring-ai-community/spring-ai-typesafe](https://github.com/spring-ai-community/spring-ai-typesafe)
