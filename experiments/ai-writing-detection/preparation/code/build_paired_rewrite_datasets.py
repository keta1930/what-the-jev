"""Build matched human / AI-rewritten article datasets after both runs finish.

Copy this script into experiments/ai-writing-detection/preparation/code/ before use.
"""

import csv
import hashlib
import json
from pathlib import Path


EXPERIMENT = Path(__file__).resolve().parents[2]
PREPARATION = EXPERIMENT / "preparation"
DATA = EXPERIMENT / "data"


def text_sha(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def main():
    rows = list(csv.DictReader((PREPARATION / "source_manifest.csv").open(encoding="utf-8-sig", newline="")))
    if len(rows) != 200:
        raise ValueError(f"Expected 200 sources, got {len(rows)}")

    manifest_rows = []
    for language in ("zh", "en"):
        sources = [row for row in rows if row["language"] == language]
        if len(sources) != 100:
            raise ValueError(f"Expected 100 {language} sources, got {len(sources)}")
        existing = json.loads((DATA / f"dataset.article-human.{language}.json").read_text(encoding="utf-8"))
        human_by_source = {sample["metadata"]["source_id"]: sample for sample in existing["samples"]}
        if len(human_by_source) != 100:
            raise ValueError(f"Unexpected human dataset size for {language}")

        paired = []
        for row in sources:
            source_id = row["id"]
            human = human_by_source[source_id]
            original = (PREPARATION / row["text_path"]).read_text(encoding="utf-8-sig").strip()
            if human["input"]["state"] != original:
                raise ValueError(f"Human text changed: {source_id}")
            if text_sha(original) != row["sha256"]:
                raise ValueError(f"Source hash mismatch: {source_id}")

            rewrite_path = PREPARATION / "clean" / "ai_rewritten" / language / f"{source_id}.txt"
            metadata_path = PREPARATION / "raw" / "rewrites" / language / f"{source_id}.json"
            rewrite = rewrite_path.read_text(encoding="utf-8-sig").strip()
            meta = json.loads(metadata_path.read_text(encoding="utf-8"))
            if meta["source_id"] != source_id or meta["language"] != language:
                raise ValueError(f"Rewrite metadata mismatch: {source_id}")
            if meta["source_sha256"] != row["sha256"] or meta["output_sha256"] != text_sha(rewrite):
                raise ValueError(f"Rewrite hash mismatch: {source_id}")
            flags = meta["quality_checks"].get("flags", [])
            approved_exception = bool(meta.get("approved_exception") or meta.get("accepted_with_exception"))
            if flags and not approved_exception:
                raise ValueError(f"Unapproved rewrite quality flag: {source_id}: {flags}")
            if not rewrite or rewrite == original:
                raise ValueError(f"Empty or unchanged rewrite: {source_id}")
            paired.append(human)
            paired.append({
                "id": f"{source_id}-ai-rewritten-article",
                "input": {
                    "state": rewrite,
                    "questions": human["input"]["questions"],
                },
                "reference": {"ai_authorship": True},
                "metadata": {
                    "source_id": source_id,
                    "language": language,
                    "condition": "ai_rewritten",
                    "unit": "article",
                    "generation_model": meta["model"],
                },
            })
            manifest_rows.append({
                "id": source_id,
                "language": language,
                "model": meta["model"],
                "source_sha256": meta["source_sha256"],
                "output_sha256": meta["output_sha256"],
                "text_path": rewrite_path.relative_to(PREPARATION).as_posix(),
                "metadata_path": metadata_path.relative_to(PREPARATION).as_posix(),
                "prompt_tokens": meta["usage"].get("prompt_tokens", ""),
                "completion_tokens": meta["usage"].get("completion_tokens", ""),
                "cost_usd": meta.get("cost_usd", ""),
                "finish_reason": meta.get("finish_reason", ""),
                "quality_flags": "|".join(flags),
                "approved_exception": approved_exception,
            })

        out = DATA / f"dataset.article-human-rewritten.{language}.json"
        out.write_text(json.dumps({"schema_version": 1, "samples": paired}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(out, len(paired))

    manifest_path = PREPARATION / "rewrite_manifest.csv"
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(manifest_rows[0]))
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(manifest_path, len(manifest_rows))


if __name__ == "__main__":
    main()
