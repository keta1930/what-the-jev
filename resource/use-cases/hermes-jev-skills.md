---
title: "Hermes Jev Skills (kerpopule)"
updated: 2026-10-09
---

# Hermes Jev Skills (kerpopule)

**Positioning** Hermes Jev Skills, by kerpopule, is a set of agent skills that puts Jev behind the small decisions in an agent's day — model routing, memory, context compaction, skill selection, and computer or browser use. Built for Hermes, the same `SKILL.md` files also install into Claude Code and Codex.

**What it does** The repository ships eleven skills as plain `SKILL.md` files, together with a `jev` command-line kit and a Hermes plugin. Across a turn the skills ask Jev which model is good enough, which retrieved passages are worth reading, which installed skill this turn needs, which turns should survive a summary, and what the next GUI or page action should be. The README documents each skill's shape and its measured latency, from about 0.4 seconds for routing and triage to about 2.8 seconds for selecting among 377 skills, and states that Jev never writes text — it returns typed answers with calibrated confidence.

**Characteristics** The plugin uses only public Hermes seams, so it runs without patching core, and every Jev-dependent path fails open: on a missing key, timeout, rate limit, low confidence, or malformed reply, routing keeps the current model, memory returns the original list, compaction drops nothing, and skill selection suggests nothing. Installation is `python3 install.py` (Python 3.9 or newer, no dependencies) and finds Hermes, Claude Code, and Codex on the machine. The project is MIT-licensed; created 2026-09-18, last pushed 2026-10-08.

**When to use** Suited to studying Jev as a per-turn router and selector inside a coding-agent workflow, or to trying it on an existing Hermes, Claude Code, or Codex setup. The README recommends starting in shadow mode, which decides and logs without switching anything. Which skills are actually enabled is a per-install setting, so verify the live state against the repository's own description.

## Links

- [GitHub – kerpopule/hermes-jev-skills repository](https://github.com/kerpopule/hermes-jev-skills)
