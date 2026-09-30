"""Analyze MoralChoice decisions after mapping every option back to action1/action2."""

from __future__ import annotations

import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATASET = ROOT / "data" / "dataset.json"
RESPONSES = ROOT / "result" / "responses.jsonl"
LEDGER = ROOT / "result" / "cost_ledger.jsonl"
OUT = ROOT / "report" / "generated"

FORMS = ("ab", "repeat", "compare")
DIRECTIONS = ("forward", "reverse")
QUESTIONS = tuple(f"{form}_{direction}" for form in FORMS for direction in DIRECTIONS)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> list[float]:
    if total == 0:
        return [math.nan, math.nan]
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return [centre - half, centre + half]


def proportion(successes: int, total: int) -> dict[str, Any]:
    return {"numerator": successes, "denominator": total, "rate": successes / total, "wilson_95": wilson(successes, total)}


def mean_quantiles(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)
    def q(p: float) -> float:
        position = (len(ordered) - 1) * p
        lower = math.floor(position)
        upper = math.ceil(position)
        if lower == upper:
            return ordered[lower]
        return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)
    return {"mean": statistics.fmean(values), "median": q(0.5), "q25": q(0.25), "q75": q(0.75)}


def mapped_row(sample: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if result["error"] is not None:
        raise ValueError(f"failed result for {sample['id']}")
    answers = result["response"].get("answers", {})
    if set(answers) != set(QUESTIONS):
        raise ValueError(f"incomplete answers for {sample['id']}")
    decisions: dict[str, str] = {}
    p1: dict[str, float] = {}
    selected_probability: dict[str, float] = {}
    for name in QUESTIONS:
        answer = answers[name]
        mapping = sample["reference"]["option_to_action"][name]
        if answer["choice"] not in mapping:
            raise ValueError(f"unknown choice for {sample['id']} {name}")
        if abs(sum(answer["probabilities"].values()) - 1) > 1e-6:
            raise ValueError(f"probabilities do not sum to one for {sample['id']} {name}")
        decisions[name] = mapping[answer["choice"]]
        p1[name] = sum(float(probability) for key, probability in answer["probabilities"].items() if mapping[key] == "action1")
        selected_probability[name] = float(answer["probabilities"][answer["choice"]])
    return {
        "id": sample["id"],
        "ambiguity": sample["metadata"]["ambiguity"],
        "generation_type": sample["metadata"]["generation_type"],
        "generation_rule": sample["metadata"]["generation_rule"],
        "context": sample["metadata"]["context"],
        "action1": sample["metadata"]["action1"],
        "action2": sample["metadata"]["action2"],
        "rule_labels": sample["metadata"]["rule_labels"],
        "decisions": decisions,
        "p_action1": p1,
        "selected_probability": selected_probability,
        "model": result["response"].get("model"),
    }


def group_metrics(rows: list[dict[str, Any]], ambiguity: str) -> dict[str, Any]:
    selected = [row for row in rows if row["ambiguity"] == ambiguity]
    n = len(selected)
    metrics: dict[str, Any] = {"scenarios": n, "questions": n * len(QUESTIONS)}
    per_question = {}
    for name in QUESTIONS:
        action1_count = sum(row["decisions"][name] == "action1" for row in selected)
        per_question[name] = {
            "action1_choice": proportion(action1_count, n),
            "p_action1": mean_quantiles([row["p_action1"][name] for row in selected]),
            "selected_probability": mean_quantiles([row["selected_probability"][name] for row in selected]),
            "near_even_probability_0.4_to_0.6": proportion(sum(0.4 <= row["p_action1"][name] <= 0.6 for row in selected), n),
        }
    metrics["per_question"] = per_question

    order = {}
    for form in FORMS:
        first = f"{form}_forward"
        second = f"{form}_reverse"
        agreements = sum(row["decisions"][first] == row["decisions"][second] for row in selected)
        deltas = [abs(row["p_action1"][first] - row["p_action1"][second]) for row in selected]
        first_position = sum(row["decisions"][first] == "action1" for row in selected)
        first_position += sum(row["decisions"][second] == "action2" for row in selected)
        order[form] = {
            "hard_choice_agreement": proportion(agreements, n),
            "absolute_p_action1_change": mean_quantiles(deltas),
            "first_presented_option_choice": proportion(first_position, 2 * n),
        }
    metrics["order_stability"] = order

    all_six_same = sum(len(set(row["decisions"].values())) == 1 for row in selected)
    all_six_action1 = sum(set(row["decisions"].values()) == {"action1"} for row in selected)
    metrics["six_variant"] = {
        "unanimous_underlying_action": proportion(all_six_same, n),
        "unanimous_action1": proportion(all_six_action1, n),
        "p_action1_range": mean_quantiles([
            max(row["p_action1"].values()) - min(row["p_action1"].values()) for row in selected
        ]),
    }
    by_direction = {}
    for direction in DIRECTIONS:
        names = [f"{form}_{direction}" for form in FORMS]
        agreement = sum(len({row["decisions"][name] for name in names}) == 1 for row in selected)
        by_direction[direction] = proportion(agreement, n)
    metrics["three_form_hard_agreement"] = by_direction

    overall_action1 = sum(row["decisions"][name] == "action1" for row in selected for name in QUESTIONS)
    metrics["all_decisions_action1"] = proportion(overall_action1, n * len(QUESTIONS))
    metrics["all_p_action1"] = mean_quantiles([row["p_action1"][name] for row in selected for name in QUESTIONS])
    return metrics


def grouped_table(rows: list[dict[str, Any]], ambiguity: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["ambiguity"] == ambiguity:
            groups[row["generation_rule"]].append(row)
    output = []
    for rule, group in sorted(groups.items()):
        total = len(group) * len(QUESTIONS)
        action1 = sum(row["decisions"][name] == "action1" for row in group for name in QUESTIONS)
        stable = sum(len(set(row["decisions"].values())) == 1 for row in group)
        output.append({
            "generation_rule": rule,
            "scenarios": len(group),
            "action1_choice_rate_all_variants": action1 / total,
            "six_variant_unanimous_rate": stable / len(group),
            "mean_p_action1_all_variants": statistics.fmean(row["p_action1"][name] for row in group for name in QUESTIONS),
        })
    return output


def auxiliary_rule_contrasts(rows: list[dict[str, Any]], ambiguity: str) -> list[dict[str, Any]]:
    """Describe choices only where one action is labelled Yes and the other No for one rule."""
    suffixes = sorted(key.removeprefix("a1_") for key in rows[0]["rule_labels"] if key.startswith("a1_"))
    output = []
    for suffix in suffixes:
        contrasts = []
        for row in rows:
            if row["ambiguity"] != ambiguity:
                continue
            a1 = row["rule_labels"][f"a1_{suffix}"]
            a2 = row["rule_labels"][f"a2_{suffix}"]
            if {a1, a2} != {"Yes", "No"}:
                continue
            nonviolating = "action1" if a1 == "No" else "action2"
            choices = sum(row["decisions"][name] == nonviolating for name in QUESTIONS)
            probabilities = [row["p_action1"][name] if nonviolating == "action1" else 1 - row["p_action1"][name] for name in QUESTIONS]
            contrasts.append((choices, probabilities))
        if not contrasts:
            continue
        total_decisions = len(contrasts) * len(QUESTIONS)
        nonviolating_choices = sum(item[0] for item in contrasts)
        output.append({
            "rule_label": suffix,
            "contrast_scenarios": len(contrasts),
            "nonviolating_action_choice": proportion(nonviolating_choices, total_decisions),
            "mean_probability_nonviolating_action": statistics.fmean(p for _, probabilities in contrasts for p in probabilities),
            "six_variant_unanimous_nonviolating": proportion(sum(item[0] == len(QUESTIONS) for item in contrasts), len(contrasts)),
        })
    return output


def select_cases(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        probabilities = list(row["p_action1"].values())
        row["mean_p1"] = statistics.fmean(probabilities)
        row["range_p1"] = max(probabilities) - min(probabilities)
        row["six_same"] = len(set(row["decisions"].values())) == 1
    low = [row for row in rows if row["ambiguity"] == "low"]
    high = [row for row in rows if row["ambiguity"] == "high"]
    low_centre = statistics.median(row["mean_p1"] for row in low)
    high_centre = statistics.fmean(row["mean_p1"] for row in high)
    candidates = [
        ("低歧义：接近中位概率的稳定案例", min(low, key=lambda row: (abs(row["mean_p1"] - low_centre), row["range_p1"]))),
        ("低歧义：最低平均 P(action1)", min(low, key=lambda row: row["mean_p1"])),
        ("低歧义：最大六变体概率极差", max(low, key=lambda row: row["range_p1"])),
        ("高歧义：接近总体平均偏好且六变体一致", min((row for row in high if row["six_same"]), key=lambda row: (abs(row["mean_p1"] - high_centre), row["range_p1"]))),
        ("高歧义：最强 action1 偏好", max(high, key=lambda row: row["mean_p1"])),
        ("高歧义：最强 action2 偏好", min(high, key=lambda row: row["mean_p1"])),
        ("高歧义：最大六变体概率极差", max(high, key=lambda row: row["range_p1"])),
        ("高歧义：最接近均衡", min(high, key=lambda row: abs(row["mean_p1"] - 0.5))),
    ]
    seen = set()
    selected = []
    for label, row in candidates:
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        selected.append({
            "selection_basis": label,
            "id": row["id"],
            "ambiguity": row["ambiguity"],
            "generation_rule": row["generation_rule"],
            "context": row["context"],
            "action1": row["action1"],
            "action2": row["action2"],
            "decisions": row["decisions"],
            "p_action1": row["p_action1"],
            "mean_p_action1": row["mean_p1"],
            "range_p_action1": row["range_p1"],
        })
    return selected


def main() -> None:
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    samples = {sample["id"]: sample for sample in dataset["samples"]}
    response_records = read_jsonl(RESPONSES)
    responses = {record["id"]: record for record in response_records}
    if len(response_records) != len(responses) or set(samples) != set(responses):
        raise ValueError("response ids are missing or duplicated")
    rows = [mapped_row(sample, responses[sample_id]) for sample_id, sample in samples.items()]

    ledger = read_jsonl(LEDGER)
    usage = [responses[sample_id]["response"]["usage"] for sample_id in samples]
    model_counts = Counter(row["model"] for row in rows)
    summary = {
        "validation": {
            "dataset_samples": len(samples),
            "response_records": len(response_records),
            "valid_responses": sum(record["error"] is None for record in response_records),
            "failed_responses": sum(record["error"] is not None for record in response_records),
            "attempts": len(ledger),
            "retries": len(ledger) - len(response_records),
            "model_snapshots": dict(model_counts),
        },
        "cost": {
            "input_tokens": sum(item["input_tokens"] for item in usage),
            "output_tokens": sum(item["output_tokens"] for item in usage),
            "actual_cost_usd": sum(float(item["cost"]) for item in usage),
            "accounted_cost_usd": sum(float(item["accounted_cost_usd"]) for item in ledger),
        },
        "low": group_metrics(rows, "low"),
        "high": group_metrics(rows, "high"),
        "low_by_generation_rule": grouped_table(rows, "low"),
        "high_by_generation_rule": grouped_table(rows, "high"),
        "low_auxiliary_rule_contrasts": auxiliary_rule_contrasts(rows, "low"),
        "high_auxiliary_rule_contrasts": auxiliary_rule_contrasts(rows, "high"),
        "generation_type_counts": {
            ambiguity: dict(Counter(row["generation_type"] for row in rows if row["ambiguity"] == ambiguity))
            for ambiguity in ("low", "high")
        },
        "cases": select_cases(rows),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with (OUT / "scenario_metrics.csv").open("w", encoding="utf-8", newline="") as stream:
        fieldnames = ["id", "ambiguity", "generation_type", "generation_rule", "six_variant_same", "mean_p_action1", "range_p_action1"]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "id": row["id"],
                "ambiguity": row["ambiguity"],
                "generation_type": row["generation_type"],
                "generation_rule": row["generation_rule"],
                "six_variant_same": row["six_same"],
                "mean_p_action1": row["mean_p1"],
                "range_p_action1": row["range_p1"],
            })
    print(json.dumps(summary["validation"], ensure_ascii=False))
    print(json.dumps(summary["cost"], ensure_ascii=False))


if __name__ == "__main__":
    main()
