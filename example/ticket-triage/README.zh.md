---
title: "工单分诊"
date: 2026-10-09
summary: "本实验测试 Jev 模型对客服工单的判断能力。"
---

# 工单分诊

本实验测试 Jev 模型对客服工单的判断能力。

包含 1 条数据。

Q：「同一笔订单被扣款两次，请退回重复扣的钱。」

要求 Jev 判断三件事：

1. 这张工单属于哪类问题？从 `billing`、`technical`、`account`、`feature`、`other` 中选出一项。（`choice`）

2. 客户是否实际要求退回款项？答案是 0 到 1 之间的概率，表示条件成立的可能性。（`noul`）

3. 这张工单有多紧急？答案是一个 0 到 2 之间的位置值，落在某一级或两级之间。（`score`）

   - `0`：一般咨询或功能建议，可等到后续版本处理。
   - `1`：影响单个客户使用或存在账单争议，需要近期处理。
   - `2`：大范围服务中断、持续资金损失或关键业务完全阻塞，需要立即处理。

## 结果

Jev 模型成功分类了这张工单。

`category` 判为 `billing`。

`refund` 给出 0.98，即认定客户要求退款。

`urgency` 落在等级 1。

`category` 与 `urgency` 的 `confidence` 均为 1。

成本：输入 684 个 token，输出 83 个，费用 `0.000028728` 美元。输出不计费。

## 复现

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/ticket-triage/config.yaml
```

结果追加写入 `result/responses.jsonl`。每条数据每轮运行只请求一次，重跑时跳过已成功的记录；上次运行失败的记录会被清理并自动重新请求。
