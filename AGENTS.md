# AGENTS.md

This repository runs single-turn decision experiments on the Jev decision model with the `decision-models` framework: given a dataset, it requests each sample one at a time, saves the complete responses, and writes reports from them.

## Knowledge Sources

| Content | Location |
| --- | --- |
| What Jev is, how it answers, capability boundaries, pricing | `docs/jev/en/what-is-jev.md` |
| Question design, reading answers, thresholds | `docs/jev/en/using-jev.md` |
| Request and response fields, error codes | `docs/jev/en/openrouter-api.md` |
| Experiment README conventions | `.claude/rules/experiment-readme.md` |
| Report conventions | `.claude/rules/report-content.md` |
| Resource entry conventions | `.claude/rules/resource-entry.md` |

`docs/jev/zh/` holds the Chinese versions of the same documents.

## Code Architecture

The entry point is `run.py`; the core lives in `src/decision_models/`.

| Module | Responsibility |
| --- | --- |
| `run.py` | CLI entry: `python run.py [config.yaml]`; defaults to `example/ticket-triage/config.yaml` when the argument is omitted |
| `config.py` | Loads and validates `config.yaml` |
| `data.py` | Validates datasets against `schema/dataset.schema.json` and returns the sample list |
| `client.py` | Sends a single HTTP POST and returns the status code and response text; it does not parse business answers and does not retry |
| `results.py` | Locking, appending, history validation, and trailing-partial-line repair for result files |
| `runner.py` | Orchestration: concurrent scheduling, result writing, progress display, and summaries |
| `json_utils.py` | Strict JSON parsing (rejects duplicate fields and NaN/Infinity) and schema validation |
| `logger.py` | CLI logging setup |

Data flow: `config.yaml` → `data/dataset.json` → per-sample POST to `endpoint` → `result/*.jsonl`.

## Configuration

`config.yaml` fields:

| Field | Required | Description |
| --- | --- | --- |
| `model` | yes | Model ID, e.g. `typesafe/jev-1.13` |
| `endpoint` | yes | Request URL, e.g. `https://openrouter.ai/api/alpha/decisions` |
| `data` | yes | Dataset path, relative to the config file's directory; may be a list of paths (e.g. bilingual `dataset_zh.json` and `dataset_en.json`), in which case it pairs one-to-one with the `output` list |
| `output` | yes | Result path, must end in `.jsonl`, relative to the config file's directory; when `data` is a list it must be a list of the same length, and paths must not repeat |
| `concurrency` | no | Initial concurrency, 1 to 16, default 4 |
| `repeat` | no | Repeat rounds, at least 1, default 1; when greater than 1, results are written as `responses_1.jsonl`, `responses_2.jsonl`, etc. |

Supplying more or fewer fields than this set is an error: all four required fields must be present, and the only allowed optional fields are `concurrency` and `repeat`.

`OPENROUTER_API_KEY` is read from the environment; a missing key is an error.

## Running

```bash
export OPENROUTER_API_KEY='<key>'
python run.py experiments/<name>/config.yaml
```

- Each sample is requested once per round; successful records are skipped on rerun.
- Failed records left by a previous run are dropped and re-requested on the next run; failures from the current run stay in the result file.
- If a result file is locked by another run, the process exits with an error.
- Concurrency adjusts by adding one on success and halving on failure, capped at 16.
- On interruption, no new requests are submitted; in-flight requests finish writing, and the file tail stays resumable.

## Data and Result Formats

`data/dataset.json` (`schema/dataset.schema.json`):

- The top level contains only `schema_version` (fixed at `1`) and `samples`.
- Each sample has an `id` (non-empty string, unique within the dataset) and an `input`; `input` contains `state` and `questions`.
- `questions` maps question names to question objects; each question's `type` is `noul`, `choice`, or `score`. When `type` is `choice`, `instructions` and `criteria` are required.
- Samples may also carry `reference` and `metadata`.

The request body sent to `endpoint` merges `model` with the sample's `input`; `id`, `reference`, and `metadata` are not sent.

`result/*.jsonl` (`schema/result.schema.json`): one `{"id": ..., "response": ..., "error": ...}` object per line. `response` is the complete JSON returned by `endpoint`, unmodified; `error` is `null` or `{"type": ..., "message": ...}`, where `type` is `network`, `http`, or `invalid_json`, and `http` additionally carries `status`.

## Directory Conventions

```
experiments/<name>/          formal experiments
example/<name>/              small examples with READMEs
├── config.yaml              run configuration
├── data/dataset.json        samples sent to the model
├── preparation/             raw data and preparation scripts, optional
│   ├── raw/                 downloaded raw data
│   └── code/                cleaning and construction scripts
├── result/responses.jsonl   results
└── report/                  reports, optional

resource/                     catalog of Jev-related resources (projects and models only; no papers, no articles)
├── README.md / README.zh.md bilingual index: title, path, and a brief summary per entry
└── <category>/              closed-source-models, open-source-models, use-cases,
                             integrations, tools, benchmarks
```

`docs/jev/` is the Jev knowledge base, `.claude/rules/` the writing conventions.

## Tests

```bash
PYTHONPATH=src python -m pytest tests
```

Covers config validation, concurrent scheduling, result-file validation and trailing-line repair, and logging setup.
