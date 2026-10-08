---
title: "Decision Index"
updated: 2026-10-09
---

# Decision Index

**Positioning** Decision Index is a third-party benchmark for typed decision engines — models that take a state plus typed questions (choice or noul with explicit criteria) and return one answer per question with a probability for every supplied option. It is not affiliated with TypeSafe AI.

**What it does** Its GitHub repository is a full reproduction kit: anyone can rebuild the frozen suite from pinned public sources, run any engine against it (an HTTP engine speaks the /v1/systemone wire format; a transformers engine scores stock causal LMs in one forward pass), and score results with the leaderboard's own scorers. The live board is Decision Index 0.3; the public suite covers 37 benchmarks in five areas — Knowledge & Reasoning, Language Understanding, Retrieval & Classification, Tools & Automation, Arts & Human Taste — over roughly 110,000 requests. Parity tests reproduce the published per-benchmark results of the board's entrants, Jev included. A Vision board ranks image-reading models, and a separate Reasoning board is planned.

**Characteristics** The main ranking, the Full score, is 20% public benchmarks, 50% private tests of the same skills, and 30% private decision tasks from new domains — most of the score comes from tests nobody can train on — with each benchmark chance-corrected and coverage-adjusted. Editions 0.1–0.3 remain reproducible side by side, and entries shift as models are re-run.

**When to use** Suited to readers comparing typed decision engines, or wanting to run their own engine against the suite; the frozen suite must first be rebuilt from pinned public sources via the reproduction kit. Check the edition and dates before citing a rank. A companion Hugging Face tracker (multimodalart) separately logs the open-source Jev replication wave entry by entry.

## Links

- [GitHub – Decision Index reproduction kit (apolinario)](https://github.com/apolinario/decision-index)
- [HF Space – Jev reproductions tracker (multimodalart)](https://huggingface.co/spaces/multimodalart/jev-reproductions-tracker)
