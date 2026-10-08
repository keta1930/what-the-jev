---
title: "toolgate (RiskAverseTech)"
updated: 2026-10-09
---

# toolgate (RiskAverseTech)

**Positioning** toolgate, from RiskAverseTech, is a calibrated firewall for agent tool calls: before an agent action executes, Jev supplies calibrated judgments that are mapped through thresholds to an allow, ask, or deny verdict.

**What it does** Before an action runs, Jev answers seven questions — is it destructive, does it exfiltrate data, escalate privileges, leak secrets, act out of scope, breach its contract, or leave a critical choice undecided — alongside a check of authorized mitigations. Static rules run first; the calibrated probabilities then map to the verdict. The gate fails closed when it cannot decide, and every decision passes through a write-then-execute behavior ledger, so actions remain auditable after the fact.

**Characteristics** It installs as a Claude Code mod/hook or runs as an MCP proxy, which puts it in front of tool-calling agents generally. Because the gate runs on the execution path of every tool call, the ledger records each action as it is allowed, questioned, or denied. Each allowed, questioned, or denied action leaves a ledger entry behind. The repository ships a frozen challenge set for regression testing and a 7-day real-world usage report. Development is active, currently at v0.16.

**When to use** Suits deployments that need an auditable interception layer in front of a tool-calling agent, with a ledger recording every allow/ask/deny decision. As with any safety gate, protection is only as good as its question set and thresholds; the frozen challenge set is the project's own mechanism for regression-testing both. Undecided actions are denied by default, so workflows sensitive to false blocks should review the threshold settings first.

## Links

- [GitHub – RiskAverseTech/toolgate repository](https://github.com/RiskAverseTech/toolgate)
- [npm – @riskaverse/toolgate package](https://www.npmjs.com/package/@riskaverse/toolgate)
