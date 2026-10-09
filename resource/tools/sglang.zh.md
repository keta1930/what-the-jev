---
title: "SGLang"
updated: 2026-10-09
---

# SGLang

【定位】高性能 LLM 服务框架 SGLang 的决策模型支持：`/v1/decisions` 端点把任意带 Jinja chat template 的生成模型变成决策模型，另有 System One 兼容的 `/v1/systemone` 端点。

【功能】`/v1/decisions` 接收 input 与类型化问题（choice 2-26 选项、score 2-10 级、yes_no），逐题返回每选项概率、argmax 选择或概率加权分数，以及 `label_mass`（答案标签在全词表上的概率）；同一服务器可与 chat 流量并存，无需专用 checkpoint。`/v1/systemone` 以 state 加 noul/choice/score 问题映射提供同一能力，官方 TypeSafe SDK 改 base_url 即可调用，choice 上限 255；两个端点均支持图片输入。

【特点】答案在答案位读取 next-token logprob（标签须为单 token），无文本生成；文档明确返回概率未经校准，阈值需在自有标注数据上验证；已验证 Qwen3.8-27B 与 Qwen3.5-35B-A3B（单张 H200，BF16）；提供 `prompt_format_version` 锁定提示词版本与 `/v1/score` 复放机制；PPLX-Decider v1/v1.1 等决策 checkpoint 经 `/v1/systemone` 使用其训练时的提示词、答案编码与校准温度。截至核查该功能需 nightly 构建。

【适用】适合已部署 SGLang、想用现有生成模型获得类型化决策能力的团队，以及需要自托管 PPLX-Decider 的场景；不适合直接依赖校准概率保证的任务。启用 `--enable-mis`、`--dllm-algorithm` 或内置会话模板的服务器拒绝决策请求。

## Links

- [Docs – Decision models](https://docs.sglang.io/docs/supported-models/decision_models.md)
- [Docs – PPLX-Decider-v1.1-27B cookbook](https://docs.sglang.io/cookbook/autoregressive/Perplexity/PPLX-Decider-v1.1-27B.md)
- [GitHub – sgl-project/sglang](https://github.com/sgl-project/sglang)
