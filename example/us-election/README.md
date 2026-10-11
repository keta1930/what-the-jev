---
title: "US Presidential Elections: Winners and Information Cutoffs"
date: 2026-10-11
summary: "This example tests Jev's knowledge of US presidential election winners from 1996 to 2024 and its response to an information cutoff."
samples: 9
input_tokens: 3.3k
cost: 0.000137844
---

# US Presidential Elections: Winners and Information Cutoffs

This example tests Jev's knowledge of US presidential election winners from 1996 to 2024 and its response to an information cutoff.

It contains 9 samples: eight election questions (`E01`–`E08`), one for each election from 1996 to 2024, and a second 2020 question (`E09`) restricted to information available before 2019. `E02` and `E09` have the same state and candidates; only the instructions differ.

## Questions

1. `E01`–`E08`: "Judge which candidate won this election."
2. `E09`: "Judge which candidate won this election, using only information available before 2019. Do not use any information about events after 2018."

Both use `choice`: `winner` returns one of `republican`, `democratic`, or `other`, with `probabilities` and `confidence`. The candidate options are:

| Sample | Election | `republican` | `democratic` |
| --- | --- | --- | --- |
| `E01` | 2024 | The Republican candidate Donald Trump wins. | The Democratic candidate Kamala Harris wins. |
| `E02`, `E09` | 2020 | The Republican candidate Donald Trump wins. | The Democratic candidate Joe Biden wins. |
| `E03` | 2016 | The Republican candidate Donald Trump wins. | The Democratic candidate Hillary Clinton wins. |
| `E04` | 2012 | The Republican candidate Mitt Romney wins. | The Democratic candidate Barack Obama wins. |
| `E05` | 2008 | The Republican candidate John McCain wins. | The Democratic candidate Barack Obama wins. |
| `E06` | 2004 | The Republican candidate George W. Bush wins. | The Democratic candidate John Kerry wins. |
| `E07` | 2000 | The Republican candidate George W. Bush wins. | The Democratic candidate Al Gore wins. |
| `E08` | 1996 | The Republican candidate Bob Dole wins. | The Democratic candidate Bill Clinton wins. |

For every sample, `other` is "Another candidate wins, the election has not been held, or the winner cannot be determined."

## Minimal Example

The cutoff sample `E09`, with `model` omitted from the input:

```json
{
  "state": "The 2020 US presidential election",
  "questions": {
    "winner": {
      "type": "choice",
      "instructions": "Judge which candidate won this election, using only information available before 2019. Do not use any information about events after 2018.",
      "criteria": {
        "republican": "The Republican candidate Donald Trump wins.",
        "democratic": "The Democratic candidate Joe Biden wins.",
        "other": "Another candidate wins, the election has not been held, or the winner cannot be determined."
      }
    }
  }
}
```

The model's output (key fields only):

```json
{
  "answers": {
    "winner": {"type": "choice", "choice": "other", "probabilities": {"republican": 0.03, "democratic": 0, "other": 0.97}, "confidence": 0.95}
  },
  "usage": {"input_tokens": 386, "output_tokens": 42, "cost": 0.000016212}
}
```

Jev chose `other`, consistent with the election not yet having taken place at the requested cutoff. This differs from the dataset's retained reference answer `democratic`, which records the actual winner.

## Results

All 9 samples returned successfully; there are no failed samples in the results below.

For the eight unrestricted questions (`E01`–`E08`), seven match the reference winner. The 2024 election was judged `other`, contradicting the reference answer `republican` (`other` 0.53, `republican` 0.44, `democratic` 0.03, `confidence` 0.30). The model did not identify a winner with confidence. The other seven elections were each judged at probability 1 and `confidence` 1.

The 2020 comparison shows how the cutoff changes the answer:

| Sample | Information restriction | Choice | `republican` probability | `democratic` probability | `other` probability | `confidence` |
| --- | --- | --- | --- | --- | --- | --- |
| `E02` | None | `democratic` | 0 | 1 | 0 | 1 |
| `E09` | Before 2019 only | `other` | 0.03 | 0 | 0.97 | 0.95 |

Without the cutoff, Jev identifies Biden as the winner. With the cutoff, it selects the option covering an election that has not been held or a winner that cannot be determined. This pair shows that the time restriction changes the model's judgment rather than leaving it at the known historical outcome. Because `other` combines several meanings, the response does not identify which of those meanings the model selected.

Across all 9 samples, 7 match the stored reference answers. The two mismatches have different interpretations: `E01` misses an unrestricted historical winner, while `E09` gives an answer consistent with the cutoff but is still compared against the actual winner in its reference.

## Cost

The English results total 3282 input tokens, 392 output tokens, and `0.000137844` USD. `E09` accounts for 386 input tokens, 42 output tokens, and `0.000016212` USD.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/us-election/config.yaml
```

The run processes the English dataset `data/dataset.json` and the Chinese dataset `data/dataset_zh.json`, appending results to `result/responses.jsonl` and `result/responses_zh.jsonl` respectively. Each sample is requested only once per run; records that already succeeded are skipped on reruns, and records that failed in the previous run are cleared and requested again.
