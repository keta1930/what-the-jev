---
title: "从像素识别数字与动物"
date: 2026-10-10
summary: "本实验测试 Jev 模型能否仅凭像素数值识别图像内容。"
samples: 2
input_tokens: 14.0k
cost: 0.000586278
---

# 从像素识别数字与动物

本实验测试 Jev 模型能否仅凭像素数值识别图像内容。

包含 2 条数据：MNIST 测试集第 1 条（28×28 灰度手写数字图），CIFAR-10 测试集第 1 条（32×32 彩色动物图）。输入只有像素数值矩阵，不含图像文件。

每条要求回答一个问题：

1. 手写数字图中写的是哪个数字？输入是 28 行 28 列的灰度像素矩阵，行优先，值为 0 到 255，0 为黑色背景、255 为白色笔画。从 `0` 到 `9` 中选出一项。（`choice`）

   - `0`：数字 0。
   - `1`：数字 1。
   - `2`：数字 2。
   - `3`：数字 3。
   - `4`：数字 4。
   - `5`：数字 5。
   - `6`：数字 6。
   - `7`：数字 7。
   - `8`：数字 8。
   - `9`：数字 9。

2. 彩色图中主体属于哪一类？输入是 `r`、`g`、`b` 三个 32 行 32 列的像素矩阵，行优先，值为 0 到 255。从 `airplane`、`automobile`、`bird`、`cat`、`deer`、`dog`、`frog`、`horse`、`ship`、`truck` 中选出一项。（`choice`）

   - `airplane`：飞机。
   - `automobile`：汽车。
   - `bird`：鸟。
   - `cat`：猫。
   - `deer`：鹿。
   - `dog`：狗。
   - `frog`：蛙。
   - `horse`：马。
   - `ship`：船。
   - `truck`：卡车。

## 结果

两个问题上 Jev 都未能从像素数值识别出图像内容，概率分布接近均匀，等同随机选择。

MNIST 样本真实标签为 7。`digit` 判为 `2`，判错。十个选项的概率落在 0.04 到 0.19 之间，正确选项 `7` 仅 0.10，`confidence` 0.09。

CIFAR-10 样本真实标签为 `cat`。`category` 判为 `automobile`，判错。十个选项的概率落在 0.03 到 0.14 之间，`cat` 为 0.13，`confidence` 0.04。

成本：输入 13959 个 token，输出 178 个，费用 `0.000586278` 美元。输出不计费。

## 复现

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/pixel-recognition/config.yaml
```

结果追加写入 `result/responses.jsonl`。每条数据每轮运行只请求一次，重跑时跳过已成功的记录；上次运行失败的记录会被清理并自动重新请求。
