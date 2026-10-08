---
title: "JevTown (NevaMind-AI)"
updated: 2026-10-09
---

# JevTown (NevaMind-AI)

【定位】JevTown 是 NevaMind-AI 开发的像素风小镇游戏引擎，自称第一个基于 Jev 的 AI 模拟系统：角色由模型而非脚本驱动，Jev 任 System One 决策者，计划在其上开发叙事游戏。

【功能】Jev 做快速、结构化的选择——是否去找某人、去找谁、往哪走、等多久；引擎给出选项、Jev 在其中选择，非法动作不可能发生。LLM 负责语言工作：agent 间对话、记忆与对世界的认知。配置 VITE_ACTION_DECIDER=jev 启用 Jev，缺省由 LLM 做全部决策，构成两种范式的内置 A/B 对照。

【特点】模拟运行于单个浏览器标签页。需 Node.js 22 LTS；Jev demo 在 feat/jev-demo-solarium 分支、未合并到 main。默认 5、最多 50 个 agent；每次决策与对话都是模型调用，代理在每次运行 2,000 次调用后停止作花费兜底。代码 MIT，基于 a16z-infra/ai-town 并署名；素材可能另有许可证。

【适用】适合作为"引擎定义选项、决策模型在其中选择"模式的实现参考，也可对照观察 Jev 与 LLM 两种决策方式。项目为 MVP、分支未合并，不宜当稳定引擎依赖；成本随角色数增长。

## Links

- [GitHub – JevTown 仓库](https://github.com/NevaMind-AI/JevTown)
- [GitHub – 上游 a16z-infra/ai-town](https://github.com/a16z-infra/ai-town)
