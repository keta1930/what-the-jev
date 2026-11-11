#!/usr/bin/env python3
"""Build sentence-labelled mixtures using monotonic many-to-many alignment units.

Unlike naive one-to-one sentence replacement, an alignment unit can map one or
two human sentences to one or two AI sentences (with a limited 1:3/3:1 repair).
Selecting a unit replaces the whole semantic unit, preventing duplicated or
omitted content when the rewrite merged or split sentence boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

from build_gpt4o_sentence_mixed import (
    Sentence,
    english_tokens,
    load_article_ids,
    pair_similarity,
    sentence_units,
    sha,
    split_sentences,
    stable_rank,
    write_json,
    zh_normalized,
)


MATCH_OPERATIONS = ((1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1))


def joined(sentences: list[Sentence], indices: list[int], language: str) -> str:
    separator = "" if language == "zh" else " "
    return separator.join(sentences[index].text for index in indices)


def align_units(human: list[Sentence], ai: list[Sentence], language: str) -> list[dict]:
    n, m = len(human), len(ai)
    dp = [[float("-inf")] * (m + 1) for _ in range(n + 1)]
    back: list[list[tuple[int, int, float] | None]] = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    gap = 0.065
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            candidates: list[tuple[float, tuple[int, int, float]]] = []
            if i:
                candidates.append((dp[i - 1][j] - gap, (1, 0, 0.0)))
            if j:
                candidates.append((dp[i][j - 1] - gap, (0, 1, 0.0)))
            for human_count, ai_count in MATCH_OPERATIONS:
                if i < human_count or j < ai_count:
                    continue
                human_indices = list(range(i - human_count, i))
                ai_indices = list(range(j - ai_count, j))
                score = pair_similarity(joined(human, human_indices, language), joined(ai, ai_indices, language), language)
                human_position = ((i - human_count) + (i - 1)) / 2 / max(1, n - 1)
                ai_position = ((j - ai_count) + (j - 1)) / 2 / max(1, m - 1)
                complexity_penalty = 0.022 * (human_count + ai_count - 2)
                value = (
                    dp[i - human_count][j - ai_count]
                    + score
                    - 0.225
                    - complexity_penalty
                    - 0.16 * abs(human_position - ai_position)
                )
                candidates.append((value, (human_count, ai_count, score)))
            dp[i][j], back[i][j] = max(
                candidates,
                key=lambda item: (
                    item[0],
                    item[1][0] > 0 and item[1][1] > 0,
                    -(item[1][0] + item[1][1]),
                ),
            )

    reversed_units: list[dict] = []
    i, j = n, m
    while i or j:
        operation = back[i][j]
        if operation is None:
            raise RuntimeError(f"Broken alignment at {i}, {j}")
        human_count, ai_count, score = operation
        human_indices = list(range(i - human_count, i)) if human_count else []
        ai_indices = list(range(j - ai_count, j)) if ai_count else []
        reversed_units.append(
            {
                "human_indices": human_indices,
                "ai_indices": ai_indices,
                "alignment_score": score if human_count and ai_count else None,
            }
        )
        i -= human_count
        j -= ai_count
    units = list(reversed(reversed_units))
    if [index for unit in units for index in unit["human_indices"]] != list(range(n)):
        raise RuntimeError("Human alignment partition is incomplete")
    if [index for unit in units for index in unit["ai_indices"]] != list(range(m)):
        raise RuntimeError("AI alignment partition is incomplete")
    return units


def unit_is_eligible(unit: dict, human: list[Sentence], ai: list[Sentence], language: str) -> bool:
    human_indices = unit["human_indices"]
    ai_indices = unit["ai_indices"]
    if not human_indices or not ai_indices:
        return False
    threshold = 0.27 if language == "zh" else 0.24
    if unit["alignment_score"] < threshold:
        return False
    human_text = joined(human, human_indices, language)
    ai_text = joined(ai, ai_indices, language)
    human_length = sentence_units(human_text, language)
    ai_length = sentence_units(ai_text, language)
    if min(human_length, ai_length) < (6 if language == "zh" else 4):
        return False
    if not 0.40 <= ai_length / human_length <= 2.50:
        return False
    human_normalized = zh_normalized(human_text) if language == "zh" else "".join(english_tokens(human_text))
    ai_normalized = zh_normalized(ai_text) if language == "zh" else "".join(english_tokens(ai_text))
    return human_normalized != ai_normalized


def unit_position_group(unit: dict, total_human: int) -> int:
    indices = unit["human_indices"]
    center = sum(indices) / len(indices)
    return min(2, int(center * 3 / max(1, total_human)))


def choose_group_units(
    source_id: str,
    language: str,
    position: int,
    candidates: list[int],
    units: list[dict],
    group_human_count: int,
) -> set[int]:
    ordered = sorted(
        candidates,
        key=lambda index: stable_rank("jev-sentence-unit-mix-v1", language, source_id, position, index),
    )
    # State maps (removed human sentences, inserted AI sentences) to unit IDs.
    states: dict[tuple[int, int], tuple[int, ...]] = {(0, 0): ()}
    for unit_index in ordered:
        human_count = len(units[unit_index]["human_indices"])
        ai_count = len(units[unit_index]["ai_indices"])
        additions = {}
        for (removed, inserted), chosen in list(states.items()):
            key = (removed + human_count, inserted + ai_count)
            candidate = chosen + (unit_index,)
            if key not in states and key not in additions:
                additions[key] = candidate
        states.update(additions)
    scored = []
    for (removed, inserted), chosen in states.items():
        if not chosen or group_human_count - removed + inserted <= 0:
            continue
        ratio = inserted / (group_human_count - removed + inserted)
        mean_score = statistics.mean(units[index]["alignment_score"] for index in chosen)
        scored.append(
            (
                abs(ratio - 1 / 3),
                abs(removed - group_human_count / 3) / max(1, group_human_count),
                -mean_score,
                stable_rank("jev-sentence-unit-mix-v1", source_id, language, position, *chosen),
                chosen,
            )
        )
    if not scored:
        raise ValueError(f"position group {position + 1} has no eligible alignment units")
    return set(min(scored)[-1])


def select_units(source_id: str, language: str, units: list[dict], human: list[Sentence], ai: list[Sentence]) -> set[int]:
    eligible = [index for index, unit in enumerate(units) if unit_is_eligible(unit, human, ai, language)]
    selected: set[int] = set()
    group_human_counts = [sum((index * 3) // max(1, len(human)) == group for index in range(len(human))) for group in range(3)]
    for group in range(3):
        candidates = [index for index in eligible if unit_position_group(units[index], len(human)) == group]
        selected.update(
            choose_group_units(source_id, language, group, candidates, units, group_human_counts[group])
        )
    return selected


def paragraph_for_ai_sentence(unit: dict, human: list[Sentence], ai_offset: int) -> int:
    human_indices = unit["human_indices"]
    ai_count = len(unit["ai_indices"])
    mapped = min(len(human_indices) - 1, math.floor(ai_offset * len(human_indices) / max(1, ai_count)))
    return human[human_indices[mapped]].paragraph_index


def assemble(source_id: str, language: str, human_text: str, ai_text: str) -> tuple[str, dict]:
    human = split_sentences(human_text, language)
    ai = split_sentences(ai_text, language)
    units = align_units(human, ai, language)
    selected_units = select_units(source_id, language, units, human, ai)
    segments = []
    output_index = 0
    for unit_index, unit in enumerate(units, 1):
        human_indices = unit["human_indices"]
        ai_indices = unit["ai_indices"]
        if unit_index - 1 in selected_units:
            for ai_offset, ai_index in enumerate(ai_indices):
                output_index += 1
                text = ai[ai_index].text
                segments.append(
                    {
                        "sentence_index": output_index,
                        "paragraph_index": paragraph_for_ai_sentence(unit, human, ai_offset),
                        "origin": "ai",
                        "text": text,
                        "output_sha256": sha(text),
                        "alignment_unit_index": unit_index,
                        "alignment_score": round(unit["alignment_score"], 6),
                        "human_sentence_indices": [index + 1 for index in human_indices],
                        "human_sha256": [sha(human[index].text) for index in human_indices],
                        "source_ai_sentence_index": ai_index + 1,
                        "source_ai_sha256": sha(text),
                        "ai_unit_sentence_indices": [index + 1 for index in ai_indices],
                    }
                )
        else:
            for human_index in human_indices:
                output_index += 1
                text = human[human_index].text
                segments.append(
                    {
                        "sentence_index": output_index,
                        "paragraph_index": human[human_index].paragraph_index,
                        "origin": "human",
                        "text": text,
                        "output_sha256": sha(text),
                        "alignment_unit_index": unit_index,
                        "alignment_score": None,
                        "source_human_sentence_index": human_index + 1,
                        "source_human_sha256": sha(text),
                        "ai_unit_sentence_indices": [],
                    }
                )

    paragraphs: dict[int, list[str]] = {}
    for segment in segments:
        paragraphs.setdefault(segment["paragraph_index"], []).append(segment["text"])
    separator = "" if language == "zh" else " "
    mixed = "\n\n".join(separator.join(paragraphs[index]) for index in sorted(paragraphs))
    ai_segments = [segment for segment in segments if segment["origin"] == "ai"]
    scores = [segment["alignment_score"] for segment in ai_segments]
    metadata = {
        "source_id": source_id,
        "language": language,
        "condition": "sentence_unit_mixed_gpt4o_mini_33pct",
        "generator_model": "openai/gpt-4o-mini-2024-07-18",
        "human_article_sha256": sha(human_text),
        "ai_article_sha256": sha(ai_text),
        "mixed_article_sha256": sha(mixed),
        "human_source_sentence_count": len(human),
        "ai_source_sentence_count": len(ai),
        "alignment_unit_count": len(units),
        "selected_alignment_unit_count": len(selected_units),
        "mixed_sentence_count": len(segments),
        "selected_ai_sentence_count": len(ai_segments),
        "actual_ai_sentence_ratio": round(len(ai_segments) / len(segments), 6),
        "selected_alignment_score_min": round(min(scores), 6),
        "selected_alignment_score_median": round(statistics.median(scores), 6),
        "selected_alignment_score_max": round(max(scores), 6),
        "segments": segments,
    }
    return mixed, metadata


def build_language(root: Path, output: Path, language: str) -> dict:
    human_dir = root / "preparation" / "clean" / "human" / language
    ai_dir = root / "preparation" / "clean" / "ai_rewritten" / language
    ids = load_article_ids(human_dir, language)
    if load_article_ids(ai_dir, language) != ids:
        raise SystemExit(f"{language}: AI IDs differ")
    target = output / language
    metadata_dir = target / "metadata"
    target.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    failures = []
    records = []
    sentence_rows = []
    for source_id in ids:
        human_text = (human_dir / f"{source_id}.txt").read_text(encoding="utf-8-sig").strip()
        ai_text = (ai_dir / f"{source_id}.txt").read_text(encoding="utf-8-sig").strip()
        try:
            mixed, metadata = assemble(source_id, language, human_text, ai_text)
        except Exception as exc:
            failures.append({"source_id": source_id, "error": f"{type(exc).__name__}: {exc}"})
            continue
        (target / f"{source_id}.txt").write_text(mixed + "\n", encoding="utf-8")
        write_json(metadata_dir / f"{source_id}.json", metadata)
        records.append(metadata)
        for segment in metadata["segments"]:
            sentence_rows.append(
                {
                    "id": f"{source_id}-sentence-{segment['sentence_index']:03d}",
                    "source_id": source_id,
                    "language": language,
                    "condition": metadata["condition"],
                    "generator_model": metadata["generator_model"],
                    **segment,
                }
            )
    with (target / "sentences.jsonl").open("w", encoding="utf-8") as stream:
        for row in sentence_rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    hashes: dict[str, list[str]] = {}
    for record in records:
        hashes.setdefault(record["mixed_article_sha256"], []).append(record["source_id"])
    duplicates = [group for group in hashes.values() if len(group) > 1]
    ratios = [record["actual_ai_sentence_ratio"] for record in records]
    audit = {
        "language": language,
        "expected_articles": 100,
        "completed_articles": len(records),
        "failed_articles": failures,
        "sentence_rows": len(sentence_rows),
        "ai_sentences": sum(record["selected_ai_sentence_count"] for record in records),
        "human_sentences": sum(record["mixed_sentence_count"] - record["selected_ai_sentence_count"] for record in records),
        "ai_ratio_min": min(ratios) if ratios else None,
        "ai_ratio_median": statistics.median(ratios) if ratios else None,
        "ai_ratio_max": max(ratios) if ratios else None,
        "minimum_selected_alignment_score": min(record["selected_alignment_score_min"] for record in records) if records else None,
        "duplicate_mixed_hash_groups": duplicates,
        "audit_failures": ([f"{len(failures)} articles failed construction"] if failures else [])
        + ([f"duplicate mixed hashes: {duplicates}"] if duplicates else []),
    }
    write_json(target / "audit_summary.json", audit)
    return audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    summaries = [build_language(args.experiment_root, args.output, language) for language in ("zh", "en")]
    overall = {
        "condition": "sentence_unit_mixed_gpt4o_mini_33pct",
        "generator_model": "openai/gpt-4o-mini-2024-07-18",
        "mixing_rule": "Deterministic selection of monotonic many-to-many semantic alignment units targeting one-third AI output sentences in each positional third",
        "languages": summaries,
        "jev_called": False,
        "external_api_called": False,
    }
    write_json(args.output / "BUILD_SUMMARY.json", overall)
    for summary in summaries:
        print(json.dumps(summary, ensure_ascii=False))
    if any(summary["audit_failures"] for summary in summaries):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
