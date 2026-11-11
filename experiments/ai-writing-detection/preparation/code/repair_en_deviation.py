"""One targeted retry for a saved English rewrite outside source ±20%.

The earlier selected text and metadata are archived before replacement. A
retry is selected only if it moves closer to the predeclared paired-length
interval while still meeting the corpus hard range and paragraph minimum.
"""

import csv
import json
import os
import shutil
import sys
from datetime import datetime, timezone

import rewrite_en as rw


def api_key():
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key and sys.platform == "win32":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as user_env:
                key = winreg.QueryValueEx(user_env, "OPENROUTER_API_KEY")[0].strip()
        except (FileNotFoundError, OSError):
            pass
    return key


def distance(word_count, source_words):
    lower = max(800, round(source_words * 0.8))
    upper = min(1500, round(source_words * 1.2))
    return max(lower - word_count, word_count - upper, 0)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"EN035", "EN080"}:
        raise SystemExit("Usage: python repair_en_deviation.py EN035|EN080")
    sample_id = sys.argv[1]
    rows = {r["id"]: r for r in csv.DictReader(rw.MANIFEST.open(encoding="utf-8-sig", newline="")) if r["language"] == "en"}
    row = rows[sample_id]
    source = (rw.SOURCE_DIR / f"{sample_id}.txt").read_text(encoding="utf-8-sig").strip()
    if rw.sha(source) != row["sha256"]:
        raise SystemExit("Source hash mismatch")
    output_path = rw.OUTPUT_DIR / f"{sample_id}.txt"
    meta_path = rw.RAW_DIR / f"{sample_id}.json"
    response_path = rw.RAW_DIR / f"{sample_id}.response.json"
    if not all(p.exists() for p in (output_path, meta_path, response_path)):
        raise SystemExit("Existing selected rewrite and provenance are required")
    selected = output_path.read_text(encoding="utf-8").strip()
    old_distance = distance(rw.words(selected), rw.words(source))
    if old_distance == 0:
        raise SystemExit("Selected rewrite already within paired length range")
    attempt = rw.MAX_ATTEMPTS + 1
    raw_path, record = rw.candidate_record(sample_id, attempt)
    if record is None:
        key = api_key()
        if not key:
            raise SystemExit("OpenRouter key missing; it was not logged")
        body = rw.request_body(source, attempt)
        spend = rw.existing_spend()
        worst = len(json.dumps(body, ensure_ascii=False).encode("utf-8")) * rw.INPUT_RATE + rw.MAX_TOKENS * rw.OUTPUT_RATE
        if spend + worst > rw.MAX_SPEND_USD:
            raise SystemExit("English hard cost cap would be exceeded")
        status, response = rw.invoke(body, key)
        record = {
            "source_id": sample_id,
            "attempt": attempt,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "endpoint": rw.ENDPOINT,
            "http_status": status,
            "request_body": body,
            "response": response,
            "cost_usd": rw.cost_of(response),
        }
        rw.save_json(raw_path, record)
    if record["cost_usd"] is None:
        raise SystemExit("Unknown response cost; saved but not selected")
    candidate, finish = rw.response_text(record["response"])
    q = rw.quality(source, candidate)
    new_distance = distance(q["output_words"], q["source_words"])
    valid = record["http_status"] == 200 and finish == "stop" and q["within_800_1500_words"] and q["at_least_6_paragraphs"]
    if valid and new_distance < old_distance:
        shutil.copy2(output_path, rw.RAW_DIR / f"{sample_id}.prior-selection.txt")
        shutil.copy2(meta_path, rw.RAW_DIR / f"{sample_id}.prior-selection.json")
        shutil.copy2(response_path, rw.RAW_DIR / f"{sample_id}.prior-selection.response.json")
        checks = rw.record_completion(row, source, attempt, raw_path, record)
        updated = json.loads(meta_path.read_text(encoding="utf-8"))
        updated["targeted_reason"] = "paired_length_deviation"
        updated["prior_selection_metadata_path"] = str((rw.RAW_DIR / f"{sample_id}.prior-selection.json").relative_to(rw.PREP)).replace("\\", "/")
        updated["approved_exception"] = not checks["within_source_20_percent"]
        rw.save_json(meta_path, updated)
        print(f"{sample_id}: selected targeted attempt {attempt}, {q['output_words']} words; paired length deviation {old_distance}->{new_distance}; cost=${record['cost_usd']:.6f}")
    else:
        updated = json.loads(meta_path.read_text(encoding="utf-8"))
        updated["approved_exception"] = True
        updated["exception_reason"] = f"Paired length deviation {old_distance} words; one targeted retry was not closer to range"
        rw.save_json(meta_path, updated)
        print(f"{sample_id}: retained prior selection ({rw.words(selected)} words); targeted candidate {q['output_words']} words not closer; cost=${record['cost_usd']:.6f}")


if __name__ == "__main__":
    main()
