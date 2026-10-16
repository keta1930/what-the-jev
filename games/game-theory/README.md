# Jev 博弈互动

运行 Jev 与其他玩家的连续博弈，保存真实行动与响应，再生成可离线查看的中文 HTML。包含囚徒困境、猎鹿博弈、鹰鸽博弈、公共物品和最后通牒。

Jev 统一以最大化自身整场累计收益为目标。模型请求使用英文，只提供玩家编号，不公开对手策略身份；收益由代码结算。同时行动只读取已结算历史，最后通牒按提议、回应的顺序执行。

## 从哪里开始

- 了解游戏：打开下方各场景说明。
- 运行实验：使用本目录 `run.py`。
- 查看已有记录：构建后打开 `output/html/index.html`。完整离线包解压后可直接查看。

```text
game-theory/
├── README.md                 使用入口
├── run.py                    Python 命令行入口
├── requirements.txt          运行依赖
├── scenarios/                五种博弈的规则和配置
│   ├── prisoner-dilemma/
│   ├── stag-hunt/
│   ├── hawk-dove/
│   ├── public-goods/
│   └── ultimatum/
├── config/                   整体运行配置
├── src/game_theory/           运行、记录与展示实现
│   ├── assets/               离线页面样式和脚本
│   └── schema/               输入与响应格式
├── tests/                    程序测试
└── output/                   运行后生成，不进入 Git
    ├── records/              完整批次与逐轮原始记录
    ├── html/                 离线展示
    └── html-archive/         重新构建前的旧展示包
```

## 场景与策略

| 场景 | 规则摘要 |
| --- | --- |
| [囚徒困境](scenarios/prisoner-dilemma/README.md) | 合作／背叛；双方合作各 3，单方背叛 5／0，双方背叛各 1 |
| [猎鹿博弈](scenarios/stag-hunt/README.md) | 共同猎鹿各 4，独鹿 0，猎兔固定 3 |
| [鹰鸽博弈](scenarios/hawk-dove/README.md) | 双方退让各 2，单方强硬 4／0，双方强硬各 −1 |
| [公共物品](scenarios/public-goods/README.md) | 3–6 人，每轮各有 10；贡献全部或保留全部，公共池乘 1.6 均分 |
| [最后通牒](scenarios/ultimatum/README.md) | 分配 10，给对方 0／2／5／8／10，接受或拒绝，交替提议 |

支持 Jev、始终合作、始终强硬、随机、循环、针锋相对、宽容针锋相对和赢留输换。各场景 README 给出精确定义；场景的 `config.yaml` 和 `scenario.json` 分别保存配置与英文规则。每场独立重置策略状态。

## 安装与运行

以下命令在仓库根目录执行。Linux、macOS 和 Windows 使用同一份 Python 代码；解释器名称按环境使用 `python3` 或 `python`。

```sh
python3 -m pip install -r games/game-theory/requirements.txt
python3 games/game-theory/run.py plan
```

`plan` 检查配置并保存不可变清单、种子和代码快照，打印运行规模与存储估算，不调用 API。默认完整清单为 5,888 条件、14,592 场，正常 Jev 请求上限 185,906 次；重试另计。先查看清单，再启动真实请求。

设置环境变量 `OPENROUTER_API_KEY` 后执行：

```sh
python3 games/game-theory/run.py run
```

认证优先使用环境变量；也兼容仓库外父目录 `OpenRouter.txt` 的本地密钥文件。密钥不写入代码、记录或 HTML。固定模型为 `typesafe/jev-1.13-20260917`，不可用时停止而不自动换模型。

已有批次使用 `resume`，无需重新生成清单；`--batch <batch-id>` 指定批次。`run`／`resume --rules-only` 只推进纯规则条件。

```sh
python3 games/game-theory/run.py resume
python3 games/game-theory/run.py validate
python3 games/game-theory/run.py build-html
```

`validate` 和 `build-html` 从已有日志计算，不调用模型；在运行器退出后执行。Git 不包含实际日志或生成页面，新克隆须取得记录包或先完成运行。

## 记录与恢复

`output/records/<batch-id>/` 保存不可变 `manifest.json`、代码快照、实时状态及可重算摘要。该批次的 `scenarios/<scenario>/<condition-id>/` 包含：

| 文件 | 内容 |
| --- | --- |
| `config.json` | 冻结的条件配置 |
| `inputs.jsonl` | 实际完整英文输入 |
| `responses.jsonl` | 按 attempt ID 保存的完整原始响应与错误 |
| `events.jsonl` | 规则行动、干预、结算与恢复事件 |
| `summary.json` | 从日志重算的概况 |

成功响应先落盘，恢复复用已保存响应与行动，不重复结算；失败不会被替代为任意行动。Ctrl+C 停止新提交并收尾，文件锁防止同批次并行写入。明确损坏的完整 JSONL 行报错，仅未完成尾行允许修复。

种子按玩家、阶段、噪声和终止分开派生，不保证远端模型重复选择。清单包含 1／20／100 轮、历史窗口、未知总轮数、随机终止和明确记录的执行扰动。费用只累加 API 返回值，缺失费用单列，不当作零。

## 离线查看

构建后打开 `output/html/index.html`。目录使用阵容图标和筛选；对局页同时显示棋盘、累计收益和实际行动趋势，可手动播放、暂停、调节轮间停留或定位轮次。默认暂停。页面中的链接可查看完整英文输入、原始响应和事件。

HTML 展示全部至少一位 Jev 参与的对局；纯规则记录仍保存在日志中。页面内嵌必要数据与资源，不调用 API，不依赖在线资源或本地服务。复制完整 `output/html/` 文件夹即可离线交付。重新构建先在 `output/` 暂存、校验，再替换正式包，旧包保留在 `html-archive/`。

行动、次数与收益只描述已发生记录，不评准确率，不作模型能力或心理动机结论。

## 测试

```sh
python3 -m pip install pytest
python3 -m pytest games/game-theory/tests -q
```

Node.js 用于实际展示脚本的隔离 DOM 与虚拟时钟测试；未安装时该项明确跳过。测试使用本地 test double，不调用真实 API，不作为 Jev 对局记录。
