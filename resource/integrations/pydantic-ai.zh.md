---
title: "Pydantic AI TypeSafeModel"
updated: 2026-10-09
---

# Pydantic AI TypeSafeModel

【定位】Pydantic AI 框架内置的 Jev 集成：`TypeSafeModel` 是框架 `DecisionModel` 的子类，让 Python agent 以调用 LLM 的同一套 API 使用 Jev，决策调用保持在框架的标准模型接口之内。

【功能】集成从 Pydantic 输出类型自动推导 Jev 问题，字段的 docstring 即提问文本，一份类型化 Schema 同时就是发给模型的问题清单，无需另行编写问题。`FallbackModel` 可在 Jev 的答案不够用时把请求升级到常规 LLM，阈值以 setting 形式配置，并支持上下文压缩以处理长输入。

【特点】文档以数字写明 Jev 的运行边界：choice 问题最多 255 个选项，score 问题 rubric 上限 10 级，另有 32k 限制，并列出 Jev 相比生成式模型的短板。这份边界说明对从其他技术栈接入 Jev 的开发者同样可作参考。

【适用】适合在 Pydantic AI 中构建 agent、要为结构化输出引入决策模型的 Python 团队，可经 `FallbackModel` 将 Jev 与常规 LLM 组合在同一链路。需要文本生成或超出选项数、rubric 级数与 32k 输入边界的任务，应交给 LLM 侧处理。

## Links

- [Docs – TypeSafeModel](https://ai.pydantic.dev/models/typesafe/)
- [GitHub – pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
