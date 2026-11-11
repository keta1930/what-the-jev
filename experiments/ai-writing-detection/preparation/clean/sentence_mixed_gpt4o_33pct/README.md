# GPT-4o-mini 句子级混合语料

## 用途

本目录用于检验检测器能否在同一篇文章内识别并定位 AI 改写句。语料由既有的人工文章与既有的 GPT-4o-mini 整篇改写版本在本地对齐后生成；本次构建没有调用 JEV、GPT 或其他外部 API，因此没有新增模型费用。

## 实验条件

- 条件名：`sentence_unit_mixed_gpt4o_mini_33pct`
- AI 来源模型：`openai/gpt-4o-mini-2024-07-18`
- 中文：100 篇，共 5,652 句，其中 AI 句 1,886、人工句 3,766
- 英文：100 篇，共 5,863 句，其中 AI 句 1,958、人工句 3,905
- 每篇目标比例：约 1/3 AI 句、2/3 人工句
- 位置控制：每篇文章的开头、中部、结尾三个位置段均包含 AI 替换单元

## 混合方法

先将人工原文和 GPT-4o-mini 整篇改写分别分句，再进行保持原顺序的语义单元对齐。对齐支持 `1↔1`、`1↔2`、`2↔1`、`2↔2`，并允许少量 `1↔3`、`3↔1` 修复。

抽中某个语义单元时，整组人工句会被整组 AI 句替换，不会只替换其中一半。这可以避免模型合句或拆句造成同一意思重复出现、或部分意思遗漏。选择规则固定且可复现。

## 文件结构

- `zh/ZH001.txt`—`ZH100.txt`：中文混合文章
- `en/EN001.txt`—`EN100.txt`：英文混合文章
- `zh/metadata/*.json`、`en/metadata/*.json`：逐篇来源与对齐元数据
- `zh/sentences.jsonl`、`en/sentences.jsonl`：逐句真值表
- `BUILD_SUMMARY.json`：构建统计
- `INDEPENDENT_AUDIT.json`：独立来源审计结果

## 逐句真值字段

- `origin`：`human` 或 `ai`
- `sentence_index`：混合文章中的句序
- `paragraph_index`：混合文章中的段落序号
- `text`：实际输出句
- `alignment_unit_index`：语义对齐单元编号
- `source_human_sentence_index`：保留的人工句在原文中的句序
- `source_ai_sentence_index`：AI 句在 GPT-4o-mini 改写稿中的句序
- `human_sentence_indices`：AI 单元所替换的人工句序范围
- `output_sha256`、`source_human_sha256`、`source_ai_sha256`：来源校验哈希

## 审计结论

独立审计通过，确认：

1. 中英文各 100 篇均完整；
2. 所有人工句和 AI 句都能回溯到对应源文件；
3. 每篇人工原文的句子均恰好被保留或被一个 AI 单元替换一次；
4. 逐句表能准确重建混合文章；
5. 没有重复的混合文章；
6. 没有发现相邻跨来源的高相似重复。

注意：本目录仅包含语料和真值，尚未送入 JEV 或其他检测器。后续检测时，应将 `.txt` 文章作为输入，将 `sentences.jsonl` 作为答案表，不要把元数据一起提交给检测器。
