#!/usr/bin/env python3
"""Analyze paired single-sentence and three-sentence-context Jev results."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


THRESHOLD = 0.50


def safe_div(a: float, b: float) -> float | None:
    return a / b if b else None


def roc_auc(rows: list[dict], probability_key: str) -> float | None:
    ordered = sorted((row[probability_key], int(row["truth"])) for row in rows)
    positives = sum(label for _, label in ordered)
    negatives = len(ordered) - positives
    if not positives or not negatives:
        return None
    rank_sum = 0.0
    position = 1
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = (position + position + end - index - 1) / 2
        rank_sum += average_rank * sum(label for _, label in ordered[index:end])
        position += end - index
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def metrics(rows: list[dict], probability_key: str) -> dict:
    tp = sum(row["truth"] and row[probability_key] >= THRESHOLD for row in rows)
    fp = sum(not row["truth"] and row[probability_key] >= THRESHOLD for row in rows)
    tn = sum(not row["truth"] and row[probability_key] < THRESHOLD for row in rows)
    fn = sum(row["truth"] and row[probability_key] < THRESHOLD for row in rows)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    ai_probabilities = [row[probability_key] for row in rows if row["truth"]]
    human_probabilities = [row[probability_key] for row in rows if not row["truth"]]
    return {
        "n": len(rows),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "accuracy": safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe_div(2 * precision * recall, precision + recall)
        if precision is not None and recall is not None and precision + recall
        else None,
        "balanced_accuracy": (recall + specificity) / 2 if recall is not None and specificity is not None else None,
        "roc_auc": roc_auc(rows, probability_key),
        "mean_ai_probability": statistics.mean(ai_probabilities) if ai_probabilities else None,
        "mean_human_probability": statistics.mean(human_probabilities) if human_probabilities else None,
    }


def exact_mcnemar(rows: list[dict], subset_truth: bool | None = None) -> dict:
    subset = rows if subset_truth is None else [row for row in rows if row["truth"] is subset_truth]
    single_only = 0
    context_only = 0
    for row in subset:
        truth = row["truth"]
        single_correct = (row["single_probability"] >= THRESHOLD) == truth
        context_correct = (row["context_probability"] >= THRESHOLD) == truth
        single_only += single_correct and not context_correct
        context_only += context_correct and not single_correct
    discordant = single_only + context_only
    if discordant == 0:
        p_value = 1.0
    else:
        tail = sum(math.comb(discordant, k) for k in range(0, min(single_only, context_only) + 1)) / (2 ** discordant)
        p_value = min(1.0, 2 * tail)
    return {
        "single_only_correct": single_only,
        "context_only_correct": context_only,
        "discordant": discordant,
        "exact_two_sided_p": p_value,
    }


def load_rows(experiment: Path, language: str) -> list[dict]:
    dataset_path = experiment / "data" / f"dataset.context3-sentence-mixed.{language}.json"
    result_path = experiment / "result" / f"responses.noul.context3-sentence-mixed.{language}.jsonl"
    samples = {
        sample["id"]: sample
        for sample in json.loads(dataset_path.read_text(encoding="utf-8"))["samples"]
    }
    records = {}
    for line in result_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record["id"] in records:
            raise ValueError(f"duplicate result id: {record['id']}")
        if record["error"] is not None:
            raise ValueError(f"unresolved error: {record['id']}: {record['error']}")
        records[record["id"]] = record
    if set(samples) != set(records):
        raise ValueError(f"dataset/result mismatch: {language}")
    rows = []
    for sample_id, sample in samples.items():
        metadata = sample["metadata"]
        response = records[sample_id]["response"]
        rows.append(
            {
                "id": sample_id,
                "language": language,
                "source_id": metadata["source_id"],
                "target_sentence_id": metadata["target_sentence_id"],
                "truth": bool(sample["reference"]["ai_authorship"]),
                "origin": metadata["target_origin"],
                "previous_origin": metadata["previous_origin"],
                "next_origin": metadata["next_origin"],
                "neighbor_ai_count": int(metadata["previous_origin"] == "ai")
                + int(metadata["next_origin"] == "ai"),
                "length_group": metadata["length_group"],
                "quote_or_dialogue": bool(metadata["quote_or_dialogue"]),
                "ai_similarity_group": metadata.get("ai_similarity_group"),
                "single_probability": float(metadata["baseline_single_probability"]),
                "context_probability": float(response["answers"]["ai_authorship"]["noul"]),
                "context_cost_usd": float(response["usage"]["cost"]),
                "context_input_tokens": int(response["usage"]["input_tokens"]),
                "model": response["model"],
            }
        )
    return rows


def grouped(rows: list[dict], key: str) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    output = []
    for value, subset in sorted(groups.items()):
        output.append(
            {
                "factor": key,
                "category": value,
                "n": len(subset),
                "single": metrics(subset, "single_probability"),
                "context": metrics(subset, "context_probability"),
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rows = [row for language in ("zh", "en") for row in load_rows(args.experiment, language)]
    summary = {
        "threshold": THRESHOLD,
        "models": sorted({row["model"] for row in rows}),
        "groups": {},
        "strata": {},
        "context_cost_usd": sum(row["context_cost_usd"] for row in rows),
        "context_input_tokens": sum(row["context_input_tokens"] for row in rows),
    }
    for language in ("zh", "en"):
        subset = [row for row in rows if row["language"] == language]
        summary["groups"][language] = {
            "single": metrics(subset, "single_probability"),
            "context": metrics(subset, "context_probability"),
            "mcnemar_all": exact_mcnemar(subset),
            "mcnemar_ai": exact_mcnemar(subset, True),
            "mcnemar_human": exact_mcnemar(subset, False),
        }
        summary["strata"][language] = {
            "length_group": grouped(subset, "length_group"),
            "quote_or_dialogue": grouped(subset, "quote_or_dialogue"),
            "neighbor_ai_count": grouped(subset, "neighbor_ai_count"),
            "ai_similarity_group": grouped([row for row in subset if row["truth"]], "ai_similarity_group"),
        }
    summary["groups"]["combined"] = {
        "single": metrics(rows, "single_probability"),
        "context": metrics(rows, "context_probability"),
        "mcnemar_all": exact_mcnemar(rows),
        "mcnemar_ai": exact_mcnemar(rows, True),
        "mcnemar_human": exact_mcnemar(rows, False),
    }
    (args.output / "context_window_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (args.output / "context_window_predictions.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
