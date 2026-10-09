---
title: "Ollaya (ollaya-dev)"
updated: 2026-10-09
---

# Ollaya (ollaya-dev)

【定位】面向决策模型的本地运行时 Ollaya，作者 Mert Cobanov，自称 "Ollama for decision models"：按名称拉取决策模型，由本地 daemon 提供服务，直接实现 TypeSafe 的 `/v1/systemone` 线格式，现有 Jev 客户端改一个环境变量即可接入。

【功能】`ollaya pull` 按名字拉取决策模型，包括 `laya`、`decider`、`kev`、`nimble`、`winnow`、`jevk5`、`jeeves`、`clef`、`jeb`、`nli`、`gliclass`、`qwen3guard` 等；`ollaya serve` 启动本地 daemon，`POST /v1/systemone`、`POST /v1/decisions` 与 `GET /v1/models` 与 TypeSafe 线格式一致，官方 TypeSafe SDK 将 `TYPESAFE_BASE_URL` 指向本地端口即可调用。运行时以 Rust 实现，采用 Cargo 工作区，另含 desktop、docs、site、skills 等部分。

【特点】运行时为 Apache-2.0，各模型保留自身许可，如 Laya 来自 ConvAI、decider 来自 Mapika、kev 来自 Jared Palmer 等。官网 ollaya.dev/results 公布自测公开基准、各机器速度与作者原码 parity 数据。GitHub 1259 stars、72 forks（2026-10-09 核实），创建于 2026-09-23，最后推送 2026-10-06，当天连发 v0.10.0、v0.11.0、v0.12.0 三个 release。

【适用】适合在本地以 Ollama 式流程运行决策模型、并需要与现有 Jev 客户端兼容的场景；项目创建于 2026-09-23，仅约两周历史，且一天内连发三个 release，采用前需评估其成熟度。

## Links

- [GitHub – ollaya-dev/ollaya](https://github.com/ollaya-dev/ollaya)
- [Website – ollaya.dev](https://ollaya.dev)
- [HF – ollaya-dev](https://huggingface.co/ollaya-dev)
