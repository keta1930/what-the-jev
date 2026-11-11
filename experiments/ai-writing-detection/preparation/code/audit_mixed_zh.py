"""Audit the 100 Chinese mixed essays and write a compact manifest."""

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


EXPERIMENT = Path(r"C:\Users\asus\Desktop\Jev文章AI检测实验\what-the-jev\experiments\ai-writing-detection")
PREP = EXPERIMENT / "preparation"
DATASET = EXPERIMENT / "data" / "dataset.block-human.zh.json"
RAW = PREP / "raw" / "mixed" / "zh"
MIXED = PREP / "clean" / "mixed" / "zh"
AI = PREP / "clean" / "mixed_ai_blocks" / "zh"


def sha(value: str) -> str:
    return hashlib.sha256(value.strip().encode("utf-8")).hexdigest()


def load_blocks():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    grouped = defaultdict(dict)
    for sample in data["samples"]:
        grouped[sample["metadata"]["source_id"]][int(sample["metadata"]["block_index"])] = sample["input"]["state"].strip()
    return {source_id: [items[index] for index in (1, 2, 3)] for source_id, items in grouped.items()}


def main():
    blocks_by_source = load_blocks()
    failures = []
    rows = []
    positions = Counter()
    selected_cost = 0.0
    all_cost = 0.0
    exceptions = []
    for source_id in sorted(blocks_by_source):
        record_path = RAW / f"{source_id}.json"
        ai_path = AI / f"{source_id}.txt"
        mixed_path = MIXED / f"{source_id}.txt"
        if not all(path.exists() for path in (record_path, ai_path, mixed_path)):
            failures.append(f"{source_id}: missing record or text")
            continue
        record = json.loads(record_path.read_text(encoding="utf-8"))
        ai_text = ai_path.read_text(encoding="utf-8-sig").strip()
        mixed_text = mixed_path.read_text(encoding="utf-8-sig").strip()
        position = int(record["target_position"])
        positions[position] += 1
        blocks = blocks_by_source[source_id]
        expected_blocks = list(blocks)
        expected_blocks[position - 1] = ai_text
        expected_mixed = "\n\n".join(expected_blocks)
        checks = {
            "record_source": record["source_id"] == source_id,
            "human_hashes": record["human_block_sha256"] == [sha(block) for block in blocks],
            "source_target_hash": record["source_ai_block_sha256"] == sha(blocks[position - 1]),
            "ai_hash": record["ai_block_sha256"] == sha(ai_text),
            "mixed_hash": record["mixed_sha256"] == sha(mixed_text),
            "exact_assembly": mixed_text == expected_mixed,
            "non_target_block_1": position == 1 or expected_blocks[0] == blocks[0],
            "non_target_block_2": position == 2 or expected_blocks[1] == blocks[1],
            "non_target_block_3": position == 3 or expected_blocks[2] == blocks[2],
            "response_exists": (PREP / record["selected_response_path"]).exists(),
            "request_exists": (PREP / record["selected_request_path"]).exists(),
        }
        for name, passed in checks.items():
            if not passed:
                failures.append(f"{source_id}: {name}")
        if record.get("approved_exception"):
            exceptions.append({"source_id": source_id, "flags": record["quality_checks"]["flags"]})
        selected_cost += float(record["selected_cost_usd"])
        all_cost += float(record["all_attempts_cost_usd"])
        rows.append({
            "source_id": source_id,
            "target_position": position,
            "source_block_sha256": record["source_ai_block_sha256"],
            "ai_block_sha256": record["ai_block_sha256"],
            "mixed_sha256": record["mixed_sha256"],
            "source_visible_characters": record["quality_checks"]["source_visible_characters"],
            "ai_visible_characters": record["quality_checks"]["output_visible_characters"],
            "source_paragraphs": record["quality_checks"]["source_paragraphs"],
            "ai_paragraphs": record["quality_checks"]["output_paragraphs"],
            "fivegram_overlap": record["quality_checks"]["fivegram_overlap"],
            "selected_attempt": record["selected_attempt"],
            "approved_exception": bool(record.get("approved_exception")),
            "selected_cost_usd": record["selected_cost_usd"],
            "all_attempts_cost_usd": record["all_attempts_cost_usd"],
            "ai_block_path": record["ai_block_path"],
            "mixed_path": record["mixed_path"],
        })

    if positions != Counter({1: 34, 2: 33, 3: 33}):
        failures.append(f"position counts: {dict(positions)}")
    if len(rows) != 100:
        failures.append(f"row count: {len(rows)}")
    if len({row["mixed_sha256"] for row in rows}) != len(rows):
        failures.append("duplicate mixed text hashes")
    secret_pattern = re.compile(r"sk-or-|Authorization\s*[:=]\s*Bearer", re.I)
    secret_hits = []
    for path in list(RAW.glob("*.json")) + list(MIXED.glob("*.txt")) + list(AI.glob("*.txt")):
        if secret_pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            secret_hits.append(str(path))
    if secret_hits:
        failures.append(f"secret-like text found: {secret_hits}")

    manifest_path = RAW / "manifest.csv"
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "expected": 100,
        "records": len(rows),
        "position_counts": {str(key): positions[key] for key in (1, 2, 3)},
        "selected_cost_usd": selected_cost,
        "all_attempts_cost_usd": all_cost,
        "approved_exceptions": exceptions,
        "audit_failures": failures,
    }
    (RAW / "audit_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit("Chinese mixed audit failed")


if __name__ == "__main__":
    main()
