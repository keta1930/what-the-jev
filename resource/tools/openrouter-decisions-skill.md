---
title: "openrouter-decisions Skill (OpenRouterTeam)"
updated: 2026-10-09
---

# openrouter-decisions Skill (OpenRouterTeam)

**Positioning** The openrouter-decisions skill is official OpenRouter tooling, published by the OpenRouterTeam, for coding agents to install and consult. It teaches an agent to hand "judgment and computation" subtasks to decision models instead of improvising those judgments in the text it generates.

**What it does** The skill prescribes a seven-step method for decomposing judgment and computation into pieces a decision model can take, before delegating them. It bundles a script that lists the catalog of decision models available through the service, and it also provides two procedures for probing thresholds: single-shot tests and comparison tests. Thresholds are treated as quantities to be measured rather than guessed — the procedures exist so that a cutoff is established empirically instead of assumed. The skill can be installed into a range of agents, including Claude Code, Cursor, and Codex.

**Characteristics** A GitHub repository, OpenRouterTeam/skills, is reported to host the skill; that link is second-hand information, not directly verified here, and should be confirmed against OpenRouter's own pages before being relied on. As official OpenRouter tooling, it is organized around the decision models that are reachable through OpenRouter.

**When to use** The intended scenarios are recurring decision points — routing, moderation, ranking, deduplication, escalation gating — where the same judgment is made many times over and a threshold, once probed, can be fixed and reused. A one-off judgment is not the target; the skill is built around decision points that recur. Teams that route requests through carriers other than OpenRouter will not find the method directly applicable and will need to adapt it to their own setup.

## Links

- [Website – openrouter-decisions skill page](https://openrouter.ai/skills/openrouter-decisions)
- [GitHub – OpenRouterTeam/skills (reported)](https://github.com/OpenRouterTeam/skills)
