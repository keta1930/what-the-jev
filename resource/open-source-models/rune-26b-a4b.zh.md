---
title: "Rune 26B-A4B (Invergent)"
updated: 2026-10-09
---

# Rune 26B-A4B (Invergent)

【定位】Rune 是 Invergent 的开源决策模型，可读文本与图像，单次前向在候选上给出概率；项目称其 Decision Index 开源权重第一（官方自报）。

【功能】文本、结构化数据或图片均可作为 state，支持三类问题类型。配套 surogate 引擎的 decisions 端点实现其训练协议，也可按 Gemma 4 checkpoint 用 transformers 读选项字母 logits；思考默认关闭。

【特点】Apache-2.0；底座为 Gemma 4 的 26B-A4B（26.5B 参数、每 token 激活 8/128 专家），上下文 262k，保留视觉塔。项目自报（Decision Index 0.2 全套，bf16，自测行）index 53.39，高于 Jev 1.13 的 51.67，Rune v1 为 47.23。默认温度过自信（ECE 12.5%），温度 2 时降至 2.2%。速度（4 并发、单卡 RTX PRO 6000 Blackwell）中位 388ms/请求。HF 仓库名带 GGUF，但 v3 实际只放 bf16 safetensors、尚无 GGUF（v1 GGUF 在历史 revision）。

【适用】适合需要在一次前向中判断图像或结构化 state 的多模态决策，也适合希望使用大上下文、并能通过标准 transformers 加载读取选项字母 logits 的团队。默认温度偏自信，使用前应确认校准设置。需留意仓库命名：名为 GGUF 的仓库当前并不提供 v3 GGUF 权重，取用 v1 GGUF 需回到历史 revision。需要生成文本解释的任务不适用。

## Links

- [HF – rune-26b-a4b 仓库](https://huggingface.co/surogate/rune-26b-a4b-GGUF)
- [GitHub – surogate 引擎](https://github.com/invergent-ai/surogate)
