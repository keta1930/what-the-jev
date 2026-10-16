# 最后通牒

每轮分配 10。提议方给对方 0、2、5、8 或 10；接受后按报价分配，拒绝则双方得 0。P1 在奇数轮提议，P2 在偶数轮提议。

每场重置状态，收益逐轮累加。Jev 统一最大化自身整场累计收益；英文请求不包含对手策略身份。

## 策略

- `jev`：调用固定版本真实 Jev，以最大化自己整场累计收益为目标。
- `cooperate`：报价 5；接受给自己至少 5 的报价。
- `defect`：报价 0；接受任何合法报价。
- `random`：合法报价均匀随机；回应时等概率接受或拒绝。
- `cycle`：报价按 0／10 轮换，接受阈值按 0／5 轮换；分别按自己担任该角色的次数与起始相位推进。
- `tit_for_tat`：报价复制对方最近一次实际报价，无历史时报 5；接受阈值为对方此前最近一次报价，无历史时为 5，不用本轮报价作为阈值。
- `generous`：报价复制对方最近一次报价，无历史时报 5；接受阈值固定为 2，低于阈值仍以 0.25 概率接受。
- `win_stay_lose_shift`：两个角色分别保存最近一次原始行动和收益。首次报价 5、首次回应接受；同角色上次收益至少 5 则保持，否则报价在 0／5 间切换、回应在接受／拒绝间切换。

规则策略使用与模型相同的可见历史；循环还使用公开轮次或角色次数。历史窗口为零时，针锋相对与赢留输换使用首次规则；自身累计收益仍可见。相位组合完整枚举，每场独立重置。

## 运行与记录

在仓库根目录执行 `python -X utf8 games/game-theory/run.py resume` 恢复全清单；`python -X utf8 games/game-theory/run.py build-html` 从已有记录重建全部展示。

本场景 `../../output/records/<batch-id>/scenarios/ultimatum/manifest.json` 索引全部条件；条件下 `config.json` 冻结配置，`inputs.jsonl` 保存实际英文模型输入，`responses.jsonl` 按唯一 attempt ID 原样保存响应，`events.jsonl` 保存规则行动、执行干预、结算和状态。`summary.json` 可由记录重建。完整批次与费用见类别根目录 `output/records/<batch-id>/`。

`config.yaml` 与英文 `scenario.json` 描述固定规则。组合、轮次和扩展由 `../../config/suite.yaml` 及公共清单生成器定义，清单数量以不可变批次 manifest 为准。中文展示标签定义在 `../../src/game_theory/display.py`，不进入模型请求。
