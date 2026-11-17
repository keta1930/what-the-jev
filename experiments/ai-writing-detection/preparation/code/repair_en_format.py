"""Recover a saved English model response using paragraph-only formatting."""

import csv
import json
import sys

import rewrite_en as rw


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python repair_en_format.py ENnnn ATTEMPT")
    sample_id, attempt_text = sys.argv[1:]
    attempt = int(attempt_text)
    rows = {r["id"]: r for r in csv.DictReader(rw.MANIFEST.open(encoding="utf-8-sig", newline="")) if r["language"] == "en"}
    if sample_id not in rows or attempt not in range(1, rw.MAX_ATTEMPTS + 1):
        raise SystemExit("Unknown source ID or invalid attempt")
    source = (rw.SOURCE_DIR / f"{sample_id}.txt").read_text(encoding="utf-8-sig").strip()
    if rw.sha(source) != rows[sample_id]["sha256"]:
        raise SystemExit("Source hash mismatch")
    if (rw.OUTPUT_DIR / f"{sample_id}.txt").exists() or (rw.RAW_DIR / f"{sample_id}.json").exists():
        raise SystemExit("Already completed")
    raw_path, record = rw.candidate_record(sample_id, attempt)
    if record is None:
        raise SystemExit("Saved model response missing")
    model_output, _ = rw.response_text(record["response"])
    if len(rw.paragraphs(model_output)) >= 6:
        raise SystemExit("Not a short-paragraph response")
    checks = rw.record_completion(rows[sample_id], source, attempt, raw_path, record)
    if not checks["accepted"]:
        raise SystemExit(f"Formatting did not meet quality rules: {json.dumps(checks)}")
    print(f"{sample_id}: recovered attempt {attempt}; {checks['output_words']} words, {checks['output_paragraphs']} paragraphs; no API call")


if __name__ == "__main__":
    main()
