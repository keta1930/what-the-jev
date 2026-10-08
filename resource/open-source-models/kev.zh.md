---
title: "Kev (Jared Palmer)"
updated: 2026-10-09
---

# Kev (Jared Palmer)

【定位】Kev 是基于 Qwen 基座的小型决策模型家族，可自行训练和本地部署，作为 TypeSafe Jev 的开源替代，解决文本判断、分类与评分等决策问题。

【功能】单次请求支持是/否、多选、评分三类问题，问题间相互隔离互不干扰。默认输出经温度校准的概率，便于按置信度设置阈值自动路由。可用自有标注数据微调，编程代理能在 Modal 上自动完成从问题发现到部署的全流程。一条命令即可部署 HTTPS 端点，闲置时自动缩容为零成本。

【特点】技术栈为 Qwen3.5/3.8 基座加 rank-16 LoRA 适配器与指针头，通过注意力掩码或独立行机制实现严格的问题隔离。提供 0.8B 至 27B 四种规模，覆盖笔记本到数据中心 GPU，支持 CUDA、ROCm 和苹果 MLX，采用 Apache-2.0 开源协议。

【适用】适合需要在本地或私有环境运行文本决策模型的开发者，典型场景包括客服工单路由、紧急度判断、客户情绪评分等业务分流。不适合追求顶级知识问答能力的任务，小模型在长文档上的准确率也会明显下降，此类需求建议选用 27B 版本。

## Links

- [Blog – Kev 发布文章](https://jaredpalmer.com/blog/introducing-kev)
- [GitHub – 源码](https://github.com/jaredpalmer/kev)
- [HF – kev-4b 权重](https://huggingface.co/jaredpalmer/kev-4b)
- [Docs – OpenRouter 托管的 kev-4b](https://openrouter.ai/jaredpalmer/kev-4b)
