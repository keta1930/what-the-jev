---
title: "Swama (Trans-N-ai)"
updated: 2026-10-09
---

# Swama (Trans-N-ai)

【定位】面向 Apple Silicon Mac 的本地 AI 运行时 Swama，作者 Trans-N-ai，用 Swift 编写并构建在 Apple MLX（mlx-swift）之上，为原生实现，通过 Homebrew 安装。

【功能】可运行语言、视觉、embedding、语音识别与 TTS 模型，提供 OpenAI 兼容 API、CLI 与菜单栏 App。决策端点包括 `POST /v1/decisions`（沿用 OpenAI Decisions API 风格，含 `predicate`、`choice`、`score` 三类问题）与 `POST /v1/systemone`（SystemOne OpenAPI 0.2.0 适配层，两者复用同一决策 scorer）；`/v1/systemone` 接受显式本地 `model`、文本或结构化 `state` 与命名 `questions`，TypeSafe JS SDK 指向本地 base URL 即可调用。图像输入支持 base64 data URL（PNG/JPEG/WebP）。

【特点】MIT 许可，README 含英、中、日三语，并提醒模型给出的置信度是"集中度"而非校准正确率。GitHub 593 stars、31 forks（2026-10-09 核实），创建于 2025-06-04，最后推送 2026-10-07，共 17 个 release，最新 v2.5.1（2026-10-07）。

【适用】运行时仅支持 Apple Silicon（仓库 README 标注 macOS 15.0+，v2.5.1 发布资产标注 15.6+），适合在 Mac 上本地运行决策与多模态模型、并需要 OpenAI 兼容接口的场景；借助 TypeSafe JS SDK 将 base URL 指向本机，即可调用其 SystemOne 端点。非 Apple Silicon 设备与更早的 macOS 版本不在支持范围内。

## Links

- [GitHub – Trans-N-ai/swama](https://github.com/Trans-N-ai/swama)
- [GitHub releases – Trans-N-ai/swama](https://github.com/Trans-N-ai/swama/releases)
