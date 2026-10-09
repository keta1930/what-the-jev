---
title: "Rune 26B-A4B (Invergent)"
updated: 2026-10-09
---

# Rune 26B-A4B (Invergent)

**Positioning** Rune is Invergent's open decision model that reads text and images and gives probabilities over candidates in a single forward pass; the project claims the top open-weight position on the Decision Index (self-reported).

**What it does** Text, structured data, or an image can serve as the state, with three question types. The companion surogate engine's decisions endpoint implements its training protocol, and it can also be read as a Gemma 4 checkpoint through transformers by scoring option-letter logits; thinking is off by default.

**Characteristics** Apache-2.0, on a Gemma 4 26B-A4B base (26.5B parameters, 8 of 128 experts active per token), with a 262k context and the vision tower retained. The project reports (self-reported, Decision Index 0.2 full set, bf16, own row) an index of 53.39, above Jev 1.13's 51.67, with Rune v1 at 47.23. At the default temperature it is overconfident (ECE 12.5%), falling to 2.2% at temperature 2. Speed (4 concurrent, single RTX PRO 6000 Blackwell) is a median 388 ms per request. The HF repository is named GGUF, but v3 holds only bf16 safetensors and has no GGUF yet (the v1 GGUF is in a historical revision).

**When to use** Suited to multimodal decisions where an image or structured state must be judged in one pass, and to teams wanting a large-context decision model that also exposes option-letter logits through standard transformers loading. Check the calibration setting first, since the default temperature is overconfident and a temperature of 2 brings ECE down to 2.2%. Note the packaging caveat before planning a deployment: the repository named GGUF does not currently provide v3 GGUF weights, and the v1 GGUF sits in a historical revision.

## Links

- [HF – rune-26b-a4b repository](https://huggingface.co/surogate/rune-26b-a4b-GGUF)
- [GitHub – surogate engine](https://github.com/invergent-ai/surogate)
