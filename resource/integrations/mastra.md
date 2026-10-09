---
title: "Mastra Classifier"
updated: 2026-10-09
---

# Mastra Classifier

**Positioning** Mastra's Classifier primitive (`@mastra/core/classifier`) asks any AI SDK evaluation model fixed-domain questions and returns typed answers with probabilities; the official example uses Jev as the core model through `@ai-sdk/typesafe-ai` (Mastra blog and docs). It serves decisions a program can act on without parsing generated text.

**What it does** A Classifier defines several named choice, score, and boolean questions over shared state and evaluates them together in one call, keying each answer by question name so downstream code can branch on it. Around it sit `createClassifierScorer()`, which maps one question to a 0-1 scorer value while retaining evidence, `ClassifierProcessor` for input and output content guardrails, `ModelSelectionProcessor` for cost routing, and a workflow `.classifier()` step (official releases and docs). Classifiers are registered through `Mastra({ classifiers })` and referenced by ID. A Classifier returns evidence only; the application holds thresholds and blocking policy (official).

**Characteristics** The timeline (third-party compilation): Classifier merged 2026-09-22 (#24458), registration #24738, ClassifierProcessor 2026-09-23 (#24768), and `createClassifierScorer()` in `@mastra/core@1.70.0` (#24792). In an official test, classifying 78 open-source issue titles and bodies with Jev put about 10 of 78 classifications in line with the maintainer's own judgment; the accompanying post states that tasks requiring evidence gathering or multi-step reasoning are not a good fit, and that an agent can collect the evidence first (official self-report).

**When to use** Suits Mastra agents that need workflow branching, tool approval, content guardrails, and evals such as classifier-as-judge. Where a task needs evidence or several reasoning steps, an agent can gather the evidence first and a classifier can then evaluate the resulting state.

## Links

- [Docs – Classifier reference](https://mastra.ai/reference/classifier/classifier)
- [Blog – Introducing classifiers with Jev](https://mastra.ai/blog/introducing-classifiers-with-jev)
- [Docs – Jev](https://mastra.ai/articles/jev)
