---
title: "jev-bench (PavelRavich)"
updated: 2026-10-09
---

# jev-bench (PavelRavich)

**Positioning** jev-bench is a solo, independent benchmark by Pavel Ravich (GitHub: PavelRavich) that tests TypeSafe's Jev decision model against the GPT-6 Luna and GPT-6 Astra models on decision-style tasks, with both datasets framed in Jev's typed question formats (Noul and Choice).

**What it does** It uses two datasets of 500 samples each: SMS Spam, framed as Noul (binary) questions, and Banking77, framed as a 77-class Choice task. Both datasets are framed in Jev's typed question formats — Noul and Choice. For every combination of model and dataset it reports accuracy, macro-F1, ECE, Brier score, p50 and p95 latency, and cost per 1,000 calls, with bootstrap confidence intervals throughout. A long-form write-up on Medium documents the methodology and the author's reading of the results.

**Characteristics** The entire run cost $1.13 in total, random seeds are fixed, and the repository doubles as a reproducible archive of the evaluation. The benchmark was completed in September 2026 and is archived rather than actively developed, which fits its nature as a point-in-time snapshot: as Jev and the GPT-6 models change, re-running the published code with newer models is the way to check whether its conclusions still hold.

**When to use** Useful for readers who want a small-scale, low-cost comparison between Jev and the GPT-6 models with a complete metric report, or a reference implementation for building similar evaluations of their own. Note the name collision: it is unrelated to the community leaderboard JevBench listed separately in this collection — the two projects share only a similar name — and its conclusions reflect the models as of September 2026.

## Links

- [GitHub – jev-bench repository (code, fixed seeds, results)](https://github.com/PavelRavich/jev-bench)
- [Blog – independent benchmark write-up](https://medium.com/@pravvich/typesafes-jev-beyond-the-hype-an-independent-benchmark-8bdc1c99d000)
