---
title: "SemIf（TheoLeeCJ，原 OpenJev）"
updated: 2026-10-09
---

# SemIf（TheoLeeCJ，原 OpenJev）

【定位】TheoLeeCJ 开发的零训练决策方案（原名 OpenJev）：不训练也不发布自有权重，直接从冻结的开源模型读取类型化决策的选项概率。它不微调任何模型，而是直接复用已有的开源模型。代码以 MIT 许可开源。

【功能】对冻结底座（Qwen3-0.6B、MiniCPM5-2B、Qwen3.5-4B、Qwen3.5-27B EXL3，覆盖从小到中等规模的开源检查点）做一次前向传播直读选项概率，没有解码循环。提供 WebGPU 浏览器 demo、共享前缀并行（项目自报可达 20 decisions/s），以及按部署的工作负载组合划分的温度校准。因不训练任何权重，更换底座模型只是配置改动，而非一次重新训练。

【特点】项目在社区中被广泛引用为 logit 读取协议的源头。JevK5 等项目明确致谢其方法来源。GitHub stars 约 1.7k–1.8k；Hugging Face 上流传社区 CPU 移植版 JEV-CPU。

【适用】适合零训练预算、普通硬件上运行类型化决策的场景，项目称其为进入类型化决策的成本最低入口，浏览器 demo 让团队在投入资源前先试用整套流程。因不训练任何权重，答案质量与语言覆盖完全取决于所指向的冻结底座模型，超出底座能力的任务受限，也无法通过微调补足，换用更强的底座是项目内可用的调节手段。

## Links

- [GitHub – SemIf 源码](https://github.com/TheoLeeCJ/SemIf)
- [HF – JEV-CPU 社区移植版](https://huggingface.co/Meanblock/JEV-CPU)
