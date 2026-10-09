---
title: "No-Code Integrations (Zapier / Make / n8n)"
updated: 2026-10-09
---

# No-Code Integrations (Zapier / Make / n8n)

【定位】三家无代码平台（Zapier、Make、n8n）上的 TypeSafe/Jev 官方集成，用于在 Zap、scenario 与工作流中无需写代码地把 Jev 作为一步做分类、路由与分流。

【功能】Zapier 提供官方 TypeSafe Jev app，action 为 `ask_questions`，支持 Yes or no questions、Pick one、Scale 输入与 Minimum confidence，可经 Zapier MCP 或 Zapier SDK 从 agent/后端调用。Make 的官方 TypeSafe app 含 Evaluate a state（对类型化问题求值并返回结构化答案）与 Make an API Call（调用现有模块未覆盖的端点）两个模块，2026-09-29 发布（官方社区公告），并可按模型名 Jev 搜索到该 app。n8n 的官方 TypeSafe AI 集成由 TypeSafe 构建维护、n8n 验证，含 Evaluate（对 System One 问题求值 state）与 Route（对单个问题求值并把 item 送往匹配的输出）两个 operation；n8n Cloud 经 Gateway credits 免费至 2026-10-10，自托管需安装节点并自带 key。

【特点】上述三家集成均为一手来源。Zapier 自家博客（2026-09-24）当时称尚无原生集成，与目录页现状不符，属时间差。

【适用】适合无代码场景把 Jev 作为 Zap/scenario/工作流里的一步做分类、路由与分流；对低置信答案走单独分支，也可借助各平台的置信度设置控制判定的松紧。

## Links

- [Directory – Zapier: TypeSafe Jev](https://zapier.com/apps/typesafe-jev/integrations)
- [Directory – n8n: TypeSafe AI](https://n8n.io/integrations/typesafe-ai/)
- [Docs – Make app updates (TypeSafe)](https://help.make.com/google-gemini-ai-video-module-update-typesafe-and-more-app-updates)
