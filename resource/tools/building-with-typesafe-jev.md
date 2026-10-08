---
title: "building-with-typesafe-jev (aaddrick)"
updated: 2026-10-09
---

# building-with-typesafe-jev (aaddrick)

**Positioning** building-with-typesafe-jev is an unofficial skill for coding agents, published by aaddrick. Its premise is that a Jev answer is only as good as the question fed to the model, so the skill's core job is teaching an agent to design the questions it asks deliberately.

**What it does** The teaching covers three levers: choosing among the question types, applying a set of 11 design rules, and setting thresholds. Alongside the teaching, the package bundles three kinds of material: an API reference; the official four usage patterns together with the 18 thresholds the cookbook lists; and a library of 150+ precedents grouped by "implementation shape." On receiving a task, an agent can look up a worked example close to it in the precedent library, then adjust what it finds against the rules and thresholds before writing the final question.

**Characteristics** The skill ships with its own evaluation, which reports that average scores rise from 0.65 to 0.96 when the skill is installed. That figure is self-reported: it was measured with the author's own harness and has not been independently verified by others. The project is a community one with no affiliation to TypeSafe AI.

**When to use** It suits teams that want a coding agent to approach question design — choosing types, applying rules, setting thresholds — in a systematic way before it calls Jev. Its rules and thresholds are one author-assembled opinion rather than an official standard, so they should be reviewed before being adopted wholesale. Treat the 0.65-to-0.96 gain as the author's own measurement, and cite it as self-reported wherever it appears.

## Links

- [GitHub – aaddrick/building-with-typesafe-jev](https://github.com/aaddrick/building-with-typesafe-jev)
