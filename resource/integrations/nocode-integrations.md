---
title: "No-Code Integrations (Zapier / Make / n8n)"
updated: 2026-10-09
---

# No-Code Integrations (Zapier / Make / n8n)

**Positioning** The official TypeSafe/Jev integrations on three no-code platforms, Zapier, Make, and n8n, for using Jev as one step of classification, routing, and triage inside Zaps, scenarios, and workflows without writing code.

**What it does** Zapier lists an official TypeSafe Jev app whose action is `ask_questions`, supporting Yes or no questions, Pick one, and Scale inputs with a Minimum confidence setting, callable from an agent or backend through Zapier MCP or the Zapier SDK. Make's official TypeSafe app includes an Evaluate a state module, which evaluates typed questions and returns structured answers, and a Make an API Call module for endpoints the existing modules do not cover; it shipped 2026-09-29 (official community announcement), and the app is searchable by the model name Jev. n8n's official TypeSafe AI integration is built and maintained by TypeSafe and verified by n8n, with two operations: Evaluate, which evaluates state against System One questions, and Route, which evaluates a single question and sends each item to the matching output. n8n Cloud access is free through Gateway credits until 2026-10-10; self-hosted use requires installing the node and supplying a key.

**Characteristics** All three integrations above are first-party sources. A Zapier blog post dated 2026-09-24 said no native integration existed at the time, which differs from the current directory listing and reflects the time gap.

**When to use** Suits no-code setups that use Jev as one step in a Zap, scenario, or workflow for classification, routing, and triage, with low-confidence answers sent down a separate branch. The three platforms differ mainly in which actions and modules each exposes for the same evaluation step.

## Links

- [Directory – Zapier: TypeSafe Jev](https://zapier.com/apps/typesafe-jev/integrations)
- [Directory – n8n: TypeSafe AI](https://n8n.io/integrations/typesafe-ai/)
- [Docs – Make app updates (TypeSafe)](https://help.make.com/google-gemini-ai-video-module-update-typesafe-and-more-app-updates)
