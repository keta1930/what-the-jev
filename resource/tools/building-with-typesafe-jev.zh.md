---
title: "building-with-typesafe-jev（aaddrick）"
updated: 2026-10-09
---

# building-with-typesafe-jev（aaddrick）

【定位】building-with-typesafe-jev 是 aaddrick 发布的非官方编码代理 Skill。它的前提是：Jev 答案的质量取决于喂给模型的问题，因此 skill 的核心工作是教代理有意识地设计问题。

【功能】教学内容覆盖三个环节：问题类型的选择、11 条设计规则的套用、阈值的设定。包内附带三类材料——API 参考；官方 4 种使用模式加 cookbook 中的 18 个阈值；按"实现形状"分组、收录 150+ 成例的先例库。代理接到任务后，可在先例库中就近找到与当前任务相似的实例，再对照规则与阈值调整。

【特点】skill 自带评测：据作者自报，安装后平均分从 0.65 升至 0.96。该数字出自作者自己的评测流程，未经独立验证。项目为社区作品，与 TypeSafe AI 无隶属关系。

【适用】适合希望编码代理在调用 Jev 前系统化设计问题与阈值的场景。其中的规则与阈值是作者整理的一套做法，并非官方规范，整体采用前应先审阅；0.65→0.96 为自报数字，引用时应注明出处与验证状态。

## Links

- [GitHub – aaddrick/building-with-typesafe-jev](https://github.com/aaddrick/building-with-typesafe-jev)
