---
title: "OpenJev (razorback16)"
updated: 2026-10-09
---

# OpenJev (razorback16)

【定位】OpenJev 是 razorback16 的独立开源 System One 决策服务器，用同一套 Jev wire API 在开源模型上作答类型化决策，读取模型概率而非解析生成文本，答案不越出 schema。

【功能】`POST /v1/systemone` 返回概率与 confidence，支持 noul、choice、score，最多 255 个选项，也接受文档、截图等图片输入。默认模型 `openjev-0.1` / `openjev-latest` 跑 DiffusionGemma 26B-A4B（总 26B、激活 4B，来自 Google/NVIDIA，Apache-2.0），经 vLLM 或 MLX 运行；Laya、Verdict、CLM、JevK5 等小模型也可挂载。它在 Codiv 上免费托管，注册赠 1 亿输入 token。服务器代码为 Apache-2.0。

【特点】JevBench v1.2 将其记为 "OpenJev razorback16 (DiffusionGemma 26B)"，总排名 #11、综合 66.4。该名称与无关项目重名：llama.cpp 自带的预转换 `ggml-org/OpenJev-GGUF` 是另一模型——27B、底座 Qwen3.8-27B、权重 CC BY-NC 4.0、约 43ms/问（据 llama.cpp 官方博客）；同名项目还有 `apus-ailab/APUS-OpenJev-v1`、"openJev Verdict"、"open-jev (MLX)" 等，引用时应带 owner。GitHub 650 stars、59 commits。

【适用】适合希望以开源模型获得可直接替换的 Jev 兼容端点、需要图片输入，或想在一个服务器后比较多种模型后端的开发者。安装或对比前应先确认某个 "OpenJev" 产物归属哪个项目，因为同名发行版不止一个。需要生成式解释而非概率分布的任务不适用。

## Links

- [GitHub – 决策服务器源码](https://github.com/razorback16/openjev)
- [HF – ggml-org OpenJev-GGUF（另一项目）](https://huggingface.co/ggml-org/OpenJev-GGUF)
- [Blog – llama.cpp 中的决策模型](https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp)
