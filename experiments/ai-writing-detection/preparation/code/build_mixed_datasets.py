"""Build Jev article and block datasets for one-AI-block mixed essays."""

import hashlib
import json
from pathlib import Path


EXPERIMENT = Path(__file__).resolve().parents[2]
PREPARATION = EXPERIMENT / "preparation"
DATA = EXPERIMENT / "data"


def assignment(language: str, source_ids: list[str]) -> dict[str, int]:
    ordered = sorted(
        source_ids,
        key=lambda source_id: hashlib.sha256(
            f"jev-mixed-v1|{language}|{source_id}".encode("utf-8")
        ).hexdigest(),
    )
    return {
        source_id: 1 if index < 34 else 2 if index < 67 else 3
        for index, source_id in enumerate(ordered)
    }


def main() -> None:
    for language in ("zh", "en"):
        human_articles = json.loads((DATA / f"dataset.article-human.{language}.json").read_text(encoding="utf-8"))["samples"]
        human_blocks = json.loads((DATA / f"dataset.block-human.{language}.json").read_text(encoding="utf-8"))["samples"]
        article_by_source = {sample["metadata"]["source_id"]: sample for sample in human_articles}
        blocks_by_source: dict[str, list[dict]] = {}
        for sample in human_blocks:
            blocks_by_source.setdefault(sample["metadata"]["source_id"], []).append(sample)
        positions = assignment(language, sorted(article_by_source))
        if {position: list(positions.values()).count(position) for position in (1, 2, 3)} != {1: 34, 2: 33, 3: 33}:
            raise ValueError("Position allocation mismatch")

        article_samples = []
        block_samples = []
        for source_id in sorted(article_by_source):
            target = positions[source_id]
            human_article = article_by_source[source_id]
            human = sorted(blocks_by_source[source_id], key=lambda item: item["metadata"]["block_index"])
            if len(human) != 3:
                raise ValueError(f"Expected three human blocks: {source_id}")
            ai_block_path = PREPARATION / "clean" / "mixed_ai_blocks" / language / f"{source_id}.txt"
            mixed_path = PREPARATION / "clean" / "mixed" / language / f"{source_id}.txt"
            ai_block = ai_block_path.read_text(encoding="utf-8-sig").strip()
            expected_blocks = [sample["input"]["state"].strip() for sample in human]
            expected_blocks[target - 1] = ai_block
            expected_mixed = "\n\n".join(expected_blocks)
            mixed = mixed_path.read_text(encoding="utf-8-sig").strip()
            if mixed != expected_mixed:
                raise ValueError(f"Mixed text does not match exact block replacement: {source_id}")

            common = {
                "source_id": source_id,
                "language": language,
                "condition": "mixed",
                "ai_block_index": target,
            }
            article_samples.append({
                "id": f"{source_id}-mixed-article",
                "input": {
                    "state": mixed,
                    "questions": human_article["input"]["questions"],
                },
                "reference": {"ai_authorship": True},
                "metadata": dict(common, unit="article"),
            })
            for index, block in enumerate(expected_blocks, 1):
                block_samples.append({
                    "id": f"{source_id}-mixed-block-{index}",
                    "input": {
                        "state": block,
                        "questions": human[index - 1]["input"]["questions"],
                    },
                    "reference": {"ai_authorship": index == target},
                    "metadata": dict(common, unit="block", block_index=index),
                })

        for unit, samples, expected in (("article", article_samples, 100), ("block", block_samples, 300)):
            ids = [sample["id"] for sample in samples]
            if len(samples) != expected or len(ids) != len(set(ids)):
                raise ValueError(f"Invalid {unit} mixed dataset for {language}")
            out = DATA / f"dataset.{unit}-mixed.{language}.json"
            out.write_text(json.dumps({"schema_version": 1, "samples": samples}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(out, len(samples))


if __name__ == "__main__":
    main()
