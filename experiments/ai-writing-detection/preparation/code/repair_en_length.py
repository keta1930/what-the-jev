"""One explicit length-repair request for an English rewrite that failed gate 1."""

import csv
import json
import os
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


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("EN"):
        raise SystemExit("Usage: python repair_en_length.py ENnnn")
    sample_id = sys.argv[1]
    rows = {r["id"]: r for r in csv.DictReader(rw.MANIFEST.open(encoding="utf-8-sig", newline="")) if r["language"] == "en"}
    if sample_id not in rows:
        raise SystemExit("Unknown English source ID")
    source = (rw.SOURCE_DIR / f"{sample_id}.txt").read_text(encoding="utf-8-sig").strip()
    if rw.sha(source) != rows[sample_id]["sha256"]:
        raise SystemExit("Source hash mismatch")
    if (rw.OUTPUT_DIR / f"{sample_id}.txt").exists() or (rw.RAW_DIR / f"{sample_id}.json").exists():
        raise SystemExit("Already completed; no paid retry")
    for n in range(1, rw.MAX_ATTEMPTS + 1):
        old_path, old = rw.candidate_record(sample_id, n)
        if old is None:
            raise SystemExit(f"Missing previous attempt {n}")
        old_text, finish = rw.response_text(old["response"])
        checks = rw.quality(source, old_text)
        if finish != "stop" or checks["within_800_1500_words"] or checks["output_words"] >= 800:
            raise SystemExit(f"Attempt {n} is not an underlength completion; inspect manually")
    attempt = rw.MAX_ATTEMPTS + 1
    while (rw.RAW_DIR / f"{sample_id}.attempt-{attempt:02d}.response.json").exists():
        previous_path, previous = rw.candidate_record(sample_id, attempt)
        previous_text, _ = rw.response_text(previous["response"])
        if rw.quality(source, previous_text)["output_words"] >= 800:
            raise SystemExit(f"Saved attempt {attempt} is already long enough; inspect it instead")
        attempt += 1
    if attempt > rw.MAX_ATTEMPTS + 2:
        raise SystemExit("At most two targeted length repairs are allowed")
    raw_path, record = rw.candidate_record(sample_id, attempt)
    if record is None:
        key = api_key()
        if not key:
            raise SystemExit("OpenRouter key missing; it was not logged")
        spend = rw.existing_spend()
        body = rw.request_body(source, attempt)
        worst = len(json.dumps(body, ensure_ascii=False).encode("utf-8")) * rw.INPUT_RATE + rw.MAX_TOKENS * rw.OUTPUT_RATE
        if spend + worst > rw.MAX_SPEND_USD:
            raise SystemExit("English cost cap would be exceeded")
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
        raise SystemExit("Unknown cost in response; stopped")
    checks = rw.record_completion(rows[sample_id], source, attempt, raw_path, record)
    print(f"{sample_id}: attempt {attempt}, {checks['output_words']} words, {checks['output_paragraphs']} paragraphs, accepted={checks['accepted']}, cost=${record['cost_usd']:.6f}")
    if not checks["accepted"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
