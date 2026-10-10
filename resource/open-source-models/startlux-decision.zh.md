---
title: "StartLux-Decision (StartLux Labs)"
updated: 2026-10-10
---

# StartLux-Decision (StartLux Labs)

【定位】StartLux-Decision 是 StartLux Labs 的类型化决策模型家族：五档稠密模型 0.8B 至 27B，另加一个 35B-A3B 混合专家版本。每个模型读入文本、JSON 或图像状态与类型化问题，单次前向返回每个选项的概率。它不做生成，答案直接读选项字母，请求使用 TypeSafe `/v1/systemone` 格式，现有 Jev 客户端无需改动即可调用。

【功能】各档均支持 262144 token 的状态与 choice、noul、score 三类问题，长状态分块读取一次，问题在其上分叉。运行方式覆盖 CUDA（依赖 flash-linear-attention 与 causal-conv1d 快速核）、苹果芯片的 MLX，以及 llama.cpp 的 GGUF，后两者只读文本。项目自报 Decision Index 0.2.1 上 27B 得 63.88，Jev 1.13 为 57.91；35B-A3B 在 JevBench 公开集 231 题中答对 210 题；单张 H200 上各档单次请求为 12.2 至 102.3 ms。推理代码 Apache-2.0，权重 CC BY-NC 4.0，非商业使用需署名，商用须另行授权。

【特点】权重同时发布在 Hugging Face 与 ModelScope，稠密档另提供 BF16、Q8_0、Q4_K_M 三种 GGUF。按同一批 231 题与原权重对比，其保留原答案的比例为 99% 至 100%；Q4_K_M 在 0.8B 与 2B 上改动较多，这两档建议改用 Q8_0，35B-A3B 暂无 GGUF。训练数据包含 Decision Index 38 个基准中 14 个的公开训练划分，对应测试题已剔除；仓库另附 LoRA 微调与温度校准。Decision Index 成绩未提交公开榜单，属项目自行跑测。

【适用】适合在本地按需选择规模部署 Jev 兼容决策，包括在 CUDA 上处理图像与超长输入。不适合无单独授权的商业使用，需要图像时也不适合走 MLX 或 GGUF 后端。

## Links

- [GitHub – 仓库](https://github.com/StartLuxLabs/StartLux-Decision)
- [HF – 模型合集](https://huggingface.co/collections/startlux-models/startlux-decision-6abba92b301b573fa154d493)
- [HF – StartLux-Decision-27B 权重](https://huggingface.co/startlux-models/StartLux-Decision-27B)
