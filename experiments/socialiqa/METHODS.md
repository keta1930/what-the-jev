# SocialIQA — Methods

## Material and adaptation

All 2,224 rows of the authors' v1.4 test release are retained. The plain and withDims test labels agree row by row. Context/question enter state; answer uses A/B/C with unchanged English and order. Labels live separately in data/reference.json and do not enter requests. Twelve fixed dev debugging items only check the interface; no prompt tuning used them. Their results/costs are separate.

## Scoring and dependence

Reference-key agreement uses all 2,224 formal items. Outputs include valid-response accuracy, Wilson intervals, first-occurrence deduplicated accuracy and a 3,000-replicate bootstrap clustered by identical context/question/options (fixed seed in code). Duplicates remain in the primary result. The nine promptDim groups describe ATOMIC generation origins; rewritten questions may diverge, so these are not nine validated abilities. Accuracy does not measure felt empathy or moral personality.

## Historical billing

attempts.jsonl includes debug/test attempts. One failed attempt has unknown cost and retains a historical USD 0.01 reservation. All final successful responses remain intact.

## Integration and reproduction

Historical runs used independent scripts and budget controls. Integration only imports completed results. config.yaml is a standard upstream-compatible entry, not a claim that the shared runner produced the historical responses. response objects remain unchanged; analysis paths are adjusted to this repository. README contains reproduction commands. No new paid calls, prompt changes or sampling occurred.
