---
title: "DeepEval (confident-ai)"
updated: 2026-10-09
---

# DeepEval (confident-ai)

【定位】DeepEval 是 confident-ai 的开源 LLM 评测框架，形态类 pytest：G-Eval、忠实度、agent 轨迹等指标以测试形式运行在 LLM 应用输出上。项目开发活跃，完整文档（含指标目录）见项目官网。

【功能】通过 JevEval 自定义指标原生支持 Jev：需要判断的指标把打分交给 Jev，返回校准概率而非生成的评语。JevEval 接入既有指标接口，不另起评测路径；指标随测试套件运行，Jev 打分与框架其他指标并存于同一套测试。

【特点】对评测负载而言，JevEval 把部分 LLM-as-judge 调用换成类型化决策。校准值本身兼作分数的置信信号，被替代的是"让生成模型下判断"的文本评语。

【适用】适合在 DeepEval 评测流程中把判断调用交给 Jev 的场景，尤其是需要分数附带置信信号的指标；它也是评测层接入 Jev 的既有案例。替换范围是部分 LLM-as-judge 调用，不覆盖全部指标；生成类指标仍走原有路径。

## Links

- [GitHub – confident-ai/deepeval 仓库](https://github.com/confident-ai/deepeval)
- [Docs – DeepEval 文档](https://deepeval.com/docs)
