---
title: "Jev Trader（jarrodwatts）"
updated: 2026-10-09
---

# Jev Trader（jarrodwatts）

【定位】Jev Trader 是 jarrodwatts 在 Monad 上的实验性 AI 交易机器人：每个区块向 TypeSafe 的 Jev 模型询问一次买/卖决策，标的是 Kuru 交易所的 MON-USDC 订单簿。

【功能】每轮循环先用一次 `eth_call` 读取订单簿，再经 AI SDK 的 `experimental_evaluate` 调用 `JevModel` 取决策，最后以 post-only 限价单挂在该方向上、进档一个 tick，并在同一次 `batchUpdate` 中撤销上一笔挂单。问题问的是 `HORIZON_BLOCKS`（默认 100，约 30 秒）内的方向，模型返回买或卖及概率；只有错过区块时才出现 hold。项目为 TypeScript + Bun，每区块经 SSE 推送，并提供仪表盘展示快照、最近 1000 条区块事件与成交事件。

【特点】热路径按单个 Monad 区块约 300 毫秒做预算，全程只有两次 RPC 往返（读订单簿、发交易），采用静态 type-2 费率与本地 nonce，读订单簿走另一条 RPC 路由。未设置 `PRIVATE_KEY` 时以 dry-run 运行：真实订单簿、真实决策、模拟成交。设 `MODEL=jev` 与 `TYPESAFE_AI_API_KEY` 使用 Jev，默认的 `mock` 是动量启发式替身。MIT 许可，2026-09-16 建库；README 明示它不证明策略可盈利。

【适用】适合研究“一次类型化决策如何接入自动执行回圈”——订单簿进、校准答案出、订单上簿——并借助仪表盘与 dry-run 观察。它本身不是可盈利策略，也未以此呈现；默认部署实例跑的是 mock 模型。任何实盘部署都同时承担执行风险与模型风险。

## Links

- [GitHub – jarrodwatts/jev-trader 仓库](https://github.com/jarrodwatts/jev-trader)
- [Demo – 已部署的 dry-run 实例](https://jev-trader-production.up.railway.app)
