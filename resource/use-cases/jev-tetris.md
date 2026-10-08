---
title: "jev-tetris (thelau)"
updated: 2026-10-09
---

# jev-tetris (thelau)

**Positioning** jev-tetris, by thelau, is a demonstration project that plays Tetris with Jev — and measures how well it plays, using explicit control conditions. It works as a compact, fully instrumented experiment on the decision layer's strengths and failure modes.

**What it does** The code enumerates every legal placement of the current piece and writes each one as an English sentence; five parallel Choice questions score the placements; and the board renders Jev's full probability distribution in real time, not just the final move it chooses. The distribution updates as the placements are judged, so how the model rates the options is visible step by step.

**Characteristics** The measurement carries three controls: a "shuffled probabilities" condition, an El-Tetris reference as an upper bound on achievable play, and a 23-line regex baseline. In the project's own measurements the regex baseline beat the model, and the README states this result and the project's limitations. The control design is documented in the README together with the measured results.

**When to use** For observing how Jev behaves and where its capabilities end: the full probability distribution is visible at every step, and the control design — shuffled probabilities, an upper-bound reference, a trivial baseline — is a template that can be reused to probe other decision models the same way. Because every legal placement is enumerated and scored, the task is fully observable: the model sees the same option set a rule-based player would. Note that on this task a simple rule-based baseline outperformed Jev, a result that should be carried along whenever the project is cited.

## Links

- [GitHub – thelau/jev-tetris repository](https://github.com/thelau/jev-tetris)
