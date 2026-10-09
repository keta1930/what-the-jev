---
title: "Ollama"
updated: 2026-10-09
---

# Ollama

【定位】本地模型运行时 Ollama 自 0.35 版本起支持 Jev 式决策模型，通过 `/v1/systemone` 端点在本机提供类型化决策服务，官方于 2026-09-29 公告。

【功能】请求发送文本 `state` 与一组命名问题，本地模型一次请求回答全部问题，返回与 Jev 相同结构的答案：choice 带每选项概率与 `confidence`，noul 返回 yes 概率，score 返回概率加权分数与 `legend`。官方 TypeSafe Python SDK 将 `TYPESAFE_BASE_URL` 指向本地端口、`TYPESAFE_API_KEY` 设为 `ollama` 即可调用，curl 直连 `http://localhost:11434/v1/systemone` 亦可用。官方博客列出的适用场景包括工单分诊、模型路由与内容/安全审核。

【特点】首批提供 `nimble`、`tev1`、`tev1:0.8b` 三个决策模型，`ollama pull nimble` 一条命令获取，更多模型与经 Ollama 云托管的模型在计划中；本地运行无网络往返，官方示例中 Nimble 9B 在 M5 Max 上平均每次决策 91ms（官方自报）。

【适用】适合在个人设备上以最低门槛本地运行 System One 兼容决策服务的场景，尤其是原型验证与对延迟敏感的实时决策；目前可用模型较少，依赖概率质量的任务应在自有标注数据上验证阈值后再采用。

## Links

- [Blog – Ollama now supports Jev-style decision models](https://ollama.com/blog/ollama-now-supports-jev-style-decision-models)
- [Website – ollama.com](https://ollama.com)
