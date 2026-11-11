#!/usr/bin/env python3
"""Calibrate language-specific Jev sentence thresholds without source leakage."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SALT = "jev-sentence-threshold-calibration-v1"
FIXED_THRESHOLD = 0.50


def safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0


def metrics(rows: list[dict], threshold: float) -> dict:
    tp = sum(row["truth"] and row["probability"] >= threshold for row in rows)
    fp = sum(not row["truth"] and row["probability"] >= threshold for row in rows)
    tn = sum(not row["truth"] and row["probability"] < threshold for row in rows)
    fn = sum(row["truth"] and row["probability"] < threshold for row in rows)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    return {
        "threshold": threshold,
        "n": len(rows),
        "positives": tp + fn,
        "negatives": tn + fp,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "accuracy": safe_div(tp + tn, len(rows)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "false_positive_rate": safe_div(fp, fp + tn),
        "f1": safe_div(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
    }


def rank(language: str, source_id: str) -> str:
    return hashlib.sha256(f"{SALT}|{language}|{source_id}".encode("utf-8")).hexdigest()


def load_rows(experiment: Path, language: str) -> list[dict]:
    dataset_path = experiment / "data" / f"dataset.sentence-mixed.{language}.json"
    result_path = experiment / "result" / f"responses.noul.sentence-mixed.{language}.jsonl"
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    samples = {sample["id"]: sample for sample in dataset["samples"]}
    records: dict[str, dict] = {}
    for line in result_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record["id"] in records:
            raise ValueError(f"duplicate result ID: {record['id']}")
        if record["error"] is not None:
            raise ValueError(f"unresolved error: {record['id']}: {record['error']}")
        records[record["id"]] = record
    if set(samples) != set(records):
        raise ValueError(f"dataset/result mismatch for {language}")
    rows = []
    for sample_id, sample in samples.items():
        probability = float(records[sample_id]["response"]["answers"]["ai_authorship"]["noul"])
        if not 0 <= probability <= 1:
            raise ValueError(f"probability outside [0,1]: {sample_id}")
        rows.append(
            {
                "id": sample_id,
                "source_id": sample["metadata"]["source_id"],
                "language": language,
                "truth": bool(sample["reference"]["ai_authorship"]),
                "probability": probability,
            }
        )
    return rows


def select_threshold(train_rows: list[dict]) -> tuple[float, dict, list[dict]]:
    candidates = sorted({0.0, 1.0, *(row["probability"] for row in train_rows)})
    evaluated = [metrics(train_rows, threshold) for threshold in candidates]
    # Primary target is F1. Ties prefer balanced accuracy, then specificity,
    # then a threshold closest to the pre-registered 0.50 value.
    best = max(
        evaluated,
        key=lambda item: (
            item["f1"],
            item["balanced_accuracy"],
            item["specificity"],
            -abs(item["threshold"] - FIXED_THRESHOLD),
            item["threshold"],
        ),
    )
    return best["threshold"], best, evaluated


def analyze_language(experiment: Path, language: str) -> dict:
    rows = load_rows(experiment, language)
    source_ids = sorted({row["source_id"] for row in rows}, key=lambda source_id: rank(language, source_id))
    if len(source_ids) != 100:
        raise ValueError(f"expected 100 {language} source articles, got {len(source_ids)}")
    train_ids = set(source_ids[:70])
    test_ids = set(source_ids[70:])
    if train_ids & test_ids:
        raise AssertionError("source leakage between train and test")
    train_rows = [row for row in rows if row["source_id"] in train_ids]
    test_rows = [row for row in rows if row["source_id"] in test_ids]
    selected, train_selected, evaluated = select_threshold(train_rows)
    test_fixed = metrics(test_rows, FIXED_THRESHOLD)
    test_selected = metrics(test_rows, selected)
    return {
        "language": language,
        "split": {
            "method": f"SHA-256 rank of {SALT}|language|source_id",
            "train_source_count": len(train_ids),
            "test_source_count": len(test_ids),
            "train_sentence_count": len(train_rows),
            "test_sentence_count": len(test_rows),
            "train_source_ids": sorted(train_ids),
            "test_source_ids": sorted(test_ids),
            "source_overlap": sorted(train_ids & test_ids),
        },
        "selection": {
            "primary_objective": "maximize training F1",
            "tie_breakers": [
                "maximize balanced accuracy",
                "maximize specificity",
                "minimize distance from 0.50",
                "prefer higher threshold",
            ],
            "candidate_count": len(evaluated),
            "selected_threshold": selected,
            "training_metrics_at_selected_threshold": train_selected,
            "training_metrics_at_fixed_threshold": metrics(train_rows, FIXED_THRESHOLD),
        },
        "independent_test": {
            "fixed_0_50": test_fixed,
            "calibrated": test_selected,
            "delta_calibrated_minus_fixed": {
                field: test_selected[field] - test_fixed[field]
                for field in ("accuracy", "precision", "recall", "specificity", "false_positive_rate", "f1", "balanced_accuracy")
            },
        },
    }


def pct(value: float) -> str:
    return f"{value:.1%}"


def build_report(result: dict) -> str:
    lines = [
        "# JEV句子级检测：中英文独立阈值校准",
        "",
        "## 设计",
        "",
        "按来源文章而不是按句子划分训练集与测试集。每种语言100篇中，使用固定SHA-256排序取70篇训练、30篇测试；同一文章的句子不会跨集合。训练集以F1最大为首要目标选择阈值，阈值确定后只在独立测试集评估一次，并与预设0.50阈值比较。该分析不调用任何API。",
        "",
        "## 独立测试集结果",
        "",
        "| 语言 | 阈值 | 准确率 | 精确率 | AI召回率 | 人工句特异度 | F1 | 平衡准确率 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文")):
        item = result["languages"][language]
        fixed = item["independent_test"]["fixed_0_50"]
        calibrated = item["independent_test"]["calibrated"]
        lines.append(
            f"| {label}（固定） | {fixed['threshold']:.2f} | {pct(fixed['accuracy'])} | {pct(fixed['precision'])} | {pct(fixed['recall'])} | {pct(fixed['specificity'])} | {fixed['f1']:.3f} | {fixed['balanced_accuracy']:.3f} |"
        )
        lines.append(
            f"| {label}（校准） | {calibrated['threshold']:.2f} | {pct(calibrated['accuracy'])} | {pct(calibrated['precision'])} | {pct(calibrated['recall'])} | {pct(calibrated['specificity'])} | {calibrated['f1']:.3f} | {calibrated['balanced_accuracy']:.3f} |"
        )
    lines += ["", "## 阈值变化的影响", ""]
    for language, label in (("zh", "中文"), ("en", "英文")):
        item = result["languages"][language]
        fixed = item["independent_test"]["fixed_0_50"]
        calibrated = item["independent_test"]["calibrated"]
        delta = item["independent_test"]["delta_calibrated_minus_fixed"]
        lines.append(
            f"- {label}阈值从0.50调整为{calibrated['threshold']:.2f}：AI召回率由{pct(fixed['recall'])}升至{pct(calibrated['recall'])}，F1由{fixed['f1']:.3f}升至{calibrated['f1']:.3f}，但人工句误报率变化为{delta['false_positive_rate']:+.1%}。"
        )
    lines += [
        "",
        "## 解释",
        "",
        "语言独立校准用于区分“模型没有排序信号”和“统一0.50阈值不适配”两种情况。若校准后召回率和F1明显提高，说明原结果的一部分问题来自概率校准；但阈值是在训练文章上选择的，因此只能以30篇独立测试文章的结果作为泛化证据。单次70/30划分仍有抽样不确定性，后续可用按文章分组的重复交叉验证补充稳定性分析。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result = {
        "analysis": "language_specific_sentence_threshold_calibration",
        "fixed_threshold": FIXED_THRESHOLD,
        "api_called": False,
        "languages": {
            language: analyze_language(args.experiment, language) for language in ("zh", "en")
        },
    }
    (args.output / "threshold_calibration.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output / "THRESHOLD_CALIBRATION.md").write_text(build_report(result), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
