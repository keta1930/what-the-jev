---
title: "数学应用题"
date: 2026-10-10
summary: "本实验测试 Jev 模型对小学算术应用题的作答能力。"
samples: 2
input_tokens: 1.8k
cost: 0.000075306
---

# 数学应用题

本实验测试 Jev 模型对小学算术应用题的作答能力。

包含 2 条数据：

1. GSM8K 测试集第 1 条（openai/grade-school-math 的 `test.jsonl` 第 1 行）：题面给出鸭子每日产蛋数、每日早餐吃掉与烘焙用掉的蛋数，以及集市上每枚鲜蛋的售价，问每日在集市的收入。
2. 同结构自拟题：情节与问法和第 1 条相同，四个数字全部替换（产蛋数、早餐吃掉、烘焙用掉、单价），标准答案随之改变。

第 2 条不是数据集样本，是为分辨作答来自逐题计算还是记忆而设：两条结构相同、数量不同，若模型照搬记忆，会答出第 1 条的答案。

Q1：「Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?」

Q2：「Rosa's ducks lay 20 eggs per day. She eats four for breakfast every morning and bakes muffins for her friends every day with five. She sells the remainder at the farmers' market daily for $3 per fresh duck egg. How much in dollars does she make every day at the farmers' market?」

两条数据回答同一组问题。

第一组：这道题的最终答案是多少？（`answer`，`choice`）

第 1 条从四个金额中选出一项：

- `9`：9 dollars.
- `16`：16 dollars.
- `18`：18 dollars.
- `32`：32 dollars.

第 2 条从五个金额中选出一项：

- `33`：33 dollars.
- `20`：20 dollars.
- `18`：18 dollars.
- `11`：11 dollars.
- `60`：60 dollars.

`18` 是第 1 条的标准答案，在第 2 条的题面数字下推不出来，本实验把它放进第 2 条的候选金额里，用作记忆探针。

第二组：这道题的最终答案是否为该金额？（`is_<金额>`，`noul`）

每个候选金额各问一次，第 1 条 4 问、第 2 条 5 问，答案是「是」的概率。

- `true`：The final answer is <金额> dollars.
- `false`：The final answer is not <金额> dollars.

## 结果

数值取自中文数据集的运行结果（`result/responses_zh.jsonl`）。两条数据都判对。

| 样本 | 标准答案 | `answer` 判定 | `confidence` |
| --- | --- | --- | --- |
| 第 1 条（GSM8K） | `18` | `18` | 0.65 |
| 第 2 条（自拟） | `33` | `33` | 0.84 |

各候选金额上的两种问法读数，加粗行为该条的标准答案：

| 样本 | 候选金额 | `choice` 概率 | `noul`「是」概率 |
| --- | --- | --- | --- |
| 第 1 条 | **`18`** | 0.74 | 0.89 |
| 第 1 条 | `16` | 0.16 | 0.26 |
| 第 1 条 | `9` | 0.09 | 0.38 |
| 第 1 条 | `32` | 0.01 | 0.02 |
| 第 2 条 | **`33`** | 0.87 | 0.92 |
| 第 2 条 | `18` | 0.10 | 0.58 |
| 第 2 条 | `60` | 0.02 | 0.11 |
| 第 2 条 | `11` | 0.01 | 0.20 |
| 第 2 条 | `20` | 0 | 0.11 |

读表：

- 两条的标准答案都拿到最高读数，作答随题面数字改变：第 2 条里标准答案 `33` 得 0.87，记忆中的 `18` 只有 0.10，没有照搬第 1 条的答案。
- 每一行的 `noul` 读数都高于同一金额的 `choice` 概率，差距最大的是第 2 条的 `18`：0.10 对 0.58。
- 那 0.58 高于同题其余干扰项的 0.11 到 0.20，是两条读数里唯一指向记忆的信号。
- `noul` 各问独立作答，返回的是各命题的成立概率，不构成候选金额上的分布，可以同时取高值。

成本：

| 样本 | 输入 token | 输出 token | 费用（美元） |
| --- | --- | --- | --- |
| 第 1 条 | 839 | 125 | `0.000035238` |
| 第 2 条 | 954 | 154 | `0.000040068` |
| 合计 | 1793 | 279 | `0.000075306` |

输出不计费。

## 复现

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/math-word-problem/config.yaml
```

英文数据集的结果追加写入 `result/responses.jsonl`，中文数据集的结果追加写入 `result/responses_zh.jsonl`。每条数据每轮运行只请求一次，重跑时跳过已成功的记录；上次运行失败的记录会被清理并自动重新请求。
