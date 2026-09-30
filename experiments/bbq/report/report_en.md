# Jev on BBQ: Evidence Use and Social Bias

## Abstract

Across 58,492 English BBQ items, Jev achieves 99.51% accuracy with insufficient information and 96.79% with sufficient information. Most under-informative cases are correctly left unknown; 131 of the 142 concrete-person answers follow the predefined stereotype direction. With sufficient information, 2.88% of answers remain unknown.

## 1 Dataset

The fixed BBQ release contains 11 files covering nine base social dimensions and two intersectional categories in U.S. English-speaking contexts. Its 14,623 quartets combine insufficient/sufficient information with negative/non-negative questions. English wording and option order are preserved. Model snapshot: typesafe/jev-1.13-20260917.

Social categories and stereotype directions come from official annotations. The 342 template families used for interval estimation are an additional grouping defined in this analysis from source templates; expansions of a template stay together. They are not new social categories.

## 2 Results

### 2.1 Overall results

Accuracy uses official answer labels. Bias scores use the official stereotype direction and are reported on a -100 to 100 scale; positive values indicate net alignment with the predefined stereotype. The uniform three-option accuracy baseline is 33.33%.

| Context | Items | Accuracy | 95% interval | Unknown | Bias score |
| --- | --- | --- | --- | --- | --- |
| Insufficient | 29,246 | 99.51% | 99.20%–99.76% | 99.51% | +0.41 |
| Sufficient | 29,246 | 96.79% | 94.57%–98.62% | 2.88% | +0.30 |

An always-unknown model scores 100% on insufficient-information items and 0% on sufficient-information items. The two conditions and unknown rates must therefore be read together. Opposite-direction errors can also cancel in a near-zero net bias score.

### 2.2 Social categories

| Category | Items per condition | Insufficient accuracy | Sufficient accuracy | Sufficient unknown |
| --- | --- | --- | --- | --- |
| Age | 1,840 | 96.85% | 99.67% | 0.33% |
| Disability status | 778 | 98.59% | 99.10% | 0.90% |
| Gender identity | 2,836 | 100.00% | 99.86% | 0.14% |
| Nationality | 1,540 | 98.83% | 98.44% | 1.56% |
| Physical appearance | 788 | 97.08% | 88.58% | 2.41% |
| Race ethnicity | 3,440 | 99.94% | 96.63% | 3.26% |
| Religion | 600 | 95.33% | 96.17% | 3.50% |
| SES | 3,432 | 99.97% | 89.42% | 10.58% |
| Sexual orientation | 432 | 100.00% | 97.45% | 2.55% |
| Race x gender | 7,980 | 100.00% | 96.30% | 3.45% |
| Race x SES | 5,580 | 99.98% | 100.00% | 0.00% |

Religion and age have lower accuracy under insufficient information. Physical appearance and socioeconomic status have lower accuracy under sufficient information. Category sizes differ, so the overall result is not a category-balanced mean.

### 2.3 Answer direction and evidence

| Behavior | Count / rate |
| --- | --- |
| Insufficient: concrete-person answers | 142 |
| Of those: stereotype-aligned | 131 / 142 (92.25%) |
| Sufficient: unknown | 842 |
| Sufficient: incorrect person | 97 |
| Sufficient: stereotype-aligned evidence accuracy | 96.63% |
| Sufficient: opposing evidence accuracy | 96.95% |

Bias scores use the subset with complete target annotations; accuracy uses all items. Correct-answer directions in sufficient-information items are not exactly balanced: even perfect answers score about +0.54 on the official overall bias metric. A nonzero score cannot therefore be attributed entirely to model error.

### 2.4 Call costs

| Input tokens | Output tokens | Reported cost (USD) |
| --- | --- | --- |
| 21,932,246 | 2,456,664 | 0.921154332 |

Costs cover every attempt with reported billing. One technical failure has no reported cost; a separate historical USD 0.002 reservation is not treated as a settled charge. All 58,492 items ultimately have valid responses.

## 3 Conclusion

Jev distinguishes insufficient from sufficient evidence on most items. Remaining issues include infrequent but directionally concentrated stereotypical inferences without enough information, and unknown answers despite sufficient information. High overall accuracy and low net bias scores should be interpreted alongside these behaviors in this U.S. English dataset.

## References

1. [Parrish et al. (2022). BBQ: A Hand-Built Bias Benchmark for Question Answering. Findings of ACL.](https://aclanthology.org/2022.findings-acl.165/)
2. [BBQ official release, commit bea11bd97d79217245b5871acd247b9d6eb24598; CC BY 4.0.](https://github.com/nyu-mll/BBQ)
