#!/usr/bin/env python3
"""Build deterministic sentence-level human/GPT-4o-mini mixed essays.

This script is fully local. It never calls a model or JEV. It aligns the existing
human and GPT-4o-mini full-essay rewrites, replaces about one third of the
high-confidence aligned human sentences, and writes sentence-level provenance
metadata. The one-third ratio mirrors the original one-AI-block/two-human-block
design while avoiding false AI labels for unchanged model output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


WORD = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
ZH_CLEAN = re.compile(r"[\s\W_]+", re.UNICODE)
PARAGRAPH_BREAK = re.compile(r"\n\s*\n")
ZH_END = set("。！？!?")
CLOSERS = set('"”’」』》）)]')
EN_ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "rev", "st", "vs", "etc",
    "e.g", "i.e", "fig", "vol", "no", "jr", "sr", "hon", "gen",
    "col", "lt", "mt", "jan", "feb", "mar", "apr", "jun", "jul",
    "aug", "sep", "sept", "oct", "nov", "dec",
}
EN_STOP = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by",
    "for", "from", "had", "has", "have", "he", "her", "his", "i", "if",
    "in", "is", "it", "its", "me", "my", "not", "of", "on", "or", "our",
    "she", "so", "that", "the", "their", "them", "there", "they", "this",
    "to", "was", "we", "were", "which", "who", "with", "you", "your",
}


@dataclass(frozen=True)
class Sentence:
    text: str
    paragraph_index: int
    sentence_in_paragraph: int


def sha(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def stable_rank(*parts: object) -> str:
    return hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in PARAGRAPH_BREAK.split(text.strip()) if part.strip()]


def split_zh_paragraph(text: str) -> list[str]:
    result: list[str] = []
    start = 0
    index = 0
    while index < len(text):
        if text[index] in ZH_END:
            end = index + 1
            while end < len(text) and (text[end] in ZH_END or text[end] in CLOSERS):
                end += 1
            value = text[start:end].strip()
            if value:
                result.append(value)
            start = end
            index = end
        else:
            index += 1
    tail = text[start:].strip()
    if tail:
        result.append(tail)
    return result or ([text.strip()] if text.strip() else [])


def is_english_boundary(text: str, punctuation_index: int, after_closers: int) -> bool:
    char = text[punctuation_index]
    if char == ".":
        if punctuation_index > 0 and punctuation_index + 1 < len(text):
            if text[punctuation_index - 1].isdigit() and text[punctuation_index + 1].isdigit():
                return False
        prefix = text[: punctuation_index + 1]
        match = re.search(r"([A-Za-z](?:[A-Za-z.]*)?)\.$", prefix)
        if match:
            token = match.group(1).lower().rstrip(".")
            if token in EN_ABBREVIATIONS or len(token) == 1:
                return False
        if punctuation_index + 1 < len(text) and text[punctuation_index + 1] == ".":
            return False
    if after_closers >= len(text):
        return True
    if not text[after_closers].isspace():
        return False
    cursor = after_closers
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor >= len(text):
        return True
    while cursor < len(text) and text[cursor] in '"“‘([':
        cursor += 1
    return cursor >= len(text) or text[cursor].isupper() or text[cursor].isdigit()


def split_en_paragraph(text: str) -> list[str]:
    result: list[str] = []
    start = 0
    index = 0
    while index < len(text):
        if text[index] in ".!?":
            end = index + 1
            while end < len(text) and text[end] in CLOSERS:
                end += 1
            if is_english_boundary(text, index, end):
                value = text[start:end].strip()
                if value:
                    result.append(value)
                start = end
                while start < len(text) and text[start].isspace():
                    start += 1
                index = start
                continue
        index += 1
    tail = text[start:].strip()
    if tail:
        result.append(tail)
    return result or ([text.strip()] if text.strip() else [])


def split_sentences(text: str, language: str) -> list[Sentence]:
    result: list[Sentence] = []
    for paragraph_index, paragraph in enumerate(paragraphs(text), 1):
        pieces = split_zh_paragraph(paragraph) if language == "zh" else split_en_paragraph(paragraph)
        for sentence_index, piece in enumerate(pieces, 1):
            if piece.strip():
                result.append(Sentence(piece.strip(), paragraph_index, sentence_index))
    return result


def jaccard(left: set, right: set) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def length_similarity(left: int, right: int) -> float:
    if not left or not right:
        return 0.0
    return min(left, right) / max(left, right)


def zh_normalized(text: str) -> str:
    return ZH_CLEAN.sub("", text).lower()


def english_tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD.finditer(text)]


def pair_similarity(human: str, ai: str, language: str) -> float:
    if language == "zh":
        left = zh_normalized(human)
        right = zh_normalized(ai)
        if not left or not right:
            return 0.0
        sequence = SequenceMatcher(None, left, right, autojunk=False).ratio()
        left_bigrams = {left[i : i + 2] for i in range(max(0, len(left) - 1))}
        right_bigrams = {right[i : i + 2] for i in range(max(0, len(right) - 1))}
        digits_left = set(re.findall(r"\d+", left))
        digits_right = set(re.findall(r"\d+", right))
        anchors = jaccard(digits_left, digits_right) if digits_left or digits_right else 0.5
        return 0.45 * sequence + 0.30 * jaccard(left_bigrams, right_bigrams) + 0.20 * length_similarity(len(left), len(right)) + 0.05 * anchors

    left_tokens = english_tokens(human)
    right_tokens = english_tokens(ai)
    if not left_tokens or not right_tokens:
        return 0.0
    sequence = SequenceMatcher(None, left_tokens, right_tokens, autojunk=False).ratio()
    left_content = {token for token in left_tokens if token not in EN_STOP}
    right_content = {token for token in right_tokens if token not in EN_STOP}
    left_anchors = set(re.findall(r"\b(?:[A-Z][A-Za-z'-]+|\d+(?:\.\d+)?)\b", human))
    right_anchors = set(re.findall(r"\b(?:[A-Z][A-Za-z'-]+|\d+(?:\.\d+)?)\b", ai))
    anchors = jaccard(left_anchors, right_anchors) if left_anchors or right_anchors else 0.5
    return 0.45 * sequence + 0.30 * jaccard(left_content, right_content) + 0.20 * length_similarity(len(left_tokens), len(right_tokens)) + 0.05 * anchors


def align_sentences(human: list[Sentence], ai: list[Sentence], language: str) -> list[tuple[int, int, float]]:
    n, m = len(human), len(ai)
    scores = [[pair_similarity(human[i].text, ai[j].text, language) for j in range(m)] for i in range(n)]
    dp = [[float("-inf")] * (m + 1) for _ in range(n + 1)]
    back: list[list[str | None]] = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    gap = 0.055
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] - gap
        back[i][0] = "human_gap"
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] - gap
        back[0][j] = "ai_gap"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            human_position = (i - 1) / max(1, n - 1)
            ai_position = (j - 1) / max(1, m - 1)
            match_value = dp[i - 1][j - 1] + scores[i - 1][j - 1] - 0.23 - 0.18 * abs(human_position - ai_position)
            candidates = [
                (match_value, "match"),
                (dp[i - 1][j] - gap, "human_gap"),
                (dp[i][j - 1] - gap, "ai_gap"),
            ]
            dp[i][j], back[i][j] = max(candidates, key=lambda item: (item[0], item[1] == "match"))
    aligned: list[tuple[int, int, float]] = []
    i, j = n, m
    while i or j:
        action = back[i][j]
        if action == "match":
            aligned.append((i - 1, j - 1, scores[i - 1][j - 1]))
            i -= 1
            j -= 1
        elif action == "human_gap":
            i -= 1
        elif action == "ai_gap":
            j -= 1
        else:
            raise RuntimeError(f"Broken alignment at {i}, {j}")
    aligned.reverse()
    return aligned


def sentence_units(text: str, language: str) -> int:
    return len(zh_normalized(text)) if language == "zh" else len(english_tokens(text))


def eligible_pairs(
    human: list[Sentence], ai: list[Sentence], aligned: list[tuple[int, int, float]], language: str
) -> dict[int, tuple[int, float]]:
    threshold = 0.27 if language == "zh" else 0.24
    result: dict[int, tuple[int, float]] = {}
    for human_index, ai_index, score in aligned:
        human_text = human[human_index].text
        ai_text = ai[ai_index].text
        left = sentence_units(human_text, language)
        right = sentence_units(ai_text, language)
        if score < threshold or min(left, right) < (6 if language == "zh" else 4):
            continue
        ratio = right / left if left else 0.0
        if not 0.40 <= ratio <= 2.50:
            continue
        normalized_human = re.sub(r"\s+", "", human_text).lower()
        normalized_ai = re.sub(r"\s+", "", ai_text).lower()
        if normalized_human == normalized_ai:
            continue
        result[human_index] = (ai_index, score)
    return result


def position_group(index: int, total: int) -> int:
    return min(2, (index * 3) // max(1, total))


def select_ai_indices(source_id: str, language: str, total: int, eligible: dict[int, tuple[int, float]]) -> set[int]:
    target_total = round(total / 3)
    if len(eligible) < target_total:
        raise ValueError(f"article has {len(eligible)} eligible pairs but needs {target_total}")
    groups = [[index for index in range(total) if position_group(index, total) == group] for group in range(3)]
    ideal_targets = [len(group) * target_total / total for group in groups]
    targets = [math.floor(value) for value in ideal_targets]
    remaining = target_total - sum(targets)
    remainder_groups = list(range(3))
    remainder_groups.sort(
        key=lambda group: (
            -(ideal_targets[group] - targets[group]),
            stable_rank("jev-sentence-mixed-v1", language, source_id, "group", group),
        )
    )
    for group in remainder_groups[:remaining]:
        targets[group] += 1
    selected: set[int] = set()
    for group, indices in enumerate(groups):
        candidates = [index for index in indices if index in eligible]
        candidates.sort(key=lambda index: stable_rank("jev-sentence-mixed-v1", language, source_id, index))
        selected.update(candidates[: min(len(candidates), targets[group])])
    # A few essays do not have enough high-confidence one-to-one alignments in
    # one positional third. Keep the article-level one-third target without lowering
    # the confidence threshold by reallocating only the small positional deficit.
    while len(selected) < target_total:
        candidates = [index for index in eligible if index not in selected]
        if not candidates:
            raise ValueError(f"unable to fill article target {target_total}")
        group_counts = [sum(position_group(index, total) == group for index in selected) for group in range(3)]
        candidates.sort(
            key=lambda index: (
                group_counts[position_group(index, total)] / max(1, len(groups[position_group(index, total)])),
                stable_rank("jev-sentence-mixed-v1", language, source_id, "reallocated", index),
            )
        )
        selected.add(candidates[0])
    return selected


def assemble(
    source_id: str,
    language: str,
    human_text: str,
    ai_text: str,
) -> tuple[str, dict]:
    human = split_sentences(human_text, language)
    ai = split_sentences(ai_text, language)
    if len(human) < 6 or len(ai) < 6:
        raise ValueError(f"too few sentences: human={len(human)} ai={len(ai)}")
    aligned = align_sentences(human, ai, language)
    eligible = eligible_pairs(human, ai, aligned, language)
    selected = select_ai_indices(source_id, language, len(human), eligible)
    by_paragraph: dict[int, list[str]] = {}
    segments = []
    selected_scores = []
    for index, human_sentence in enumerate(human):
        origin = "human"
        output_text = human_sentence.text
        ai_index = None
        alignment_score = None
        if index in selected:
            ai_index, alignment_score = eligible[index]
            output_text = ai[ai_index].text
            origin = "ai"
            selected_scores.append(alignment_score)
        by_paragraph.setdefault(human_sentence.paragraph_index, []).append(output_text)
        segments.append(
            {
                "sentence_index": index + 1,
                "paragraph_index": human_sentence.paragraph_index,
                "sentence_in_paragraph": human_sentence.sentence_in_paragraph,
                "origin": origin,
                "text": output_text,
                "output_sha256": sha(output_text),
                "human_sentence_index": index + 1,
                "human_sha256": sha(human_sentence.text),
                "ai_sentence_index": None if ai_index is None else ai_index + 1,
                "ai_sha256": None if ai_index is None else sha(ai[ai_index].text),
                "alignment_score": None if alignment_score is None else round(alignment_score, 6),
                "position_group": ["beginning", "middle", "ending"][position_group(index, len(human))],
            }
        )
    separator = "" if language == "zh" else " "
    mixed = "\n\n".join(separator.join(by_paragraph[index]) for index in sorted(by_paragraph))
    metadata = {
        "source_id": source_id,
        "language": language,
        "condition": "sentence_mixed_gpt4o_mini_33pct",
        "generator_model": "openai/gpt-4o-mini-2024-07-18",
        "human_article_sha256": sha(human_text),
        "ai_article_sha256": sha(ai_text),
        "mixed_article_sha256": sha(mixed),
        "human_sentence_count": len(human),
        "ai_source_sentence_count": len(ai),
        "aligned_pair_count": len(aligned),
        "eligible_pair_count": len(eligible),
        "mixed_sentence_count": len(segments),
        "selected_ai_sentence_count": len(selected),
        "actual_ai_sentence_ratio": round(len(selected) / len(segments), 6),
        "selected_alignment_score_min": round(min(selected_scores), 6),
        "selected_alignment_score_median": round(statistics.median(selected_scores), 6),
        "selected_alignment_score_max": round(max(selected_scores), 6),
        "segments": segments,
    }
    return mixed, metadata


def load_article_ids(directory: Path, language: str) -> list[str]:
    prefix = "ZH" if language == "zh" else "EN"
    expected = [f"{prefix}{index:03d}" for index in range(1, 101)]
    actual = sorted(path.stem for path in directory.glob(f"{prefix}*.txt"))
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise SystemExit(f"{language}: source IDs mismatch missing={missing} extra={extra}")
    return expected


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    duplicate_hashes = {}
    for record in records:
        duplicate_hashes.setdefault(record["mixed_article_sha256"], []).append(record["source_id"])
    duplicates = [ids for ids in duplicate_hashes.values() if len(ids) > 1]
    ratios = [record["actual_ai_sentence_ratio"] for record in records]
    selected_scores = [record["selected_alignment_score_min"] for record in records]
    audit = {
        "language": language,
        "expected_articles": 100,
        "completed_articles": len(records),
        "failed_articles": failures,
        "sentence_rows": len(sentence_rows),
        "ai_sentences": sum(record["selected_ai_sentence_count"] for record in records),
        "human_sentences": sum(record["mixed_sentence_count"] - record["selected_ai_sentence_count"] for record in records),
        "ai_ratio_min": None if not ratios else min(ratios),
        "ai_ratio_median": None if not ratios else statistics.median(ratios),
        "ai_ratio_max": None if not ratios else max(ratios),
        "minimum_selected_alignment_score": None if not selected_scores else min(selected_scores),
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
        "condition": "sentence_mixed_gpt4o_mini_33pct",
        "generator_model": "openai/gpt-4o-mini-2024-07-18",
        "mixing_rule": "Deterministic one-third selection among high-confidence monotonic one-to-one sentence alignments, balanced across beginning/middle/ending thirds",
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
