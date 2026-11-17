"""Audit the Chinese full-essay rewrites without making API requests."""

import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(r"C:\Users\asus\Desktop\Jev文章AI检测实验\what-the-jev\experiments\ai-writing-detection")
PREP = ROOT / "preparation"
OUT = PREP / "raw" / "rewrites" / "zh"
TEXT_OUT = PREP / "clean" / "ai_rewritten" / "zh"
REPORT = PREP / "raw" / "rewrites" / "zh" / "quality_report.csv"
SIMP = "这们说书后过无与为学国体东长实写发里见进还听时问关头话电点节鸟鱼马车门开报语结经"
TRAD = "這們說書後過無與為學國體東長實寫發裡見進還聽時問關頭話電點節鳥魚馬車門開報語結經"


def grams(text, n=5):
    text = re.sub(r"\s+", "", text)
    return {text[i:i+n] for i in range(max(0, len(text)-n+1))}


def script_fraction(text):
    simplified = sum(text.count(char) for char in SIMP)
    traditional = sum(text.count(char) for char in TRAD)
    return simplified / (simplified + traditional) if simplified + traditional else None


def paragraphs(text):
    return len([x for x in re.split(r"\n\s*\n", text) if x.strip()])


def main():
    rows = [r for r in csv.DictReader((PREP / "source_manifest.csv").open(encoding="utf-8-sig", newline="")) if r["language"] == "zh"]
    report = []
    for row in rows:
        source_id = row["id"]
        source = (PREP / row["text_path"]).read_text(encoding="utf-8-sig").strip()
        path = TEXT_OUT / f"{source_id}.txt"
        record_path = OUT / f"{source_id}.json"
        response_path = OUT / f"{source_id}.response.json"
        if not path.exists() or not record_path.exists() or not response_path.exists():
            report.append({"source_id": source_id, "status": "missing", "flags": "missing_artifact"})
            continue
        output = path.read_text(encoding="utf-8").strip()
        record = json.loads(record_path.read_text(encoding="utf-8"))
        source_script = script_fraction(source)
        output_script = script_fraction(output)
        sg, og = grams(source), grams(output)
        overlap = len(sg & og) / len(og) if og else 0.0
        flags = list(record["quality_checks"]["flags"])
        if overlap > 0.5:
            flags.append("high_5gram_overlap")
        if source_script is not None and output_script is not None and abs(source_script - output_script) > 0.3:
            flags.append("simplified_traditional_shift")
        if hashlib.sha256(output.encode("utf-8")).hexdigest() != record["output_sha256"]:
            flags.append("output_hash_mismatch")
        if paragraphs(output) != record["output_paragraphs"]:
            flags.append("paragraph_count_mismatch")
        report.append({
            "source_id": source_id,
            "status": "present",
            "source_visible_characters": record["source_visible_characters"],
            "output_visible_characters": record["output_visible_characters"],
            "length_ratio": round(record["output_visible_characters"] / record["source_visible_characters"], 4),
            "source_paragraphs": record["source_paragraphs"],
            "output_paragraphs": record["output_paragraphs"],
            "fivegram_overlap": round(overlap, 4),
            "source_simplified_fraction": None if source_script is None else round(source_script, 4),
            "output_simplified_fraction": None if output_script is None else round(output_script, 4),
            "cost_usd": record["cost_usd"],
            "flags": ";".join(flags),
        })
    fields = ["source_id", "status", "source_visible_characters", "output_visible_characters", "length_ratio", "source_paragraphs", "output_paragraphs", "fivegram_overlap", "source_simplified_fraction", "output_simplified_fraction", "cost_usd", "flags"]
    with REPORT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report)
    print(f"present={sum(r['status'] == 'present' for r in report)} missing={sum(r['status'] == 'missing' for r in report)}")
    print(f"flagged={sum(bool(r['flags']) for r in report)} cost=${sum(float(r.get('cost_usd') or 0) for r in report):.6f}")
    print("report:", REPORT)
    for row in report:
        if row["flags"] and row["status"] == "present":
            print(row["source_id"], row["flags"], "ratio=", row["length_ratio"], "overlap=", row["fivegram_overlap"])


if __name__ == "__main__":
    main()
