---
title: "Ollaya (ollaya-dev)"
updated: 2026-10-09
---

# Ollaya (ollaya-dev)

**Positioning** Ollaya is a local runtime for decision models, created by Mert Cobanov and described as "Ollama for decision models". It pulls decision models by name, serves them from a local daemon, and implements TypeSafe's `/v1/systemone` wire format directly, so an existing Jev client connects by changing a single environment variable and nothing else in the client has to change.

**What it does** Models are fetched by name — `laya`, `decider`, `kev`, `nimble`, `winnow`, `jevk5`, `jeeves`, `clef`, `jeb`, `nli`, `gliclass`, `qwen3guard` and others — and run behind the local daemon. The endpoints `POST /v1/systemone`, `POST /v1/decisions` and `GET /v1/models` follow TypeSafe's wire format, so the official TypeSafe SDK reaches the local server once `TYPESAFE_BASE_URL` points at its port. The runtime is written in Rust and organized as a Cargo workspace that also holds desktop, docs, site and skills components.

**Characteristics** The runtime is Apache-2.0, and each model keeps its own license: Laya comes from ConvAI, decider from Mapika and kev from Jared Palmer, among others. The project's website publishes self-run numbers at ollaya.dev/results, covering public benchmarks, speed on each machine, and parity against the authors' own code. As of 2026-10-09 the GitHub repository had 1,259 stars and 72 forks; it was created on 2026-09-23 and last pushed on 2026-10-06, the same day it released v0.10.0, v0.11.0 and v0.12.0.

**When to use** Suits running decision models locally in an Ollama-style workflow while keeping compatibility with existing Jev clients. The project was created on 2026-09-23 and is about two weeks old; it published three releases on a single day, so its maturity should be assessed before adoption.

## Links

- [GitHub – ollaya-dev/ollaya](https://github.com/ollaya-dev/ollaya)
- [Website – ollaya.dev](https://ollaya.dev)
- [HF – ollaya-dev](https://huggingface.co/ollaya-dev)
