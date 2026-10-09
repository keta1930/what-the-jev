---
title: "Microsoft Agent Framework: agent-framework-typesafe"
updated: 2026-10-09
---

# Microsoft Agent Framework: agent-framework-typesafe

**Positioning** An official alpha package that adapts TypeSafe System One models, including Jev, to the Microsoft Agent Framework Python chat client contract. It maps TypeSafe's structured decision API onto that contract, so Jev evaluates application state against explicit typed questions and returns probabilities and scores rather than ordinary chat text (official).

**What it does** For this connector, Agent Framework's `response_format` option is a TypeSafe `Questions` mapping; the connector forwards it as the SDK's `questions` argument and uses `SystemOneResponse` as the actual response model. `Noul`, `Choice`, and `Score` questions are supported, and `default_questions` on the client lets a fixed contract omit per-call configuration. Tool selection and supported arguments are converted into internal `Choice` and `Noul` questions that emit Agent Framework function calls; MCP tools are supported through `Agent`, which expands discovered functions into `FunctionTool` objects. `TypeSafeChatClient` is the recommended client, layering function invocation, middleware, and telemetry over `RawTypeSafeChatClient`, which is for composing a custom layer stack. Internally created clients read `TYPESAFE_API_KEY`, `TYPESAFE_DEFAULT_MODEL`, and `TYPESAFE_BASE_URL`, defaulting to the `jev-latest` model at `api.typesafe.ai`. Streaming, non-text message content, and generative settings such as `temperature` are rejected (official).

**Characteristics** The package is alpha, installed with `pip install agent-framework-typesafe --pre`, and Python-only; .NET is not supported. It is MIT licensed. PyPI lists version 1.0.0a261002, released 2026-10-02 (PyPI). A request supports at most 32 routable tools, 64 properties per tool, 64 enum members per argument, and 128 generated internal questions (official).

**When to use** Suits Microsoft Agent Framework Python agents that need typed decisions for routing, tool-call gating, or judging. It does not fit .NET, streaming output, or tasks that require generative text.

## Links

- [GitHub – microsoft/agent-framework python/packages/typesafe](https://github.com/microsoft/agent-framework/tree/main/python/packages/typesafe)
- [Docs – TypeSafe AI, Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/integrations/by-provider/type-safe-ai)
- [PyPI – agent-framework-typesafe](https://pypi.org/project/agent-framework-typesafe/)
