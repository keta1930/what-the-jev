---
title: "Jev 资源库"
updated: 2026-10-10
---

# Jev 资源库

Jev 相关模型、项目、工具与评测的收录清单。除本仓库的实验（`example/` 与 `experiments/`）外，这里收录社区围绕 Jev 及其开创的 System One 决策模型构建的项目。

- **持续更新**：条目随生态发展定期维护与增补，每个条目在 frontmatter 中标注更新日期（`updated` 字段），该日期为本仓库的修订日期，与上游项目的发布日期无关。
- **收录范围**：仅收录项目与模型，不收录论文与文章。
- **选取依据**：优先收录成熟、可验证、资料完整的项目；无法验证或尚不成熟的项目暂不收录。
- **欢迎提交**：欢迎通过 GitHub issue 或 pull request 推荐符合上述范围与依据的项目。

每个条目为一对文件：`<slug>.md`（英文）与 `<slug>.zh.md`（中文），正文按【定位】【功能】【特点】【适用】四段组织，后附公开链接。全部内容基于互联网公开来源整理，转述的二手信息以"据报道"标注。

## 分类

| 分类 | 内容 |
| --- | --- |
| [闭源模型](#闭源模型) | 商业决策模型：Jev 本体与其闭源竞品 |
| [开源模型](#开源模型) | 开放权重决策模型：复刻、替代与同范式先行者 |
| [使用案例](#使用案例) | 用 Jev 构建的应用与示例（含同范式对照） |
| [平台与集成](#平台与集成) | 提供 Jev 接入的网关、框架与平台 |
| [工具与 SDK](#工具与-sdk) | 使用 Jev 的 SDK、MCP 服务器、CLI 与库 |
| [评测与校准](#评测与校准) | Jev 及其替代品的独立与官方评测 |

## 闭源模型

| 标题 | 路径 | 简介 |
| --- | --- | --- |
| Jev (TypeSafe AI) | [closed-source-models/jev.zh.md](closed-source-models/jev.zh.md) | TypeSafe AI 的闭源 System One 决策模型，输出带校准概率的类型化答案，零输出 token。 |
| OpenAI Decisions API (GPT-6 Luna) | [closed-source-models/openai-decisions-api.zh.md](closed-source-models/openai-decisions-api.zh.md) | OpenAI 公开 beta 的类型化决策 API，单一模型 gpt-6-luna，state 支持文本与图像混合。 |
| Liquid d1 (Liquid AI) | [closed-source-models/liquid-d1.zh.md](closed-source-models/liquid-d1.zh.md) | Liquid AI 的决策模型族，TypeSafe SDK 兼容，三个托管变体覆盖文本、图像与音频。 |
| Solar Decide (Upstage) | [closed-source-models/solar-decide.zh.md](closed-source-models/solar-decide.zh.md) | Upstage 基于 Solar Mini 4 的 System One 决策模型，512K 上下文、韩语能力、输出 token 免费。 |
| Hanzo Kai | [closed-source-models/hanzo-kai.zh.md](closed-source-models/hanzo-kai.zh.md) | Hanzo 闭源决策模型，返回四类类型化答案，支持多决策一次通过与回放，输出免费。 |
| Span-01 (Respan) | [closed-source-models/span-01.zh.md](closed-source-models/span-01.zh.md) | Respan 的行为检测分类器，单次前向返回 present/absent/not_observable 概率。 |

## 开源模型

| 标题 | 路径 | 简介 |
| --- | --- | --- |
| Laya (ConvAI Innovations) | [open-source-models/laya.zh.md](open-source-models/laya.zh.md) | 多语言非自回归决策引擎，单次前向输出类型化决策与校准置信度，覆盖 100+ 语言。 |
| chinese-laya (yanqiangmiffy) | [open-source-models/chinese-laya.zh.md](open-source-models/chinese-laya.zh.md) | Laya 多语言 checkpoint 的中文微调复现，含机译数据划分与作者自报测试结果。 |
| Kev (Jared Palmer) | [open-source-models/kev.zh.md](open-source-models/kev.zh.md) | 基于 Qwen 的小型决策模型家族，可自训自部署，三类问题相互隔离并输出校准概率。 |
| decider (Mapika) | [open-source-models/mapika-decider.zh.md](open-source-models/mapika-decider.zh.md) | Mapika 的 Apache-2.0 决策模型家族，0.8B 至 35B 多变体，训练配方公开。 |
| JevK5 (allebee) | [open-source-models/jevk5.zh.md](open-source-models/jevk5.zh.md) | 蒸馏 LoRA 加选项字母 logit 读取的开源决策模型，JevBench v1.4 开源第一。 |
| Hopper (hopit-ai) | [open-source-models/hopper.zh.md](open-source-models/hopper.zh.md) | 单次前向决策服务器及 5 个配套模型，4B 适配器仅限研究与演示用途。 |
| SemIf (TheoLeeCJ) | [open-source-models/semif.zh.md](open-source-models/semif.zh.md) | 零训练方案，从冻结开源模型一次前向直读选项概率，代码 MIT 开源。 |
| pplx-decider (Perplexity) | [open-source-models/pplx-decider.zh.md](open-source-models/pplx-decider.zh.md) | 基于 Qwen3.8-27B 的多模态决策模型，权重 Apache-2.0 开源并提供商业托管 API。 |
| Clef / Clef-flash (Cloudflare) | [open-source-models/clef.zh.md](open-source-models/clef.zh.md) | Cloudflare 的 27B/9B 决策模型，支持图片输入与 64K 上下文，兼容 Jev API。 |
| Tev1 (Together AI) | [open-source-models/tev1.zh.md](open-source-models/tev1.zh.md) | Qwen3.5 4B/0.8B LoRA 决策权重，仅支持 choice 型，附 17 美元训练记录。 |
| Prometheus / Prometheus-Eval | [open-source-models/prometheus-eval.zh.md](open-source-models/prometheus-eval.zh.md) | KAIST 开放权重评审模型家族，输出评分与文字判断，非类型化概率分布。 |
| Nimble (Bespoke Labs) | [open-source-models/nimble.zh.md](open-source-models/nimble.zh.md) | Bespoke Labs 的开放 Jev 替代，基于 Qwen3.5-9B 的一步式类型化文本决策模型。 |
| OpenJev (razorback16) | [open-source-models/openjev-razorback16.zh.md](open-source-models/openjev-razorback16.zh.md) | razorback16 的开源 System One 决策服务器，同名项目多需带 owner 区分。 |
| Lev (Interfaze AI) | [open-source-models/lev.zh.md](open-source-models/lev.zh.md) | Interfaze AI 的 System One 决策模型，附带 levbench 评测 harness。 |
| Julia-1 (Supersonic Labs) | [open-source-models/julia-1.zh.md](open-source-models/julia-1.zh.md) | Supersonic Labs 的 144.3M 紧凑决策模型，可在 CPU 与浏览器运行。 |
| Jebadiah (Frontier Infra) | [open-source-models/jebadiah.zh.md](open-source-models/jebadiah.zh.md) | Frontier Infra 的 System One 风格决策模型，含训练与评测完整流水线。 |
| Rune 26B-A4B (Invergent) | [open-source-models/rune-26b-a4b.zh.md](open-source-models/rune-26b-a4b.zh.md) | Invergent 的多模态决策模型，可读文本与图像，单次前向给出概率。 |
| NeoHorse-Jev-4B (TokenRhythm) | [open-source-models/neohorse-jev.zh.md](open-source-models/neohorse-jev.zh.md) | TokenRhythm 的 prefill-only 决策模型，面向 agent 的路由与评分。 |
| StartLux-Decision (StartLux Labs) | [open-source-models/startlux-decision.zh.md](open-source-models/startlux-decision.zh.md) | 0.8B 至 35B-A3B 的类型化决策模型家族，可读文本、JSON 与图像，权重限非商业使用。 |

## 使用案例

| 标题 | 路径 | 简介 |
| --- | --- | --- |
| jev-ultrafast (browser-use) | [use-cases/jev-ultrafast.zh.md](use-cases/jev-ultrafast.zh.md) | Browser Use 官方浏览器 agent：单次 Jev 请求决定操作与元素，仅输入文本时调用小 LLM。 |
| toolgate (RiskAverseTech) | [use-cases/toolgate.zh.md](use-cases/toolgate.zh.md) | Agent 工具调用防火墙：Jev 七问经阈值映射为 allow/ask/deny，行为账本可审计。 |
| Inbox Zero (elie222) | [use-cases/inbox-zero.zh.md](use-cases/inbox-zero.zh.md) | 开源邮件助手，Jev 作为可选分类后端，用有界类别与 yes/no 概率驱动整理过滤。 |
| JEV Paper Radar (Eliot5566) | [use-cases/paper-radar.zh.md](use-cases/paper-radar.zh.md) | 每日 arXiv 全量论文雷达，每兴趣一个 Noul 问题，效果数字为作者自报。 |
| HA-Jev (AboveColin) | [use-cases/ha-jev.zh.md](use-cases/ha-jev.zh.md) | Home Assistant 集成：问题即传感器，四个 action 供自动化调用，附 25 个蓝图与花费看板。 |
| JevTown (NevaMind-AI) | [use-cases/jevtown.zh.md](use-cases/jevtown.zh.md) | 像素风小镇模拟引擎，Jev 任动作决策者、LLM 负责对话，处于 MVP 阶段。 |
| jev-tetris (thelau) | [use-cases/jev-tetris.zh.md](use-cases/jev-tetris.zh.md) | 用 Jev 玩俄罗斯方块并做对照测量，项目测量中 23 行正则基线胜过模型。 |
| Milvus bootcamp: Search with Jev | [use-cases/milvus-bootcamp.zh.md](use-cases/milvus-bootcamp.zh.md) | Milvus 官方教程子目录：九个 Notebook 演示 RAG 管线中由 Jev 出判断的决策点。 |
| DeepEval (confident-ai) | [use-cases/deepeval.zh.md](use-cases/deepeval.zh.md) | 类 pytest 的 LLM 评测框架，JevEval 把打分交给 Jev，返回校准概率作置信信号。 |
| Semantic Router (aurelio-labs) | [use-cases/semantic-router.zh.md](use-cases/semantic-router.zh.md) | 早于 Jev 的向量空间决策层，Route/Encoder 十几毫秒返回路由，正处 1.x 重写期。 |
| RouteLLM (lm-sys) | [use-cases/routellm.zh.md](use-cases/routellm.zh.md) | 按难度路由强弱模型的开源框架，官方自报省 85% 成本、保持 95% GPT-4 水平。 |
| Jev Trader (jarrodwatts) | [use-cases/jev-trader.zh.md](use-cases/jev-trader.zh.md) | Monad 上每区块一次的 Jev 买/卖决策交易机器人，默认跑 mock 模型。 |
| QuantDinger (OpenByteInc) | [use-cases/quantdinger.zh.md](use-cases/quantdinger.zh.md) | 开源 AI 交易 OS，可选在实盘入场订单前接入 Jev System One 决策网关。 |
| Hermes Jev Skills (kerpopule) | [use-cases/hermes-jev-skills.zh.md](use-cases/hermes-jev-skills.zh.md) | 面向 Hermes、Claude Code、Codex 的十一个 Jev 驱动 agent skill 集合。 |

## 平台与集成

| 标题 | 路径 | 简介 |
| --- | --- | --- |
| OpenRouter Jev Hub | [integrations/openrouter.zh.md](integrations/openrouter.zh.md) | OpenRouter 托管的 Jev 文档与调用入口，含指南、教程与 cookbook。 |
| Pydantic AI TypeSafeModel | [integrations/pydantic-ai.zh.md](integrations/pydantic-ai.zh.md) | Pydantic AI 内置 Jev 集成，由输出类型推导问题，支持回退到 LLM。 |
| LiteLLM Jev Support | [integrations/litellm.zh.md](integrations/litellm.zh.md) | LiteLLM 网关提供 Jev 决策调用与上下文裁剪 guardrail。 |
| Vercel AI Gateway & AI SDK | [integrations/vercel-ai-gateway.zh.md](integrations/vercel-ai-gateway.zh.md) | Vercel AI Gateway 托管 Jev，AI SDK 与 eve 框架接入。 |
| Cloudflare Workers AI: typesafe/jev | [integrations/cloudflare-workers-ai.zh.md](integrations/cloudflare-workers-ai.zh.md) | Workers AI 目录内的 Jev 托管，经 env.AI.run() 直接调用。 |
| LangChain langchain-typesafe | [integrations/langchain.zh.md](integrations/langchain.zh.md) | LangChain 的 Jev 裁判实验：五类轨迹各评百次，量化准确率与成本。 |
| Spring AI TypeSafe | [integrations/spring-ai-typesafe.zh.md](integrations/spring-ai-typesafe.zh.md) | Spring 社区的 Jev 集成，含判定、护栏、评估等适配器。 |
| LEAPERone Decisions API | [integrations/leaperone.zh.md](integrations/leaperone.zh.md) | OpenRouter 兼容网关，透传 Jev 决策请求，中文文档、英文页 404。 |
| Microsoft Agent Framework | [integrations/microsoft-agent-framework.zh.md](integrations/microsoft-agent-framework.zh.md) | 把 System One 模型适配到 Microsoft Agent Framework Python 的官方 alpha 包。 |
| DSPy TypeSafe Integration | [integrations/dspy.zh.md](integrations/dspy.zh.md) | DSPy 3.4.0 的实验性 Jev/TypeSafe 集成，含决策类型与 ReAnchor 校准。 |
| Mastra Classifier | [integrations/mastra.zh.md](integrations/mastra.zh.md) | Mastra 的 Classifier 原语，用决策模型做类型化分类。 |
| No-Code Integrations (Zapier / Make / n8n) | [integrations/nocode-integrations.zh.md](integrations/nocode-integrations.zh.md) | Zapier、Make、n8n 三家无代码平台的 TypeSafe/Jev 官方集成。 |

## 工具与 SDK

| 标题 | 路径 | 简介 |
| --- | --- | --- |
| TypeSafe AI 官方 GitHub | [tools/typesafe-ai-github.zh.md](tools/typesafe-ai-github.zh.md) | TypeSafe AI 官方 GitHub 组织：Jev 官方 SDK、adapter、agent skills 与评测源码的发布处。 |
| jev-mcp (jkudish) | [tools/jev-mcp.zh.md](tools/jev-mcp.zh.md) | jkudish 开发的 MCP 服务器，向编码代理等客户端开放 12 个 Jev 判定工具，支持四种 carrier。 |
| duckdb-jev (colliber) | [tools/duckdb-jev.zh.md](tools/duckdb-jev.zh.md) | colliber 的 DuckDB 扩展，用四个标量函数在 SQL 内对每行做 Jev 分类与打分。 |
| jev-reranker (hotchpotch) | [tools/jev-reranker.zh.md](tools/jev-reranker.zh.md) | hotchpotch 的 Python 库，用 Jev 做 RAG 候选重排与相关性过滤，输出可按阈值切分的分数。 |
| building-with-typesafe-jev (aaddrick) | [tools/building-with-typesafe-jev.zh.md](tools/building-with-typesafe-jev.zh.md) | aaddrick 的非官方代理 Skill，教代理设计 Jev 问题与阈值，自报评测 0.65 升至 0.96。 |
| openrouter-decisions Skill (OpenRouterTeam) | [tools/openrouter-decisions-skill.zh.md](tools/openrouter-decisions-skill.zh.md) | OpenRouter 官方技能，教代理把判断与计算交给决策模型，含七步拆解法与阈值探测流程。 |
| llama.cpp | [tools/llama-cpp.zh.md](tools/llama-cpp.zh.md) | llama-server 自 2026-10-02 起提供 /v1/systemone 端点，官方预转换五个决策模型 GGUF。 |
| SGLang | [tools/sglang.zh.md](tools/sglang.zh.md) | SGLang 以 /v1/decisions 与 /v1/systemone 把任意 chat 模型变成决策模型，概率未校准。 |
| Ollama | [tools/ollama.zh.md](tools/ollama.zh.md) | Ollama 0.35 起在本地 /v1/systemone 提供 Jev 式决策模型，首批为 nimble 与 tev1 系列。 |
| Ollaya (ollaya-dev) | [tools/ollaya.zh.md](tools/ollaya.zh.md) | 本地决策模型运行时，Ollama 式拉取，直接实现 TypeSafe /v1/systemone 线格式。 |
| Swama (Trans-N-ai) | [tools/swama.zh.md](tools/swama.zh.md) | 面向 Apple Silicon 的本地 AI 运行时，提供 OpenAI 兼容与 SystemOne 决策端点。 |

## 评测与校准

| 标题 | 路径 | 简介 |
| --- | --- | --- |
| Jevals.com | [benchmarks/jevals.zh.md](benchmarks/jevals.zh.md) | 独立排行榜：Jev 与六个 LLM 同答类型化决策题，公开逐决策概率数据。 |
| jev-bench (PavelRavich) | [benchmarks/jev-bench.zh.md](benchmarks/jev-bench.zh.md) | 个人独立基准：Jev 对比两款 GPT-6 模型，报告校准、成本与延迟指标。 |
| JevBench (Benchmark Heaven) | [benchmarks/jevbench.zh.md](benchmarks/jevbench.zh.md) | Benchmark Heaven 的 Jev 级决策模型榜单，四轴几何平均计分，引用须带版本号。 |
| Decision Index | [benchmarks/decision-index.zh.md](benchmarks/decision-index.zh.md) | 类型化决策引擎基准，含复现套件与公私混合题集，按 edition 引用。 |
| evals.typesafe.ai | [benchmarks/evals-typesafe.zh.md](benchmarks/evals-typesafe.zh.md) | TypeSafe 官方工作流评测站点，数字为厂商自报，工作流代码已开源。 |
| classifier-benchmark (jabr) | [benchmarks/classifier-benchmark.zh.md](benchmarks/classifier-benchmark.zh.md) | 覆盖 choice/noul/score 的 System One 风格分类模型 head-to-head 基准，含两套哈希锁定用例。 |
| S1MB | [benchmarks/s1mb.zh.md](benchmarks/s1mb.zh.md) | 跨 100 多个基准比较 Jev 与开源决策模型的排行榜项目。 |
| jev-rerank-bench (anessbelbati) | [benchmarks/jev-rerank-bench.zh.md](benchmarks/jev-rerank-bench.zh.md) | 14 数据集上把 Jev 当重排器，对比 Cohere、ZeroEntropy 与开源模型。 |
| jev-sec-bench (Gaurav-Gosain) | [benchmarks/jev-sec-bench.zh.md](benchmarks/jev-sec-bench.zh.md) | 面向 Jev 的提示词注入与漏洞代码双项盲测安全基准。 |
