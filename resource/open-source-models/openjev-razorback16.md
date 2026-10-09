---
title: "OpenJev (razorback16)"
updated: 2026-10-09
---

# OpenJev (razorback16)

**Positioning** OpenJev is razorback16's independent open-source System One decision server: it answers typed decisions on open models through the same Jev wire API, reading model probabilities instead of parsing generated text, so answers stay inside the schema.

**What it does** `POST /v1/systemone` returns probabilities and a confidence value, supporting noul, choice, and score questions with up to 255 options, and it also accepts image input such as documents and screenshots. The default model, `openjev-0.1` / `openjev-latest`, runs DiffusionGemma 26B-A4B (26B total, 4B active, from Google/NVIDIA, Apache-2.0) through vLLM or MLX; other small models such as Laya, Verdict, CLM, and JevK5 can be mounted as well. It is additionally hosted free on Codiv, where registration grants 100 million input tokens. The server code is Apache-2.0.

**Characteristics** JevBench v1.2 lists it as "OpenJev razorback16 (DiffusionGemma 26B)" at overall rank #11 with a combined 66.4. The name is shared with unrelated projects: the pre-converted `ggml-org/OpenJev-GGUF` shipped with llama.cpp is a different model — 27B, on a Qwen3.8-27B backbone, with CC BY-NC 4.0 weights and about 43 ms per question according to the llama.cpp official blog — and other same-named items include `apus-ailab/APUS-OpenJev-v1`, "openJev Verdict", and "open-jev (MLX)". Cite these with their owner. The GitHub repository has 650 stars and 59 commits.

**When to use** Suited to developers who want a drop-in Jev-compatible endpoint over open models, including image input, or who want to compare several model backends behind one server. Before installing or comparing, confirm which project a given "OpenJev" artifact belongs to, since the name covers several unrelated releases. Not suited to tasks that need a generated explanation rather than a probability distribution.

## Links

- [GitHub – Decision server source code](https://github.com/razorback16/openjev)
- [HF – ggml-org OpenJev-GGUF (different project)](https://huggingface.co/ggml-org/OpenJev-GGUF)
- [Blog – Decision models in llama.cpp](https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp)
