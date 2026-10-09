# Style

Comments and wording in this repository's Python code (`src/`, `tests/`, `run.py`, and the scripts under `experiments/` and `example/`) follow this file. Reference implementations: `src/decision_models/runner.py`, `tests/test_results.py`.

## Comments

All comments are English and describe the current code; they never record history or what changed.

- One line at script level, on the first line; every script with content has one.
- At most one line per function, covering what the name and signature do not: timing, side effects, a lock the caller must hold, how the return value is judged. A function whose name already says it, including tests named after their case, has none.
- Keep only the line comments the code cannot supply, and delete the rest.

A line comment is necessary when it carries information the code cannot express:

- External identifiers and provenance: paper IDs, data sources, passwords, licenses.
- Units, encodings, and ordering conventions, such as output paths expanding by data order and then by round.
- The reason for an unusual construct: a race, a fallback branch, why a more direct form is not used.

Delete what the code already reflects:

- A restatement of what the adjacent code does.
- A restatement of a function docstring or an error message already in the same file; a field annotation repeating a rule stated elsewhere is the same case.
- A meaning the type or the field name already carries.

## Wording

Everything written for a human is English, all four kinds together: `print`, `raise`, `logger`, and `argparse` help and usage.

- An error states the failing object and the cause, such as `f'duplicate sample id on line {number} of the result file: {sample_id}'`.
- Identifiers keep their original values and are not translated: field names, option keys, answer types, model IDs, paths, and status-code fields, such as `id`, `response`, `error`, `noul`, `typesafe/jev-1.13`.
- Text that comes with a dataset or is sent to a model (`criteria`, level text, `instructions`, judge prompts) is experiment material, not code wording, and stays as it is; the same holds for notes written into data files (`raw/*.jsonl`).
- When a test asserts on wording, update the assertion with it and search the whole repository for leftover references to the old wording.

## Exceptions

- Non-ASCII fixtures a test builds on purpose stay: `'中文'`, which checks an `ensure_ascii=False` round trip, and `'中'.encode('utf-8')[:2]`, which checks a truncated UTF-8 tail.
- Tool directives such as `# noqa: E402` are not comments and stay. Interpreter directives are deleted; scripts are always invoked as `python <script>`.

## Running a Wording Pass

Rewording a comment or a human-facing string changes no behaviour: no logic, no formatting, no opportunistic refactoring.

- Prove afterwards by token-level comparison that only strings and comments changed: drop string tokens, f-string fragments, and comments, then compare token types and text file by file. An f-string rewrite adds or removes literal segments, so do not compare AST node counts.
- Run `PYTHONPATH=src python -m pytest tests`; a pass is done only when the suite is green.

## Pre-delivery Self-check

Answer each item; if any answer is yes, fix it before delivering.

- Any comment or wording still in Chinese?
- Any script without its one-line script-level comment?
- Any line comment restating code, a function docstring, or an error message in the same file?
- Any function comment that says nothing beyond the function name?
- Any comment about history or what changed?
- Any identifier translated, or dataset text rewritten?
- Any test assertion still pointing at old wording, or old wording left unsearched?
- Any logic, formatting, or structure changed along the way?
- The test suite not run, or the token-level comparison not run?
