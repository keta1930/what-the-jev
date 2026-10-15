---
title: "Estimating JEV's Knowledge Cutoff Date"
date: 2026-10-15
summary: "Estimate JEV's knowledge cutoff using monthly news facts, with GPT-4.1-mini as a control whose cutoff is known."
samples: 1680
input_tokens: 630.7k
cost: 0.026487636
---

# Estimating JEV's Knowledge Cutoff Date

## Abstract

This experiment estimates JEV's knowledge cutoff date through monthly news facts. The dataset covers January 2023 through June 2026, with ten widely reported facts per month expressed as paired choice and true/false questions in Chinese and English. GPT-4.1-mini serves as a control with a known cutoff. Its pooled results place the best split between June and July 2024, adjacent to its officially documented June 2024 cutoff month. Applying the same method to JEV, both choice accuracy and the rate of answering “unknown” place the best split **between January and February 2025**.

JEV's pooled choice accuracy falls from 80.0% in January 2025 to 37.5% in February–March and 5.3% from April onward, when 93.3% of choice answers are “unknown.” Language-specific analysis, option-count sensitivity and fact-level resampling support **early 2025, with January–February as the main estimate**. Neighboring candidates still span the first quarter; the experiment cannot identify an exact day.

![Monthly choice accuracy for JEV and GPT-4.1-mini; Chinese questions above and English questions below](fig/en/monthly-accuracy.png)

Figure 1. Each point is the observed accuracy on that month's ten questions, without smoothing. The narrow purple band marks GPT-4.1-mini's official cutoff month. The teal dashed line marks JEV's best pooled split; the pale band flags the first-quarter candidate region. The gray baseline uses that month's actual numbers of concrete options. The language versions test the same facts, not twenty independent events per month.

## 1 Purpose

The experiment asks: **approximately when is JEV's knowledge cutoff?** It groups questions by the month when the underlying fact first became public, then looks for a sustained rise in errors or “unknown” answers. Questions target prominent, easily encountered core news outcomes, so that changes over time are less likely to be driven by obscure details.

A model with a known cutoff provides a control for the same procedure. OpenAI's model page gives GPT-4.1-mini a knowledge cutoff of **2024-06-01**. This date is used as a reference, not supplied to the fitting procedure. [Source: OpenAI model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

## 2 Dataset

The dataset contains 420 news facts across 42 months. Each fact produces one choice question and one true/false question per language: 840 Chinese and 840 English questions. Each model completes 1,680 independent requests, producing 3,360 successful response records across the two models. Paired questions are sent separately, without the preceding question or its answer in context.

Facts are selected for newly public information, prominent reporting and an unambiguous core outcome. Each retains evidence from at least two independently originating news publishers, with dates and support statements, as a proxy for exposure. This is not an exact ranking of the world's ten most popular stories each month. Sources, prominence explanations and review records remain in the raw bank; models receive only questions and criteria.

Choice questions provide concrete alternatives plus “unknown.” Of the 420 facts, 370 have four concrete options, 18 have three and 32 have two. Naturally limited candidate sets, such as runoffs and finals, keep their eligible contenders. Uniform guessing among concrete options, without abstaining, has a dataset-wide expected accuracy of 27.3%, rather than a fixed 25%. Gold labels A/B/C/D occur 105 times each per language.

The paired assertion substitutes either the correct answer or a distractor into a statement about the same fact. Each month contains exactly five true and five false assertions. A `pair_id` associates the question types and language versions; it is used for analysis and is not sent to the models.

### Calls and scoring

| Setting | JEV | LLM control |
| --- | --- | --- |
| Requested model | `typesafe/jev-1.13` | `openai/gpt-4.1-mini` |
| Returned model | `typesafe/jev-1.13-20260917` | `openai/gpt-4.1-mini` |
| Provider | TypeSafe through OpenRouter | OpenAI through OpenRouter |
| Input | Native `state` and one `answer` question | The same `state` and question inside fixed system/user messages |
| Generation settings | Experiment config and endpoint defaults | `temperature=0`, `max_tokens=256`, strict JSON Schema |
| Each record | One independent successful response | One independent successful response |

The LLM prompt requests existing knowledge only and supplies no retrieval tools. Complete request bodies are saved in `preparation/raw/prompts.gpt-4.1-mini.jsonl`. JEV's returned version date is not treated as its knowledge cutoff.

Choice answers are correct only when they match the reference label. “Unknown” stays in the denominator and is not correct. For JEV assertions, `noul > 0.5` predicts true and `< 0.5` predicts false; an exact 0.5 is unresolved and not credited. LLM assertions are scored using their explicit Boolean `answer`, without replacing it with `probability_true`. Pair accuracy requires both question types about the same fact to be correct.

## 3 Minimal Example

The following is English sample `knowledge-cutoff-2025-01-10-headline-v1-choice`. It shows the full JEV input, excluding the model field and the reference and metadata that are not sent:

```json
{
  "state": "Near which US city did an airliner collide with an Army helicopter and crash into a river in January 2025?",
  "questions": {
    "answer": {
      "type": "choice",
      "instructions": "Choose the only correct concrete option for the historical knowledge question in state; choose unknown if unsure.",
      "criteria": {
        "A": "Washington, D.C.",
        "B": "New York",
        "C": "Philadelphia",
        "D": "Chicago",
        "unknown": "Cannot determine / do not know"
      }
    }
  }
}
```

The reference is A. The relevant fields from JEV's actual response are:

```json
{
  "answers": {
    "answer": {
      "type": "choice",
      "choice": "A",
      "probabilities": {"A": 0.71, "B": 0.07, "C": 0.01, "D": 0.01, "unknown": 0.2},
      "confidence": 0.64
    }
  }
}
```

The paired assertion is “The January 2025 airliner–Army helicopter collision occurred near Washington, D.C..” Its reference is true. The text, including the doubled period, is reproduced from the saved dataset. The two independent requests produce:

| Model | Choice output | Assertion output | Pair result |
| --- | --- | --- | --- |
| JEV | A, correct | `noul=0.64`, predicts true, correct | Both correct |
| GPT-4.1-mini | `unknown`, `confidence=0.0`, not correct | `answer=false`, `probability_true=0.1`, incorrect | Neither correct |

The Chinese version of this same fact has different outcomes: both models answer the choice correctly, but both miss the assertion. Individual answers and language versions can disagree, so cutoff inference below uses the monthly pattern across all facts.

## 4 Results

### Monthly accuracy and “unknown”

Figure 1 shows GPT-4.1-mini's decline around mid-2024 and JEV's later decline. Figure 2 uses identical dates, model colors and language panels to check whether the loss of accuracy is accompanied by explicit abstention.

![Monthly unknown rates for JEV and GPT-4.1-mini; Chinese questions above and English questions below](fig/en/monthly-unknown.png)

Figure 2. Unknown rate is the number of `unknown` outputs divided by ten choice questions in that month. JEV rarely abstains before 2025; abstention rises early in 2025 and subsequently approaches 100% on English questions. The two signals jointly support the turning point rather than relying on an isolated error. Shading in both figures is a reference annotation, not a statistical confidence interval for the training date.

Pooling JEV's Chinese and English answers gives the following stages. Each fact contributes two language measurements; these denominators are not counts of independent facts.

| News period | Correct choices | Unknown choices | Correct assertions |
| --- | ---: | ---: | ---: |
| 2023–2024 | 414/480 (86.3%) | 19/480 (4.0%) | 389/480 (81.0%) |
| January 2025 | 16/20 (80.0%) | 3/20 (15.0%) | 15/20 (75.0%) |
| February–March 2025 | 15/40 (37.5%) | 22/40 (55.0%) | 20/40 (50.0%) |
| April 2025–June 2026 | 16/300 (5.3%) | 280/300 (93.3%) | 150/300 (50.0%) |

### Locating the cutoff month

A single change point is fitted separately to choice correctness and whether the answer is “unknown.” Every boundary between months is considered, requiring at least three months on each side. Each side uses its aggregate rate; the boundary maximizing the sum of the two binomial log-likelihoods is selected. This is descriptive localization, without tuning to GPT's documented date or deleting questions based on model answers.

| Model and signal | Pooled languages | Chinese only | English only | Four concrete options only |
| --- | --- | --- | --- | --- |
| JEV accuracy | 2025-01 → 02 | 2025-01 → 02 | 2025-02 → 03 | 2025-01 → 02 |
| JEV unknown | 2025-01 → 02 | 2025-01 → 02 | 2025-01 → 02 | 2025-01 → 02 |
| GPT accuracy | 2024-06 → 07 | 2024-06 → 07 | 2024-04 → 05 | 2024-06 → 07 |
| GPT unknown | 2024-06 → 07 | 2024-06 → 07 | 2024-06 → 07 | 2024-06 → 07 |

An arrow denotes the best boundary between months, not an exact inferred day. GPT's pooled split recovers the neighborhood of its official cutoff month, providing a check on monthly detection. However, its English accuracy alone shifts the split earlier to April–May. The method is sensitive to questions and language and does not exactly recover the documented June 1 date.

To assess sensitivity to the chosen facts, each month's ten facts are resampled with replacement, keeping both language versions of a fact together. There are 2,000 repetitions with seed `20261015`. JEV's results are:

| Best boundary | Accuracy resamples | Unknown resamples |
| --- | ---: | ---: |
| 2024-12 → 2025-01 | 4 (0.2%) | 17 (0.9%) |
| 2025-01 → 02 | 1,017 (50.9%) | 1,598 (79.9%) |
| 2025-02 → 03 | 518 (25.9%) | 103 (5.2%) |
| 2025-03 → 04 | 461 (23.1%) | 282 (14.1%) |

January–February remains the most frequent boundary for both signals, while accuracy also selects the next two monthly boundaries. This supports “early 2025, with January–February as the main estimate.” Shading covers the months preceding boundaries selected in at least 5% of resamples, which span Q1 2025, to flag this sensitivity. Resampling assesses conditional stability within this manually chosen fact bank, not a confidence interval for the true training cutoff.

### Overall and paired results

Each row contains 420 choice questions, 420 assertions and 420 pairs. Overall accuracy mixes periods before and after the cutoff and describes performance on this bank; cutoff estimation uses the temporal changes.

| Model | Language | Choice accuracy | Unknown | Assertion accuracy | Both in pair correct |
| --- | --- | ---: | ---: | ---: | ---: |
| JEV | Chinese | 56.4% | 37.1% | 67.4% | 44.5% |
| JEV | English | 53.3% | 40.0% | 69.3% | 45.0% |
| GPT-4.1-mini | Chinese | 34.5% | 38.8% | 56.2% | 23.1% |
| GPT-4.1-mini | English | 32.6% | 51.4% | 61.2% | 26.2% |

Excluding unknowns, JEV answers 237 of 264 concrete Chinese choices correctly (89.8%) and 224 of 252 English choices (88.9%). GPT's corresponding results are 145/257 (56.4%) and 137/204 (67.2%). These are conditional accuracies among answered questions and exclude abstentions.

### Interpreting assertions and probabilities

From February 2025 onward, JEV predicts false on 338 of 340 assertions and true on only two. Since every month is balanced, predicting false everywhere already produces 50% accuracy. The later 50% result therefore cannot be interpreted as knowing half of the later news. This is why choice correctness and unknown rate are used together for localization. Across the full period, JEV has four Chinese and one English `noul=0.5` results, counted as unresolved and not correct.

GPT's Boolean answers disagree in direction with `probability_true` on 175/420 Chinese and 177/420 English assertions: 352/840 (41.9%) overall. For example, an explicit false answer can accompany a probability above 0.5. Main tables score the Boolean answer; thresholding the probability field instead gives only 53.6% Chinese and 53.3% English accuracy. That field is not used to infer the cutoff or directly compared with JEV's scores as if both were identically calibrated probabilities.

### Call cost and reproduction

| Model | Successful requests | Input tokens | Output tokens | Recorded response cost (USD) |
| --- | ---: | ---: | ---: | ---: |
| JEV | 1,680 | 630,658 | 59,332 | 0.026487636 |
| GPT-4.1-mini | 1,680 | 408,206 | 22,760 | 0.1996984 |
| Total | 3,360 | 1,038,864 | 82,092 | 0.226186036 |

Network failures were rerun. Final files contain no failed records or duplicate IDs and cover all inputs. Costs sum `usage.cost` from the final successful responses; failures returning no usage are outside this accounting, which is not a full invoice reconciliation. Front matter records JEV's own sample count, input tokens and cost.

Statistics and both figures can be regenerated from the saved data and responses without new model calls:

```bash
python experiments/knowledge-cutoff/report/scripts/analyze.py
```

The script reads files inside this experiment, uses NumPy, Matplotlib and an available CJK font, recreates both language versions of the figures and prints all statistics to standard output. It does not depend on a temporary workspace or fetch news pages.

## 5 Conclusion

The results support estimating **JEV's knowledge cutoff in early 2025, with the best monthly boundary between January and February 2025**. Falling accuracy and rising unknown rate agree on the pooled split, which also survives restricting choices to four concrete options. The GPT-4.1-mini control turns around June–July 2024, providing a reference near its known cutoff.

There are only ten facts per month, and the language versions are repeated measurements. Some later facts can still be inferred from background knowledge, while earlier facts need not all have appeared in training. Language-specific and resampling results retain neighboring first-quarter candidates. This experiment therefore estimates a month-level neighborhood; it cannot prove an exact training date or treat every correct later answer as direct evidence of post-event training data.

## References

- [OpenAI: GPT-4.1-mini model documentation and official knowledge cutoff](https://developers.openai.com/api/docs/models/gpt-4.1-mini)
- [420 news facts with sources, distractor rationales and review records](../preparation/raw/questions.jsonl)
- [Chinese JEV dataset](../data/dataset.zh.json), [English JEV dataset](../data/dataset.en.json)
- [Complete LLM requests](../preparation/raw/prompts.gpt-4.1-mini.jsonl), [raw LLM responses](../preparation/raw/responses.gpt-4.1-mini.jsonl)
- [Raw Chinese JEV responses](../result/responses.mixed.zh.jsonl), [raw English JEV responses](../result/responses.mixed.en.jsonl)
- [Analysis and plotting script](scripts/analyze.py)
