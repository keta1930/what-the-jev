# what-the-jev?!

![cover](docs/cover.png)

*[English](README.md) | 简体中文*

## 项目简介

**what-the-jev** 展示 Jev（TypeSafe AI 的 System One 决策模型）在各种任务上的能力。这是一套持续扩充的可复现 benchmark 与实验合集：每个任务都附带数据集、运行配置、原始模型响应和分析报告。如果你刚接触或想深入探索 Jev，本项目是一个不错的起点。

## 仓库结构

```text
what-the-jev/
├── example/                轻量级示例
│   ├── us-election/        【历史常识】测试JEV模型能否回忆 1996 至 2024 年八届美国总统大选的胜选者。
│   ├── math-word-problem/  【算术与计算】测试JEV模型在小学算术应用题上的表现。
│   ├── university-math/    【算术与计算】测试JEV模型在微积分、线性代数与概率计算题上的表现。
│   ├── pixel-recognition/  【图像识别】测试JEV模型能否仅凭像素数值识别图像内容。
│   ├── ethics-dilemmas/    【伦理决策】测试JEV模型在经典伦理困境中的行为可接受性判断。
│   ├── injection-guard/    【安全】测试JEV模型能否发现多轮 agent 对话中藏在工具调用结果里的提示词注入攻击。
│   ├── paper-qa/           【论文阅读】测试JEV模型能否根据论文的部分内容回答关于该论文的问题。
│   └── ticket-triage/      【业务决策】测试JEV模型对客服工单的分类、退款诉求与紧急程度判断。
├── experiments/            专业级实验
└── docs/jev/               【AGENT】JEV 知识库
```

轻量级示例的完整索引见 [example/INDEX.zh.md](example/INDEX.zh.md)。

## 欢迎贡献

欢迎添加更多有趣的、有价值的实验。

## Citation

引用本仓库：

```bibtex
@software{what_the_jev,
  author = {Yan, Yixin and Cao, Rong},
  title = {what-the-jev: A showcase of Jev decision-model capabilities across tasks},
  url = {https://github.com/keta1930/what-the-jev},
  license = {MIT}
}
```

## 联系方式

📧 Email: yandeheng1@gmail.com

## 许可证

[MIT](LICENSE)
