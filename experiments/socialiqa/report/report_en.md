# Jev on SocialIQA: Social Commonsense Decisions

## Abstract

Jev answered 1,792 of 2,224 English SocialIQA v1.4 test questions correctly, achieving 80.58% accuracy with a duplicate-question cluster 95% interval of 78.81%–82.21%. Accuracy across the nine official source groups ranges from 78.11% to 84.66%. These results describe selection judgments about everyday motives, emotions and consequences.

## 1 Dataset

The material contains all 2,224 rows of the authors’ v1.4 test release. Each item contains an English context, a question and three options. Each is answered independently and scored against the released reference label. Model snapshot: typesafe/jev-1.13-20260917.

The nine groups use the official promptDim field, which records the ATOMIC question-generation source. Rewritten questions can depart from that source, so these groups are not treated as nine independent psychological abilities. The evaluation concerns a long-public English multiple-choice dataset.

## 2 Results

### 2.1 Overall results

The dataset labels are the scoring criterion. Every formal item has a valid response. Uniform random three-option selection has an expected accuracy of 33.33%.

| Measure | Result |
| --- | --- |
| Formal items | 2,224 |
| Correct | 1,792 |
| Accuracy | 80.58% |
| Question-cluster 95% interval | 78.81%–82.21% |
| Distinct complete questions | 2203 |
| Distinct-question accuracy | 80.57% |

### 2.2 Official source groups

| Group | Items | Correct | Accuracy |
| --- | --- | --- | --- |
| oEffect (Effect on others) | 159 | 127 | 79.87% |
| oReact (Others’ reactions) | 223 | 179 | 80.27% |
| oWant (Others’ wants) | 252 | 201 | 79.76% |
| xAttr (Actor attributes) | 297 | 232 | 78.11% |
| xEffect (Effect on actor) | 103 | 82 | 79.61% |
| xIntent (Actor intent) | 297 | 239 | 80.47% |
| xNeed (Actor prerequisites) | 277 | 225 | 81.23% |
| xReact (Actor reactions) | 277 | 220 | 79.42% |
| xWant (Actor wants) | 339 | 287 | 84.66% |

The xWant group has the highest accuracy and xAttr the lowest. Group sizes differ; this ordering describes the dataset rather than a stable hierarchy of abilities.

### 2.3 Call costs

| Input tokens | Output tokens | Reported cost (USD) |
| --- | --- | --- |
| 851,327 | 84,512 | 0.035755734 |

Reported formal-evaluation cost is USD 0.035755734. Twelve separate interface-debugging items bring the reported total to USD 0.035949816, with 855,948 input tokens and 84,968 output tokens. One technical failure has unknown billing; the historical ledger retains USD 0.01 as a reservation, not a settled charge.

## 3 Conclusion

Jev achieves 80.58% accuracy on this English social-commonsense dataset, selecting the reference answer for most questions about motives, emotions and consequences. It misses 432 reference answers. The result provides a baseline for social-situation understanding under the tested selection format; it does not measure emotional experience or willingness to help.

## References

1. [Sap et al. (2019). Social IQa: Commonsense Reasoning about Social Interactions. EMNLP-IJCNLP.](https://aclanthology.org/D19-1454/)
2. [SocialIQA v1.4: authors’ dataset release, CC BY 4.0.](https://maartensap.com/social-iqa/)
