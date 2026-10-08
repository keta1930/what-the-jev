---
title: "duckdb-jev（colliber）"
updated: 2026-10-09
---

# duckdb-jev（colliber）

【定位】duckdb-jev 是 colliber 开发的 DuckDB 扩展，把 Jev 判定引入 SQL 查询。逐行的模型判定由此成为查询本身的一部分，为分析数据集的批量加工提供 SQL 内的实现方式。

【功能】扩展提供 jev_choice、jev_score、jev_noul、jev_ask 四个标量函数，对查询结果的每一行提出一个类型化问题，直接作用于 Parquet 文件做逐行分类与打分。结果按行缓存，jev_usage() 函数报告用量。其他引擎的同类扩展——pg_typesafe、sqlite3-jev、jevql——收录在下方链接的 awesome-jev 清单中。

【特点】criteria 以列类型表达：choice 选项用 ENUM，score 打分用 DOUBLE，结构化问题用 STRUCT。问题校验发生在查询规划期——选项数以 255 为上限，重复选项被拒绝——格式不当的问题在查询运行前即失败，而非中途报错。

【适用】适合用 SQL 批量加工分析数据集、为每一行附加模型分类或评分的场景；使用其他引擎的团队可参考 awesome-jev 清单中的对应扩展。大表上逐行调用 API 的开销会累积，需借助 jev_usage() 盯住用量与成本。

## Links

- [GitHub – colliber/duckdb-jev](https://github.com/colliber/duckdb-jev)
- [Directory – awesome-jev 同类数据库扩展清单](https://github.com/fatwang2/awesome-jev)
