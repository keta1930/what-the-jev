---
title: "jev-ultrafast (browser-use)"
updated: 2026-10-09
---

# jev-ultrafast (browser-use)

**Positioning** jev-ultrafast is a browser agent from the official Browser Use organization. It drops the usual perceive–plan–act loop in favor of Jev, and the repository exists to demonstrate the division of labor that follows: decisions go to Jev, and text generation happens only where text is actually needed.

**What it does** Every cycle sends a single Jev request that simultaneously decides the browser action to take — CLICK, TYPE, SELECT, and so on — and the element to target it on. A small LLM is invoked only when the chosen action is TYPE, to generate the text to enter, so the per-cycle model cost is one decision call plus at most one small generation call. The agent is driven by structured page state rather than screenshots, which keeps the decision input compact and the loop tight. The repository ships an inspector for examining that structured state.

**Characteristics** The quantified self-comparison is project-reported, not third-party verified: protocol calls for a baseline flow drop from 1092 to 101, and the showcase task — searching for Zurich→London flights — completes in 7.1 seconds.

**When to use** A reference implementation for building decision-driven browser automation on Jev, in particular when the goal is to cut protocol calls and keep the decision loop small. The showcase task is the flight-search flow described above. The pattern it demonstrates — one typed decision per step, generation only at the text-entry point — carries over to other decision-driven agents. It is a demonstration project rather than a supported product, and its figures are self-reported, so verify them independently before relying on them.

## Links

- [GitHub – jev-ultrafast repository](https://github.com/browser-use/jev-ultrafast)
