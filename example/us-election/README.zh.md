---
title: "美国总统大选"
date: 2026-10-10
summary: "本实验测试 Jev 模型是否掌握 1996 年至 2024 年八届美国总统大选的结果。"
samples: 8
input_tokens: 3.2k
cost: 0.000136038
---

# 美国总统大选

本实验测试 Jev 模型是否掌握 1996 年至 2024 年八届美国总统大选的结果。

包含 8 条数据，每届大选一条，主题分别为「2024年美国总统大选」「2020年美国总统大选」「2016年美国总统大选」「2012年美国总统大选」「2008年美国总统大选」「2004年美国总统大选」「2000年美国总统大选」「1996年美国总统大选」。

每条要求回答同一个问题：

1. 该次大选由哪位候选人获胜？从 `republican`、`democratic`、`other` 中选出一项。（`choice`）

   - `republican`：共和党候选人获胜。各届候选人依次为特朗普、特朗普、特朗普、罗姆尼、麦凯恩、布什、布什、多尔。
   - `democratic`：民主党候选人获胜。各届候选人依次为哈里斯、拜登、希拉里·克林顿、奥巴马、奥巴马、克里、戈尔、比尔·克林顿。
   - `other`：其他候选人获胜、选举尚未举行，或无法确定获胜者。

## 最小示例

本节取 2024 年这一条样本，展示其输入与输出。发给模型的输入如下（省略 model 字段）：

```json
{
  "state": "2024年美国总统大选",
  "questions": {
    "winner": {
      "type": "choice",
      "instructions": "判断该次大选由哪位候选人获胜。",
      "criteria": {
        "republican": "共和党候选人唐纳德·特朗普（Donald Trump）获胜。",
        "democratic": "民主党候选人卡玛拉·哈里斯（Kamala Harris）获胜。",
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
    "winner": {"type": "choice", "choice": "republican", "probabilities": {"republican": 0.59, "democratic": 0.01, "other": 0.4}, "confidence": 0.39}
  },
  "usage": {"input_tokens": 405, "output_tokens": 44, "cost": 0.00001701}
}
```

Jev 选了 `republican`，与实际获胜方一致，但 `other` 也拿到 0.40，`confidence` 只有 0.39。

## 结果

`winner`：八届全部判对。2024年一届判 `republican` 但带有保留（`republican` 0.59、`other` 0.40，`confidence` 0.39）；其余七届均以概率 1 判出获胜政党，其中六届 `confidence` 为 1，2020年一届为 0.99。

成本：输入 3239 个 token，输出 352 个，费用 `0.000136038` 美元。输出不计费。

## 复现

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/us-election/config.yaml
```

结果追加写入 `result/responses.jsonl`。每条数据每轮运行只请求一次，重跑时跳过已成功的记录；上次运行失败的记录会被清理并自动重新请求。
