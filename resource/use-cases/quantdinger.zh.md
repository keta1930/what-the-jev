---
title: "QuantDinger（OpenByteInc）"
updated: 2026-10-09
---

# QuantDinger（OpenByteInc）

【定位】QuantDinger 是 OpenByteInc 的开源 AI 交易 OS（agent trading / vibe trading），覆盖加密货币、股票与外汇的研究、回测、模拟与实盘，可自建为多租户 SaaS；Jev 是它接入的一种决策网关。

【功能】用户把想法写成 Python 策略，经回测、模拟到实盘执行与监控。可选的 AI Decision Filter 部署在实盘入场订单之前：把订单、策略上下文、敞口、持仓与预算状态发给 TypeSafe Jev，由 Jev 返回带概率与置信度的类型化 Choice 结果；应用在决策时间线中展示 provider、各项检查、结果、置信度、延迟与理由。配置项为 `JEV_API_KEY`、`JEV_BASE_URL`、`JEV_MODEL`、`JEV_TIMEOUT_SECONDS`，文档给出的 HTTP 契约为 `POST /v1/systemone`。

【特点】平台以 Python 实现，后端依赖 PostgreSQL 与 Redis、用 Docker Compose 部署，内置用户管理、计费、支付与结算，供自建交易 SaaS 之用。Jev 只是若干选项之一：被拒订单不会到交易所，退出动作绕过过滤器；未配置 Jev 时回退到所配置的 LLM，无任何 AI provider 时订单照常放行并记录 fail-open 结果。网格、DCA、马丁格尔运行时不在首版范围内。Apache-2.0，2025-12-28 建库，2026-10-06 仍有推送。

【适用】适合希望自建交易栈、并在入场订单前接入类型化决策网关、保留可审计记录的团队。应把 Jev 集成理解为可选组件之一、而非核心决策层——策略逻辑、执行策略、风控规则与退出都在 QuantDinger 自身，且 Jev 不可用时 AI 路径为 fail-open。

## Links

- [GitHub – OpenByteInc/QuantDinger 仓库](https://github.com/OpenByteInc/QuantDinger)
- [Website – ai.quantdinger.com](https://ai.quantdinger.com)
