---
title: "toolgate (RiskAverseTech)"
updated: 2026-10-09
---

# toolgate (RiskAverseTech)

【定位】toolgate 是 RiskAverseTech 出品的 agent 工具调用防火墙：动作执行前由 Jev 出校准判断，经阈值映射为放行、询问或拒绝的判定。

【功能】Agent 动作执行前，Jev 回答七个问题——是否具有破坏性、是否渗出数据、是否提权、是否泄密、是否越界、是否违约、是否留有未决的关键选择——并核对 authorized 缓解项。静态规则先行；校准概率经阈值映射为 allow/ask/deny 判定；无法判定时默认拒绝（fail-closed）。每个决策经 write-then-execute 行为账本落账，事后可审计。

【特点】可作为 Claude Code mod/hook 安装，也可作为 MCP 代理运行，能部署在各类工具调用 agent 之前。仓库附冻结挑战集（用于回归测试）与 7 天实测报告。开发活跃，当前版本 v0.16。

【适用】适合需要为工具调用 agent 增加可审计拦截层、并保留每次判定记录的场景。防护质量取决于问题集与阈值的设计，冻结挑战集是项目用于回归检验这两者的机制；无法判定时动作被拒绝，对误拦截敏感的流程需先评估阈值设置。

## Links

- [GitHub – RiskAverseTech/toolgate 仓库](https://github.com/RiskAverseTech/toolgate)
- [npm – @riskaverse/toolgate 包](https://www.npmjs.com/package/@riskaverse/toolgate)
