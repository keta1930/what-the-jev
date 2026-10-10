---
title: "Jev Resources"
updated: 2026-10-10
---

# Jev Resources

A catalog of Jev-related models, projects, tools, and benchmarks. Alongside this repository's own experiments (`example/` and `experiments/`), it collects community projects built around Jev and the "System One" decision-model category it started.

- **Continuously updated**: entries are maintained and extended as the ecosystem evolves. Each entry carries an `updated` date in its frontmatter — the date this repository last reviewed it, unrelated to upstream release dates.
- **Scope**: projects and models only — no papers, no articles.
- **Selection criteria**: mature, verifiable, well-documented projects are preferred; unverified or early-stage leads are left out for now.
- **Submissions welcome**: recommend a project that fits the scope and criteria via a GitHub issue or pull request.

Each entry is a pair of files: `<slug>.md` (English) and `<slug>.zh.md` (Chinese). The body is organized into four labeled sections — Positioning, What it does, Characteristics, When to use — followed by public links. All content is compiled from public internet sources; second-hand claims are marked "reported".

## Categories

| Category | Contents |
| --- | --- |
| [Closed-Source Models](#closed-source-models) | Commercial decision models: Jev itself and its proprietary competitors |
| [Open-Source Models](#open-source-models) | Open-weight decision models: replicas, alternatives, and same-paradigm predecessors |
| [Use Cases](#use-cases) | Applications and demos built with Jev (plus same-paradigm references) |
| [Integrations](#integrations) | Gateways, frameworks, and platforms that provide access to Jev |
| [Tools](#tools) | SDKs, MCP servers, CLIs, and libraries for working with Jev |
| [Benchmarks](#benchmarks) | Independent and official evaluations of Jev and its alternatives |

## Closed-Source Models

| Title | Path | Summary |
| --- | --- | --- |
| Jev (TypeSafe AI) | [closed-source-models/jev.md](closed-source-models/jev.md) | TypeSafe AI's closed-source System One decision model returning typed answers with calibrated probabilities. |
| OpenAI Decisions API (GPT-6 Luna) | [closed-source-models/openai-decisions-api.md](closed-source-models/openai-decisions-api.md) | OpenAI's public-beta typed decisions API with a single gpt-6-luna model and text-plus-image states. |
| Liquid d1 (Liquid AI) | [closed-source-models/liquid-d1.md](closed-source-models/liquid-d1.md) | Liquid AI's TypeSafe SDK-compatible decision model family with three hosted variants covering text, image, and audio. |
| Solar Decide (Upstage) | [closed-source-models/solar-decide.md](closed-source-models/solar-decide.md) | Upstage's System One decision model on Solar Mini 4, with a 512K context, Korean support, and free output tokens. |
| Hanzo Kai | [closed-source-models/hanzo-kai.md](closed-source-models/hanzo-kai.md) | Hanzo's closed decision model returning four typed answer kinds, supporting multi-decision runs and replay, with free output. |
| Span-01 (Respan) | [closed-source-models/span-01.md](closed-source-models/span-01.md) | Respan's behavior classifier that returns present, absent, and not_observable probabilities in a single forward pass. |

## Open-Source Models

| Title | Path | Summary |
| --- | --- | --- |
| Laya (ConvAI Innovations) | [open-source-models/laya.md](open-source-models/laya.md) | Multilingual non-autoregressive decision engine returning typed decisions with calibrated confidence in one forward pass across 100+ languages. |
| chinese-laya (yanqiangmiffy) | [open-source-models/chinese-laya.md](open-source-models/chinese-laya.md) | Chinese fine-tune of Laya's multilingual checkpoint, with machine-translated data splits and author-reported test results. |
| Kev (Jared Palmer) | [open-source-models/kev.md](open-source-models/kev.md) | Small Qwen-based decision model family for self-training and local deployment, with three isolated question types and calibrated probabilities. |
| decider (Mapika) | [open-source-models/mapika-decider.md](open-source-models/mapika-decider.md) | Mapika's Apache-2.0 decision model family spanning 0.8B to 35B variants, with the training recipe published in full. |
| JevK5 (allebee) | [open-source-models/jevk5.md](open-source-models/jevk5.md) | Open decision model pairing distilled Qwen3.5 LoRA with option-letter logit readout; ranked first among open-source models on JevBench v1.4. |
| Hopper (hopit-ai) | [open-source-models/hopper.md](open-source-models/hopper.md) | Single-forward-pass decision server with five models; its 4B adapters are restricted to research and demonstration use. |
| SemIf (TheoLeeCJ) | [open-source-models/semif.md](open-source-models/semif.md) | Zero-training approach reading option probabilities from frozen open models in one forward pass, with MIT-licensed code. |
| pplx-decider (Perplexity) | [open-source-models/pplx-decider.md](open-source-models/pplx-decider.md) | Multimodal decision model fine-tuned from Qwen3.8-27B, with Apache-2.0 weights and a commercial hosted API. |
| Clef / Clef-flash (Cloudflare) | [open-source-models/clef.md](open-source-models/clef.md) | Cloudflare decision models at 27B and 9B with image input, 64K context, and Jev API compatibility. |
| Tev1 (Together AI) | [open-source-models/tev1.md](open-source-models/tev1.md) | Open Qwen3.5 4B/0.8B LoRA decision weights supporting choice-type only, with a $17 training walkthrough. |
| Prometheus / Prometheus-Eval | [open-source-models/prometheus-eval.md](open-source-models/prometheus-eval.md) | KAIST-led open-weight judge model family outputting scores and written judgments, not typed calibrated probabilities. |
| Nimble (Bespoke Labs) | [open-source-models/nimble.md](open-source-models/nimble.md) | Bespoke Labs' open Jev alternative: a Qwen3.5-9B one-step typed text decision model with public data and recipe. |
| OpenJev (razorback16) | [open-source-models/openjev-razorback16.md](open-source-models/openjev-razorback16.md) | razorback16's open System One decision server; several unrelated projects share the OpenJev name. |
| Lev (Interfaze AI) | [open-source-models/lev.md](open-source-models/lev.md) | Interfaze AI's System One decision model plus the levbench evaluation harness; adoption is early. |
| Julia-1 (Supersonic Labs) | [open-source-models/julia-1.md](open-source-models/julia-1.md) | Supersonic Labs' 144.3M-parameter compact decision model that runs on CPU and in the browser. |
| Jebadiah (Frontier Infra) | [open-source-models/jebadiah.md](open-source-models/jebadiah.md) | Frontier Infra's System One-style decision model with a full training, data, and evaluation pipeline. |
| Rune 26B-A4B (Invergent) | [open-source-models/rune-26b-a4b.md](open-source-models/rune-26b-a4b.md) | Invergent's multimodal decision model reading text and images and returning probabilities in one pass. |
| NeoHorse-Jev-4B (TokenRhythm) | [open-source-models/neohorse-jev.md](open-source-models/neohorse-jev.md) | TokenRhythm's prefill-only decision model for agent routing, tool selection, and scoring. |
| StartLux-Decision (StartLux Labs) | [open-source-models/startlux-decision.md](open-source-models/startlux-decision.md) | Typed decision family from 0.8B to 35B-A3B reading text, JSON, and images, with non-commercial weights. |

## Use Cases

| Title | Path | Summary |
| --- | --- | --- |
| jev-ultrafast (browser-use) | [use-cases/jev-ultrafast.md](use-cases/jev-ultrafast.md) | Official Browser Use agent making one Jev decision per cycle, with an LLM only for text entry. |
| toolgate (RiskAverseTech) | [use-cases/toolgate.md](use-cases/toolgate.md) | Calibrated firewall for agent tool calls: seven Jev questions map through thresholds to allow/ask/deny verdicts. |
| Inbox Zero (elie222) | [use-cases/inbox-zero.md](use-cases/inbox-zero.md) | Open-source email assistant using Jev as an optional classification backend for sorting and filtering. |
| JEV Paper Radar (Eliot5566) | [use-cases/paper-radar.md](use-cases/paper-radar.md) | Daily radar screening the full arXiv feed with one Noul question per declared interest; author-reported figures. |
| HA-Jev (AboveColin) | [use-cases/ha-jev.md](use-cases/ha-jev.md) | Home Assistant integration exposing Jev questions as sensors and actions, with 25 blueprints and a spend dashboard. |
| JevTown (NevaMind-AI) | [use-cases/jevtown.md](use-cases/jevtown.md) | Pixel-art town simulation engine where Jev picks actions from engine-defined options; LLM handles dialogue. MVP stage. |
| jev-tetris (thelau) | [use-cases/jev-tetris.md](use-cases/jev-tetris.md) | Plays Tetris with Jev under controlled measurement; a 23-line regex baseline beat the model in its own tests. |
| Milvus bootcamp: Search with Jev | [use-cases/milvus-bootcamp.md](use-cases/milvus-bootcamp.md) | Nine official Milvus notebooks using Jev for judgment calls across a RAG pipeline, with pymilvus reranking merged. |
| DeepEval (confident-ai) | [use-cases/deepeval.md](use-cases/deepeval.md) | Pytest-style LLM evaluation framework whose JevEval metric delegates scoring to Jev for calibrated probabilities. |
| Semantic Router (aurelio-labs) | [use-cases/semantic-router.md](use-cases/semantic-router.md) | Pre-Jev decision layer routing via encoder similarity in tens of milliseconds; currently being rewritten for 1.x. |
| RouteLLM (lm-sys) | [use-cases/routellm.md](use-cases/routellm.md) | Framework routing traffic between strong and weak models by difficulty; 85% cost savings officially self-reported. |
| Jev Trader (jarrodwatts) | [use-cases/jev-trader.md](use-cases/jev-trader.md) | An experimental Monad trading bot that asks Jev for one buy-or-sell decision per block. |
| QuantDinger (OpenByteInc) | [use-cases/quantdinger.md](use-cases/quantdinger.md) | An open-source AI trading OS with Jev as one optional pre-trade decision gate. |
| Hermes Jev Skills (kerpopule) | [use-cases/hermes-jev-skills.md](use-cases/hermes-jev-skills.md) | Eleven Jev-powered agent skills for Hermes, Claude Code, and Codex. |

## Integrations

| Title | Path | Summary |
| --- | --- | --- |
| OpenRouter Jev Hub | [integrations/openrouter.md](integrations/openrouter.md) | OpenRouter's Jev hub: concept guide, tutorial, cookbooks, and an interactive demo on one platform. |
| Pydantic AI TypeSafeModel | [integrations/pydantic-ai.md](integrations/pydantic-ai.md) | Pydantic AI's TypeSafeModel derives Jev questions from output types, with LLM fallback. |
| LiteLLM Jev Support | [integrations/litellm.md](integrations/litellm.md) | LiteLLM gateway support: a Jev pass-through endpoint and a relevance-compression guardrail. |
| Vercel AI Gateway & AI SDK | [integrations/vercel-ai-gateway.md](integrations/vercel-ai-gateway.md) | Vercel serves Jev via AI Gateway, with AI SDK 7 evaluate API and eve framework integration. |
| Cloudflare Workers AI: typesafe/jev | [integrations/cloudflare-workers-ai.md](integrations/cloudflare-workers-ai.md) | Jev served inside Cloudflare Workers AI, callable with a single env.AI.run() call. |
| LangChain langchain-typesafe | [integrations/langchain.md](integrations/langchain.md) | LangChain's Jev-as-judge benchmark: five trace classes each judged 100 times on accuracy, variance, cost, latency. |
| Spring AI TypeSafe | [integrations/spring-ai-typesafe.md](integrations/spring-ai-typesafe.md) | Spring AI community integration: TypeSafeClient with Jev judge, guardrail, and evaluator adapters. |
| LEAPERone Decisions API | [integrations/leaperone.md](integrations/leaperone.md) | OpenRouter-compatible gateway passing Jev decision requests through; Chinese docs only. |
| Microsoft Agent Framework | [integrations/microsoft-agent-framework.md](integrations/microsoft-agent-framework.md) | Official alpha package adapting TypeSafe System One models to Microsoft Agent Framework Python. |
| DSPy TypeSafe Integration | [integrations/dspy.md](integrations/dspy.md) | Experimental Jev/TypeSafe integration in DSPy 3.4.0 with decision types and the ReAnchor calibrator. |
| Mastra Classifier | [integrations/mastra.md](integrations/mastra.md) | Mastra's Classifier primitive for typed classification with decision models. |
| No-Code Integrations (Zapier / Make / n8n) | [integrations/nocode-integrations.md](integrations/nocode-integrations.md) | Official TypeSafe/Jev integrations on the no-code platforms Zapier, Make, and n8n. |

## Tools

| Title | Path | Summary |
| --- | --- | --- |
| TypeSafe AI Official GitHub | [tools/typesafe-ai-github.md](tools/typesafe-ai-github.md) | Official TypeSafe AI GitHub organization hosting the Jev SDKs, LLM-provider adapter, agent skills, and evaluation source. |
| jev-mcp (jkudish) | [tools/jev-mcp.md](tools/jev-mcp.md) | MCP server by jkudish exposing 12 Jev judgment tools to coding agents over four carriers or compatible endpoints. |
| duckdb-jev (colliber) | [tools/duckdb-jev.md](tools/duckdb-jev.md) | DuckDB extension by colliber that poses a typed Jev question per row via four scalar SQL functions. |
| jev-reranker (hotchpotch) | [tools/jev-reranker.md](tools/jev-reranker.md) | Python library by hotchpotch using Jev for RAG candidate reranking and relevance filtering with threshold-friendly scores. |
| building-with-typesafe-jev (aaddrick) | [tools/building-with-typesafe-jev.md](tools/building-with-typesafe-jev.md) | Unofficial agent skill by aaddrick teaching Jev question design; self-reported evaluation gain of 0.65 to 0.96. |
| openrouter-decisions Skill (OpenRouterTeam) | [tools/openrouter-decisions-skill.md](tools/openrouter-decisions-skill.md) | Official OpenRouter skill teaching agents to delegate judgment and computation to decision models via a seven-step method. |
| llama.cpp | [tools/llama-cpp.md](tools/llama-cpp.md) | llama-server exposes /v1/systemone since 2026-10-02, with five pre-converted decision-model GGUFs under ggml-org. |
| SGLang | [tools/sglang.md](tools/sglang.md) | SGLang turns any chat model into a decision model via /v1/decisions and /v1/systemone; probabilities are uncalibrated. |
| Ollama | [tools/ollama.md](tools/ollama.md) | Ollama 0.35+ serves Jev-style decision models locally on /v1/systemone, starting with nimble and tev1 models. |
| Ollaya (ollaya-dev) | [tools/ollaya.md](tools/ollaya.md) | Local runtime for decision models, Ollama-style; serves TypeSafe's /v1/systemone wire format, written in Rust. |
| Swama (Trans-N-ai) | [tools/swama.md](tools/swama.md) | Local AI runtime for Apple Silicon Macs, serving OpenAI-compatible and SystemOne decision endpoints. |

## Benchmarks

| Title | Path | Summary |
| --- | --- | --- |
| Jevals.com | [benchmarks/jevals.md](benchmarks/jevals.md) | Independent leaderboard scoring Jev and six LLMs on identical typed decision questions, with public per-decision probability data. |
| jev-bench (PavelRavich) | [benchmarks/jev-bench.md](benchmarks/jev-bench.md) | Solo independent benchmark comparing Jev with two GPT-6 models on two 500-sample datasets. |
| JevBench (Benchmark Heaven) | [benchmarks/jevbench.md](benchmarks/jevbench.md) | Benchmark Heaven's leaderboard for Jev-class decision models; four-axis geometric-mean score, cite with version. |
| Decision Index | [benchmarks/decision-index.md](benchmarks/decision-index.md) | Benchmark for typed decision engines with a full reproduction kit and a public-private mixed suite. |
| evals.typesafe.ai | [benchmarks/evals-typesafe.md](benchmarks/evals-typesafe.md) | TypeSafe's official workflow-evals site; figures are vendor-reported, workflow code is open-sourced. |
| classifier-benchmark (jabr) | [benchmarks/classifier-benchmark.md](benchmarks/classifier-benchmark.md) | A head-to-head benchmark for choice, noul, and score classification models, with two hash-locked suites. |
| S1MB | [benchmarks/s1mb.md](benchmarks/s1mb.md) | A leaderboard comparing Jev and open decision models across more than 100 benchmarks. |
| jev-rerank-bench (anessbelbati) | [benchmarks/jev-rerank-bench.md](benchmarks/jev-rerank-bench.md) | A 14-dataset study of Jev as a reranker against Cohere, ZeroEntropy, and open models. |
| jev-sec-bench (Gaurav-Gosain) | [benchmarks/jev-sec-bench.md](benchmarks/jev-sec-bench.md) | A blind security benchmark testing Jev on prompt injection and vulnerable-code detection. |
