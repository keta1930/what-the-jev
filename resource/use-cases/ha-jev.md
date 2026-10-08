---
title: "HA-Jev (AboveColin)"
updated: 2026-10-09
---

# HA-Jev (AboveColin)

**Positioning** HA-Jev, by AboveColin, integrates Jev into Home Assistant, bringing a decision model into consumer home automation: recurring household judgment calls expressed as typed questions, asked at automation frequency, with per-decision spend tracked against a budget.

**What it does** Questions defined in the integration surface as sensors, and four actions — jev.noul, jev.choice, jev.score, and jev.ask — can be called from automations; the integration can also serve as an Assist voice agent. It ships 25 one-click blueprints for everyday household judgments, such as forgot-the-laundry reminders and heating while windows are open, plus a dashboard for tracking spend against a budget; the blueprints also work as examples of what a household-judgment question looks like. An automation can therefore ask the same typed question on every trigger.

**Characteristics** Requests route through OpenRouter with the model id typesafe/jev-latest. Home Assistant 2026.9 or newer is required. The spend dashboard shows the cost of each decision against the configured budget, which keeps the per-decision economics visible.

**When to use** For Home Assistant users who want a decision model making recurring household judgment calls, and as a reference for wiring a decision model into an existing automation platform — questions as sensors, callable actions, a voice agent, and ready-made blueprints in one package. For anyone wiring a decision model into another automation platform, it shows the full shape of such an integration: sensors for questions, actions for asking, a voice agent, and a budget dashboard that keeps cost visible per decision. It applies only to the Home Assistant platform, and only at version 2026.9 or newer.

## Links

- [GitHub – AboveColin/HA-Jev repository](https://github.com/AboveColin/HA-Jev)
