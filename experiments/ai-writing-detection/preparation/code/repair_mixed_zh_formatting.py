"""Apply recorded whitespace-only paragraph repairs to selected Chinese AI blocks."""

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


EXPERIMENT = Path(r"C:\Users\asus\Desktop\Jev文章AI检测实验\what-the-jev\experiments\ai-writing-detection")
PREP = EXPERIMENT / "preparation"
DATASET = EXPERIMENT / "data" / "dataset.block-human.zh.json"
RAW = PREP / "raw" / "mixed" / "zh"
AI = PREP / "clean" / "mixed_ai_blocks" / "zh"
MIXED = PREP / "clean" / "mixed" / "zh"
TARGETS = ("ZH034", "ZH045", "ZH097")


def sha(value: str) -> str:
    return hashlib.sha256(value.strip().encode("utf-8")).hexdigest()


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def paragraphs(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", value) if part.strip()]


def atomic_json(path: Path, data) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def atomic_text(path: Path, value: str) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(value.strip() + "\n", encoding="utf-8")
    temp.replace(path)


def load_blocks():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    grouped = defaultdict(dict)
    for sample in data["samples"]:
        grouped[sample["metadata"]["source_id"]][int(sample["metadata"]["block_index"])] = sample["input"]["state"].strip()
    return {source_id: [items[index] for index in (1, 2, 3)] for source_id, items in grouped.items()}


def split_once(parts: list[str]) -> list[str]:
    choices = []
    for part_index, part in enumerate(parts):
        boundaries = [match.end() for match in re.finditer(r"[。！？；]", part) if 0 < match.end() < len(part)]
        if not boundaries:
            continue
        midpoint = len(part) / 2
        cut = min(boundaries, key=lambda value: abs(value - midpoint))
        choices.append((len(part), part_index, cut))
    if not choices:
        raise ValueError("No natural sentence boundary available for formatting repair")
    _, part_index, cut = max(choices)
    part = parts[part_index]
    return parts[:part_index] + [part[:cut].strip(), part[cut:].strip()] + parts[part_index + 1:]


def main():
    blocks_by_source = load_blocks()
    for source_id in TARGETS:
        record_path = RAW / f"{source_id}.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        ai_path = AI / f"{source_id}.txt"
        mixed_path = MIXED / f"{source_id}.txt"
        model_text = ai_path.read_text(encoding="utf-8-sig").strip()
        model_output_path = RAW / f"{source_id}.model-output.txt"
        if not model_output_path.exists():
            atomic_text(model_output_path, model_text)
        else:
            model_text = model_output_path.read_text(encoding="utf-8-sig").strip()
        target_count = int(record["quality_checks"]["source_paragraphs"])
        parts = paragraphs(model_text)
        while len(parts) < target_count:
            parts = split_once(parts)
        if len(parts) != target_count:
            raise ValueError(f"{source_id}: unable to reach target paragraph count")
        final_text = "\n\n".join(parts)
        if compact(final_text) != compact(model_text):
            raise ValueError(f"{source_id}: non-whitespace content changed")
        blocks = blocks_by_source[source_id]
        mixed_blocks = list(blocks)
        mixed_blocks[int(record["target_position"]) - 1] = final_text
        mixed_text = "\n\n".join(mixed_blocks)
        atomic_text(ai_path, final_text)
        atomic_text(mixed_path, mixed_text)
        flags = [flag for flag in record["quality_checks"]["flags"] if flag != "paragraph_count_changed"]
        record["model_output_sha256"] = sha(model_text)
        record["model_output_path"] = str(model_output_path.relative_to(PREP)).replace("\\", "/")
        record["formatting_only"] = True
        record["formatting_algorithm"] = "insert blank line after the nearest complete Chinese sentence boundary in the longest splittable paragraph until the source paragraph count is reached"
        record["model_paragraphs"] = len(paragraphs(model_text))
        record["final_paragraphs"] = len(paragraphs(final_text))
        record["ai_block_sha256"] = sha(final_text)
        record["mixed_sha256"] = sha(mixed_text)
        record["quality_checks"]["flags"] = flags
        record["quality_checks"]["output_paragraphs"] = len(paragraphs(final_text))
        record["approved_exception"] = bool(flags)
        atomic_json(record_path, record)
        print(source_id, record["model_paragraphs"], "->", record["final_paragraphs"], "flags", flags)


if __name__ == "__main__":
    main()
