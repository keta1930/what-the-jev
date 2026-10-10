---
title: "chinese-laya (yanqiangmiffy)"
updated: 2026-10-10
---

# chinese-laya (yanqiangmiffy)

【定位】chinese-laya 是 yanqiangmiffy 的中文适配实验与工程复现记录：把公开英文类型化决策数据集的自然语言字段机译为简体中文，再微调 Laya 多语言决策 checkpoint 的编码器与决策头。它是单次微调实验的记录，自述不是 Laya 官方训练器、官方中文模型或官方 benchmark，训练权重未发布。

【功能】仓库包含翻译与微调脚本、中文数据划分、基线与评测报告，以及含 9 个场景、27 条参考样本的本地 React 加 FastAPI 演示。在 2000 题中文测试集上，作者自报校准后的目标类一致率为原始多语言 checkpoint 34.05%、4 epoch 微调 74.95%、10 epoch 运行最优轮 76.25%；同一组 checkpoint 上 Soft-target NLL 由 1.2374 降至 0.8706，score 期望值 MAE 由 0.7172 降至 0.2358，ECE 由 0.0764 升至约 0.15。作者据此认为不宜声称全面改善。

【特点】数据源为 LocalLLaMA/typed-decisions（Apache-2.0）的四条合成工作流 agent_trace_observability、customer_service、invoice_processing、security_incidents，经 OpenAI 兼容接口用 Ternary-Bonsai-2-27B 逐字段翻译，case ID、候选顺序、枚举值与金标概率保持原值。划分为 960/120/120/400 个 case，即 4800/600/600/2000 题，题型为 choice、score、noul，每 case 5 题。训练在单张 A800 80GB 上从 322M 参数的 convaiinnovations/laya-multilingual checkpoint 出发，损失为 soft-target 交叉熵加 RLCD 风格策略项。仓库为 Apache-2.0，权重与训练目录未随仓库提交。

【适用】适合需要中文决策模型微调参考的读者，或作为复现与扩展该实验的起点。不适合据此判断真实中文业务准确率：作者说明结果反映的是对机译 benchmark 的拟合，译文未经专家复核，监督标签来自原始英文数据集，数字来自单次运行且无置信区间。

## Links

- [GitHub – 仓库](https://github.com/yanqiangmiffy/chinese-laya)
- [HF – 基座 checkpoint laya-multilingual](https://huggingface.co/convaiinnovations/laya-multilingual)
- [HF – 源数据集 typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions)
