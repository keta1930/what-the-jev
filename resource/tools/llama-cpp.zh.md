---
title: "llama.cpp"
updated: 2026-10-09
---

# llama.cpp

【定位】本地推理引擎 llama.cpp 自 2026-10-02 合并 PR #29818 起原生支持决策模型：`llama-server` 提供 `/v1/systemone` 端点，以 Jev 的 System One 请求与响应形状提供类型化决策。

【功能】面向 Jev 编写的客户端（含官方 TypeSafe SDK）只需把 base URL 指向本地 `llama-server`。官方在 `ggml-org` 组织下提供五个预转换 GGUF——OpenJev（27B，支持视觉输入）、Kev-4B、Laya、Lev、Julia-1，`llama-server -hf ggml-org/Kev-4B-GGUF` 一条命令即可启动服务。

【特点】实现上将决策模型视为嵌入模型（BERT/Qwen 等）的封装，经 GGUF 元数据 `{arch}.decision.type` 切换输入输出处理，对 libllama 的改动保持最小；PR 附与参考实现的逐题概率对照测试，各模型最大概率差介于 8.4e-4 与 2.2e-2 之间，并带一个用于测试的 OpenJev tiny 模型；共享前缀的并行支持、文档与开发文档、视觉输入也随该 PR 加入，Cloudflare Clef 的支持列为后续计划。语义版本 v0.5.0 早于该合并，需使用包含此功能的较新构建。

【适用】适合在私有硬件上零成本运行 System One 兼容决策服务的场景，此路径不涉及 Jev 的专有权重；采用前需确认所用构建已含该端点，并自行验证模型输出是否满足业务阈值。

## Links

- [GitHub – PR #29818: add /v1/systemone API](https://github.com/ggml-org/llama.cpp/pull/29818)
- [GitHub – llama.cpp repository](https://github.com/ggml-org/llama.cpp)
