---
title: "JEV Paper Radar (Eliot5566)"
updated: 2026-10-09
---

# JEV Paper Radar (Eliot5566)

【定位】JEV Paper Radar 是 Eliot5566 基于 Jev 构建的每日论文雷达，对 arXiv 全量新入库论文按声明兴趣逐篇筛选。

【功能】对每篇新列入的 arXiv 论文（全量、而非精选子集），每个声明的兴趣发一个 Jev Noul 问题，命中结果渲染成 must-read 页面并提供 RSS 订阅。整条管线 fork-and-go：fork 仓库即可运行，无需自建服务器。仓库附带 calibrate 命令，可按读者自己的判断校准阈值。

【特点】作者实测基准：501 篇论文 33 秒筛完，花费 $0.0196；系统综述筛查模式在 4 个 Cochrane 评审上复现 96.9% recall、节省 78% 筛查工作量。以上数字均为作者自报。

【适用】适合低成本筛选大批文献的场景，如每日论文跟踪与系统综述初筛；其用法模式是语料库规模的大量小型校准决策——每篇论文每个兴趣一次轻量类型化提问。效果数字为作者自报而非第三方验证，采信前建议先用 calibrate 命令按自己的判断调校阈值。

## Links

- [GitHub – Eliot5566/JEV-Paper-Radar 仓库](https://github.com/Eliot5566/JEV-Paper-Radar)
- [Demo – 生成的 must-read 页面](https://eliot5566.github.io/JEV-Paper-Radar/public/)
