---
title: "美国总统大选：获胜者与信息时间限制"
date: 2026-10-11
summary: "本示例测试 Jev 对 1996 年至 2024 年美国总统大选获胜者的掌握情况，以及限定信息时间后的判断。"
samples: 9
input_tokens: 3.7k
cost: 0.000154728
---

# 美国总统大选：获胜者与信息时间限制

本示例测试 Jev 对 1996 年至 2024 年美国总统大选获胜者的掌握情况，以及限定信息时间后的判断。

共 9 条样本：`E01`–`E08` 覆盖 1996 年至 2024 年八届大选，每届一条；`E09` 再问一次 2020 年大选，但仅允许使用 2019 年之前可获得的信息。`E02` 与 `E09` 的主题和候选人选项相同，只有提问指令不同。

## 提问

1. `E01`–`E08`：「判断该次大选由哪位候选人获胜。」
2. `E09`：「判断该次大选由哪位候选人获胜。仅使用 2019 年之前可获得的信息，不得使用 2018 年之后发生的任何事件信息。」

两种提问均使用 `choice`，`winner` 返回 `republican`、`democratic`、`other` 中的一项，并附带 `probabilities` 与 `confidence`。候选人选项如下：

| 样本 | 大选年份 | `republican` | `democratic` |
| --- | --- | --- | --- |
| `E01` | 2024 | 共和党候选人唐纳德·特朗普（Donald Trump）获胜。 | 民主党候选人卡玛拉·哈里斯（Kamala Harris）获胜。 |
| `E02`、`E09` | 2020 | 共和党候选人唐纳德·特朗普（Donald Trump）获胜。 | 民主党候选人乔·拜登（Joe Biden）获胜。 |
| `E03` | 2016 | 共和党候选人唐纳德·特朗普（Donald Trump）获胜。 | 民主党候选人希拉里·克林顿（Hillary Clinton）获胜。 |
| `E04` | 2012 | 共和党候选人米特·罗姆尼（Mitt Romney）获胜。 | 民主党候选人贝拉克·奥巴马（Barack Obama）获胜。 |
| `E05` | 2008 | 共和党候选人约翰·麦凯恩（John McCain）获胜。 | 民主党候选人贝拉克·奥巴马（Barack Obama）获胜。 |
| `E06` | 2004 | 共和党候选人乔治·沃克·布什（George W. Bush）获胜。 | 民主党候选人约翰·克里（John Kerry）获胜。 |
| `E07` | 2000 | 共和党候选人乔治·沃克·布什（George W. Bush）获胜。 | 民主党候选人阿尔·戈尔（Al Gore）获胜。 |
| `E08` | 1996 | 共和党候选人鲍勃·多尔（Bob Dole）获胜。 | 民主党候选人比尔·克林顿（Bill Clinton）获胜。 |

所有样本的 `other` 均为「其他候选人获胜、选举尚未举行，或无法确定获胜者。」

## 最小示例

取限定信息时间的 `E09`，发给模型的输入如下（省略 `model` 字段）：

```json
{
  "state": "2020年美国总统大选",
  "questions": {
    "winner": {
      "type": "choice",
      "instructions": "判断该次大选由哪位候选人获胜。仅使用 2019 年之前可获得的信息，不得使用 2018 年之后发生的任何事件信息。",
      "criteria": {
        "republican": "共和党候选人唐纳德·特朗普（Donald Trump）获胜。",
        "democratic": "民主党候选人乔·拜登（Joe Biden）获胜。",
        "other": "其他候选人获胜、选举尚未举行，或无法确定获胜者。"
      }
    }
  }
}
```

模型输出如下（仅保留关键字段）：

```json
{
  "answers": {
    "winner": {"type": "choice", "choice": "other", "probabilities": {"republican": 0.03, "democratic": 0.01, "other": 0.96}, "confidence": 0.94}
  },
  "usage": {"input_tokens": 445, "output_tokens": 42, "cost": 0.00001869}
}
```

Jev 选择 `other`，与限定时间下选举尚未举行的情境相符。这与数据集保留的 `democratic` 参考答案不同，后者记录的是实际获胜方。

## 结果

9 条样本均成功返回，以下结果不含失败样本。

未限定信息时间的八条样本（`E01`–`E08`）全部与参考获胜方一致。2024 年一届判 `republican`，但仍有较大不确定性（`republican` 0.59、`other` 0.40，`confidence` 0.39）；其余七届均以概率 1 判出获胜政党，其中六届 `confidence` 为 1，2020 年一届为 0.99。

2020 年大选的两条样本展示了信息时间限制对答案的影响：

| 样本 | 信息时间限制 | 选择 | `republican` 概率 | `democratic` 概率 | `other` 概率 | `confidence` |
| --- | --- | --- | --- | --- | --- | --- |
| `E02` | 无 | `democratic` | 0 | 1 | 0 | 0.99 |
| `E09` | 仅限 2019 年之前 | `other` | 0.03 | 0.01 | 0.96 | 0.94 |

未加限制时，Jev 判断拜登获胜；加上限制后，转而选择包含「选举尚未举行」与「无法确定获胜者」的 `other`。这一对照表明，时间限制改变了模型判断，模型没有继续给出已知的历史赢家。由于 `other` 合并了多种含义，响应无法进一步区分模型选择的是其中哪一种。

按数据集现有参考答案计，全部 9 条中有 8 条一致。唯一不一致的 `E09` 仍以实际赢家 `democratic` 为参考，因此这一差异应结合时间限制解读：其回答符合限定时间下无法确定赢家的情境。

## 成本

中文结果共输入 3684 个 token，输出 394 个，费用 `0.000154728` 美元。其中 `E09` 输入 445 个 token，输出 42 个，费用 `0.00001869` 美元。

## 复现

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/us-election/config.yaml
```

该命令运行英文数据集 `data/dataset.json` 与中文数据集 `data/dataset_zh.json`，结果分别追加写入 `result/responses.jsonl` 与 `result/responses_zh.jsonl`。每条数据每轮运行只请求一次，重跑时跳过已成功的记录；上次运行失败的记录会被清理并自动重新请求。
