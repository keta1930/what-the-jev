---
title: "Spring AI TypeSafe (Spring AI Community)"
updated: 2026-10-09
---

# Spring AI TypeSafe (Spring AI Community)

【定位】Spring 生态的 Jev 集成，由 Christian Tzolov 维护于 spring-ai-community 组织。

【功能】核心是 `TypeSafeClient`，外围是一组把 Jev 映射到 Spring AI 习惯用法的适配器：`JevJudge`、`JevSelfRefineAdvisor`、`JevGuardrailAdvisor`、`JevDocumentFilter`/Reranker、`JevToolIndex` 与 `JevEvaluator`，实现的是 Spring AI 自有的 SPI，而非移植其他框架的接口。自 v0.3.0 起，同一客户端也可指向 Laya、Ollama 等本地决策引擎，两类后端之间切换无需改动调用点。

【特点】两周内从 0.1.0 到 0.3.0 发布三版；发布博客（2026-09-21）介绍各组件及 advisor 在 Spring AI 流水线中的嵌入方式。作为核心 Spring AI 之外的社区项目，发版节奏独立。

【适用】适合基于 Spring AI 构建 Java 应用、需要判定、护栏、文档过滤、工具索引与评估能力的团队，也适合需要在托管与本地决策引擎之间切换的部署。引入时应关注版本与兼容性变化。

## Links

- [Blog – Spring AI TypeSafe: structured judgment](https://spring.io/blog/2026/09/21/spring-ai-typesafe-structured-judgment)
- [GitHub – spring-ai-community/spring-ai-typesafe](https://github.com/spring-ai-community/spring-ai-typesafe)
