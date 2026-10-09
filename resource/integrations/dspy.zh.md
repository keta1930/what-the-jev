---
title: "DSPy TypeSafe Integration"
updated: 2026-10-09
---

# DSPy TypeSafe Integration

【定位】DSPy 3.4.0（2026-09-25 发布）引入的实验性 Jev/TypeSafe 集成（GitHub release 与官方教程），让 DSPy 程序以调用其他语言模型的同一 `lm=` 接口使用 Jev，把判断步骤表示为带概率证据的类型化决策。

【功能】`from dspy.experimental import TypeSafe, Noul, Score, Choice, ReAnchor`，再 `dspy.configure(lm=TypeSafe("jev-latest"))`，`Predict` 即自动把 signature、输入、demonstrations 与字段 criteria 翻译成 Jev 决策请求。`Noul`、`Choice`、`Score` 分别返回布尔、选项与有序评分的决策及概率证据；阈值、score cuts 与 choice weights 在本地应用，便于复用缓存的证据。`ReAnchor` 优化器按程序 metric 拟合 `Noul` 阈值、score cuts 与 choice weights，含 5 折校验。默认 `jev-latest` 与 `api.typesafe.ai`，环境变量同其他 TypeSafe 客户端。安装 `pip install "dspy[typesafe]"`，依赖 `typesafe-sdk>=0.6.0,<1.0.0`，未加入基础安装。

【特点】Jev 后端不支持生成参数（`temperature` 等），无自动生成式 fallback，所有输出字段必须是决策类型；不支持决策 streaming 与 RLM 决策输出（官方）。API 为实验性，可能变更。集成由 @isaacbmiller、@dbreunig 贡献（PR #10463、#10475）。

【适用】适合用 DSPy 优化/校准流程、把判断步骤交给 Jev 且需要可缓存概率证据的场景；不适合需要生成式回落、嵌套决策输出或流式的场景。

## Links

- [Docs – Jev decisions tutorial](https://dspy.ai/current/tutorials/jev_decisions/)
- [GitHub – DSPy 3.4.0 release](https://github.com/stanfordnlp/dspy/releases/tag/3.4.0)
- [GitHub – PR #10463](https://github.com/stanfordnlp/dspy/pull/10463)
