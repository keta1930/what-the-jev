---
title: "JevTown (NevaMind-AI)"
updated: 2026-10-09
---

# JevTown (NevaMind-AI)

**Positioning** JevTown, from NevaMind-AI, describes itself as the first Jev-based AI simulation system: a pixel-art town game engine in which the characters are driven by models rather than scripts. The project is an MVP that is still taking shape, with a narrative game planned on top of the engine.

**What it does** Two kinds of models cooperate. Jev, as the System One decider, makes the fast, structured choices — whether to seek someone out, who to go to, where to wander, how long to wait; the engine offers the options and Jev chooses within them, so an illegal move is never possible. An LLM does the language work: conversations between agents, memory, and what each agent believes about the world. Setting VITE_ACTION_DECIDER=jev selects Jev as the action decider; leaving it out lets the LLM make every decision instead — a built-in A/B of the two paradigms.

**Characteristics** The simulation runs in a single browser tab. Node.js 22 LTS is required, and the Jev demo lives on the feat/jev-demo-solarium branch until it merges to main. The default cast is five agents, up to fifty; every decision and every line of dialogue is a model call, and the proxy stops after 2,000 model calls per run as a spend backstop. Code is MIT, built on a16z-infra/ai-town with attribution; assets may carry their own licenses.

**When to use** A working reference for the "engine defines the options, Jev picks" pattern, and a way to run Jev and an LLM head-to-head on the same decisions. Being an MVP with the demo on an unmerged branch, it should not be treated as a stable engine to depend on; cost scales with cast size, so it suits small casts.

## Links

- [GitHub – JevTown repository](https://github.com/NevaMind-AI/JevTown)
- [GitHub – upstream a16z-infra/ai-town](https://github.com/a16z-infra/ai-town)
