---
title: "Laya (ConvAI Innovations)"
updated: 2026-10-09
---

# Laya (ConvAI Innovations)

【定位】多语言非自回归决策引擎，以单次前向传播对文本状态输出类型化决策（分类、评分、是非判断），用高速确定性推理替代生成式 LLM。

【功能】以类型化问题定义决策需求，单次前向传播返回答案与校准置信度，无文本生成、无幻觉。Router 亚毫秒检测语言与文字系统，在三个检查点间自动路由，覆盖 100+ 语言。支持在自有决策数据上微调，项目自报：微调后基准准确率可从 0.362 提升至 0.766。另提供 Jev 兼容 HTTP 服务、MCP、LangChain 集成、CLI 与网页演练场。

【特点】基于 ModernBERT 与 mmBERT 编码器，以强化学习配合严格恰当评分规则训练；T4 上单题约 33 毫秒、批量每题 7.2 毫秒（项目公布口径）；长文档支持 8192 token，可选 ONNX 与 TileLang GPU 加速路径，并配套 Docker 与 NixOS 部署方案。

【适用】适合工单分诊、邮件路由、内容审核、流失预警等高吞吐结构化决策场景，尤其是多语言生产环境——Router 会按输入自动选择检查点——与不能容忍幻觉的业务。不适合开放式文本生成、多步复杂推理，以及超出长文档能力边界的深度理解需求。

## Links

- [Website – 项目主页](https://laya.convaiinnovations.com/)
- [GitHub – 源码与 laya-serve](https://github.com/NandakishorM/laya)
- [HF – 模型权重](https://huggingface.co/convaiinnovations/laya)
- [PyPI – laya 安装包](https://pypi.org/project/laya/)
