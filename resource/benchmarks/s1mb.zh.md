---
title: "System One Mosaic Benchmark（S1MB）"
updated: 2026-10-09
---

# System One Mosaic Benchmark（S1MB）

【定位】System One Mosaic Benchmark（S1MB）是 hotchpotch 的排行榜项目，在 100 多个基准上比较 Jev 与开源决策模型。

【功能】模型在相同输入与指标下评测三类决策：Choice、Noul、Score；mosaic 把既有公开 NLP 数据集的任务与合成任务放进同一评测流程。英语套件含 137 个基准、106 个数据子集，其中六个为合成基准，用于考察模型对多变指令、上下文与决策标准的反应。结果记录精确的数据集与模型版本、评测者来源与推理设置。已支持的适配器包括 TypeSafe/Jev 与 Bekko，其他模型可实现类型化适配器契约，或经 Hugging Face 数据集 PR 提交社区结果。

【特点】查看器默认按 Borda Score 排序，这是每个基准等权的相对排名，会随模型名单变化而变动；Task Avg 是另一个 0–100 的基线校正分数，三类任务等权，两者都要求在所选范围内覆盖完整。仓库含 Python 评测器与 Next.js 查看器，MIT 许可，2026-09-29 建库、2026-10-08 仍有推送。配套博客给出 Jev 1.13 的 Task Avg 96.27、Borda 97.73 居首（作者自报）。

【适用】适合跟踪 Jev 级决策模型的排名，并查看各模型在哪些任务上表现较好、哪些吃力。覆盖面仍在扩张，且项目自述其分数不构成未见过任务的泛化证据、也不保证训练数据不重叠；引用任何排名须连同版本。

## Links

- [GitHub – hotchpotch/S1MB 仓库](https://github.com/hotchpotch/S1MB)
- [HF – System One Mosaic Benchmark 博客](https://huggingface.co/blog/hotchpotch/system-one-mosaic-benchmark)
