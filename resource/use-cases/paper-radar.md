---
title: "JEV Paper Radar (Eliot5566)"
updated: 2026-10-09
---

# JEV Paper Radar (Eliot5566)

**Positioning** JEV Paper Radar, by Eliot5566, is a daily paper radar built on Jev: every day it screens the full feed of newly listed arXiv papers against each interest the reader declares. The declared interests are the reader's own, and the radar asks about them on every paper.

**What it does** For every newly listed arXiv paper — the full feed, not a curated subset — it asks one Jev Noul question per declared interest, then renders the hits as a generated must-read page plus an RSS feed. The whole pipeline is fork-and-go: fork the repository and it runs, with no server of your own to operate. A calibrate command ships with the repo so thresholds can be tuned against a reader's own judgment.

**Characteristics** The author's measured benchmark: 501 papers screened in 33 seconds for $0.0196. A systematic-review screening mode reproduced 96.9% recall across 4 Cochrane reviews while cutting 78% of the screening workload. All of these figures are self-reported by the author, not third-party verified.

**When to use** Suits low-cost screening of large document flows, such as daily paper tracking or the first pass of a systematic review — for reviews, the screening mode is the relevant one to evaluate first, since its recall figures were measured against Cochrane reviews. The calibrate command lets a reader set thresholds against their own judgment. Its usage pattern is many small, cheap, calibrated decisions at corpus scale: one lightweight typed question per paper per interest. The recall and workload numbers are author-reported, so before relying on them, run the calibrate command against your own judgments and thresholds.

## Links

- [GitHub – Eliot5566/JEV-Paper-Radar repository](https://github.com/Eliot5566/JEV-Paper-Radar)
- [Demo – generated must-read page](https://eliot5566.github.io/JEV-Paper-Radar/public/)
