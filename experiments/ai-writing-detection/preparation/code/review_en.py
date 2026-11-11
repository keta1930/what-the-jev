"""Audit English human/rewrite pairs without calling any model."""

import csv
import hashlib
import json
import re
from pathlib import Path


PREP = Path(__file__).resolve().parents[1]
HUMAN = PREP / "clean" / "human" / "en"
REWRITE = PREP / "clean" / "ai_rewritten" / "en"
RAW = PREP / "raw" / "rewrites" / "en"
WORD = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def tokenized(text):
    return [m.group(0).lower() for m in WORD.finditer(text)]


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def overlap(source, rewrite, n=5):
    s = tokenized(source)
    r = tokenized(rewrite)
    source_grams = {tuple(s[i:i+n]) for i in range(len(s)-n+1)}
    rewrite_grams = [tuple(r[i:i+n]) for i in range(len(r)-n+1)]
    return sum(gram in source_grams for gram in rewrite_grams) / len(rewrite_grams) if rewrite_grams else 0.0


def digest(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def main():
    rows = []
    cost = 0.0
    for i in range(1, 101):
        sample_id = f"EN{i:03d}"
        human_path = HUMAN / f"{sample_id}.txt"
        output_path = REWRITE / f"{sample_id}.txt"
        meta_path = RAW / f"{sample_id}.json"
        raw_path = RAW / f"{sample_id}.response.json"
        present = output_path.exists() and meta_path.exists() and raw_path.exists()
        row = {"id": sample_id, "present": present, "source_words": "", "output_words": "", "output_paragraphs": "", "within_20_percent": "", "fivegram_overlap": "", "hash_ok": "", "raw_ok": "", "cost_usd": "", "flags": "", "blocking_flags": "", "reviewed_flags": ""}
        if present:
            source = human_path.read_text(encoding="utf-8-sig").strip()
            output = output_path.read_text(encoding="utf-8-sig").strip()
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            sw = len(tokenized(source))
            ow = len(tokenized(output))
            para = len(paragraphs(output))
            ov = overlap(source, output)
            hash_ok = meta.get("source_sha256") == digest(source) and meta.get("output_sha256") == digest(output)
            raw_ok = raw.get("source_id") == sample_id and raw.get("response", {}).get("choices", [{}])[0].get("finish_reason") == "stop"
            model_output = raw.get("response", {}).get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if meta.get("formatting_only"):
                model_path = PREP / meta.get("model_output_path", "")
                raw_ok = raw_ok and model_path.exists() and model_path.read_text(encoding="utf-8").strip() == model_output
                raw_ok = raw_ok and re.sub(r"\s+", "", model_output) == re.sub(r"\s+", "", output)
                raw_ok = raw_ok and meta.get("model_paragraphs") == len(paragraphs(model_output)) and meta.get("final_paragraphs") == para
            else:
                raw_ok = raw_ok and output == model_output
            amount = meta.get("cost_usd", 0.0)
            cost += amount
            flags = []
            if not 800 <= ow <= 1500:
                flags.append("word_range")
            if para < 6:
                flags.append("paragraphs")
            if not 0.8 * sw <= ow <= 1.2 * sw:
                flags.append("source_length_deviation")
            if ov > 0.20:
                flags.append("high_5gram_overlap_review")
            if not hash_ok:
                flags.append("hash_mismatch")
            if not raw_ok:
                flags.append("raw_response_error")
            reviewed = []
            blocking = []
            for flag in flags:
                if flag == "high_5gram_overlap_review" and meta.get("reviewed_quote_overlap"):
                    reviewed.append(flag)
                elif flag in ("source_length_deviation", "word_range") and meta.get("approved_exception"):
                    reviewed.append(flag)
                else:
                    blocking.append(flag)
            row.update(source_words=sw, output_words=ow, output_paragraphs=para, within_20_percent=0.8*sw<=ow<=1.2*sw, fivegram_overlap=round(ov, 5), hash_ok=hash_ok, raw_ok=raw_ok, cost_usd=round(amount, 9), flags=";".join(flags), blocking_flags=";".join(blocking), reviewed_flags=";".join(reviewed))
        else:
            row["flags"] = "missing"
            row["blocking_flags"] = "missing"
        rows.append(row)
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / "quality_report.csv"
    with target.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "expected": 100,
        "present": sum(r["present"] for r in rows),
        "missing": [r["id"] for r in rows if not r["present"]],
        "flags": {r["id"]: r["flags"] for r in rows if r["flags"] and r["flags"] != "missing"},
        "blocking_flags": {r["id"]: r["blocking_flags"] for r in rows if r["blocking_flags"]},
        "reviewed_flags": {r["id"]: r["reviewed_flags"] for r in rows if r["reviewed_flags"]},
        "cost_usd_accepted": round(cost, 9),
        "cost_usd_all_attempts": round(sum((json.loads(p.read_text(encoding="utf-8")).get("cost_usd") or 0.0) for p in RAW.glob("EN*.attempt-*.response.json")), 9),
        "max_5gram_overlap": max((r["fivegram_overlap"] for r in rows if r["present"]), default=0.0),
    }
    (RAW / "quality_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
