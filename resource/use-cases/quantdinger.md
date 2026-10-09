---
title: "QuantDinger (OpenByteInc)"
updated: 2026-10-09
---

# QuantDinger (OpenByteInc)

**Positioning** QuantDinger, by OpenByteInc, is an open-source AI trading OS that spans research, backtesting, paper and live trading across crypto, stocks, and forex, and can be self-hosted as a multi-tenant SaaS; one of its integrations is a Jev decision gate.

**What it does** Users turn ideas into Python strategies and run them through backtest, paper, and live execution with monitoring. An optional AI Decision Filter sits in front of live entry orders: it sends the order, strategy context, exposure, positions, and budget state to TypeSafe Jev, which returns typed Choice results with probabilities and confidence, and the app shows provider, checks, result, confidence, latency, and reason in a decision timeline. Configuration uses `JEV_API_KEY`, `JEV_BASE_URL`, `JEV_MODEL`, and `JEV_TIMEOUT_SECONDS`; the documented HTTP contract is `POST /v1/systemone`.

**Characteristics** The platform is written in Python, backed by PostgreSQL and Redis and deployed with Docker Compose, and includes user management, billing, payments, and settlement for running a trading SaaS. Jev is one option among several: rejected entries never reach the exchange and exits bypass the filter, but when Jev is not configured the platform falls back to the configured LLM, and with no AI provider available the order proceeds and the fail-open result is logged. Grid, DCA, and martingale runtimes are excluded from this first version. Apache-2.0; created 2025-12-28, last pushed 2026-10-06.

**When to use** Suited to teams wanting a self-hostable trading stack that can put a typed decision gate in front of entry orders and keep an auditable record of the result. Read the Jev integration as one optional component, not the core decision layer: strategy logic, execution policy, risk rules, and exits live in QuantDinger itself, and the AI path fails open when Jev is unavailable.

## Links

- [GitHub – OpenByteInc/QuantDinger repository](https://github.com/OpenByteInc/QuantDinger)
- [Website – ai.quantdinger.com](https://ai.quantdinger.com)
