---
title: "Pixel Recognition"
date: 2026-10-10
summary: "This experiment tests whether the Jev model can recognize image content from pixel values alone."
samples: 2
input_tokens: 13.9k
cost: 0.000585228
---

# Pixel Recognition

This experiment tests whether the Jev model can recognize image content from pixel values alone.

It contains 2 samples: MNIST test item 1 (a 28×28 grayscale handwritten-digit image) and CIFAR-10 test item 1 (a 32×32 color animal image). The input is only the pixel value matrices; no image file is provided.

Each sample asks one question:

1. Which digit is written in the handwritten-digit image? The input is a grayscale pixel matrix of 28 rows by 28 columns, row-major, with values from 0 to 255, where 0 is the black background and 255 is the white stroke. Pick one of `0` through `9`. (`choice`)

   - `0`: The digit 0.
   - `1`: The digit 1.
   - `2`: The digit 2.
   - `3`: The digit 3.
   - `4`: The digit 4.
   - `5`: The digit 5.
   - `6`: The digit 6.
   - `7`: The digit 7.
   - `8`: The digit 8.
   - `9`: The digit 9.

2. Which category does the main subject of the color image belong to? The input is three 32-by-32 pixel matrices `r`, `g`, `b`, row-major, with values from 0 to 255. Pick one of `airplane`, `automobile`, `bird`, `cat`, `deer`, `dog`, `frog`, `horse`, `ship`, `truck`. (`choice`)

   - `airplane`: An airplane.
   - `automobile`: An automobile.
   - `bird`: A bird.
   - `cat`: A cat.
   - `deer`: A deer.
   - `dog`: A dog.
   - `frog`: A frog.
   - `horse`: A horse.
   - `ship`: A ship.
   - `truck`: A truck.

## Minimal Example

This section takes `mnist-0001` and shows its input and output. The input sent to the model (the model field is omitted; the 28-row pixel matrix is truncated to its first, middle, and last rows):

```json
{
  "state": {
    "pixels": [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      "…",
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 129, 254, 238, 44, 0, 0, 0, 0, 0, 0, 0],
      "…",
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
  },
  "questions": {
    "digit": {
      "type": "choice",
      "instructions": "state.pixels is the pixel matrix of a grayscale handwritten-digit image: 28 rows by 28 columns, row-major, each value a grayscale from 0 to 255, where 0 is the black background and 255 is the white stroke. Judge which digit is written in the image.",
      "criteria": {"0": "The digit 0.", "1": "The digit 1.", "2": "The digit 2.", "3": "The digit 3.", "4": "The digit 4.", "5": "The digit 5.", "6": "The digit 6.", "7": "The digit 7.", "8": "The digit 8.", "9": "The digit 9."}
    }
  }
}
```

The model's output (key fields only):

```json
{
  "answers": {
    "digit": {"type": "choice", "choice": "2", "probabilities": {"0": 0.13, "1": 0.08, "2": 0.18, "3": 0.07, "4": 0.05, "5": 0.05, "6": 0.08, "7": 0.1, "8": 0.12, "9": 0.14}, "confidence": 0.08}
  },
  "usage": {"input_tokens": 2321, "output_tokens": 87, "cost": 0.000097482}
}
```

Jev chose `2` where the true label is `7`, and the ten probabilities stay near uniform, from 0.05 to 0.18.

## Results

On both questions Jev failed to recognize the image content from pixel values; the probability distributions are near-uniform, equivalent to random choice.

The MNIST sample's true label is 7. `digit` was judged `2`, which is wrong. The ten options' probabilities fall between 0.05 and 0.18, the correct option `7` got only 0.10, and `confidence` is 0.08.

The CIFAR-10 sample's true label is `cat`. `category` was judged `airplane`, which is wrong. The ten options' probabilities fall between 0.03 and 0.17, `cat` got 0.13, and `confidence` is 0.06.

Cost: 13934 input tokens, 178 output tokens, total charge `0.000585228` USD. Output tokens are not billed.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/pixel-recognition/config.yaml
```

One run requests both the English dataset and the Chinese dataset, appending results to `result/responses.jsonl` and `result/responses_zh.jsonl` respectively. Each sample is requested only once per run; reruns skip records that already succeeded, and records that failed in the previous run are cleared and requested again automatically.
