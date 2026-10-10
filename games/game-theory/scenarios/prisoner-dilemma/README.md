# 囚徒困境

双方同时选择合作或背叛。双方合作各得 3；单方背叛时，背叛方得 5、合作方得 0；双方背叛各得 1。

每场重置状态，收益逐轮累加。Jev 统一最大化自身整场累计收益；英文请求不包含对手策略身份。

## 策略

- `jev`：调用固定版本真实 Jev，以最大化自己整场累计收益为目标。
- `cooperate`：每轮选择合作。
- `defect`：每轮选择背叛。
- `random`：在两种合法行动间均匀随机，使用保存的独立随机种子。
- `cycle`：按 合作／背叛 交替，使用公开轮次和起始相位。
- `tit_for_tat`：首轮选择合作；之后其他玩家上一轮至少一半执行合作类行动时选择合作，否则选择背叛。
- `generous`：同针锋相对；原本应选择背叛时，以 0.25 概率改为合作。
- `win_stay_lose_shift`：首轮选择合作。自己上一轮实际收益至少为 3 时保持上一轮原始行动，否则切换。

规则策略使用与模型相同的可见历史；循环还使用公开轮次或角色次数。历史窗口为零时，针锋相对与赢留输换使用首次规则；自身累计收益仍可见。相位组合完整枚举，每场独立重置。

## 运行与记录

在仓库根目录执行 `python -X utf8 games/game-theory/run.py resume` 恢复全清单；`python -X utf8 games/game-theory/run.py build-html` 从已有记录重建全部展示。

本场景 `../../output/records/<batch-id>/scenarios/prisoner-dilemma/manifest.json` 索引全部条件；条件下 `config.json` 冻结配置，`inputs.jsonl` 保存实际英文模型输入，`responses.jsonl` 按唯一 attempt ID 原样保存响应，`events.jsonl` 保存规则行动、执行干预、结算和状态。`summary.json` 可由记录重建。完整批次与费用见类别根目录 `output/records/<batch-id>/`。

`config.yaml` 与英文 `scenario.json` 描述固定规则。组合、轮次和扩展由 `../../config/suite.yaml` 及公共清单生成器定义，清单数量以不可变批次 manifest 为准。中文展示标签定义在 `../../src/game_theory/display.py`，不进入模型请求。
