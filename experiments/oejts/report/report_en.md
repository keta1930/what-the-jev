# Jev on OEJTS: Response Tendencies and Repeat Stability

## Abstract

Ten rounds of the 32 English five-position OEJTS 1.2 items yield 320 valid responses. The scale’s scoring rule yields ISTJ in all ten rounds. SN lies closest to its classification boundary and falls exactly on it in two rounds. 25 of 32 items retain the same position in every round. Results describe response and scoring stability under fixed wording.

## 1 Dataset

OEJTS 1.2 is an open alternative scale released by Eric Jorgenson, not the official MBTI. Each item presents two endpoint descriptions and five positions under a fixed model-self-description instruction. Items are requested independently across ten rounds. Model snapshot: typesafe/jev-1.13-20260917.

The scale’s scoring and boundaries are used for IE, SN, FT and JP. Because items include human lived-experience descriptions, this is an exploratory adaptation of model response tendencies. Type counts are repeated scoring outcomes, not personality probabilities.

## 2 Results

### 2.1 Overall results

The criterion is the scale’s numerical scoring rule; there is no correct-answer accuracy. Selecting the middle position on every item gives 24 on each dimension and ISFJ under the original classification rule, providing a boundary reference.

| Measure | Result |
| --- | --- |
| Distinct items | 32 |
| Complete rounds | 10 |
| Valid responses | 320 |
| Type counts | ISTJ: 10 |
| Items unchanged across ten rounds | 25 / 32 |

### 2.2 Dimension stability

| Dimension | Mean | Minimum | Maximum | Mean distance from 24 | Boundary rounds |
| --- | --- | --- | --- | --- | --- |
| IE | 13.90 | 13 | 15 | 10.10 | 0 |
| SN | 22.40 | 22 | 24 | 1.60 | 2 |
| FT | 29.90 | 28 | 31 | 5.90 | 0 |
| JP | 16.30 | 16 | 17 | 7.70 | 0 |

SN has a mean boundary distance of 1.60, smaller than the other dimensions. An identical type across ten rounds does not imply identical item answers or that every dimension is far from its boundary.

### 2.3 Scores by round

| Round | Type | IE | SN | FT | JP | Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ISTJ | 14 | 22 | 28 | 16 | - |
| 2 | ISTJ | 14 | 22 | 30 | 16 | - |
| 3 | ISTJ | 13 | 22 | 30 | 17 | - |
| 4 | ISTJ | 13 | 22 | 30 | 17 | - |
| 5 | ISTJ | 14 | 22 | 30 | 16 | - |
| 6 | ISTJ | 14 | 22 | 30 | 16 | - |
| 7 | ISTJ | 13 | 22 | 31 | 16 | - |
| 8 | ISTJ | 15 | 22 | 30 | 16 | - |
| 9 | ISTJ | 15 | 24 | 30 | 17 | SN |
| 10 | ISTJ | 14 | 24 | 30 | 16 | SN |

### 2.4 Call costs

| Input tokens | Output tokens | Reported cost (USD) |
| --- | --- | --- |
| 156,530 | 16,640 | 0.00657426 |

All 320 requests have valid responses and billing records, with no unknown charges. There are no results from the official MBTI.

## 3 Conclusion

Jev shows high repeat stability under the fixed instruction, English wording and position order, yielding ISTJ under OEJTS rules in every round. SN lies near the boundary and some item choices vary. This finding concerns questionnaire responses and scoring, not a validated measurement of model personality.

## References

1. [Eric Jorgenson (2015). Open Extended Jungian Type Scales 1.2. Original items: CC BY-NC-SA 4.0. Questionnaire text is not redistributed here.](https://openpsychometrics.org/tests/OJTS/development/OEJTS1.2.pdf)
