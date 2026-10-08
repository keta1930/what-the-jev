---
title: "openrouter-decisions Skill（OpenRouterTeam）"
updated: 2026-10-09
---

# openrouter-decisions Skill（OpenRouterTeam）

【定位】openrouter-decisions skill 是 OpenRouterTeam 发布的 OpenRouter 官方技能，供编码代理安装使用。它教代理把"判断与计算"类子任务交给决策模型处理，而不是在生成文本里即兴给出结论。

【功能】skill 给出拆解"判断与计算"的七步法，把这类子任务逐步分解后交给决策模型。附带一个脚本，用于列出当前可用的决策模型目录；另提供单发与对比两种测试流程来探测阈值——阈值被定位为需要实测确定的量，而非凭直觉猜测的对象。skill 可安装进 Claude Code、Cursor、Codex 等代理。

【特点】GitHub 仓库 OpenRouterTeam/skills 据报道托管该 skill；该链接为二手信息，此处未经直接验证，使用前应自行确认。作为 OpenRouter 官方工具，其内容围绕经 OpenRouter 可达的决策模型组织。

【适用】适合路由、审核、排序、去重、升级门控这类反复出现、可以明确设定阈值的判定点场景，一次性的判断不在目标场景内。经由其他 carrier 发送请求的团队不能直接照搬，需结合自身环境改造这套方法。

## Links

- [Website – openrouter-decisions skill 页面](https://openrouter.ai/skills/openrouter-decisions)
- [GitHub – OpenRouterTeam/skills（据报道）](https://github.com/OpenRouterTeam/skills)
