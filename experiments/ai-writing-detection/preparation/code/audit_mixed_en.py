"""Independently audit the 100 English mixed-condition artifacts."""

import csv
import hashlib
import json
import math
import re
from pathlib import Path


PREP = Path(__file__).resolve().parents[1]
DATASET = PREP.parent / "data" / "dataset.block-human.en.json"
AI_DIR = PREP / "clean" / "mixed_ai_blocks" / "en"
MIXED_DIR = PREP / "clean" / "mixed" / "en"
RAW_DIR = PREP / "raw" / "mixed" / "en"
WORD = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def sha(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def words(text):
    return len(WORD.findall(text))


def paragraphs(text):
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def fivegrams(text):
    tokens = [match.group(0).lower() for match in WORD.finditer(text)]
    return {tuple(tokens[index:index + 5]) for index in range(max(0, len(tokens) - 4))}


def overlap(source, output):
    out = fivegrams(output)
    return len(out & fivegrams(source)) / len(out) if out else 1.0


def expected_assignment(ids):
    ranked = sorted(ids, key=lambda sid: hashlib.sha256(f"jev-mixed-v1|en|{sid}".encode()).hexdigest())
    return {sid: 1 if index < 34 else 2 if index < 67 else 3 for index, sid in enumerate(ranked)}


def main():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    grouped = {}
    for sample in data["samples"]:
        source_id = sample["metadata"]["source_id"]
        grouped.setdefault(source_id, {})[int(sample["metadata"]["block_index"])] = sample["input"]["state"].strip()
    assignment = expected_assignment(grouped)
    failures = []
    rows = []
    ai_hashes = set()
    mixed_hashes = set()
    selected_cost = 0.0
    formatting_count = 0
    exception_ids = []

    for source_id in sorted(grouped):
        try:
            blocks = [grouped[source_id][index] for index in (1, 2, 3)]
            position = assignment[source_id]
            source = blocks[position - 1]
            meta_path = RAW_DIR / f"{source_id}.json"
            ai_path = AI_DIR / f"{source_id}.txt"
            mixed_path = MIXED_DIR / f"{source_id}.txt"
            response_path = RAW_DIR / f"{source_id}.response.json"
            if not all(path.exists() for path in (meta_path, ai_path, mixed_path, response_path)):
                raise ValueError("missing final artifact")
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            ai = ai_path.read_text(encoding="utf-8-sig").strip()
            mixed = mixed_path.read_text(encoding="utf-8-sig").strip()
            response = json.loads(response_path.read_text(encoding="utf-8"))
            if meta["replaced_block_index"] != position:
                raise ValueError("position mismatch")
            if meta["human_block_sha256"] != [sha(block) for block in blocks]:
                raise ValueError("human block hash mismatch")
            if meta["source_block_sha256"] != sha(source) or meta["ai_block_sha256"] != sha(ai):
                raise ValueError("source/AI block hash mismatch")
            expected = list(blocks)
            expected[position - 1] = ai
            if mixed != "\n\n".join(expected) or meta["mixed_sha256"] != sha(mixed):
                raise ValueError("mixed assembly mismatch")
            if response["source_id"] != source_id or response["target_position"] != position:
                raise ValueError("selected response mismatch")
            lower = max(250, math.ceil(words(source) * 0.8))
            upper = math.floor(words(source) * 1.2)
            output_words = words(ai)
            paragraph_ok = len(paragraphs(ai)) == len(paragraphs(source))
            overlap_value = overlap(source, ai)
            approved = bool(meta.get("approved_exception"))
            if not paragraph_ok or overlap_value >= 0.55 or ai == source:
                raise ValueError("structural or rewrite gate failed")
            if not (lower <= output_words <= upper):
                if not (source_id == "EN087" and approved and 230 <= output_words < 250 and math.ceil(words(source) * 0.8) <= output_words <= upper):
                    raise ValueError("unapproved length failure")
            if approved:
                exception_ids.append(source_id)
            if meta.get("formatting_only"):
                formatting_count += 1
                model_path = PREP / meta["model_output_path"]
                model = model_path.read_text(encoding="utf-8-sig").strip()
                if re.sub(r"\s+", "", model) != re.sub(r"\s+", "", ai):
                    raise ValueError("formatting-only output changed non-whitespace characters")
            selected_cost += float(meta["cost_usd"])
            if sha(ai) in ai_hashes or sha(mixed) in mixed_hashes:
                raise ValueError("duplicate final text hash")
            ai_hashes.add(sha(ai)); mixed_hashes.add(sha(mixed))
            rows.append({
                "source_id": source_id,
                "replaced_block_index": position,
                "source_words": words(source),
                "ai_words": output_words,
                "source_paragraphs": len(paragraphs(source)),
                "ai_paragraphs": len(paragraphs(ai)),
                "fivegram_overlap": overlap_value,
                "selected_attempt": meta["selected_attempt"],
                "formatting_only": bool(meta.get("formatting_only")),
                "approved_exception": approved,
                "cost_usd": meta["cost_usd"],
                "source_block_sha256": sha(source),
                "ai_block_sha256": sha(ai),
                "mixed_sha256": sha(mixed),
            })
        except Exception as exc:
            failures.append({"source_id": source_id, "error": str(exc)})

    all_attempt_cost = 0.0
    attempts = 0
    for path in sorted(RAW_DIR.glob("EN*.attempt-*.response.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        all_attempt_cost += float(record["cost_usd"])
        attempts += 1
    secret_files = []
    for path in RAW_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".txt", ".csv"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if "sk-or-" in text or "Authorization: Bearer" in text or '"Authorization"' in text:
                secret_files.append(str(path))
    if secret_files:
        failures.append({"source_id": "*", "error": f"secret-like text in {secret_files}"})

    positions = {str(index): sum(row["replaced_block_index"] == index for row in rows) for index in (1, 2, 3)}
    if positions != {"1": 34, "2": 33, "3": 33}:
        failures.append({"source_id": "*", "error": f"position counts {positions}"})
    summary = {
        "expected": 100,
        "records": len(rows),
        "position_counts": positions,
        "attempts": attempts,
        "selected_cost_usd": selected_cost,
        "all_attempts_cost_usd": all_attempt_cost,
        "formatting_only_count": formatting_count,
        "approved_exception_ids": exception_ids,
        "minimum_ai_words": min((row["ai_words"] for row in rows), default=None),
        "maximum_ai_words": max((row["ai_words"] for row in rows), default=None),
        "maximum_fivegram_overlap": max((row["fivegram_overlap"] for row in rows), default=None),
        "audit_failures": failures,
    }
    (RAW_DIR / "audit_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (RAW_DIR / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]) if rows else ["source_id"])
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
