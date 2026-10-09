---
title: "System One Mosaic Benchmark (S1MB)"
updated: 2026-10-09
---

# System One Mosaic Benchmark (S1MB)

**Positioning** The System One Mosaic Benchmark (S1MB), by hotchpotch, is a leaderboard project that compares Jev with open decision models across more than 100 benchmarks.

**What it does** Models are evaluated on the same inputs and metrics for the three decision types — Choice, Noul, and Score — and the mosaic combines tasks from existing public NLP datasets with synthetic tasks in one workflow. The English suite contains 137 benchmarks across 106 dataset subsets, including six synthetic benchmarks that probe how models respond to varied instructions, contexts, and decision criteria. Results record exact dataset and model revisions, evaluator provenance, and effective inference settings. Supported adapters include TypeSafe/Jev and Bekko; other models can implement the typed adapter contract or be submitted as community results through a Hugging Face dataset pull request.

**Characteristics** The viewer sorts by Borda Score, a relative ranking with equal weight per benchmark that can change when the model roster changes; Task Avg is a separate 0–100 baseline-adjusted score with equal weight across the three tasks, and both require complete coverage in the selected scope. The repository holds a Python evaluator and a Next.js viewer and is MIT-licensed; created 2026-09-29, last pushed 2026-10-08. A companion blog post reports Jev 1.13 at Task Avg 96.27 and Borda 97.73 in first place (the author's own figures).

**When to use** Suited to tracking rankings of Jev-class decision models and inspecting which tasks a model handles or struggles with. Coverage is still expanding, and the project states that its scores do not establish unseen-task generalization or training-data non-overlap; cite any ranking together with its version.

## Links

- [GitHub – hotchpotch/S1MB repository](https://github.com/hotchpotch/S1MB)
- [HF – System One Mosaic Benchmark blog](https://huggingface.co/blog/hotchpotch/system-one-mosaic-benchmark)
