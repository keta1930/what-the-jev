# Jev on MoralChoice: Moral Choices and Response Stability

## Abstract

Each of 1,367 English MoralChoice scenarios receives six structured judgments. All six variants select the reference action in every one of the 687 low-ambiguity scenarios. In the 680 high-ambiguity scenarios, 69.07% of judgments select action1 and 90.59% of scenarios retain the same underlying action across all variants. High-ambiguity choices are usually stable, with remaining sensitivity to form and order.

## 1 Dataset

The release contains 687 low-ambiguity and 680 high-ambiguity scenarios. The reference action is action1 for low-ambiguity scenarios; no universal correct action is assigned to high-ambiguity scenarios. Each scenario has ab, repeat and compare forms in both orders, yielding 8,202 judgments. Model snapshot: typesafe/jev-1.13-20260917.

Forms and order swaps follow the original design, while output is adapted to Jev’s structured binary choice. Six questions are answered in one request per scenario; repeat does not test verbatim text repetition. Order and cross-form stability are analysis measures for this adaptation, and six judgments are not counted as six independent scenarios.

## 2 Results

### 2.1 Overall results

Low-ambiguity judgments use the released reference action, with a 50% uniform binary-choice baseline. High-ambiguity results describe choices rather than accuracy.

| Measure | Low ambiguity | High ambiguity |
| --- | --- | --- |
| Scenarios | 687 | 680 |
| Judgments | 4122 | 4080 |
| Share selecting action1 | 100.00% | 69.07% |
| Same action across all six | 100.00% | 90.59% |
| Mean P(action1) | 99.82% | 67.11% |

Every low-ambiguity scenario selects the reference action in all variants: 100%, with a scenario-level Wilson 95% interval of 99.44%–100%. The high-ambiguity action1 share depends on the content arrangement in the release; it is not a first-position preference.

### 2.2 High-ambiguity stability

| Form | Order agreement | Rate | Mean probability change | First-position share |
| --- | --- | --- | --- | --- |
| ab | 661 / 680 | 97.21% | 3.15% | 49.04% |
| repeat | 658 / 680 | 96.76% | 3.25% | 48.97% |
| compare | 643 / 680 | 94.56% | 6.36% | 47.57% |

All six variants agree in 616 of 680 scenarios. The compare form has the lowest order agreement, indicating greater sensitivity of yes/no comparisons to order. The mean within-scenario probability range across six variants is 10.75 percentage points.

### 2.3 Auxiliary rule groups

Auxiliary rule labels come from the release and may overlap. Comparisons use scenarios where one action is marked as violating a rule and the other explicitly is not. Full aggregate tables are retained in the machine-readable summary.

| Rule label | High-ambiguity scenarios | Nonviolating choice share | All six nonviolating |
| --- | --- | --- | --- |
| break_law | 195 | 84.02% | 76.92% |
| break_promise | 108 | 68.21% | 65.74% |
| cheat | 138 | 93.24% | 91.30% |
| death | 84 | 64.88% | 59.52% |
| deceive | 262 | 86.39% | 82.44% |
| disable | 144 | 67.13% | 61.11% |
| duty | 409 | 86.15% | 81.66% |
| freedom | 219 | 54.26% | 48.86% |
| pain | 356 | 57.12% | 51.97% |
| pleasure | 276 | 50.60% | 45.65% |

### 2.4 Call costs

| Input tokens | Output tokens | Reported cost (USD) |
| --- | --- | --- |
| 1,098,374 | 250,161 | 0.046131708 |

All 1,367 requests succeeded, with no retries or unknown charges.

## 3 Conclusion

Jev fully agrees with the reference choices in low-ambiguity scenarios. High-ambiguity scenarios have no universal correct answer; about nine in ten retain the same underlying action across the six form/order combinations, with more changes in the comparison form. The result describes structured choices and their stability, without equating concentrated probabilities with moral correctness or human opinion shares.

## References

1. [Scherrer et al. (2023). Evaluating the Moral Beliefs Encoded in LLMs. NeurIPS.](https://proceedings.neurips.cc/paper_files/paper/2023/file/a2cf225ba392627529efef14dc857e22-Paper-Conference.pdf)
2. [MoralChoice data release, commit 89c0fe7b158b5ade5d10e0644c1aa20ab4c78cbe; CC BY 4.0.](https://huggingface.co/datasets/ninoscherrer/moralchoice)
