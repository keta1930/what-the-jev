"""Build three-block human/AI-rewritten datasets for block-level Jev evaluation."""

import json
import re
from pathlib import Path


EXPERIMENT = Path(__file__).resolve().parents[2]
PREPARATION = EXPERIMENT / "preparation"
DATA = EXPERIMENT / "data"


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def measure(text: str, language: str) -> int:
    if language == "zh":
        return len(re.sub(r"\s+", "", text))
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def balanced_blocks(text: str, language: str) -> tuple[list[str], tuple[int, int], list[int]]:
    parts = paragraphs(text)
    if len(parts) < 3:
        raise ValueError("Need at least three paragraphs")
    best = None
    minimum = 350 if language == "zh" else 250
    for i in range(1, len(parts) - 1):
        for j in range(i + 1, len(parts)):
            blocks = ["\n\n".join(parts[:i]), "\n\n".join(parts[i:j]), "\n\n".join(parts[j:])]
            lengths = [measure(block, language) for block in blocks]
            shortfalls = [max(0, minimum - value) for value in lengths]
            score = (
                sum(value > 0 for value in shortfalls),
                sum(shortfalls),
                max(lengths) - min(lengths),
                sum((x - sum(lengths) / 3) ** 2 for x in lengths),
            )
            candidate = (score, i, j, blocks, lengths)
            if best is None or candidate[0] < best[0]:
                best = candidate
    _, i, j, blocks, lengths = best
    return blocks, (i, j), lengths


def main() -> None:
    manifest = []
    for language in ("zh", "en"):
        human_data = json.loads((DATA / f"dataset.block-human.{language}.json").read_text(encoding="utf-8"))
        human_samples = human_data["samples"]
        if len(human_samples) != 300:
            raise ValueError(f"Expected 300 human blocks for {language}")
        by_source: dict[str, list[dict]] = {}
        for sample in human_samples:
            by_source.setdefault(sample["metadata"]["source_id"], []).append(sample)
        if len(by_source) != 100:
            raise ValueError(f"Expected 100 human sources for {language}")

        samples = list(human_samples)
        for source_id in sorted(by_source):
            human = sorted(by_source[source_id], key=lambda item: item["metadata"]["block_index"])
            rewrite_path = PREPARATION / "clean" / "ai_rewritten" / language / f"{source_id}.txt"
            rewrite = rewrite_path.read_text(encoding="utf-8-sig").strip()
            blocks, cuts, lengths = balanced_blocks(rewrite, language)
            for index, block in enumerate(blocks, 1):
                template = human[index - 1]
                samples.append({
                    "id": f"{source_id}-ai-rewritten-block-{index}",
                    "input": {
                        "state": block,
                        "questions": template["input"]["questions"],
                    },
                    "reference": {"ai_authorship": True},
                    "metadata": {
                        "source_id": source_id,
                        "language": language,
                        "condition": "ai_rewritten",
                        "unit": "block",
                        "block_index": index,
                    },
                })
            manifest.append({
                "source_id": source_id,
                "language": language,
                "paragraph_cuts": list(cuts),
                "block_lengths": lengths,
                "minimum_block_length": min(lengths),
            })

        ids = [sample["id"] for sample in samples]
        if len(samples) != 600 or len(ids) != len(set(ids)):
            raise ValueError(f"Invalid block dataset for {language}")
        out = DATA / f"dataset.block-human-rewritten.{language}.json"
        out.write_text(json.dumps({"schema_version": 1, "samples": samples}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(out, len(samples))

    report = PREPARATION / "rewrite_block_manifest.json"
    report.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report, len(manifest))


if __name__ == "__main__":
    main()
