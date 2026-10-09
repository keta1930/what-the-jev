---
title: "Swama (Trans-N-ai)"
updated: 2026-10-09
---

# Swama (Trans-N-ai)

**Positioning** Swama is a local AI runtime built for Apple Silicon Macs by Trans-N-ai. It is written in Swift, sits on top of Apple's MLX framework through `mlx-swift`, is a native implementation, and it installs through Homebrew.

**What it does** The runtime can run language, vision, embedding, speech-recognition and text-to-speech models. Beyond generation, it exposes an OpenAI-compatible API, a command-line interface and a menu bar app. Decision questions are served on two endpoints: `POST /v1/decisions`, which follows the OpenAI Decisions API style with `predicate`, `choice` and `score` questions, and `POST /v1/systemone`, a SystemOne OpenAPI 0.2.0 adaptation layer that reuses the same decision scorer as the Decisions endpoint. The `/v1/systemone` route accepts an explicit local `model`, a text or structured `state`, and named `questions`, and the TypeSafe JavaScript SDK can call it once it points at the local base URL. Image input is accepted as base64 data URLs carrying PNG, JPEG or WebP data.

**Characteristics** Swama is MIT-licensed, and its README ships in English, Chinese and Japanese. The README notes that the confidence a model reports is a "concentration" rather than a calibrated correctness rate. As of 2026-10-09 the GitHub repository had 593 stars and 31 forks. It was created on 2025-06-04, was last pushed on 2026-10-07, and has 17 releases in total, with the latest, v2.5.1, published on 2026-10-07.

**When to use** Swama suits running local decision models and multimodal models on a Mac behind an OpenAI-compatible interface. It is a macOS-only runtime: because it supports Apple Silicon only (macOS 15.0+ per the repository README; the v2.5.1 release assets list 15.6+), it does not run on Intel Macs or other hardware.

## Links

- [GitHub – Trans-N-ai/swama](https://github.com/Trans-N-ai/swama)
- [GitHub releases – Trans-N-ai/swama](https://github.com/Trans-N-ai/swama/releases)
