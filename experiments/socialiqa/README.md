# SocialIQA

*English | [简体中文](README.zh.md)*

Evaluate three-option English social-commonsense judgments on 2,224 formal items. Twelve separate interface-debugging items are excluded from accuracy.

## Questions

The example below preserves the exact context, questions and full option set. See the source notice for attribution/license. Actual wording varies by item.

`id`: `socialiqa-test-00001`

```json
{
  "context": "bailey was a nice person so she called the family together.",
  "question": "What will happen to Others?"
}
```

**`answer` — `choice`**

Select the most plausible answer to the question based on the context and everyday social commonsense. Choose exactly one option.

| Key | criteria |
| --- | --- |
| `A` | talk to the family |
| `B` | hate bailey |
| `C` | thank bailey |

## Results

Jev matches 1,792/2,224 reference answers (80.58%) and misses 432. Every formal item has a valid response. The actor-wants source group is higher (84.66%) and actor-attributes lower (78.11%); source groups are not independent psychological abilities.

[English report](report/report_en.md) · [English PDF](report/report_en.pdf) · [Methods](METHODS.md) · [Machine summary](report/generated/summary.json)

## Cost

Formal set: 851,327 input tokens, 84,512 output tokens, USD 0.035755734 reported. Including debugging: 855,948 input tokens, 84,968 output tokens, USD 0.035949816 reported. One failed attempt has unreported billing, with a separate historical USD 0.01 reservation.

## Reproduction

Run from the repository root with Python 3.10+. These commands only prepare/recompute/build locally and make no model calls.

```bash
python -m pip install -r requirements.txt -r experiments/socialiqa/requirements-analysis.txt
python experiments/socialiqa/preparation/code/prepare_data.py
python experiments/socialiqa/report/code/analyze.py
python experiments/socialiqa/report/code/build_report.py
```

With XeLaTeX installed, add --pdf to the report command. All recorded model responses identify typesafe/jev-1.13-20260917. Integration made no new model calls.

For a fresh model run, the shared project entry point is below. Existing successful results are skipped; use a separate experiment copy and new output for an independent run. This entry follows upstream behavior and does not include the original custom budget guards. Historical budgets do not authorize new calls.

The model runner requires Linux/macOS/WSL because upstream uses fcntl, with OPENROUTER_API_KEY set in the environment. Offline analysis runs on Windows.

```bash
python run.py experiments/socialiqa/config.yaml
```

## Source and license

Maarten Sap, Hannah Rashkin, Derek Chen, Ronan Le Bras, Yejin Choi. [SocialIQA](https://maartensap.com/social-iqa/). SocialIQA v1.4. CC BY 4.0.

See the [source record](preparation/SOURCE.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

## Offline integrity check

```bash
python experiments/socialiqa/verify.py
```

All analysis/report helpers are local to this experiment; no other new experiment is required.
