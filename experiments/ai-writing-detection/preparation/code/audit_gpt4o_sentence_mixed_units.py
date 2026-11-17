#!/usr/bin/env python3
"""Independent provenance audit for the GPT-4o-mini sentence-unit corpus.

This script does not call any model or external API.  It validates the built
corpus against the frozen human and GPT-4o-mini source files.
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path

from build_gpt4o_sentence_mixed import english_tokens, pair_similarity, sha, split_sentences, zh_normalized


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(text: str, language: str) -> str:
    if language == "zh":
        return zh_normalized(text)
    return "".join(english_tokens(text))


def reconstruct(segments: list[dict], language: str) -> str:
    paragraphs: dict[int, list[str]] = defaultdict(list)
    for segment in segments:
        paragraphs[int(segment["paragraph_index"])].append(segment["text"])
    separator = "" if language == "zh" else " "
    return "\n\n".join(separator.join(paragraphs[index]) for index in sorted(paragraphs))


def audit_article(root: Path, output: Path, language: str, source_id: str) -> tuple[dict, list[str], list[dict]]:
    failures: list[str] = []
    diagnostics: list[dict] = []
    human_text = (root / "preparation" / "clean" / "human" / language / f"{source_id}.txt").read_text(
        encoding="utf-8-sig"
    ).strip()
    ai_text = (root / "preparation" / "clean" / "ai_rewritten" / language / f"{source_id}.txt").read_text(
        encoding="utf-8-sig"
    ).strip()
    mixed_text = (output / language / f"{source_id}.txt").read_text(encoding="utf-8-sig").strip()
    metadata = load_json(output / language / "metadata" / f"{source_id}.json")
    human = split_sentences(human_text, language)
    ai = split_sentences(ai_text, language)
    segments = metadata.get("segments", [])

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    require(metadata.get("source_id") == source_id, "metadata source_id mismatch")
    require(metadata.get("language") == language, "metadata language mismatch")
    require(metadata.get("condition") == "sentence_unit_mixed_gpt4o_mini_33pct", "condition mismatch")
    require(metadata.get("generator_model") == "openai/gpt-4o-mini-2024-07-18", "model mismatch")
    require(metadata.get("human_article_sha256") == sha(human_text), "human article hash mismatch")
    require(metadata.get("ai_article_sha256") == sha(ai_text), "AI article hash mismatch")
    require(metadata.get("mixed_article_sha256") == sha(mixed_text), "mixed article hash mismatch")
    require(metadata.get("human_source_sentence_count") == len(human), "human sentence count mismatch")
    require(metadata.get("ai_source_sentence_count") == len(ai), "AI sentence count mismatch")
    require(metadata.get("mixed_sentence_count") == len(segments), "mixed sentence count mismatch")
    require(reconstruct(segments, language) == mixed_text, "segments do not reconstruct mixed article")

    unit_groups: dict[int, list[dict]] = defaultdict(list)
    for expected_index, segment in enumerate(segments, 1):
        require(segment.get("sentence_index") == expected_index, f"output sentence index {expected_index} mismatch")
        require(segment.get("origin") in {"human", "ai"}, f"invalid origin at output sentence {expected_index}")
        require(segment.get("output_sha256") == sha(segment.get("text", "")), f"output hash mismatch at sentence {expected_index}")
        unit_groups[int(segment["alignment_unit_index"])].append(segment)

    covered_human: list[int] = []
    selected_ai_indices: list[int] = []
    selected_unit_count = 0
    selected_scores: list[float] = []
    positional_groups: set[int] = set()
    exact_cross_origin_duplicates = 0

    for unit_index in sorted(unit_groups):
        group = unit_groups[unit_index]
        origins = {item["origin"] for item in group}
        require(len(origins) == 1, f"alignment unit {unit_index} mixes origins")
        if origins == {"human"}:
            for item in group:
                index = int(item["source_human_sentence_index"])
                covered_human.append(index)
                require(1 <= index <= len(human), f"human index out of range in unit {unit_index}")
                if 1 <= index <= len(human):
                    require(item["text"] == human[index - 1].text, f"human text mismatch in unit {unit_index}")
                    require(item["source_human_sha256"] == sha(human[index - 1].text), f"human source hash mismatch in unit {unit_index}")
                require(item.get("ai_unit_sentence_indices") == [], f"human segment carries AI indices in unit {unit_index}")
            continue

        selected_unit_count += 1
        first = group[0]
        human_indices = [int(index) for index in first.get("human_sentence_indices", [])]
        ai_indices = [int(index) for index in first.get("ai_unit_sentence_indices", [])]
        require(bool(human_indices), f"selected unit {unit_index} has no replaced human span")
        require(bool(ai_indices), f"selected unit {unit_index} has no AI span")
        require(all(item.get("human_sentence_indices") == human_indices for item in group), f"selected unit {unit_index} has inconsistent human span")
        require(all(item.get("ai_unit_sentence_indices") == ai_indices for item in group), f"selected unit {unit_index} has inconsistent AI span")
        require(len(group) == len(ai_indices), f"selected unit {unit_index} AI output count mismatch")
        covered_human.extend(human_indices)
        selected_ai_indices.extend(ai_indices)
        score = float(first["alignment_score"])
        # The builder stores score statistics per emitted AI sentence, so a
        # 1-to-2 unit contributes the same alignment score twice.
        selected_scores.extend([score] * len(group))
        require(all(float(item["alignment_score"]) == score for item in group), f"selected unit {unit_index} has inconsistent score")

        expected_human_hashes = [sha(human[index - 1].text) for index in human_indices if 1 <= index <= len(human)]
        require(first.get("human_sha256") == expected_human_hashes, f"selected unit {unit_index} human hashes mismatch")
        for item, ai_index in zip(group, ai_indices):
            require(1 <= ai_index <= len(ai), f"AI index out of range in unit {unit_index}")
            if 1 <= ai_index <= len(ai):
                require(item["text"] == ai[ai_index - 1].text, f"AI text mismatch in unit {unit_index}")
                require(item["source_ai_sha256"] == sha(ai[ai_index - 1].text), f"AI source hash mismatch in unit {unit_index}")
                require(item["source_ai_sentence_index"] == ai_index, f"AI source index mismatch in unit {unit_index}")

        human_unit = " ".join(human[index - 1].text for index in human_indices if 1 <= index <= len(human))
        ai_unit = " ".join(item["text"] for item in group)
        require(normalized(human_unit, language) != normalized(ai_unit, language), f"selected unit {unit_index} is an exact normalized copy")
        for index in human_indices:
            positional_groups.add(min(2, ((index - 1) * 3) // max(1, len(human))))

        # Diagnostic only: compare the selected AI unit with nearby, retained human
        # sentences.  High values may indicate a rewrite that crosses unit borders.
        retained_neighbors = []
        for neighbor in range(max(1, min(human_indices) - 2), min(len(human), max(human_indices) + 2) + 1):
            if neighbor not in human_indices:
                retained_neighbors.append(neighbor)
                similarity = pair_similarity(human[neighbor - 1].text, ai_unit, language)
                if normalized(human[neighbor - 1].text, language) == normalized(ai_unit, language):
                    exact_cross_origin_duplicates += 1
                if similarity >= 0.72:
                    diagnostics.append(
                        {
                            "source_id": source_id,
                            "alignment_unit_index": unit_index,
                            "retained_human_sentence_index": neighbor,
                            "similarity": round(similarity, 6),
                            "ai_text": ai_unit,
                            "human_text": human[neighbor - 1].text,
                        }
                    )

    require(sorted(covered_human) == list(range(1, len(human) + 1)), "human source coverage is not exactly once")
    require(len(covered_human) == len(set(covered_human)), "human source coverage contains duplicates")
    require(len(selected_ai_indices) == len(set(selected_ai_indices)), "selected AI source indices contain duplicates")
    require(metadata.get("selected_alignment_unit_count") == selected_unit_count, "selected unit count mismatch")
    ai_count = sum(item["origin"] == "ai" for item in segments)
    require(metadata.get("selected_ai_sentence_count") == ai_count, "selected AI sentence count mismatch")
    ratio = ai_count / len(segments) if segments else 0.0
    require(abs(float(metadata.get("actual_ai_sentence_ratio", -1)) - round(ratio, 6)) < 1e-9, "AI ratio mismatch")
    require(0.25 <= ratio <= 0.40, f"AI ratio outside allowed range: {ratio:.6f}")
    require(positional_groups == {0, 1, 2}, f"AI replacements do not cover all positional thirds: {sorted(positional_groups)}")
    require(exact_cross_origin_duplicates == 0, "exact AI/human duplicate found across neighboring units")
    if selected_scores:
        require(abs(metadata["selected_alignment_score_min"] - round(min(selected_scores), 6)) < 1e-9, "minimum score mismatch")
        require(abs(metadata["selected_alignment_score_median"] - round(statistics.median(selected_scores), 6)) < 1e-9, "median score mismatch")
        require(abs(metadata["selected_alignment_score_max"] - round(max(selected_scores), 6)) < 1e-9, "maximum score mismatch")

    return metadata, failures, diagnostics


def audit_language(root: Path, output: Path, language: str) -> dict:
    prefix = "ZH" if language == "zh" else "EN"
    ids = [f"{prefix}{index:03d}" for index in range(1, 101)]
    failures: dict[str, list[str]] = {}
    diagnostics: list[dict] = []
    records: list[dict] = []
    mixed_hashes: dict[str, list[str]] = defaultdict(list)
    all_rows: list[dict] = []
    sentence_path = output / language / "sentences.jsonl"
    with sentence_path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                all_rows.append(json.loads(line))

    expected_rows: list[dict] = []
    for source_id in ids:
        try:
            metadata, article_failures, article_diagnostics = audit_article(root, output, language, source_id)
        except Exception as exc:  # keep the audit report complete
            failures[source_id] = [f"{type(exc).__name__}: {exc}"]
            continue
        records.append(metadata)
        diagnostics.extend(article_diagnostics)
        if article_failures:
            failures[source_id] = article_failures
        mixed_hashes[metadata["mixed_article_sha256"]].append(source_id)
        for segment in metadata["segments"]:
            expected_rows.append(
                {
                    "id": f"{source_id}-sentence-{segment['sentence_index']:03d}",
                    "source_id": source_id,
                    "language": language,
                    "condition": metadata["condition"],
                    "generator_model": metadata["generator_model"],
                    **segment,
                }
            )

    if all_rows != expected_rows:
        failures.setdefault("_language", []).append("sentences.jsonl does not exactly match article metadata")
    duplicate_groups = [group for group in mixed_hashes.values() if len(group) > 1]
    if duplicate_groups:
        failures.setdefault("_language", []).append(f"duplicate mixed article hashes: {duplicate_groups}")
    diagnostics.sort(key=lambda item: item["similarity"], reverse=True)
    return {
        "language": language,
        "expected_articles": 100,
        "audited_articles": len(records),
        "sentence_rows": len(expected_rows),
        "ai_sentences": sum(record["selected_ai_sentence_count"] for record in records),
        "human_sentences": sum(record["mixed_sentence_count"] - record["selected_ai_sentence_count"] for record in records),
        "failures": failures,
        "duplicate_mixed_hash_groups": duplicate_groups,
        "high_neighbor_similarity_diagnostics_count": len(diagnostics),
        "top_neighbor_similarity_diagnostics": diagnostics[:20],
        "passed": not failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reports = [audit_language(args.experiment_root, args.output, language) for language in ("zh", "en")]
    result = {
        "audit": "independent_sentence_unit_provenance_audit",
        "condition": "sentence_unit_mixed_gpt4o_mini_33pct",
        "jev_called": False,
        "external_api_called": False,
        "languages": reports,
        "passed": all(report["passed"] for report in reports),
    }
    (args.output / "INDEPENDENT_AUDIT.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
