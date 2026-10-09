---
title: "Hermes Jev Skills（kerpopule）"
updated: 2026-10-09
---

# Hermes Jev Skills（kerpopule）

【定位】Hermes Jev Skills 是 kerpopule 的一组 agent skill：把 agent 日常中的那些小决策交给 Jev——模型路由、记忆、上下文压缩、技能选择以及 computer/browser use。它为 Hermes 而建，同一批 `SKILL.md` 文件也可装入 Claude Code 与 Codex。

【功能】仓库以纯 `SKILL.md` 形式提供十一个 skill，另有 `jev` 命令行工具与一个 Hermes 插件。在一轮对话中，这些 skill 向 Jev 询问：哪个模型足够好、检索到的哪些段落值得读、本轮需要哪个已安装技能、摘要该保留哪些轮次、下一步的 GUI 或页面动作是什么。README 逐项给出各 skill 的形态与实测延迟，从路由与分诊的约 0.4 秒到在 377 个技能中选择的约 2.8 秒，并说明 Jev 从不生成文本，只返回带校准置信度的类型化答案。

【特点】插件只使用 Hermes 的公开接缝，无需改动核心即可运行；依赖 Jev 的路径全部 fail-open：缺 key、超时、限流、置信度过低或回复格式错误时，路由保持当前模型、记忆返回原列表、压缩不丢弃任何内容、技能选择不给出建议。安装方式为 `python3 install.py`（Python 3.9 或更新，无依赖），会自动发现机器上的 Hermes、Claude Code 与 Codex。MIT 许可，2026-09-18 建库、2026-10-08 有推送。

【适用】适合研究在编码 agent 工作流中用 Jev 做逐轮路由与技能选择，或直接在已有的 Hermes、Claude Code、Codex 环境试用。README 建议先跑 shadow 模式：只决策与记录，不切换任何东西。各 skill 的实际启用状态属于安装时的配置，需按仓库自述核实。

## Links

- [GitHub – kerpopule/hermes-jev-skills 仓库](https://github.com/kerpopule/hermes-jev-skills)
