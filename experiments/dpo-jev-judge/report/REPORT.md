---
title: "Judging DPO Preference Pairs: JEV Picking the Better of Two Thinking Traces"
date: 2026-10-09
summary: "【Judge Agreement】Can JEV pick the better of two thinking traces, matching an LLM judge's preference?"
---

# Judging DPO Preference Pairs: JEV Picking the Better of Two Thinking Traces

## Abstract

This experiment tests whether JEV can reproduce an LLM judge's preference between two thinking traces. The setting is 150 open-ended reasoning questions; each pair consists of the judge's winning trace and one random loser from the same question, and JEV picks the better one. JEV agreed with the judge on 83.3% of the pairs (95% CI 76.6–88.4%), far above the 50% random level, with no position bias: picks split exactly 75 to 75 between A and B. Confidence separates trustworthy judgments from coin flips: the 24 pairs at confidence ≥0.8 contain zero errors, while the 24 pairs below 0.2 sit near the random level. An alternative layout that moves the candidate texts into the criteria drops agreement to 79.3%. The standard-layout run consumed 359,825 input tokens and 4,650 output tokens, costing $0.0151. We conclude that in pair form JEV can directly serve as the preference-pair labeler, with confidence as a working trust switch.

## 1 Purpose

This experiment measures JEV's ability to judge thinking quality in pairs: given two thinking traces answering the same question, pick the better one. The scenario comes from DPO-style training, which consumes chosen/rejected preference pairs; the labeling step is exactly this two-way pick. A DeepSeek LLM judge's picks define the preferred side of each pair, and we ask whether JEV reproduces them.

### Relation to grpo-jev-judge

The pairs are built from the upstream data of grpo-jev-judge: the same 150 questions, the same eight rollouts per question, and the same judge winners (see experiments/grpo-jev-judge/report/REPORT.md). Each pair here joins one judge winner with one random loser from the same eight traces. The two experiments measure the same judging ability at pair level (two-choice, here) and at group level (eight-choice, where the hit rate is 45.3%).

## 2 Dataset

The dataset holds 150 preference pairs, one per open-ended Chinese reasoning question. The two traces in a pair come from the question's eight Qwen3-0.6B rollouts: the chosen side is the DeepSeek judge's winner, the rejected side is one random trace from the remaining seven. Which side sits at option A is decided per pair by coin flip, ending at 76 pairs with the preferred trace at A and 74 at B. That preferred position is the reference; JEV answers under the same written quality standard the judge used.

Questions fall into three types by form: causal explanation, cause finding, and trade-off advice, 50 each. This division is recovered from the id prefix (g-causal, g-diagnosis, g-tradeoff) by this analysis; the samples carry no original type labels.

Each pair is posed in two layouts. In the standard layout, the two traces sit in `state.responses` and the criteria are pointers to them; in the criteria-text layout, the trace texts themselves serve as the criteria and the state keeps only the question.

## 3 A Minimal Example

This section shows one real pair with its complete input and output (standard layout). The input sent to the model (the model field is omitted; the original text is Chinese and is translated here):

```json
{
  "state": {
    "prompt": "A colleague left a handover document before departing, yet the person who took over still makes frequent mistakes while following it. Explain why errors persist even with a documented handover.",
    "responses": {
      "A": "Well, the user asks: a colleague left a handover document when departing, yet the successor still makes frequent mistakes while following it; I need to explain why errors persist even with a handover document. First, let me identify the core of the question: they want to know the possible reasons the successor still errs despite the document. …",
      "B": "Hmm, let me think about this situation. After the employee left, the successor follows the handover document but still makes frequent mistakes. Why is that? First, the document may not be detailed or accurate enough, or some information may be missing. …"
    }
  },
  "questions": {
    "better": {
      "type": "choice",
      "instructions": "1. Task\nPick the thinking trace with the better quality from responses.A and responses.B.\n… (the remaining six sections omitted)",
      "criteria": {"A": "responses.A", "B": "responses.B"}
    }
  }
}
```

The model's output (key fields only):

```json
{
  "answers": {
    "better": {
      "type": "choice",
      "choice": "A",
      "probabilities": {"A": 0.74, "B": 0.26},
      "confidence": 0.48
    }
  },
  "usage": {"input_tokens": 2177, "output_tokens": 31, "cost": 0.0000914}
}
```

JEV chose A, the trace the LLM judge preferred.

## 4 Results

### Overall

All 150 pairs received a valid answer; no call failed. Judged against the DeepSeek LLM judge's preferences — the questions are open-ended with no single right answer, so this measures agreement with that judge, not correctness — JEV agreed on 125 pairs: an agreement rate of 83.3%, with a 95% confidence interval of 76.6–88.4%. A random pick between two options agrees 50% of the time.

### By question type

Agreement is flat across the three question types:

| Question type | Pairs | Agreements | Agreement rate |
| --- | ---: | ---: | ---: |
| causal explanation | 50 | 42 | 84.0% |
| cause finding | 50 | 41 | 82.0% |
| trade-off advice | 50 | 42 | 84.0% |

### Confidence and agreement

JEV reports a confidence with each answer. Agreement rises monotonically with confidence, from near-random at the bottom to flawless at the top (Figure 1):

| Confidence | Pairs | Share | Agreement |
| --- | ---: | ---: | ---: |
| < 0.2 | 24 | 16.0% | 54.2% |
| 0.2–0.4 | 31 | 20.7% | 71.0% |
| 0.4–0.6 | 24 | 16.0% | 87.5% |
| 0.6–0.8 | 47 | 31.3% | 95.7% |
| ≥ 0.8 | 24 | 16.0% | 100% |

![Agreement by confidence](fig/en/confidence-agreement.png)

Figure 1: agreement rises monotonically with confidence; the top bin makes no error, the bottom bin sits near the 50% random level marked by the dashed line.

The separation is wide: the mean confidence is 0.559 on agreements and 0.257 on disagreements. A threshold at 0.8 keeps 24 pairs (16.0%) at zero errors.

### Behavior

JEV's picks split exactly 75 to 75 between A and B, and agreement is symmetric: 82.9% when the judge's preference sits at A, 83.8% at B. Every answer's probabilities sum to 1 and match the chosen option.

### Cost

The standard-layout run consumed 359,825 input tokens and 4,650 output tokens, for a total cost of $0.0151.

### Layout ablation

The two layouts differ only in where the candidate texts live. Moving them into the criteria costs four points of agreement, introduces a first-option bias, and compresses confidence until the trust switch disappears:

| Layout | Agreement (95% CI) | A picks | Median confidence | Input tokens | Output tokens | Cost |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| standard | 83.3% (76.6–88.4%) | 75 (50.0%) | 0.56 | 359,825 | 4,650 | $0.0151 |
| criteria-text | 79.3% (72.2–85.0%) | 91 (60.7%) | 0.32 | 356,225 | 4,650 | $0.0150 |

Under criteria-text, JEV picks A in 60.7% of the pairs; agreement reaches 89.5% when the judge's preference sits at A but only 68.9% at B. Confidence compression leaves a single pair at 0.8 or above, against 24 in the standard layout.

## 5 Conclusion

In pair form, JEV reproduces the LLM judge's preference on five pairs out of six, without any position bias, and its confidence cleanly separates judgments that can be trusted from coin flips. Pair-level judging is where JEV's judging ability becomes dependable: label preference pairs directly, gate on confidence, and route the low-confidence tail to review. The criteria-text layout is worse on every axis and should not be used for this task.

## 6 Insights

1. Pairwise judging is the dependable form of JEV's judging ability: high agreement with no position bias makes it usable as a preference-pair labeler directly.
2. In two-choice judging, confidence works as a trust switch: accept high-confidence judgments outright and route the lowest band, which is close to a coin flip, to review.
3. Keep candidate texts in the state with pointer criteria: moving the texts into the criteria introduces a first-option bias and destroys the confidence signal's separation.
4. Question type barely moves pairwise agreement, so per-type thresholds are unnecessary for this task.

## Related Resources

- DPO paper: https://arxiv.org/abs/2305.18290
- Qwen3-0.6B (rollout model): https://huggingface.co/Qwen/Qwen3-0.6B
- DeepSeek API documentation (LLM judge): https://api-docs.deepseek.com/
