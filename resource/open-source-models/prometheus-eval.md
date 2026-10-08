---
title: "Prometheus / Prometheus-Eval"
updated: 2026-10-09
---

# Prometheus / Prometheus-Eval

**Positioning** Prometheus is a family of open-weight judge models, models that score other models' outputs, developed by a KAIST-led team. It predates Jev and appears here as an early example of the same paradigm: structured evaluation of model outputs with reproducible open weights rather than a closed API. The family targets evaluation workloads, not the typed decision interface Jev defines.

**What it does** Prometheus 2 offers 7B and 8x7B models that perform absolute scoring on a 1–5 scale and pairwise comparison between two outputs. The 7B model is the one with a public weights page listed here; the 8x7B is the larger sibling. The project reports agreement with human judgments in the 72–85% range (project-reported). In 2025-04 the line extended to the multilingual M-Prometheus at 3B, 7B, and 14B, widening language coverage beyond the earlier releases.

**Characteristics** The surrounding toolkit includes the prometheus-eval pip package, training scripts, and the BiGGen-Bench suite — a complete evaluation stack rather than a bare model release, with both scoring runs and training covered by shipped code. The two scales — the 7B and the larger 8x7B — serve those evaluation workloads rather than Jev-style typed decision interfaces. The repository is still maintained, though the release cadence has slowed.

**When to use** For judging and scoring model outputs — LLM-as-judge workflows. A Jev question returns a typed answer with calibrated probabilities; a Prometheus run returns a generative score and a written judgment. That is the key difference: Prometheus does not produce calibrated probability distributions over typed noul/choice/score answers, so in typed-decision pipelines it complements a decision model rather than substituting for one.

## Links

- [GitHub – prometheus-eval library and training code](https://github.com/prometheus-eval/prometheus-eval)
- [HF – prometheus-7b-v2.0 weights](https://huggingface.co/prometheus-eval/prometheus-7b-v2.0)
