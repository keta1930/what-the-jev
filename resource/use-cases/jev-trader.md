---
title: "Jev Trader (jarrodwatts)"
updated: 2026-10-09
---

# Jev Trader (jarrodwatts)

**Positioning** Jev Trader, by jarrodwatts, is an experimental AI trading bot on Monad: it asks a TypeSafe Jev model for one buy-or-sell decision per block while watching the Kuru MON-USDC order book.

**What it does** Each loop reads the order book in one `eth_call`, sends the decision question to Jev through the AI SDK's `experimental_evaluate` on a `JevModel`, and posts the result as a post-only limit order on that side, one tick inside the touch, in the same `batchUpdate` that cancels the previous resting order. The model is asked about the move over `HORIZON_BLOCKS` (default 100, roughly 30 seconds) and returns buy or sell with probabilities; a hold appears only when the block was missed. Written in TypeScript and run with Bun, the bot streams every block over SSE and serves a dashboard with snapshots, the last 1,000 block events, and fill events.

**Characteristics** The hot path is budgeted at about 300 ms per Monad block and makes exactly two RPC round trips — one book read and one send — using static type-2 fees and a local nonce, with the book read routed through a second RPC endpoint. Without a `PRIVATE_KEY` it dry-runs: real book, real decisions, simulated fills. `MODEL=jev` with `TYPESAFE_AI_API_KEY` selects Jev; the default `mock` is a momentum heuristic stand-in. The project is MIT-licensed, created 2026-09-16, and its README states that it does not demonstrate a profitable strategy.

**When to use** Suited to studying how one typed decision can sit inside an automated execution loop — order book in, calibrated answer out, order on the book — with a dashboard and a dry-run mode for observation. It is not presented as a profitable strategy, and the default deployed instance runs the mock model. Any live deployment carries both execution risk and model risk.

## Links

- [GitHub – jarrodwatts/jev-trader repository](https://github.com/jarrodwatts/jev-trader)
- [Demo – deployed dry-run instance](https://jev-trader-production.up.railway.app)
