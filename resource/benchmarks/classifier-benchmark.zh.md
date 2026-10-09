---
title: "classifier-benchmark（jabr）"
updated: 2026-10-09
---

# classifier-benchmark（jabr）

【定位】classifier-benchmark 是 jabr 的 head-to-head 基准，面向 System One 风格分类模型——即针对状态回答结构化问题的轻量决策模型——覆盖 choice、noul、score 三类原语。

【功能】所有模型对同一批任务回答同一份 question JSON。仓库提供两个哈希锁定的套件：v1 为 8 任务 78 例，v2 为 49 任务 866 例，后者扩展了 v1 的每个问题，并新增邻近域与远域任务、与 v1 无重复用例。套件是带 schema 的纯 TOML 用例文件，非 Python 语言的评测框架可直接读取，`just validate` 会核对套件内容哈希。全部用例为合成数据，由多模型委员会生成并交叉复核（参与任务定义、扩充与评审），有争议的用例在冻结前删除；仓库提示用例是公开的，可能被模型纳入训练数据。

【特点】v2 套件（49 任务 866 例，Apple MPS）的头条结果（仓库自报）为：Jev micro 0.964、macro 0.966，约 330 毫秒、约 $0.000014/次；Von 1.1 micro 0.724、GLiNER2 0.688、Laya 0.585。模型后端含本地 Von、GLiNER2 与决策微调的 GLiNER2.5、Laya，以及托管的 `typesafe/jev-1.13`。仓库以 CC0 1.0 发布，逐任务榜单与逐例原始 JSON 随评测框架一并提交。

【适用】适合在统一的提问格式下比较 Jev 与本地轻量分类器，覆盖 choice、noul、score 三类问题。由于用例为合成数据且可能已进入训练集，这些数字应视为一次比较而非泛化证据；引用任何数值须连同套件版本。

## Links

- [GitHub – jabr/classifier-benchmark 仓库](https://github.com/jabr/classifier-benchmark)
