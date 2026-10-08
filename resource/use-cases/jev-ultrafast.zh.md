---
title: "jev-ultrafast (browser-use)"
updated: 2026-10-09
---

# jev-ultrafast (browser-use)

【定位】jev-ultrafast 是 Browser Use 官方组织出品的浏览器 agent，用 Jev 替代常见的"感知—规划—行动"循环，示范"决策交给 Jev、只在真正需要文本时才生成"的分工模式。

【功能】每个周期只发一次 Jev 请求，同时决定浏览器操作（CLICK、TYPE、SELECT 等）与目标元素；仅当动作是 TYPE 时才调用小 LLM 生成要输入的文本，每周期模型成本为一次决策调用加至多一次小生成调用。Agent 由结构化页面状态驱动，不使用截图，决策输入紧凑、循环更快。仓库附带 inspector，用于检查结构化页面状态。

【特点】项目自报的量化对比：基线流程的协议调用从 1092 次降到 101 次，演示任务"苏黎世→伦敦机票搜索"耗时 7.1 秒；以上数字均未经第三方验证。

【适用】适合在 Jev 上构建决策驱动浏览器自动化的开发者作为实现参考，尤其是希望压缩协议调用、收紧决策循环的场景。其分工模式——每步一次类型化决策、仅在文本输入环节生成——也可迁移到其他决策驱动的 agent。仓库定位是示范实现，数字为项目自报，采信前需自行验证。

## Links

- [GitHub – jev-ultrafast 仓库](https://github.com/browser-use/jev-ultrafast)
