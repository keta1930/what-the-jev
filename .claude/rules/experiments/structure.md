# 结构

`experiments/<name>/` 的骨架与新增流程。报告的内容与结构按 `.claude/rules/experiments/report.md`，运行配置的字段含义按 `AGENTS.md`，代码措辞按 `.claude/rules/code/style.md`。

## 定位

实验是可复现的单轮评测：样本规模大，数据来自外部来源，交付物是 `report/` 下的双语报告；报告之外一并提交取数与构建脚本、数据集和结果。实验不写 README。

## 目录骨架

```text
experiments/<name>/
├── config.yaml    运行配置
├── data/          发给模型的数据集
├── preparation/
│   ├── raw/       下载的原始数据
│   └── code/      取数与构建脚本
├── result/        结果
└── report/        双语报告与配图
```

目录名小写连字符，在 `experiments/` 内唯一。`preparation/` 与 `report/` 按需取用；报告目录内部的组成按 `.claude/rules/experiments/report.md`。

## 变体（消融）

同一实验有多个版本时，配置、数据、结果各加同名后缀：

- 配置：无变体写 `config.yaml`，有变体写 `config.<variant>.yaml`。
- 数据：`data/dataset.<variant>.json`。
- 结果：无变体的基线写 `result/responses.jsonl`，有变体写 `result/responses.<type>.<variant>.jsonl`，`<type>` 取该问的答案类型。

## config.yaml

本文件只规定实验特有的部分：`data` 与 `output` 等长且同序对应，路径相对本目录；`repeat` 显式写出。

```yaml
data: data/dataset.json
output: result/responses.jsonl
```

多组数据时 `data` 与 `output` 写成长度相同的列表。其余字段照 `AGENTS.md` 的配置表填写。

## 数据、原始数据与结果

- 数据集的字段与校验见 `schema/dataset.schema.json`；标准答案与分组维度随样本内联。
- `preparation/raw/` 原样保留下载内容，不手工编辑。
- `preparation/code/` 从 `raw/` 产出 `data/`；脚本以 `python <script>` 直接运行。
- `result/` 逐行保存完整响应，随目录提交。

## 新增流程

1. 建目录，把取到的原始数据放入 `preparation/raw/`，写 `preparation/code/` 脚本产出 `data/dataset.json`。
2. 写 `config.yaml`。
3. 运行 `run.py`，生成 `result/responses.jsonl`。
4. 写 `report/scripts/`，产出报告配图。
5. 写报告，按 `.claude/rules/experiments/report.md`。
6. 更新 `experiments/INDEX.md` 与 `experiments/INDEX.zh.md`：插入对应分组，组内编号顺延；条目为不带标签的一句话，链到该实验的报告，英文索引链英文报告，中文索引链中文报告。
7. 更新根 `README.md` 与 `README.zh.md` 的仓库结构树：在 `experiments/` 下加一行，后接场景标签与一句话简介；英文用方括号标签，中文用【】标签。

## 验证

```bash
PYTHONPATH=src python -m pytest tests
export OPENROUTER_API_KEY='<key>'
python run.py experiments/<name>/config.yaml
```

结果文件的记录数与数据集样本数一致；报告配图可由 `report/scripts/` 重新生成。

## 交付前自检

逐条回答，任一为「是」则先改。

- 目录名不是小写连字符，或在 `experiments/` 内重名？
- 变体的配置、数据、结果未加同名后缀，或结果缺答案类型段？
- 结果文件未提交，或 `data/` 可由 `preparation/code/` 从 `raw/` 重新产出而不一致？
- 报告缺中文版本，或有配图无法由 `report/scripts/` 重新生成？
- `experiments/` 两份索引未同步，或根 README 结构树未加行？
- 有内容违 `.claude/rules/experiments/report.md` 或 `.claude/rules/code/style.md`？
