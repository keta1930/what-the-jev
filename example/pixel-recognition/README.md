---
title: "Image Recognition from Pixel Matrices"
date: 2026-10-11
summary: "This example tests whether Jev can identify a handwritten digit and an image category from numeric pixel matrices."
samples: 2
input_tokens: 13.9k
cost: 0.000585228
---

# Image Recognition from Pixel Matrices

This example tests whether Jev can identify a handwritten digit and an image category from numeric pixel matrices.

It contains 2 samples. `mnist-0001`, the first MNIST test image, is a 28×28 grayscale handwritten digit. `cifar-10-0001`, the first CIFAR-10 test image, is a 32×32 color image. Only numeric pixel matrices are sent, without an image attachment or reference label.

## Questions

1. `digit`: Which digit is written in the handwritten-digit image? `state.pixels` is a 28-row by 28-column, row-major grayscale matrix, with values from 0 to 255: 0 is the black background and 255 is the white stroke.
2. `category`: Which category does the main subject of the color image belong to? The `r`, `g`, and `b` fields of `state.pixels` are each a 32-row by 32-column, row-major channel matrix, with values from 0 to 255.

Both use `choice`, returning one option key with `probabilities` and `confidence`. Each question has ten options:

| Option key | `digit` description | Option key | `category` description |
| --- | --- | --- | --- |
| `0` | The digit 0. | `airplane` | An airplane. |
| `1` | The digit 1. | `automobile` | An automobile. |
| `2` | The digit 2. | `bird` | A bird. |
| `3` | The digit 3. | `cat` | A cat. |
| `4` | The digit 4. | `deer` | A deer. |
| `5` | The digit 5. | `dog` | A dog. |
| `6` | The digit 6. | `frog` | A frog. |
| `7` | The digit 7. | `horse` | A horse. |
| `8` | The digit 8. | `ship` | A ship. |
| `9` | The digit 9. | `truck` | A truck. |

## Minimal Example

The input for `mnist-0001`, with `model` omitted. The pixel matrix shows only the first row, one middle row, and the last row. `…` marks omitted rows:

```json
{
  "state": {
    "pixels": [
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      "…",
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,129,254,238,44,0,0,0,0,0,0,0],
      "…",
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
  },
  "questions": {
    "digit": {
      "type": "choice",
      "instructions": "state.pixels is the pixel matrix of a grayscale handwritten-digit image: 28 rows by 28 columns, row-major, each value a grayscale from 0 to 255, where 0 is the black background and 255 is the white stroke. Judge which digit is written in the image.",
      "criteria": {
        "0": "The digit 0.",
        "1": "The digit 1.",
        "2": "The digit 2.",
        "3": "The digit 3.",
        "4": "The digit 4.",
        "5": "The digit 5.",
        "6": "The digit 6.",
        "7": "The digit 7.",
        "8": "The digit 8.",
        "9": "The digit 9."
      }
    }
  }
}
```

The model's output (key fields only):

```json
{
  "answers": {
    "digit": {"type": "choice", "choice": "2", "probabilities": {"0": 0.13, "1": 0.08, "2": 0.18000000000000002, "3": 0.07, "4": 0.05, "5": 0.05, "6": 0.08, "7": 0.1, "8": 0.12, "9": 0.14}, "confidence": 0.08}
  },
  "usage": {"input_tokens": 2321, "output_tokens": 87, "cost": 0.000097482}
}
```

Jev chose `2` instead of the reference digit `7`. With only 0.18 on its chosen answer and `confidence` 0.08, it also failed to make a clear selection.

## Results

Both samples returned successfully, but neither recognized the reference category.

| Question | Reference label | Model choice | Chosen-option probability | Correct-option probability | `confidence` |
| --- | --- | --- | --- | --- | --- |
| `digit` (MNIST) | `7` | `2` | 0.18 | 0.10 | 0.08 |
| `category` (CIFAR-10) | `cat` | `airplane` | 0.17 | 0.13 | 0.06 |

In both responses, the highest option probability is below 0.20, leaving most probability spread across other categories. For the color image, `airplane` has 0.17 and the correct `cat` has 0.13; the selected category has little support over the reference. The two submitted pixel matrices produced wrong answers with little separation between candidates.

## Cost

The English results total 13934 input tokens, 178 output tokens, and `0.000585228` USD.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/pixel-recognition/config.yaml
```

The run processes the English dataset `data/dataset.json` and the Chinese dataset `data/dataset_zh.json`, appending results to `result/responses.jsonl` and `result/responses_zh.jsonl` respectively. Each sample is requested only once per run. Records that already succeeded are skipped on reruns, and records that failed in the previous run are cleared and requested again.
