---
title: "SocialIQA Social Commonsense: JEV as a Three-Choice Judge"
date: 2026-10-09
summary: "【Social Commonsense】Can JEV answer SocialIQA social commonsense questions in three-choice form, and does its confidence mark trustworthy answers?"
---

# SocialIQA Social Commonsense: JEV as a Three-Choice Judge

## Abstract

This experiment tests whether JEV can answer questions about everyday social situations. The setting is the full SocialIQA test split: 2,224 questions, each with a short social scenario and three candidate answers. JEV answered 80.58% correctly (95% CI 78.93–82.22%), far above the 33.3% random level, with accuracy nearly uniform across the nine ATOMIC question dimensions (78.11–84.66%). The confidence JEV reports is reliable: its mean (0.803) matches the actual accuracy, answers at confidence ≥0.85 make up 61.2% of the set and are 93.24% correct, and answers below 0.6 fall to 50.96%. The full run consumed 851,327 input tokens and 84,512 output tokens, costing $0.0358 in total. We conclude that JEV performs consistently across social commonsense question types, and that its confidence can indicate which answers are reliable.

## 1 Purpose

This experiment asks whether JEV can reason about everyday social situations: what people intend, need, and feel, and what happens to them next. SocialIQA is the standard benchmark for this kind of social commonsense, which is why we chose it. The three-choice format adds a second check: JEV reports a confidence with each answer, and we test whether that confidence indicates when an answer is reliable.

## 2 Dataset

SocialIQA is an English benchmark for commonsense reasoning about social situations. Each item gives a short context describing an everyday social event, asks a question about it, and offers three candidate answers. We use the official SocialIQA v1.4 release with dimension annotations, archived in `preparation/raw/`, and take its full test split of 2,224 questions.

Each question is posed to JEV as a single-choice question over the dataset's three options, kept in their original order. Correct answers are spread near-evenly over the three positions (720 A, 754 B, 750 C), so guessing by position offers no advantage.

The release annotates each question with the ATOMIC dimension it probes; these labels come from the dataset. Six dimensions ask about the central person: why they acted (xIntent), what they needed beforehand (xNeed), how to describe them (xAttr), how they feel afterward (xReact), what happens to them (xEffect), and what they want to do next (xWant). Three ask about the other people involved: how they feel (oReact), what happens to them (oEffect), and what they want to do next (oWant).

## 3 A Minimal Example

This section shows one real question from the dataset with its complete input and output. The input sent to the model (the model field is omitted):

```json
{
  "state": {
    "context": "bailey was a nice person so she called the family together.",
    "question": "What will happen to Others?"
  },
  "questions": {
    "answer": {
      "type": "choice",
      "instructions": "Select the most plausible answer to the question based on the context and everyday social commonsense. Choose exactly one option.",
      "criteria": {
        "A": "talk to the family",
        "B": "hate bailey",
        "C": "thank bailey"
      }
    }
  }
}
```

The model's output (key fields only):

```json
{
  "answers": {
    "answer": {
      "type": "choice",
      "choice": "C",
      "probabilities": {"A": 0.41, "B": 0, "C": 0.59},
      "confidence": 0.38
    }
  },
  "usage": {"input_tokens": 375, "output_tokens": 38, "cost": 0.00001575}
}
```

JEV chose C, the correct answer.

## 4 Results

### Overall

All 2,224 questions received a valid answer; no call failed. Judged against the reference answers provided by the dataset, 1,792 answers are correct: an accuracy of 80.58%, with a 95% confidence interval of 78.93–82.22%. Random guessing over three options scores 33.3%.

### Confidence and accuracy

JEV reports a confidence value with each answer. The mean confidence over all answers is 0.803, almost exactly the actual accuracy. Accuracy rises steadily with confidence (Figure 1):

| Confidence | Answers | Share | Accuracy |
| --- | ---: | ---: | ---: |
| < 0.6 | 467 | 21.0% | 50.96% |
| 0.6–0.85 | 396 | 17.8% | 71.97% |
| ≥ 0.85 | 1,361 | 61.2% | 93.24% |

![Accuracy by confidence](fig/en/confidence-accuracy.png)

Figure 1: most answers cluster at high confidence, and accuracy rises steadily with confidence; the dashed line marks the 33.3% random level.

### Behavior

Three answers (0.13%) carry option probabilities that sum to 0.99 rather than 1. In eight answers (0.36%) two options tie for the highest probability, and the selected option is one of the two; no answer selects an option below the highest probability. The two sets do not overlap, and 2,213 answers show neither.

### Cost

The run consumed 851,327 input tokens and 84,512 output tokens, for a total cost of $0.0358.

### Results by dimension

Accuracy is nearly uniform across the nine ATOMIC dimensions (Figure 2):

| Dimension | Question asked | Questions | Accuracy |
| --- | --- | ---: | ---: |
| xWant | What the person wants next | 339 | 84.66% |
| xNeed | What the person needed before | 277 | 81.23% |
| xIntent | Why the person acted | 297 | 80.47% |
| oReact | How others feel after | 223 | 80.27% |
| oEffect | What happens to others | 159 | 79.87% |
| oWant | What others want next | 252 | 79.76% |
| xEffect | What happens to the person | 103 | 79.61% |
| xReact | How the person feels after | 277 | 79.42% |
| xAttr | How to describe the person | 297 | 78.11% |

![Accuracy by ATOMIC dimension](fig/en/dimension-accuracy.png)

Figure 2: all nine dimensions land in a narrow band of 78.11–84.66%, with no dimension clearly behind.

## 5 Conclusion

JEV answers about four in five social commonsense questions correctly, and it does about as well on one question type as another; no dimension lags behind. What is most useful here is the confidence: on average it matches the actual accuracy, and it separates near-certain answers from less accurate ones. Accepting only answers at confidence ≥0.85 keeps more than 60% of the questions at above 93% accuracy; the remaining answers stay well above the random level, so they should go to review rather than be discarded.

## Related Resources

- SocialIQA dataset: https://maartensap.com/social-iqa/
- SocialIQA paper: https://arxiv.org/abs/1904.09728
- ATOMIC paper: https://arxiv.org/abs/1811.00146
