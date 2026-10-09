---
title: "Hanzo Kai"
updated: 2026-10-09
---

# Hanzo Kai

【定位】Hanzo 的决策模型，2026 年 9 月 28 日发布，权重闭源，仅经 Hanzo API 提供，不提供权重下载，也无自托管路径（官方）。

【功能】输入情况事实与带选项的问题，返回 Choice、Score、Predicate（yes/no）、Defer（信心不足时转人工或规则）四类类型化答案，每个选项带概率，没有自由文本可解析。设计上支持混合证据（文本 / 图像 / 传感器）、一次通过多个有依赖的决策，以及可回放：每条决策记录 program version、证据指纹、模型 revision、完整概率分布、审批与执行轨迹，便于事后回放（官方）。端点为 `POST https://api.hanzo.ai/v1/decisions`，输入 $0.021/1M tokens、输出免费（官方）。

【特点】官方自报基准：12 个任务平均准确率 86.2% 对 Jev 的 77.2%（hanzo.ai/kai，Decision Index v2）；博客另载 85.7% 对 78.0%。官方另自述，在 1000 个及以上选项时准确率趋近于零。

【适用】适合 agent 内的 model / tool selection、stop 判断、何时转人工，业务工作流的 lead scoring、意图识别、升级判断，以及基于传感器数据的物理系统；不适合超大规模选项集（1000 个及以上）、否定式 yes/no 与依赖型多问题程序。

## Links

- [Kai – Hanzo 官网](https://hanzo.ai/kai) (Website)
- [Introducing Kai – Hanzo 博客](https://hanzo.blog/blog/2026-09-28-introducing-kai/) (Blog)
