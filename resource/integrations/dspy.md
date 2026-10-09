---
title: "DSPy TypeSafe Integration"
updated: 2026-10-09
---

# DSPy TypeSafe Integration

**Positioning** DSPy 3.4.0, released 2026-09-25, introduced an experimental Jev/TypeSafe integration (GitHub release and official tutorial) that lets DSPy programs call Jev through the same `lm=` interface used for other language models. Instead of parsing generated text, a program expresses its judgment steps as typed decisions that carry probability evidence.

**What it does** Importing `TypeSafe`, `Noul`, `Score`, `Choice`, and `ReAnchor` from `dspy.experimental` and calling `dspy.configure(lm=TypeSafe("jev-latest"))` makes `Predict` translate a signature, its inputs, demonstrations, and field criteria into Jev decision requests automatically. `Noul`, `Choice`, and `Score` return boolean, option, and ordered-rubric decisions with probability evidence, and thresholds, score cuts, and choice weights are applied locally so identical requests can reuse cached evidence. The `ReAnchor` optimizer fits `Noul` thresholds, score cuts, and choice weights against the program's metric, with five-fold checks. The defaults are `jev-latest` and `api.typesafe.ai`, with the same environment variables as the other TypeSafe clients. Installation is `pip install "dspy[typesafe]"`, which requires `typesafe-sdk>=0.6.0,<1.0.0` and is not added to the base installation.

**Characteristics** The Jev backend supports no generative settings such as `temperature` and offers no automatic generative fallback, so every output field must be a supported decision type; decision streaming and RLM decision outputs are unsupported (official). The APIs are experimental and may change. The integration was contributed by @isaacbmiller and @dbreunig (PR #10463, #10475).

**When to use** Suits teams that use DSPy optimization and calibration workflows and want to hand judgment steps to Jev while keeping cacheable probability evidence, with the `ReAnchor` optimizer fitting decision parameters against the program's own metric. It does not fit scenarios that need a generative fallback, nested decision outputs, or streaming.

## Links

- [Docs – Jev decisions tutorial](https://dspy.ai/current/tutorials/jev_decisions/)
- [GitHub – DSPy 3.4.0 release](https://github.com/stanfordnlp/dspy/releases/tag/3.4.0)
- [GitHub – PR #10463](https://github.com/stanfordnlp/dspy/pull/10463)
