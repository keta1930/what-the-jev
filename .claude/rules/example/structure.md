# 结构

`example/<name>/` 的骨架与新增流程。README 的内容与措辞按 `.claude/rules/example/report.md`，运行配置的字段含义按 `AGENTS.md`，代码措辞按 `.claude/rules/code/style.md`。

## 定位

示例是轻量的单轮实验：样本少，自包含，一个目录即可读完全貌。示例交付运行配置、双语数据集与结果、双语 README；不设 `preparation/`，不产报告。

## 目录骨架

```text
example/<name>/
├── README.md            英文说明
├── README.zh.md         中文说明
├── config.yaml          运行配置
├── data/
│   ├── dataset.json     英文数据集
│   └── dataset_zh.json  中文数据集
└── result/
    ├── responses.jsonl     英文结果
    └── responses_zh.jsonl  中文结果
```

目录名小写连字符，概括场景，在 `example/` 内唯一。两份 README 各以自己的语言写标题。

## 双语约定

示例的每类产物都成对：数据集、结果、README 各有英文与中文两份。

- 中文数据集与英文结构相同，题干译为中文；`questions` 与 `criteria` 的键保持原值。
- 中文 README 用中文写作，引用等级文本与选项描述时抄中文数据集的原文。

## config.yaml

本文件只规定示例特有的部分：`data` 与 `output` 各两条，按英文、中文同序一一对应，路径相对本目录；示例不写 `repeat`。

```yaml
data:
- data/dataset.json
- data/dataset_zh.json
output:
- result/responses.jsonl
- result/responses_zh.jsonl
```

其余字段照 `AGENTS.md` 的配置表填写。

## 数据与结果

- 数据集的字段与校验见 `schema/dataset.schema.json`。
- 结果由 `run.py` 产生，逐行保存完整响应，随目录提交；README 中的数字核自结果文件。

## 新增流程

1. 建目录，写 `config.yaml`。
2. 写 `data/dataset.json`，再写结构相同、题干为中文的 `data/dataset_zh.json`。
3. 运行 `run.py`，生成 `result/responses.jsonl` 与 `result/responses_zh.jsonl`。
4. 写 `README.md` 与 `README.zh.md`，按 `.claude/rules/example/report.md`。
5. 更新 `example/INDEX.md` 与 `example/INDEX.zh.md`：插入对应分组，组内编号顺延；条目为不带标签的一句话，英文索引只链 `.md`，中文索引只链 `.zh.md`。
6. 更新根 `README.md` 与 `README.zh.md` 的仓库结构树：在 `example/` 下加一行，后接场景标签与一句话简介；英文用方括号标签，中文用【】标签。

## 验证

```bash
PYTHONPATH=src python -m pytest tests
export OPENROUTER_API_KEY='<key>'
python run.py example/<name>/config.yaml
```

两条结果文件的记录数均与各自数据集的样本数一致。

## 交付前自检

逐条回答，任一为「是」则先改。

- 目录名不是小写连字符，或在 `example/` 内重名？
- 缺中文的数据集、结果或 README 中任一项？
- `data` 与 `output` 不是各两条、顺序不对应，或路径不是相对本目录？
- 结果文件未提交，或 README 数字不是核自结果文件？
- `example/` 两份索引未同步，或根 README 结构树未加行？
- 有内容违 `.claude/rules/example/report.md` 或 `.claude/rules/code/style.md`？
