---
title: "HA-Jev (AboveColin)"
updated: 2026-10-09
---

# HA-Jev (AboveColin)

【定位】HA-Jev 是 AboveColin 开发的 Home Assistant 集成，把 Jev 接入消费级智能家居自动化：周期性的家务判断表达为类型化问题、以自动化频率反复发问。

【功能】在集成中定义的问题以传感器形式出现；jev.noul、jev.choice、jev.score、jev.ask 四个 action 可在自动化中调用；还能担任 Assist 语音代理。自带 25 个一键蓝图，覆盖忘洗衣提醒、开窗时开暖气等日常家务判断，并配有花费预算看板。自动化因此能在每次触发时重复发问同一类型化问题。

【特点】请求经 OpenRouter 路由，模型 id 为 typesafe/jev-latest。要求 Home Assistant 2026.9 及以上版本。花费看板按预算展示每次决策的开销，单次决策成本可见。

【适用】适合在 Home Assistant 中用决策模型承担周期性家务判断的用户；也可作为把决策模型接入既有自动化平台的集成范例通读：问题即传感器、可调用 action、语音代理与预制蓝图在同一包内。仅适用于 Home Assistant 平台，且要求 2026.9 以上版本。

## Links

- [GitHub – AboveColin/HA-Jev 仓库](https://github.com/AboveColin/HA-Jev)
