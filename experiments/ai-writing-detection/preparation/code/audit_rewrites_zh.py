"""Final deterministic audit of 100 Chinese rewrite outputs and all API attempts."""

import csv
import hashlib
import json
import re
from collections import Counter

import generate_rewrites_zh as gen
from harmonize_rewrites_zh import expected_payload
from repair_rewrites_zh import quality


REPORT = gen.OUT / "audit_summary.json"


def main():
    rows = [row for row in csv.DictReader(gen.MANIFEST.open(encoding="utf-8-sig", newline="")) if row["language"] == "zh"]
    failures = []
    flagged = []
    selected_cost = 0.0
    length_ratios = []
    rewrite_count = 0
    targeted = Counter()
    for row in rows:
        source_id = row["id"]
        text_path = gen.TEXT_OUT / f"{source_id}.txt"
        record_path = gen.OUT / f"{source_id}.json"
        if not text_path.exists() or not record_path.exists():
            failures.append(f"{source_id}: missing text or record")
            continue
        record = json.loads(record_path.read_text(encoding="utf-8"))
        source = (gen.PREP / row["text_path"]).read_text(encoding="utf-8-sig").strip()
        output = text_path.read_text(encoding="utf-8").strip()
        request_path = gen.PREP / record["request_path"]
        response_path = gen.PREP / record["response_path"]
        if not request_path.exists() or not response_path.exists():
            failures.append(f"{source_id}: missing request or response")
            continue
        request = json.loads(request_path.read_text(encoding="utf-8"))
        response = json.loads(response_path.read_text(encoding="utf-8"))
        core = expected_payload(source)["messages"][0]["content"]
        system = request["messages"][0]["content"]
        if not system.startswith(core):
            failures.append(f"{source_id}: non-frozen prompt core")
        if request["messages"][1]["content"] != gen.USER.format(body=source):
            failures.append(f"{source_id}: source or metadata leakage in user prompt")
        if (request["model"], request["temperature"], request["top_p"], request["max_tokens"]) != (gen.MODEL, gen.TEMPERATURE, gen.TOP_P, gen.MAX_TOKENS):
            failures.append(f"{source_id}: generation parameter mismatch")
        if record["prompt"]["system"] != system:
            failures.append(f"{source_id}: metadata prompt mismatch")
        if hashlib.sha256(source.encode("utf-8")).hexdigest() != row["sha256"] or record["source_sha256"] != row["sha256"]:
            failures.append(f"{source_id}: source hash mismatch")
        if hashlib.sha256(output.encode("utf-8")).hexdigest() != record["output_sha256"]:
            failures.append(f"{source_id}: output hash mismatch")
        choices = response.get("choices") or []
        response_text = (choices[0].get("message") or {}).get("content", "").strip() if choices else ""
        if record.get("formatting_only"):
            if re.sub(r"\s+", "", response_text) != re.sub(r"\s+", "", output):
                failures.append(f"{source_id}: formatting changed substantive response text")
        elif response_text != output:
            failures.append(f"{source_id}: response does not reproduce saved text")
        if record["model"] != gen.MODEL or record["model_returned"] != response.get("model"):
            failures.append(f"{source_id}: model metadata mismatch")
        cost, source_kind = gen.get_cost(response)
        if source_kind != "reported" or abs(float(record["cost_usd"]) - cost) > 1e-9:
            failures.append(f"{source_id}: actual cost unavailable or mismatched")
        selected_cost += cost
        flags, overlap = quality(source, output)
        if flags:
            flagged.append({"source_id": source_id, "flags": flags, "fivegram_overlap": overlap})
        length_ratios.append(gen.visible_length(output) / gen.visible_length(source))
        if record.get("attempt_history"):
            rewrite_count += 1
        for key in ("targeted_script_retry", "targeted_length_retry", "targeted_paragraph_retry", "targeted_overlap_retry"):
            if record.get(key):
                targeted[key] += 1
    responses = sorted(gen.OUT.glob("*.response.json"))
    total_cost = sum(gen.get_cost(json.loads(path.read_text(encoding="utf-8")))[0] for path in responses)
    report = {
        "expected": 100,
        "records": sum((gen.OUT / f"{row['id']}.json").exists() for row in rows),
        "texts": sum((gen.TEXT_OUT / f"{row['id']}.txt").exists() for row in rows),
        "paid_response_count": len(responses),
        "rewritten_after_first_attempt_count": rewrite_count,
        "selected_cost_usd": selected_cost,
        "all_attempts_cost_usd": total_cost,
        "length_ratio_min": min(length_ratios) if length_ratios else None,
        "length_ratio_max": max(length_ratios) if length_ratios else None,
        "targeted_counts": dict(targeted),
        "flagged": flagged,
        "audit_failures": failures,
    }
    gen.atomic_json(REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
