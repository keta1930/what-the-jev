---
title: "JevBench (Benchmark Heaven)"
updated: 2026-10-09
---

# JevBench (Benchmark Heaven)

**Positioning** JevBench is Benchmark Heaven's own benchmark for Jev-class decision models (independent, third-party source). It is not affiliated with or endorsed by TypeSafe AI; Jev is simply one of the systems measured.

**What it does** A system under test is handed a state and a bounded rubric and returns a typed answer, ideally with a probability for every option. The board iterates fast — v1.0 through v1.4.x at review time, with a frozen v1.5 method index — and covers 95 systems, 91 of which are ranked. The frozen v1.5 method index fixes the methodology for that version. As of v1.4.2.2 the top of the board reads: Imajev-4B 67.37, Plumb-4B 65.84, decider-4b v2 64.13, Jev 1.13.0 63.29, JevK5 v0.2.0 62.04.

**Characteristics** The JevBench Score blends four equal-weight axes — chance-corrected Intelligence, Calibration, Speed, and Cost — via a geometric mean, with the Cost axis priced per 1,000 decisions rather than per 1,000 tokens. Items are frozen and hashed before any system runs, a private hard tier is held out, only aggregate sealed statistics are published, cost corrections are logged with tests, and a service that resells another entrant's model is listed but not ranked. The MIT-licensed harness is reproducible end to end; the project is a one-person effort paid out of pocket.

**When to use** Suited to readers tracking rankings of Jev-class decision models, or wanting to reproduce the evaluation with the MIT-licensed harness. Always attach a version number when citing a ranking — the figures above belong to v1.4.2.2. Despite the similar name, JevBench is a different project from PavelRavich's jev-bench benchmark listed separately in this collection.

## Links

- [GitHub – JevBench repository](https://github.com/fstandhartinger/jevbench)
- [Website – live board](https://benchmarkheaven.com/jev-models)
