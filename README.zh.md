# what-the-jev?!

![cover](docs/cover.png)

*[English](README.md) | 简体中文*

在线站点：[English](https://keta1930.github.io/what-the-jev/) | [简体中文](https://keta1930.github.io/what-the-jev/zh/)。

## 项目简介

**what-the-jev** 展示 Jev（TypeSafe AI 的 System One 决策模型）在各种任务上的能力。这是一套持续扩充的可复现 benchmark 与实验合集：每个任务都附带数据集、运行配置、原始模型响应和分析报告。如果你刚接触或想深入探索 Jev，本项目是一个不错的起点。

## 仓库结构

```text
what-the-jev/
├── example/                            轻量级示例
│   ├── us-election/                    【历史常识】测试JEV模型能否回忆 1996 至 2024 年八届美国总统大选的胜选者。
│   ├── math-word-problem/              【算术与计算】测试JEV模型在小学算术应用题上的表现。
│   ├── university-math/                【算术与计算】测试JEV模型在微积分、线性代数与概率计算题上的表现。
│   ├── pixel-recognition/              【图像识别】测试JEV模型能否仅凭像素数值识别图像内容。
│   ├── ethics-dilemmas/                【伦理决策】测试JEV模型在经典伦理困境中的行为可接受性判断。
│   ├── prompt-injection-detection/     【安全】测试JEV模型能否发现多轮 agent 对话中藏在工具调用结果里的提示词注入攻击。
│   ├── paper-qa/                       【论文阅读】测试JEV模型能否根据论文的部分内容回答关于该论文的问题。
│   └── ticket-triage/                  【业务决策】测试JEV模型对客服工单的分类、退款诉求与紧急程度判断。
├── experiments/                        专业级实验
│   ├── gpqa-diamond/                   【benchmark】探索 JEV 在 GPQA Diamond 研究生级科学题上的表现。
│   ├── gsm8k/                          【benchmark】探索 JEV 在 GSM8K 小学数学应用题上的表现。
│   ├── mmlu-pro/                       【benchmark】探索 JEV 在 MMLU-Pro 覆盖 14 个学科的大学水平题目上的表现。
│   ├── bbq/                            【benchmark】探索 JEV 在 BBQ 偏见敏感问答题上的表现，以及是否会偏向刻板印象。
│   ├── socialiqa/                      【benchmark】探索 JEV 在 SocialIQA 社会常识题上的表现。
│   ├── paper-classification/           【论文分类】探索 JEV 能否按研究偏好判断一篇 arXiv 论文该不该收入论文库，并归入正确的主题。
│   ├── paper-qa/                       【论文问答】探索 JEV 能否基于原文回答关于该论文的问题。
│   ├── prompt-routing/                 【提示词路由】探索 JEV 能否仅凭提问文本，判断提问该走 JEV 快路径还是 LLM 慢路径。
│   ├── skill-routing/                  【技能路由】探索 JEV 能否把用户任务路由到 126 个真实 Agent Skill 中的正确技能、技能组合或 none。
│   ├── boston-housing/                 【数值回归】探索 JEV 能否预测波士顿社区的房价，并比较不同社区的房价高低。
│   ├── titanic/                        【分类预测】探索 JEV 能否根据乘客记录预测乘客是否生还，并比较结构化字段与自然语言文本两种输入下的表现。
│   ├── dpo-jev-judge/                  【大模型训练】探索 JEV 在 DPO 训练数据偏好标注上的表现。
│   └── grpo-jev-judge/                 【大模型训练】探索 JEV 在 GRPO 轨迹奖励分配上的表现。
├── resource/                           Jev 相关项目与模型的收录清单
│   ├── closed-source-models/           【闭源模型】Jev 本体与闭源竞品
│   ├── open-source-models/             【开源模型】开放权重决策模型与复刻
│   ├── use-cases/                      【使用案例】用 Jev 构建的应用
│   ├── integrations/                   【平台与集成】提供 Jev 接入的网关与框架
│   ├── tools/                          【工具与 SDK】使用 Jev 的 SDK、MCP 服务器与 CLI
│   └── benchmarks/                     【评测与校准】Jev 及其替代品的独立与官方评测
├── docs/site/                          中英文文档站点
├── docs/jev/                           【AGENT】JEV 知识库
├── src/decision_models/                运行实验的框架
├── schema/                             数据集与结果的 schema
├── tests/                              框架的测试
├── run.py                              命令行入口
├── AGENTS.md                           【AGENT】项目执行指令
└── .claude/rules/                      【AGENT】项目执行规范
```

轻量级示例的完整索引见 [example/INDEX.zh.md](example/INDEX.zh.md)。

实验的完整索引见 [experiments/INDEX.zh.md](experiments/INDEX.zh.md)。

资源库的完整索引见 [resource/README.zh.md](resource/README.zh.md)。

## 欢迎贡献

我们的目标是打造一个完全由开源精神驱动的决策模型社区，探索决策模型的使用场景与能力边界。

我们非常欢迎任何贡献，包括代码、纠错、提供实验或示例、添加资源等。

期待您的 PR。

本地预览文档修改需要 Node.js 24 和 npm：

```bash
cd docs/site
npm ci
npm run dev
```

打开 <http://localhost:20242>（英文）或 <http://localhost:20242/zh>（中文）。编辑仓库中的 Markdown 源文件，站点会自动更新。提交 PR 前，在 `docs/site` 中运行 `npm test`、`npm run check` 和 `npm run build`；静态构建产物导出到 `out/`。站点开发详情见 [docs/site/README.md](docs/site/README.md)。推送到 `master` 会通过 [GitHub Actions](.github/workflows/pages.yml) 自动发布站点。

## Citation

引用本仓库：

```bibtex
@software{what_the_jev,
  author = {{what-the-jev contributors}},
  title = {what-the-jev: Decision-model use cases and capability boundaries},
  url = {https://github.com/keta1930/what-the-jev},
  license = {MIT}
}
```

## 联系方式

📧 Email: yandeheng1@gmail.com

## 许可证

[MIT](LICENSE)
