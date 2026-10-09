---
title: "classifier-benchmark (jabr)"
updated: 2026-10-09
---

# classifier-benchmark (jabr)

**Positioning** classifier-benchmark, by jabr, is a head-to-head benchmark for "System One"-style classification models — lightweight decision models that answer structured questions on a state — covering the three primitives choice, noul, and score.

**What it does** Every model answers the same question JSON for the same tasks. Two hash-locked suites are provided: v1 with 8 tasks and 78 cases, and v2 with 49 tasks and 866 cases, the latter extending every v1 question and adding adjacent- and distant-domain tasks with no case overlap. Suites are plain TOML case files with a documented schema, so harnesses in languages other than Python can read the cases directly, and `just validate` checks each suite's content hash against a stored value. All cases are synthetic, generated and cross-checked by a committee of language models that contributed to task definition, expansion, and review, with debatable cases removed before freezing. The project notes the cases are public and may be incorporated into training data.

**Characteristics** On the v2 suite (49 tasks, 866 cases; Apple MPS), the reported headline results are Jev micro accuracy 0.964 and macro accuracy 0.966 at roughly 330 ms and about $0.000014 per call, against Von 1.1 at 0.724, GLiNER2 at 0.688, and Laya at 0.585 micro accuracy (the repository's own figures). Model backends include local Von, GLiNER2 and a decision-tuned GLiNER2.5, Laya, and the hosted `typesafe/jev-1.13`. The repository is released under CC0 1.0, with per-task scoreboards and raw per-case JSON committed alongside the harness.

**When to use** Suited to comparing Jev with small local classifiers on the choice, noul, and score primitives under one shared question format. Because the cases are synthetic and may enter training data, treat the numbers as one comparison rather than evidence of generalization, and cite the suite version with any figure.

## Links

- [GitHub – jabr/classifier-benchmark repository](https://github.com/jabr/classifier-benchmark)
