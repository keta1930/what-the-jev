---
title: "University Math Multiple Choice"
date: 2026-10-10
summary: "This experiment tests the Jev model's ability to answer university-level computational math problems."
samples: 5
input_tokens: 3.3k
cost: 0.000138978
---

# University Math Multiple Choice

This experiment tests the Jev model's ability to answer university-level computational math problems.

It contains 5 samples, all authored rather than taken from any dataset: 2 on calculus, 2 on linear algebra, and 1 on probability.

The five problems (`state`):

1. Evaluate the definite integral ∫₀¹ x·eˣ dx.
2. Evaluate the definite integral ∫₀^{π/2} sin²x dx.
3. Compute the determinant of the matrix A = [[1, 2, 3], [4, 5, 6], [7, 8, 10]].
4. Find the largest eigenvalue of the matrix [[2, 1], [1, 2]].
5. Let the random variable X follow an exponential distribution with parameter 1, i.e. density f(x) = e⁻ˣ (x > 0). Compute the conditional probability P(X > 2 | X > 1).

Each sample answers two kinds of questions.

First kind: What is the answer to this problem? Choose one of four. (`answer`, `choice`)

| Problem | A | B | C | D | Correct answer |
| --- | --- | --- | --- | --- | --- |
| 1 | `e - 1` | `1` | `e - 2` | `e` | B |
| 2 | `π/2` | `π` | `π/4` | `1` | C |
| 3 | `-3` | `0` | `3` | `-6` | A |
| 4 | `4` | `3` | `1` | `2` | B |
| 5 | `1/e²` | `1/2` | `1 - 1/e` | `1/e` | D |

Second kind: Is the answer to this problem equal to this option? (`is_A`, `is_B`, `is_C`, `is_D`, `noul`) Each of the four options is asked once, and the answer is the probability of "yes".

- `true`: The answer to this problem is <option content>.
- `false`: The answer to this problem is not <option content>.

## Results

Figures are taken from the run on the English dataset (`result/responses.jsonl`). All five problems are judged correctly.

| Problem | Topic | Correct answer | `answer` judgment | `confidence` |
| --- | --- | --- | --- | --- |
| 1 | calculus | `1` | `B` (1) | 0.50 |
| 2 | calculus | `π/4` | `C` (π/4) | 1 |
| 3 | linear algebra | `-3` | `A` (-3) | 0.56 |
| 4 | linear algebra | `3` | `B` (3) | 1 |
| 5 | probability | `1/e` | `D` (1/e) | 0.99 |

Readings of the two question forms on each option, with the correct answer marked:

| Problem | Option | `choice` probability | `noul` "yes" probability |
| --- | --- | --- | --- |
| 1 | `e - 1` | 0.22 | 0.41 |
| 1 | `1` correct answer | 0.62 | 0.92 |
| 1 | `e - 2` | 0.14 | 0.44 |
| 1 | `e` | 0.02 | 0.28 |
| 2 | `π/2` | 0 | 0.02 |
| 2 | `π` | 0 | 0.02 |
| 2 | `π/4` correct answer | 1 | 0.98 |
| 2 | `1` | 0 | 0.02 |
| 3 | `-3` correct answer | 0.67 | 0.82 |
| 3 | `0` | 0.06 | 0.12 |
| 3 | `3` | 0.20 | 0.64 |
| 3 | `-6` | 0.07 | 0.40 |
| 4 | `4` | 0 | 0 |
| 4 | `3` correct answer | 1 | 0.99 |
| 4 | `1` | 0 | 0.01 |
| 4 | `2` | 0 | 0.02 |
| 5 | `1/e²` | 0.01 | 0.10 |
| 5 | `1/2` | 0 | 0.02 |
| 5 | `1 - 1/e` | 0 | 0.04 |
| 5 | `1/e` correct answer | 0.99 | 0.93 |

Reading the tables:

- The judgment matches the correct answer on all five problems; none of the three topics is answered wrong.
- Confidence falls into two bands. Problems 2, 4, and 5 have `confidence` of 0.99 or above, with the correct answer taking nearly all of the `choice` probability. Problems 1 and 3 are lower, at 0.50 and 0.56 — and these are exactly the two that require working through a computation: the integral needs integration by parts, and the determinant needs a third-order expansion.
- Distractors are inflated under `noul`. Of the 20 (problem, option) pairs, 16 have a `noul` reading above the same option's `choice` probability, 1 is equal, and 3 are lower; the 3 lower ones all fall on problems where `choice` already assigns 0.99 or more — the correct answers of problems 2, 4, and 5.
- The wrong options of problem 1 are inflated across the board. The three wrong options hold only 0.02 to 0.22 under `choice`, yet get 0.28 to 0.44 when asked "is this the answer" on its own; the same problem's correct answer `1` rises from 0.62 under `choice` to 0.92 under `noul`. The largest single-option lift is problem 3's `3`, from 0.20 to 0.64.
- Each `noul` question is answered independently and returns the probability that its proposition holds; the readings do not form a distribution over the options and can be high at the same time.

Costs:

| Problem | Input tokens | Output tokens | Cost (USD) |
| --- | --- | --- | --- |
| 1 | 653 | 114 | `0.000027426` |
| 2 | 647 | 114 | `0.000027174` |
| 3 | 660 | 114 | `0.00002772` |
| 4 | 643 | 114 | `0.000027006` |
| 5 | 706 | 114 | `0.000029652` |
| Total | 3309 | 570 | `0.000138978` |

Output tokens are not billed.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/university-math/config.yaml
```

Results for the English dataset are appended to `result/responses.jsonl`, and results for the Chinese dataset to `result/responses_zh.jsonl`. Each sample is requested once per run; reruns skip records that already succeeded, while records that failed in the previous run are cleaned up and requested again automatically.
