---
title: "OpenRouter Jev Hub"
updated: 2026-10-09
---

# OpenRouter Jev Hub

**Positioning** The OpenRouter hub for Jev, TypeSafe AI's "System One" decision model: one place that collects the model's public concept guide, the official tutorial, and the supporting learning material around them.

**What it does** The concept guide covers the Choice, Score, and Noul question types and explains that Jev returns typed answers with calibrated probabilities instead of generating text. It lays out the two call surfaces open to developers: the Decisions API, reached at `POST /api/alpha/decisions`, and the System One API. The official tutorial starts from a first call made with `curl` and works up to interpreting the probabilities in a response, illustrated with real API response examples. Around the core documentation sit SDK guides, five official cookbooks, and Jev Lab, an interactive demo that runs in the browser.

**Characteristics** The documentation set reflects the state as of 2026-10-05. The guide, the tutorial, and the linked blog post divide the work between them: model background, question types, and how to read a response in practice. A related offering on the platform, Jev Router, uses Jev itself to choose the model and the reasoning tier for each request and supports contexts of up to 1M tokens, per the official documentation.

**When to use** It fits teams that already route other models through OpenRouter and want to add Jev within the same stack, and developers who want a guided path from a first request to reading probabilities in responses. The pages are static material dated 2026-10-05, so interface changes after that point should be checked against the platform's current pages.

## Links

- [Docs – Jev guide](https://openrouter.ai/docs/guides/community/jev)
- [Docs – Jev tutorial](https://openrouter.ai/docs/guides/community/jev-tutorial)
- [Blog – What is Jev?](https://openrouter.ai/blog/insights/what-is-jev/)
