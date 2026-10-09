---
title: "Judging GRPO Rollouts: JEV Picking the Best of Eight Thinking Traces"
date: 2026-10-09
summary: "【Judge Agreement】Can JEV pick the same best thinking trace as an LLM judge among eight rollouts of one open-ended reasoning question?"
---

# Judging GRPO Rollouts: JEV Picking the Best of Eight Thinking Traces

## Abstract

This experiment tests whether JEV can judge thinking quality the way an LLM judge does. The setting is 150 open-ended reasoning questions, each with eight thinking traces sampled from the same model; a DeepSeek LLM judge has picked one winner per question, and JEV must pick the same trace out of eight. JEV matched the judge on 45.3% of the questions (95% CI 37.6–53.3%), well above the 12.5% random level but far from saturation, and its picks tilt toward the first position: 34.0% land on R1 while R8 is picked only 7 times. The confidence JEV reports barely discriminates: the mean is 0.377 on hits and 0.285 on misses. An alternative layout that moves the candidate texts into the criteria scores 42.0%. The standard-layout run consumed 1,020,099 input tokens and 12,750 output tokens, costing $0.0428. We conclude that JEV's eight-way judgment agrees with the judge above chance but carries a clear order bias, so it can pre-filter candidates but cannot replace the judge as a labeler.

## 1 Purpose

This experiment measures JEV's ability to judge thinking quality among many candidates: given eight thinking traces answering the same question, pick the best one. The scenario comes from GRPO-style reinforcement learning, where a group of rollouts needs a winner signal, and the labeling step is exactly this eight-way pick. A DeepSeek LLM judge has already made these picks under a written quality standard; we ask whether JEV reproduces them.

### Relation to dpo-jev-judge

The same rollouts and judge choices feed the pair-level experiment dpo-jev-judge: there, each judge winner is paired with one random loser from the same eight traces, and JEV picks the better of the two (see experiments/dpo-jev-judge/report/REPORT.md). The two experiments measure the same judging ability at group level (eight-choice, here) and at pair level (two-choice), where agreement reaches 83.3%.

## 2 Dataset

The dataset holds 150 open-ended Chinese reasoning questions about everyday situations. Each question comes with eight thinking traces (R1–R8) sampled from Qwen3-0.6B at temperature 1.0 in thinking mode; the traces contain reasoning only, no final conclusion, and their order is the sampling order. A DeepSeek judge applied a written quality standard — no contradictions, covers every part of the question, followable steps, concrete grounding — and picked one winner per question. That winner is the reference; JEV answers under the same written standard.

Questions fall into three types by form: causal explanation, cause finding, and trade-off advice, 50 each. This division is recovered from the id prefix (g-causal, g-diagnosis, g-tradeoff) by this analysis; the samples carry no original type labels.

Each question is posed in two layouts. In the standard layout, the eight traces sit in `state.responses` and the criteria are pointers to them; in the criteria-text layout, the trace texts themselves serve as the criteria and the state keeps only the question.

## 3 A Minimal Example

This section shows one real question with its complete input and output (standard layout). The input sent to the model (the model field is omitted; the original text is Chinese and is translated here):

```json
{
  "state": {
    "prompt": "A colleague left a handover document before departing, yet the person who took over still makes frequent mistakes while following it. Explain why errors persist even with a documented handover.",
    "responses": {
      "R1": "OK, I need to solve this problem. The user says a colleague left a handover document before departing, and the person taking over ran into problems while following it. The user wants to know why a documented handover can still go wrong. First, let me consider common causes. The document itself may be flawed — incomplete, for example, or poorly worded. …",
      "…": "…R2 to R8 omitted…"
    }
  },
  "questions": {
    "winner_overall": {
      "type": "choice",
      "instructions": "1. Task\nPick the thinking trace with the best quality from responses.R1 to responses.R8.\n… (the remaining six sections omitted)",
      "criteria": {
        "R1": "responses.R1",
        "R2": "responses.R2",
        "…": "…",
        "R8": "responses.R8"
      }
    }
  }
}
```

The model's output (key fields only):

```json
{
  "answers": {
    "winner_overall": {
      "type": "choice",
      "choice": "R5",
      "probabilities": {"R1": 0.07, "R2": 0.21, "R3": 0.09, "R4": 0.12, "R5": 0.43, "R6": 0.02, "R7": 0.04, "R8": 0.02},
      "confidence": 0.35
    }
  },
  "usage": {"input_tokens": 4872, "output_tokens": 85, "cost": 0.000204624}
}
```

JEV chose R5, matching the LLM judge's pick.

## 4 Results

### Overall

All 150 questions received a valid answer; no call failed. Judged against the DeepSeek LLM judge's choices — the questions are open-ended with no single right answer, so this measures agreement with that judge, not correctness — JEV matched the winner on 68 questions: a hit rate of 45.3%, with a 95% confidence interval of 37.6–53.3%. A random pick among eight options hits 12.5%.

### By question type

Hit rates differ moderately across the three question types:

| Question type | Questions | Hits | Hit rate |
| --- | ---: | ---: | ---: |
| causal explanation | 50 | 27 | 54.0% |
| cause finding | 50 | 21 | 42.0% |
| trade-off advice | 50 | 20 | 40.0% |

### By option position

The judge's winners spread over all eight positions (R1 at 19.3% and R6 at 18.7% are the most frequent), but JEV's picks tilt hard to the front (Figure 1): 51 picks (34.0%) land on R1, while R8 is picked only 7 times (4.7%). The tilt inflates the hit rate where the judge happened to pick early positions: when the judge's winner is R1, JEV hits 21 of 29 (72.4%); when it is R6, only 7 of 28 (25.0%).

![Picks per option position, judge vs JEV](fig/en/position-distribution.png)

Figure 1: the judge's winners spread across positions while JEV's picks pile up on the first position.

### Confidence and hit rate

JEV reports a confidence with each answer. The hit rate rises with confidence, yet every bin sits in a low confidence range and even the top bin stays far from reliable (Figure 2):

| Confidence | Answers | Share | Hit rate |
| --- | ---: | ---: | ---: |
| < 0.2 | 27 | 18.0% | 29.6% |
| 0.2–0.3 | 47 | 31.3% | 31.9% |
| 0.3–0.4 | 35 | 23.3% | 51.4% |
| 0.4–0.5 | 18 | 12.0% | 61.1% |
| ≥ 0.5 | 23 | 15.3% | 69.6% |

![Hit rate by confidence](fig/en/confidence-hit.png)

Figure 2: the hit rate rises with confidence, but answers concentrate at low confidence and no bin approaches full reliability; the dashed line marks the 12.5% random level.

As a trust signal, confidence barely discriminates here: the mean confidence is 0.377 on hits and 0.285 on misses, the median answer carries 0.30, and the highest value seen is 0.81. No threshold separates trustworthy picks from untrustworthy ones.

### Behavior

Probabilities sum to 1 in every answer. In 3 answers (2.0%) the chosen option is not the one with the highest probability.

### Cost

The standard-layout run consumed 1,020,099 input tokens and 12,750 output tokens, for a total cost of $0.0428.

### Layout ablation

The two layouts differ only in where the candidate texts live. Moving them into the criteria costs a little accuracy, weakens — but does not remove — the position bias, and compresses confidence downward:

| Layout | Hit rate (95% CI) | R1 picks | Median confidence | Input tokens | Output tokens | Cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| standard | 45.3% (37.6–53.3%) | 51 (34.0%) | 0.30 | 1,020,099 | 12,750 | $0.0428 |
| criteria-text | 42.0% (34.4–50.0%) | 25 (16.7%) | 0.18 | 1,005,999 | 12,750 | $0.0423 |

## 5 Conclusion

As an eight-way judge of thinking quality, JEV agrees with the LLM judge far above chance — 45.3% against a 12.5% random level — but its picks carry a clear first-position bias, and its confidence cannot tell good judgments from bad ones. In this pipeline, JEV's group-level judgment can pre-filter candidates; the actual labeling is better left to a stronger judge or to the pair-level formulation tested in dpo-jev-judge.

## 6 Insights

1. When JEV judges among many candidates, it favors early positions; long candidate lists call for shuffled or rotated option order.
2. In eight-way judging, JEV's confidence has almost no discriminating power, so it cannot gate which judgments to trust; shrinking the candidate set works better than thresholding confidence.
3. Keeping long candidate texts in the state with pointer criteria is the steadier layout: moving the texts into the criteria lowers the hit rate and compresses confidence without buying anything.
4. Agreement with a judge that is far above chance but far from saturation makes JEV a candidate pre-filter in rollout labeling, not the labeler itself.

## Related Resources

- Qwen3-0.6B (rollout model): https://huggingface.co/Qwen/Qwen3-0.6B
- DeepSeek API documentation (LLM judge): https://api-docs.deepseek.com/
- GRPO paper (DeepSeekMath): https://arxiv.org/abs/2402.03300
