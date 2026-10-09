---
title: "Nimble (Bespoke Labs)"
updated: 2026-10-09
---

# Nimble (Bespoke Labs)

**Positioning** Nimble is an open alternative to Jev from Bespoke Labs that releases the data, model, and training recipe together, as a one-step typed text decision model.

**What it does** A single request carries a state and a question schema of enum and boolean fields; the model scores candidate answer tokens directly and returns the selected answer with a probability for each option, with no reasoning output. Prompts are limited to 8,192 tokens, and choice and score questions support 2 to 26 options. The project provides a Jev-compatible `/v1/systemone` server along with public data and evaluation scripts, and Nimble is one of the first decision models released in Ollama 0.35, installed with `ollama pull nimble` (Q8_0, about 9.53 GB).

**Characteristics** Built on a Qwen3.5-9B backbone with LoRA. On a 324-sample held-out set the project reports (self-reported) 90.12% agreement with reference labels (292/324), against 66.36% for the base model and 93.21% for Jev 1.13.0; an Ollama official example reports an average 91 ms per decision on an M5 Max (self-reported). JevBench v1.2.8 lists a Bespoke Nimble 9B row. Licensing is split by version: Bespoke-Nimble-9B is Apache-2.0, while Bespoke-Nimble-9B-v3 is CC BY-NC 4.0 (non-commercial). The GitHub repository shows 2.1k stars, with the latest commit on 2026-10-05.

**When to use** Suited to teams that want the whole stack open — data, weights, and recipe — and to run typed decisions locally or behind a Jev-compatible self-hosted service, where the Ollama build lowers setup cost. The v3 weights are non-commercial, so commercial deployment must first confirm which version it uses. Because the model returns only choices and probabilities and no explanations, tasks that need stated reasons are out of scope.

## Links

- [GitHub – Source code](https://github.com/bespokelabsai/nimble)
- [HF – Bespoke-Nimble-9B weights](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B)
- [Blog – Ollama support for Jev-style decision models](https://ollama.com/blog/ollama-now-supports-jev-style-decision-models)
