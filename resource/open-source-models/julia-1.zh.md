---
title: "Julia-1 (Supersonic Labs)"
updated: 2026-10-09
---

# Julia-1 (Supersonic Labs)

【定位】Julia-1 是 Supersonic Labs 的紧凑型决策模型，除加速器外也能在 CPU 上运行，用一个接口处理分类、路由、有序评分与布尔判断。

【功能】单次调用处理 choice、score、noul 三类问题，按调用方选项顺序返回完整 softmax 概率，不生成文本。层级 Router 可处理更大的 choice 列表，单次原生调用覆盖 2 至 20 个选项。`SupersonicLabs/Julia-1-ONNX` 提供 ONNX + WebGPU 版本，可在浏览器内运行。

【特点】144.3M 参数，由 JHU CLSP 的 mmBERT-small 多语编码器加决策头组成，Apache-2.0；FP32 权重约 550.5 MiB，运行时上限定 8,192 token。项目自报（2026-09-24，H200 BF16）类型化决策 73.15%（1,463/2,000，Jev 参考 72.70%）、AG News 94%、DAIR Emotion 86%、MASSIVE 52 locale 71.50%，但 Banking77 仅 64%（Jev 参考 87%）。第三方报道称 M4 上中位延迟 33ms。llama.cpp 官方有 `ggml-org/Julia-1-GGUF`（约 3ms/问，据 llama.cpp 官方博客）。训练总花费约 $104。

【适用】适合仅有 CPU、需在浏览器内运行或追求高吞吐类型化决策的场景，包括多语分类与路由。在 Banking77 等单一领域集合上准确率落后于更大模型，上手前应先在目标任务上做基准，必要时把困难样例分流。不适用于开放式文本生成或多步推理。

## Links

- [HF – Julia-1 模型](https://huggingface.co/SupersonicLabs/Julia-1)
- [HF – ggml-org Julia-1-GGUF](https://huggingface.co/ggml-org/Julia-1-GGUF)
- [News – 发布报道](https://www.marktechpost.com/2026/09/26/supersonic-labs-releases-julia-1-a-144-3m-parameter-open-decision-model-that-runs-on-a-cpu)
