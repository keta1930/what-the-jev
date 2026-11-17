"""Mark the closest saved underlength rewrite as a transparent exception."""

import csv
import json
import sys

import rewrite_en as rw


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python recover_en_underlength.py ENnnn")
    sample_id = sys.argv[1]
    rows = {r["id"]: r for r in csv.DictReader(rw.MANIFEST.open(encoding="utf-8-sig", newline="")) if r["language"] == "en"}
    if sample_id not in rows:
        raise SystemExit("Unknown English source ID")
    source = (rw.SOURCE_DIR / f"{sample_id}.txt").read_text(encoding="utf-8-sig").strip()
    if rw.sha(source) != rows[sample_id]["sha256"]:
        raise SystemExit("Source hash mismatch")
    if (rw.OUTPUT_DIR / f"{sample_id}.txt").exists() or (rw.RAW_DIR / f"{sample_id}.json").exists():
        raise SystemExit("Already completed")
    choices = []
    for attempt in range(1, rw.MAX_ATTEMPTS + 3):
        raw_path, record = rw.candidate_record(sample_id, attempt)
        if record is None:
            raise SystemExit(f"Expected saved attempt {attempt}")
        model_output, finish = rw.response_text(record["response"])
        checks = rw.quality(source, model_output)
        if finish == "stop" and record["http_status"] == 200 and checks["at_least_6_paragraphs"] and checks["within_source_20_percent"] and 750 <= checks["output_words"] < 800:
            choices.append((checks["output_words"], -attempt, attempt, raw_path, record))
    if not choices:
        raise SystemExit("No eligible saved output for underlength exception")
    _, _, attempt, raw_path, record = max(choices)
    checks = rw.record_completion(rows[sample_id], source, attempt, raw_path, record, allow_underlength_exception=True)
    meta = json.loads((rw.RAW_DIR / f"{sample_id}.json").read_text(encoding="utf-8"))
    if not meta.get("accepted_with_exception"):
        raise SystemExit("Exception metadata was not recorded")
    print(f"{sample_id}: chose saved attempt {attempt}, {checks['output_words']} words; explicit underlength exception, no API call")


if __name__ == "__main__":
    main()
