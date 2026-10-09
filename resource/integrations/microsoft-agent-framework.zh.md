---
title: "Microsoft Agent Framework: agent-framework-typesafe"
updated: 2026-10-09
---

# Microsoft Agent Framework: agent-framework-typesafe

【定位】把 TypeSafe System One 模型（含 Jev）适配到 Microsoft Agent Framework（Python）的官方 alpha 包，将 TypeSafe 的结构化决策 API 接到 Agent Framework 的 chat client 契约上：Jev 对显式类型化问题求值应用状态并返回概率与分数，不生成普通聊天文本。

【功能】对 Agent Framework 而言，`response_format` 即 TypeSafe 的 `Questions` 映射，连接器把它转发为 SDK 的 `questions` 参数，并以 `SystemOneResponse` 作为实际响应模型；支持 `Noul`、`Choice`、`Score`，客户端上的 `default_questions` 可为固定契约省略逐次传参。工具选择与受支持参数会转成内部 `Choice`/`Noul` 问题并发出 Agent Framework function call；MCP 工具经 `Agent` 展开为 `FunctionTool`。`TypeSafeChatClient` 为推荐客户端，`RawTypeSafeChatClient` 供自定义层栈。内部创建的客户端读取 `TYPESAFE_API_KEY`、`TYPESAFE_DEFAULT_MODEL`、`TYPESAFE_BASE_URL`，默认模型 `jev-latest`、默认 base url `api.typesafe.ai`；拒绝 streaming、非文本内容与 `temperature`（官方）。

【特点】alpha 阶段，安装为 `pip install agent-framework-typesafe --pre`，仅支持 Python，.NET 未支持；MIT 许可。PyPI 列出 1.0.0a261002，最近发布 2026-10-02（PyPI）。单请求支持至多 32 个可路由工具、每工具 64 个属性、每参数 64 个枚举成员、128 个生成问题（官方）。

【适用】适合在 MAF Python agent 中需要类型化决策做路由、工具调用门控或 judge 的场景；不适合 .NET、流式输出或需要生成式文本的任务。

## Links

- [GitHub – microsoft/agent-framework python/packages/typesafe](https://github.com/microsoft/agent-framework/tree/main/python/packages/typesafe)
- [Docs – TypeSafe AI, Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/integrations/by-provider/type-safe-ai)
- [PyPI – agent-framework-typesafe](https://pypi.org/project/agent-framework-typesafe/)
