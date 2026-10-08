---
title: "duckdb-jev (colliber)"
updated: 2026-10-09
---

# duckdb-jev (colliber)

**Positioning** duckdb-jev is a DuckDB extension by colliber that moves Jev judgments into SQL. Row-by-row model judgments become part of the query itself rather than a separate processing step, giving analytical datasets an in-SQL route to batch enrichment.

**What it does** Four scalar functions — jev_choice, jev_score, jev_noul, and jev_ask — pose a typed question for every row of a query result — one judgment per row — performing row-by-row classification and scoring directly over Parquet files. Results are cached at the row level, so repeated jobs re-use earlier judgments instead of asking again, and a jev_usage() function reports consumption. A rerun over cached rows issues no new judgments. For engines other than DuckDB, similar extensions — pg_typesafe, sqlite3-jev, and jevql — are tracked in the awesome-jev list linked below, so the same idea is not DuckDB-only.

**Characteristics** Criteria are expressed as column types: ENUM holds the choice options, DOUBLE the scores, STRUCT the structured questions. Validation happens at planning time — option lists are checked against a 255-option cap and duplicate options are rejected — so malformed questions fail before the query runs rather than partway through it, after some rows have already been judged.

**When to use** It fits batch work that enriches analytical datasets with a classification or a score on every row, all inside SQL, without moving the data out of the engine; teams running other engines can turn to the similar extensions tracked in the awesome-jev list instead. The cost caveat is the usual one for this pattern: per-row API calls over large tables add up. That accumulation is what jev_usage() is there to watch.

## Links

- [GitHub – colliber/duckdb-jev](https://github.com/colliber/duckdb-jev)
- [Directory – awesome-jev, similar database extensions](https://github.com/fatwang2/awesome-jev)
