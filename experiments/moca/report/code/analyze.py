"""Analyze Jev responses for the MoCa evaluation using only the standard library."""

from __future__ import annotations

import csv
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "dataset.json"
RESULTS = ROOT / "result" / "responses.jsonl"
ATTEMPTS = ROOT / "result" / "attempts.jsonl"
GENERATED = ROOT / "report" / "generated"
SEED = 20260930
BOOTSTRAPS = 10_000


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def label3(p_yes: float) -> str:
    if p_yes > 0.6:
        return "Yes"
    if p_yes < 0.4:
        return "No"
    return "Ambiguous"


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def bootstrap_ci(rows: list[dict[str, Any]], metric: Callable[[list[dict[str, Any]]], float]) -> list[float]:
    rng = random.Random(SEED + len(rows))
    values = []
    for _ in range(BOOTSTRAPS):
        sample = [rows[rng.randrange(len(rows))] for _ in rows]
        value = metric(sample)
        if not math.isnan(value):
            values.append(value)
    return [percentile(values, 0.025), percentile(values, 0.975)]


def agreement(rows: list[dict[str, Any]]) -> float:
    return statistics.mean(row["human_label_3"] == row["jev_label_3"] for row in rows)


def yes_mae(rows: list[dict[str, Any]]) -> float:
    return statistics.mean(abs(row["human_p_yes"] - row["jev_p_yes"]) for row in rows)


def matched_label_mae(rows: list[dict[str, Any]]) -> float:
    errors = []
    for row in rows:
        human_confidence = max(row["human_p_yes"], 1 - row["human_p_yes"])
        model_matched = row["jev_p_yes"] if row["human_p_yes"] >= 0.5 else 1 - row["jev_p_yes"]
        errors.append(abs(human_confidence - model_matched))
    return statistics.mean(errors)


def brier(rows: list[dict[str, Any]]) -> float:
    return statistics.mean((row["jev_p_yes"] - row["human_p_yes"]) ** 2 for row in rows)


def cross_entropy(rows: list[dict[str, Any]]) -> float:
    losses = []
    for row in rows:
        human = row["human_p_yes"]
        model = min(max(row["jev_p_yes"], 1e-12), 1 - 1e-12)
        losses.append(-(human * math.log(model) + (1 - human) * math.log(1 - model)))
    return statistics.mean(losses)


def auroc(rows: list[dict[str, Any]]) -> float:
    filtered = [row for row in rows if row["human_label_3"] != "Ambiguous"]
    positives = sum(row["human_label_3"] == "Yes" for row in filtered)
    negatives = len(filtered) - positives
    if not positives or not negatives:
        return float("nan")
    ordered = sorted(enumerate(filtered), key=lambda item: item[1]["jev_p_yes"])
    rank_sum = 0.0
    position = 0
    while position < len(ordered):
        end = position + 1
        score = ordered[position][1]["jev_p_yes"]
        while end < len(ordered) and ordered[end][1]["jev_p_yes"] == score:
            end += 1
        average_rank = ((position + 1) + end) / 2
        rank_sum += average_rank * sum(
            ordered[index][1]["human_label_3"] == "Yes" for index in range(position, end)
        )
        position = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    human_counts = Counter(row["human_label_3"] for row in rows)
    jev_counts = Counter(row["jev_label_3"] for row in rows)
    tri = agreement(rows)
    mae = yes_mae(rows)
    auc = auroc(rows)
    majority_baseline = max(human_counts.values()) / len(rows)
    confusion = {
        human: {jev: 0 for jev in ("Yes", "No", "Ambiguous")}
        for human in ("Yes", "No", "Ambiguous")
    }
    for row in rows:
        confusion[row["human_label_3"]][row["jev_label_3"]] += 1
    return {
        "n": len(rows),
        "human_label_counts": dict(human_counts),
        "jev_label_counts": dict(jev_counts),
        "three_class_agreement": tri,
        "three_class_agreement_ci95": bootstrap_ci(rows, agreement),
        "uniform_random_baseline": 1 / 3,
        "majority_class_baseline": majority_baseline,
        "auroc_human_unambiguous": auc,
        "auroc_ci95": bootstrap_ci(rows, auroc),
        "yes_probability_mae": mae,
        "yes_probability_mae_ci95": bootstrap_ci(rows, yes_mae),
        "matched_label_mae_paper_style": matched_label_mae(rows),
        "brier_against_human_yes_share": brier(rows),
        "cross_entropy_against_human_distribution": cross_entropy(rows),
        "confusion": confusion,
    }


def factor_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        for dimension, attributes in row["factors"].items():
            for attribute in attributes:
                groups[(row["subset"], dimension, attribute)].append(row)
    output = []
    for (subset, dimension, attribute), members in sorted(groups.items()):
        output.append(
            {
                "subset": subset,
                "dimension": dimension,
                "attribute": attribute,
                "n": len(members),
                "human_mean_p_yes": statistics.mean(row["human_p_yes"] for row in members),
                "jev_mean_p_yes": statistics.mean(row["jev_p_yes"] for row in members),
                "three_class_agreement": agreement(members),
            }
        )
    return output


def factor_contrasts(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_dimension: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in groups:
        by_dimension[(row["subset"], row["dimension"])].append(row)
    output = []
    for (subset, dimension), members in sorted(by_dimension.items()):
        if len(members) != 2:
            continue
        members = sorted(members, key=lambda row: row["attribute"])
        first, second = members
        output.append(
            {
                "subset": subset,
                "dimension": dimension,
                "attribute_a": first["attribute"],
                "attribute_b": second["attribute"],
                "n_a": first["n"],
                "n_b": second["n"],
                "human_delta_b_minus_a": second["human_mean_p_yes"] - first["human_mean_p_yes"],
                "jev_delta_b_minus_a": second["jev_mean_p_yes"] - first["jev_mean_p_yes"],
                "agreement_a": first["three_class_agreement"],
                "agreement_b": second["three_class_agreement"],
            }
        )
    return output


def main() -> None:
    if not DATA.exists():
        raise SystemExit("MoCa source texts are not distributed. Prepare data with preparation/code/prepare_data.py --source-dir <authorized-local-folder>. Reports can be rebuilt from the included aggregate summary without source texts.")
    dataset = json.loads(DATA.read_text(encoding="utf-8"))["samples"]
    results = {record["id"]: record for record in read_jsonl(RESULTS)}
    attempts = read_jsonl(ATTEMPTS)
    rows = []
    failures = []
    for sample in dataset:
        record = results.get(sample["id"])
        if record is None or record["error"] is not None:
            failures.append(sample["id"])
            continue
        answer = record["response"]["answers"]["judgment"]
        p_yes = float(answer["probabilities"]["Yes"])
        ref = sample["reference"]
        rows.append(
            {
                "id": sample["id"],
                "subset": sample["metadata"]["subset"],
                "factors": sample["metadata"]["factors"],
                "human_p_yes": float(ref["human_yes_probability"]),
                "human_label_3": ref["human_label_3"],
                "jev_p_yes": p_yes,
                "jev_label_3": label3(p_yes),
                "jev_choice": answer["choice"],
            }
        )

    reported_attempts = [
        attempt
        for attempt in attempts
        if isinstance(attempt.get("response"), dict)
        and isinstance(attempt["response"].get("usage"), dict)
    ]
    cost = {
        "attempts": len(attempts),
        "failed_attempts": sum(attempt["error"] is not None for attempt in attempts),
        "input_tokens": sum(int(attempt["response"]["usage"].get("input_tokens", 0)) for attempt in reported_attempts),
        "output_tokens": sum(int(attempt["response"]["usage"].get("output_tokens", 0)) for attempt in reported_attempts),
        "actual_cost_usd": sum(float(attempt["response"]["usage"].get("cost", 0)) for attempt in reported_attempts),
        "unknown_cost_attempts": len(attempts) - len(reported_attempts),
        "model_versions": dict(
            Counter(
                attempt["response"].get("model", "missing")
                for attempt in attempts
                if isinstance(attempt.get("response"), dict)
            )
        ),
    }
    subsets = {
        subset: summarize([row for row in rows if subset == "overall" or row["subset"] == subset])
        for subset in ("overall", "causal", "moral")
    }
    groups = factor_rows(rows)
    contrasts = factor_contrasts(groups)
    summary = {
        "analysis_seed": SEED,
        "bootstrap_replicates": BOOTSTRAPS,
        "valid_samples": len(rows),
        "failed_sample_ids": failures,
        "cost": cost,
        "metrics": subsets,
        "factor_groups": groups,
        "factor_contrasts": contrasts,
    }
    GENERATED.mkdir(parents=True, exist_ok=True)
    (GENERATED / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for filename, records in (("factor-groups.csv", groups), ("factor-contrasts.csv", contrasts)):
        with (GENERATED / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    print(json.dumps({"valid": len(rows), "failures": failures, "cost": cost, "metrics": subsets}, indent=2))


if __name__ == "__main__":
    main()
