# SocialIQA

*[English](README.md) | 简体中文*

检验英语社会常识三选一判断。正式集包含 2,224 题，另有 12 道接口调试题，不并入准确率。

## 提问

以下示例逐字保留材料、设问和完整选项；署名与许可见来源说明。每题实际文本随材料变化。

`id`: `socialiqa-test-00001`

```json
{
  "context": "bailey was a nice person so she called the family together.",
  "question": "What will happen to Others?"
}
```

**`answer` — `choice`**

Select the most plausible answer to the question based on the context and everyday social commonsense. Choose exactly one option.

| Key | criteria |
| --- | --- |
| `A` | talk to the family |
| `B` | hate bailey |
| `C` | thank bailey |

## 结果

报告暂不纳入本次提交，待与项目维护者共同讨论后编写。保留完整模型回答、离线分析代码和机器可读统计。

[方法说明](METHODS.zh.md) · [机器汇总](report/generated/summary.json)

## 成本

正式集：851,327 输入 token，84,512 输出 token，已报告费用 0.035755734 美元。含调试：855,948 输入 token，84,968 输出 token，已报告费用 0.035949816 美元。一次失败无已报告费用，另记历史预留 0.01 美元。

## 复现

从仓库根目录执行，以下命令只做本地准备和复算，不调用模型。Python 3.10+。

```bash
python -m pip install -r requirements.txt -r experiments/socialiqa/requirements-analysis.txt
python experiments/socialiqa/preparation/code/prepare_data.py
python experiments/socialiqa/report/code/analyze.py
```

所有模型响应记录的版本均为 `typesafe/jev-1.13-20260917`。本次整合未新增模型调用。

实际重新调用使用下列项目统一入口。现有结果会被跳过；独立新实验应复制目录并使用新的 output 文件。此入口按上游规则执行，不包含原独立实验的预算保护。原历史预算不自动授权新调用。

模型运行入口需 Linux/macOS/WSL（上游使用 `fcntl`），并在环境中设置 `OPENROUTER_API_KEY`。离线分析脚本可在 Windows 运行。

```bash
python run.py experiments/socialiqa/config.yaml
```

## 来源与许可

Maarten Sap, Hannah Rashkin, Derek Chen, Ronan Le Bras, Yejin Choi. [SocialIQA](https://maartensap.com/social-iqa/). SocialIQA v1.4. CC BY 4.0.

详见 [来源记录](preparation/SOURCE.md) 与 [第三方许可说明](THIRD_PARTY_NOTICES.md)。

## 离线完整性检查

```bash
python experiments/socialiqa/verify.py
```

本目录包含全部分析依赖，不依赖其他新增实验。
