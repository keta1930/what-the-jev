# Jev on MoCa: Agreement with Human Causal and Moral Judgments

## Abstract

Across 206 English MoCa stories, Jev’s three-class agreement with the aggregated judgments of 25 human respondents per item is 43.69%. Agreement is 39.58% for causal items and 53.23% for moral items. Jev distinguishes clear human yes/no judgments but rarely places human-ambiguous causal stories in the ambiguous interval.

## 1 Dataset

The dataset includes 144 causal stories and 62 moral-permissibility stories, each with 25 binary human judgments. The classes are Yes, No and Ambiguous, using the 0.4/0.6 boundaries; Jev’s third class is derived from its binary-choice probability. Model snapshot: typesafe/jev-1.13-20260917.

Factor names follow the source’s expert annotations, and factors may overlap within a story. Human response proportions and Jev’s structured-choice probabilities have different meanings; this report describes their agreement and numerical differences on these stories.

## 2 Results

### 2.1 Overall results

Agreement is judged against the dataset’s aggregated human labels, without treating majority judgments as moral truth. Uniform three-class chance is 33.33%; the overall majority-class baseline is 36.41%. AUROC uses only human-unambiguous items.

| Subset | Items | Agreement | 95% interval | AUROC | Probability MAE |
| --- | --- | --- | --- | --- | --- |
| All | 206 | 43.69% | 36.89%–50.49% | 0.704 | 0.308 |
| Causal | 144 | 39.58% | 31.94%–47.92% | 0.748 | 0.333 |
| Moral | 62 | 53.23% | 40.32%–66.13% | 0.852 | 0.249 |

### 2.2 Judgment distributions

| Subset | Source | Yes | No | Ambiguous |
| --- | --- | --- | --- | --- |
| Causal | Human | 48 | 50 | 46 |
| Causal | Jev | 98 | 35 | 11 |
| Moral | Human | 23 | 10 | 29 |
| Moral | Jev | 22 | 21 | 19 |

Only 1 of 46 human-ambiguous causal items is also classified as ambiguous by Jev; the corresponding count is 12 of 29 moral items. Jev gives substantially more affirmative causal judgments, showing that lower three-class agreement involves distribution and boundary differences.

### 2.3 Mean differences across factor groups

| Group transition | Group sizes | Human difference | Jev difference |
| --- | --- | --- | --- |
| Action to omission | 80 / 32 | +0.028 | -0.179 |
| Aware to unaware | 23 / 20 | -0.009 | +0.195 |
| Conjunctive to disjunctive | 66 / 32 | -0.030 | -0.250 |
| Abnormal to normal | 44 / 45 | -0.228 | -0.294 |
| Other to self beneficiary | 26 / 22 | +0.101 | -0.015 |
| Accidental to instrumental | 18 / 30 | -0.118 | -0.067 |
| Avoidable to inevitable | 22 / 26 | +0.131 | +0.136 |
| Impersonal to personal force | 24 / 24 | -0.058 | -0.067 |

Differences describe changes in mean affirmative share/probability from the first group to the second. Factors overlap and story content changes across groups; these are descriptive associations, not isolated causal effects.

### 2.4 Call costs

| Input tokens | Output tokens | Reported cost (USD) |
| --- | --- | --- |
| 109,940 | 6,798 | 0.00461748 |

All 206 requests succeeded on the first attempt, with no unknown charges or retries.

## 3 Conclusion

Jev shows partial agreement with aggregated human judgments, with higher agreement on moral than causal items. Its ability to distinguish clear human yes/no judgments does not translate into comparable identification of human ambiguity. Some factor-group mean directions match and others differ; the findings describe judgments on the same stories.

## References

1. [Nie et al. (2023). MoCa: Measuring Human-Language Model Alignment on Causal and Moral Judgment Tasks. NeurIPS.](https://arxiv.org/abs/2310.19677)
2. [MoCa official repository, commit 1b61a20294247480d64675ceb19751ef4e1e878f.](https://github.com/cicl-stanford/moca)
