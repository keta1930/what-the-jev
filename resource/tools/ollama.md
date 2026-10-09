---
title: "Ollama"
updated: 2026-10-09
---

# Ollama

**Positioning** The local model runtime Ollama supports Jev-style decision models as of version 0.35, serving typed decisions on the local machine through a `/v1/systemone` endpoint, announced on 2026-09-29.

**What it does** A request sends a text `state` with a set of named questions, and a model running on the machine answers all of them in one request, returning answers in the same structure as Jev: choice with per-option probabilities and `confidence`, noul as the probability of yes, and score as the probability-weighted value with a `legend`. The response carries the model name, answers keyed by question id, and token usage, matching the fields Jev clients expect. The official TypeSafe Python SDK works by pointing `TYPESAFE_BASE_URL` at the local port and setting `TYPESAFE_API_KEY` to `ollama`; curl against `http://localhost:11434/v1/systemone` works as well. Use cases named in the official blog post include ticket triage, model routing, and content or safety moderation.

**Characteristics** Three decision models ship initially — `nimble`, `tev1`, and `tev1:0.8b` — fetched with a single `ollama pull nimble` command, with more models including Ollama-cloud-served ones planned. Running locally removes the network round trip, and requests stay on the machine, so state does not travel over a network. In the vendor's own example, Nimble 9B averaged 91ms per decision on an M5 Max (vendor-reported).

**When to use** Suits running a System One-compatible decision service on a personal machine with the least setup, especially for prototyping and latency-sensitive real-time decisions; the endpoint requires version 0.35 or newer. The model selection is still small, and tasks that depend on probability quality should validate thresholds on labeled data before adoption.

## Links

- [Blog – Ollama now supports Jev-style decision models](https://ollama.com/blog/ollama-now-supports-jev-style-decision-models)
- [Website – ollama.com](https://ollama.com)
