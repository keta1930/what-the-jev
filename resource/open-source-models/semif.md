---
title: "SemIf (TheoLeeCJ, formerly OpenJev)"
updated: 2026-10-09
---

# SemIf (TheoLeeCJ, formerly OpenJev)

**Positioning** SemIf (formerly OpenJev), by TheoLeeCJ, takes a zero-training route to Jev-style decisions. It trains and releases no weights of its own; instead it reads option probabilities directly from frozen open models in a single forward pass, with no decode loop. Instead of fine-tuning anything, it repurposes models that already exist. The code is MIT-licensed and runs on commodity hardware.

**What it does** Supported base models include Qwen3-0.6B, MiniCPM5-2B, Qwen3.5-4B, and Qwen3.5-27B EXL3, small through mid-size open checkpoints. The project ships a WebGPU browser demo, shared-prefix parallelism that the project reports at 20 decisions per second, and per-workload temperature calibration for each deployment's workload mix. Because nothing is trained, switching to a different base model is a configuration choice rather than a retraining project.

**Characteristics** It is widely cited across the community as the origin of the logit-readout protocol, and JevK5 among other systems explicitly acknowledges it. It has gathered roughly 1.7k–1.8k GitHub stars. A community CPU port, JEV-CPU, runs the same approach on CPU and circulates on Hugging Face.

**When to use** For running typed decisions on commodity hardware with no training budget — the project describes it as the cheapest entry point into typed decisions, and the browser demo lets a team try the flow before allocating anything. Since no weights are trained, quality and language coverage depend entirely on whichever frozen base model it is pointed at: tasks beyond the base model's reach stay out of scope, accuracy cannot be lifted by fine-tuning within this project, and switching to a stronger base model is the available lever within it.

## Links

- [GitHub – SemIf source code](https://github.com/TheoLeeCJ/SemIf)
- [HF – JEV-CPU community port](https://huggingface.co/Meanblock/JEV-CPU)
