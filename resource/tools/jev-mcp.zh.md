---
title: "jev-mcp（jkudish）"
updated: 2026-10-09
---

# jev-mcp（jkudish）

【定位】jev-mcp 是 GitHub 用户 jkudish 开发的 Model Context Protocol（MCP）服务器，把 Jev 的类型化判定能力开放给编码代理等 MCP 客户端。撰写时约 320 星，为个人维护的第三方项目。

【功能】服务器提供 12 个 Jev 判定工具——verify、screen、rerank、classify、extract、audit、review、gate 等——覆盖代理任务中反复出现的判定点。请求可经 TypeSafe、OpenRouter、Cloudflare、Vercel 四种 carrier 发出，也可指向任意 System One 兼容端点。随附的 agent skill 说明各工具的适用时机，无需记忆整套工具集。

【特点】以 npm 包 `@jkudish/jev-mcp` 分发，支持 stdio 与 HTTP 两种运行模式。320 星为撰写时的快照。工具与 carrier 列表同样以撰写时仓库状态为准。

【适用】适合让编码代理在任务中直接调用 Jev，完成校验、筛选、重排、分类等判定的场景，其他 MCP 客户端同样可接。项目不由 TypeSafe AI 维护，生产使用前应对照仓库核实工具名、carrier 选项与行为；引用星数等快照数据时需注明时间。

## Links

- [GitHub – jkudish/jev-mcp](https://github.com/jkudish/jev-mcp)
