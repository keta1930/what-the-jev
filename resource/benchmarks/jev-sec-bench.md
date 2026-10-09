---
title: "jev-sec-bench (Gaurav-Gosain)"
updated: 2026-10-09
---

# jev-sec-bench (Gaurav-Gosain)

**Positioning** jev-sec-bench, by Gaurav-Gosain, is a blind security benchmark for Jev covering prompt injection and vulnerable-code detection, implemented in Go on top of jev-go.

**What it does** Both benchmarks are blind and use public corpora. Prompt-injection detection runs on all 662 labelled messages in `deepset/prompt-injections`, 263 of them injections, one request each with no threshold tuning. Vulnerable-code detection runs on 200 matched pairs from `CyberNative/Code_Vulnerability_Security_DPO`, where both halves solve the same task in the same language and style and one carries a vulnerability; the halves are shuffled apart and scored independently, without telling Jev the vulnerability class or that pairs exist. The repository also runs a no-context ablation and a corpus label audit, and keeps per-sample output.

**Characteristics** At a plain 0.50 cut, the injection benchmark reports accuracy 96.5%, precision 96.2%, recall 95.1%, F1 95.6%, and ROC-AUC 0.9927, with 22.7 s wall time for 662 messages; adding the deployment's purpose as context raised accuracy from 89.7% to 96.5%. In the code benchmark the vulnerable half scored above its own secure twin in 178 of 200 pairs (89.0%) — the author's headline figure — while the 0.50-cut absolute accuracy was 71.5%. MIT-licensed, a Go implementation, run once on 2026-09-16.

**When to use** Suited to evaluating Jev for security and guardrail scenarios where a probability can drive a threshold, and to seeing how much a context-free guardrail loses. The author states the limits plainly: the code corpus is synthetic and its labels are demonstrably noisy — the audit shows at least 38% of the apparent false positives are provable corpus label errors, a floor rather than an estimate — the run is single with no repeats, and small per-class cells carry real variance. Validate thresholds on your own labelled data and cite these limits with any figure.

## Links

- [GitHub – Gaurav-Gosain/jev-sec-bench repository](https://github.com/Gaurav-Gosain/jev-sec-bench)
