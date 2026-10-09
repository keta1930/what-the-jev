---
title: "Ticket Triage"
date: 2026-10-09
summary: "This experiment tests the Jev model's judgment on customer support tickets."
---

# Ticket Triage

This experiment tests the Jev model's judgment on customer support tickets.

It contains 1 sample.

Ticket: "I was charged twice for the same order. Please refund the duplicate charge."

Jev is asked to judge three things:

1. Which category does this ticket belong to? Choose one of `billing`, `technical`, `account`, `feature`, `other`. (`choice`)

2. Does the customer actually ask for money back? The answer is a probability between 0 and 1, giving the likelihood that the condition holds. (`noul`)

3. How urgent is this ticket? The answer is a position value between 0 and 2, falling on one level or between two levels. (`score`)

   - `0`: "General inquiry or feature suggestion; can wait for a later release."
   - `1`: "Affects a single customer's usage or involves a billing dispute; needs handling soon."
   - `2`: "Large-scale service outage, ongoing financial loss, or a completely blocked critical business process; needs immediate handling."

## Results

The Jev model classified this ticket correctly.

`category` was judged `billing`.

`refund` came out 0.98, meaning the model holds that the customer is asking for a refund.

`urgency` fell on level 1.

`confidence` was 1 for both `category` and `urgency`.

Cost: 616 input tokens, 83 output tokens, `0.000025872` USD. Output tokens are not billed.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='<key>'
python run.py example/ticket-triage/config.yaml
```

The run processes the English dataset `data/dataset.json` and the Chinese dataset `data/dataset_zh.json`, appending results to `result/responses.jsonl` and `result/responses_zh.jsonl` respectively. Each sample is requested only once per run; records that already succeeded are skipped on reruns, and records that failed in the previous run are cleared and requested again.
