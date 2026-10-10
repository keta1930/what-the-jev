---
title: "US Presidential Election"
date: 2026-10-10
summary: "This experiment tests whether the Jev model knows the outcomes of the eight US presidential elections from 1996 to 2024."
samples: 8
input_tokens: 2.9k
cost: 0.000121632
---

# US Presidential Election

This experiment tests whether the Jev model knows the outcomes of the eight US presidential elections from 1996 to 2024.

It contains 8 samples, one per election, with states "The 2024 US presidential election", "The 2020 US presidential election", "The 2016 US presidential election", "The 2012 US presidential election", "The 2008 US presidential election", "The 2004 US presidential election", "The 2000 US presidential election", and "The 1996 US presidential election".

Each sample asks the same question:

1. "Judge which candidate won this election." Choose one of `republican`, `democratic`, `other`. (`choice`)

   - `republican`: the Republican candidate wins. The candidates by election are Trump, Trump, Trump, Romney, McCain, Bush, Bush, Dole.
   - `democratic`: the Democratic candidate wins. The candidates by election are Harris, Biden, Hillary Clinton, Obama, Obama, Kerry, Gore, Bill Clinton.
   - `other`: "Another candidate wins, the election has not been held, or the winner cannot be determined."

## Results

`winner`: seven of the eight elections were judged correctly. The 2024 election was judged `other`, contradicting the reference answer `republican` (`other` 0.53, `republican` 0.44, `democratic` 0.03, `confidence` 0.30); the model leaned toward `republican` but fell back to `other`. The other seven elections were each judged at probability 1 and `confidence` 1.

Cost: 2896 input tokens, 350 output tokens, `0.000121632` USD. Output tokens are not billed.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/us-election/config.yaml
```

The run processes the English dataset `data/dataset.json` and the Chinese dataset `data/dataset_zh.json`, appending results to `result/responses.jsonl` and `result/responses_zh.jsonl` respectively. Each sample is requested only once per run; records that already succeeded are skipped on reruns, and records that failed in the previous run are cleared and requested again.
