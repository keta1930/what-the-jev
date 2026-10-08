---
title: "Pydantic AI TypeSafeModel"
updated: 2026-10-09
---

# Pydantic AI TypeSafeModel

**Positioning** Pydantic AI's built-in integration for Jev: `TypeSafeModel` is a subclass of the framework's `DecisionModel`, and it lets Python agents call Jev through the same API they already use for LLMs, keeping decision calls inside the framework's standard model interface.

**What it does** The integration derives Jev questions automatically from Pydantic output types — a field's docstring becomes the question text — so one typed schema doubles as the questionnaire sent to the model, with no separate set of questions to write by hand. The same schema drives both the output type and the questions. Because the model sits inside Pydantic AI, it composes with the rest of the framework: a `FallbackModel` can escalate a request to a conventional LLM when Jev's answer is not enough, thresholds are exposed as configurable settings, and context compression is supported for long inputs.

**Characteristics** The documentation states Jev's operating envelope in numbers: a 255-option limit for choice questions, a 10-level rubric ceiling for score questions, and a 32k limit, plus a list of where Jev falls short of a generative model. That account of the boundaries serves developers wiring Jev from other stacks as well.

**When to use** Suits Python teams already building agents in Pydantic AI that want typed, probabilistic decisions behind their structured outputs, with `FallbackModel` combining Jev and a conventional LLM in one path. Because the questions are derived from the schema, the question set stays aligned with the type definitions in the code. Work that needs generated text or exceeds the option, rubric, or 32k input limits should go to the LLM side of the fallback.

## Links

- [Docs – TypeSafeModel](https://ai.pydantic.dev/models/typesafe/)
- [GitHub – pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
