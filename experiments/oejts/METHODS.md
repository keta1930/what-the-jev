# OEJTS 1.2 — Methods

## Material and reproduction boundary

Eric Jorgenson's OEJTS 1.2 PDF marks its questions CC BY-NC-SA 4.0. This repository does not redistribute the questionnaire, endpoint wording, item requests or source PDF, and contains no official MBTI item bank. Preparation reads only a user-supplied local PDF/transcription and checks every historical input hash. Generated data/raw content is ignored and the release check fails if it is present.

## Historical protocol and conversion

Each item uses a model-self-description instruction and five positions. The 32 items are requested independently across ten consecutive rounds, without conversation context. import_manifest.json records 320 original-file hashes and 32 input hashes. Conversion only wraps each original response in the upstream id/response/error format; response bodies remain unchanged. IDs are oejts-q01 through oejts-q32 in each round. repeat:10 maps to responses_1.jsonl through responses_10.jsonl.

## Scoring

The following independently implemented numerical rules cite the source without reproducing questionnaire wording. Q is the selected position from 1 through 5.

```text
IE = 30 - Q3 - Q7 - Q11 + Q15 - Q19 + Q23 + Q27 - Q31
SN = 12 + Q4 + Q8 + Q12 + Q16 + Q20 - Q24 - Q28 + Q32
FT = 30 - Q2 + Q6 + Q10 - Q14 - Q18 + Q22 - Q26 - Q30
JP = 18 + Q1 + Q5 - Q9 + Q13 - Q17 + Q21 - Q25 + Q29
```

Scores >24 select E/N/T/P respectively; otherwise they select I/S/F/J. Exact 24 follows the same rule and is flagged in boundary_axes. All-middle responses give four 24s and ISFJ. The original scale is human self-report with lived-experience wording; this adaptation explores response/scoring stability rather than claiming psychological personality measurement.

## Integration and reproduction

Historical runs used independent scripts and budget controls. Integration only imports completed results. config.yaml is a standard upstream-compatible entry, not a claim that the shared runner produced the historical responses. response objects remain unchanged; analysis paths are adjusted to this repository. README contains reproduction commands. No new paid calls, prompt changes or sampling occurred.
