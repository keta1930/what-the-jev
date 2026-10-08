---
title: "decider (Mapika)"
updated: 2026-10-09
---

# decider (Mapika)

**Positioning** decider is Mapika's family of open, System One-style decision models — the same category as Jev — released under Apache-2.0 with code, weights, and the full training recipe public. Its question types match Jev's, covering choice, score, and noul, the three types Jev answers.

**What it does** Across its sizes, a single forward pass produces the probability distributions over Choice, Score, and Noul answers. The RL stage optimizes calibration directly through log scoring, and calibration temperatures are maintained as an independent system rather than folded into the weights. The training recipe — a mixture of 95 public datasets — is published in full, so the run can be reproduced from it.

**Characteristics** The family spans 0.8B to 35B-A3B, including Gemma-4-12B and Gemma-4-31B variants plus GGUF, NVFP4, and NPU ports, which extend the same family to smaller-footprint hardware. Per the project's published results (self-reported): on JevBench v1.5.2, decider-4b v2 ranks #7 of 99, with Jev itself at #3; on the Decision Index, the chat-oriented decider-chat-gemma4-31b ranks #2 of 70 with an ECE of 0.047. The benchmark tables are kept in the repository's RESULTS.md, and both leaderboard readings above come from those tables. Development is ongoing, with releases still shipping as of 2026-10-07.

**When to use** For teams that need a self-hostable decision model whose question types match Jev's — choice, score, and noul — and that must run across many hardware targets, including the GGUF, NVFP4, and NPU builds that ship alongside the main checkpoints. Its JevBench scores remain below Jev itself, which matters when selecting against that leaderboard; on that version, it sits inside the top ten of 99 entries but under Jev.

## Links

- [GitHub – Source code and training recipe](https://github.com/Mapika/decider)
- [HF – decider-4b weights](https://huggingface.co/Mapika/decider-4b)
- [Docs – RESULTS.md benchmark tables](https://github.com/Mapika/decider/blob/main/docs/RESULTS.md)
