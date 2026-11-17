#!/usr/bin/env python3
"""Analyze Jev article- and sentence-level results for the mixed corpus."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


THRESHOLD = 0.50


def safe_div(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator else None


def roc_auc(rows: list[dict]) -> float | None:
    ordered = sorted((row["probability"], int(row["truth"])) for row in rows)
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


def average_precision(rows: list[dict]) -> float | None:
    ordered = sorted(rows, key=lambda row: (-row["probability"], row["id"]))
    positives = sum(row["truth"] for row in ordered)
    if not positives:
        return None
    found = 0
    total = 0.0
    for rank, row in enumerate(ordered, 1):
        if row["truth"]:
            found += 1
            total += found / rank
    return total / positives


def classification_metrics(rows: list[dict]) -> dict:
    tp = sum(row["truth"] and row["predicted"] for row in rows)
    tn = sum(not row["truth"] and not row["predicted"] for row in rows)
    fp = sum(not row["truth"] and row["predicted"] for row in rows)
    fn = sum(row["truth"] and not row["predicted"] for row in rows)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    precision = safe_div(tp, tp + fp)
    return {
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
        "f1": safe_div(2 * precision * recall, precision + recall)
        if precision is not None and recall is not None and precision + recall
        else None,
        "balanced_accuracy": (recall + specificity) / 2 if recall is not None and specificity is not None else None,
        "roc_auc": roc_auc(rows),
        "average_precision": average_precision(rows),
        "mean_ai_probability": statistics.mean(row["probability"] for row in rows if row["truth"]),
        "mean_human_probability": statistics.mean(row["probability"] for row in rows if not row["truth"]),
        "median_ai_probability": statistics.median(row["probability"] for row in rows if row["truth"]),
        "median_human_probability": statistics.median(row["probability"] for row in rows if not row["truth"]),
    }


def article_metrics(rows: list[dict]) -> dict:
    probabilities = [row["probability"] for row in rows]
    return {
        "n": len(rows),
        "detected": sum(row["predicted"] for row in rows),
        "detection_rate": sum(row["predicted"] for row in rows) / len(rows),
        "mean_probability": statistics.mean(probabilities),
        "median_probability": statistics.median(probabilities),
        "minimum_probability": min(probabilities),
        "maximum_probability": max(probabilities),
    }


def localization_metrics(rows: list[dict]) -> dict:
    by_source: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        by_source[(row["language"], row["source_id"])].append(row)
    article_aucs: list[float] = []
    top_k_recalls: list[float] = []
    exact_top_k = 0
    ai_mean_higher = 0
    at_least_one_ai_detected = 0
    all_ai_detected = 0
    no_human_false_positive = 0
    perfect_threshold = 0
    for source_rows in by_source.values():
        ai_rows = [row for row in source_rows if row["truth"]]
        human_rows = [row for row in source_rows if not row["truth"]]
        current_auc = roc_auc(source_rows)
        if current_auc is not None:
            article_aucs.append(current_auc)
        k = len(ai_rows)
        top_k = sorted(source_rows, key=lambda row: (-row["probability"], row["id"]))[:k]
        hits = sum(row["truth"] for row in top_k)
        top_k_recalls.append(hits / k)
        exact_top_k += hits == k
        ai_mean_higher += statistics.mean(row["probability"] for row in ai_rows) > statistics.mean(
            row["probability"] for row in human_rows
        )
        ai_hits = sum(row["predicted"] for row in ai_rows)
        human_hits = sum(row["predicted"] for row in human_rows)
        at_least_one_ai_detected += ai_hits >= 1
        all_ai_detected += ai_hits == len(ai_rows)
        no_human_false_positive += human_hits == 0
        perfect_threshold += ai_hits == len(ai_rows) and human_hits == 0
    count = len(by_source)
    return {
        "articles": count,
        "mean_within_article_roc_auc": statistics.mean(article_aucs),
        "median_within_article_roc_auc": statistics.median(article_aucs),
        "mean_top_k_recall": statistics.mean(top_k_recalls),
        "median_top_k_recall": statistics.median(top_k_recalls),
        "exact_top_k_set_rate": exact_top_k / count,
        "ai_mean_probability_higher_rate": ai_mean_higher / count,
        "at_least_one_ai_sentence_detected_rate": at_least_one_ai_detected / count,
        "all_ai_sentences_detected_rate": all_ai_detected / count,
        "no_human_false_positive_rate": no_human_false_positive / count,
        "perfect_threshold_article_rate": perfect_threshold / count,
    }


def load_run(experiment: Path, unit: str, language: str) -> list[dict]:
    data_path = experiment / "data" / f"dataset.{unit}-sentence-mixed.{language}.json"
    if unit == "sentence":
        data_path = experiment / "data" / f"dataset.sentence-mixed.{language}.json"
    result_path = experiment / "result" / f"responses.noul.{unit}-sentence-mixed.{language}.jsonl"
    if unit == "sentence":
        result_path = experiment / "result" / f"responses.noul.sentence-mixed.{language}.jsonl"
    dataset = json.loads(data_path.read_text(encoding="utf-8"))
    samples = {sample["id"]: sample for sample in dataset["samples"]}
    records = {}
    for line in result_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record["id"] in records:
            raise ValueError(f"duplicate result id: {record['id']}")
        if record["error"] is not None:
            raise ValueError(f"unresolved result error: {record['id']}: {record['error']}")
        records[record["id"]] = record
    if set(samples) != set(records):
        raise ValueError(f"dataset/result mismatch for {unit}/{language}")
    rows = []
    for sample_id, sample in samples.items():
        response = records[sample_id]["response"]
        probability = float(response["answers"]["ai_authorship"]["noul"])
        if not 0 <= probability <= 1:
            raise ValueError(f"probability outside [0,1]: {sample_id}")
        metadata = sample["metadata"]
        usage = response["usage"]
        rows.append(
            {
                "id": sample_id,
                "unit": unit,
                "language": language,
                "source_id": metadata["source_id"],
                "sentence_index": metadata.get("sentence_index"),
                "paragraph_index": metadata.get("paragraph_index"),
                "origin": metadata.get("origin", "mixed"),
                "truth": bool(sample["reference"]["ai_authorship"]),
                "probability": probability,
                "predicted": probability >= THRESHOLD,
                "input_tokens": int(usage["input_tokens"]),
                "output_tokens": int(usage.get("output_tokens", 0)),
                "cost_usd": float(usage["cost"]),
                "model": response["model"],
                "provider": response["provider"],
            }
        )
    return rows


def fmt(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    all_rows = []
    for unit in ("article", "sentence"):
        for language in ("zh", "en"):
            all_rows.extend(load_run(args.experiment, unit, language))

    article_rows = [row for row in all_rows if row["unit"] == "article"]
    sentence_rows = [row for row in all_rows if row["unit"] == "sentence"]
    summary = {
        "threshold": THRESHOLD,
        "condition": "sentence_unit_mixed_gpt4o_mini_33pct",
        "models": sorted({row["model"] for row in all_rows}),
        "article": {
            language: article_metrics([row for row in article_rows if row["language"] == language])
            for language in ("zh", "en")
        },
        "sentence": {
            language: classification_metrics([row for row in sentence_rows if row["language"] == language])
            for language in ("zh", "en")
        },
        "localization": {
            language: localization_metrics([row for row in sentence_rows if row["language"] == language])
            for language in ("zh", "en")
        },
        "cost": {},
    }
    summary["sentence"]["combined"] = classification_metrics(sentence_rows)
    summary["localization"]["combined"] = localization_metrics(sentence_rows)
    for unit in ("article", "sentence"):
        for language in ("zh", "en"):
            subset = [row for row in all_rows if row["unit"] == unit and row["language"] == language]
            summary["cost"][f"{unit}_{language}"] = {
                "requests": len(subset),
                "input_tokens": sum(row["input_tokens"] for row in subset),
                "output_tokens": sum(row["output_tokens"] for row in subset),
                "cost_usd": sum(row["cost_usd"] for row in subset),
            }
    summary["cost"]["total"] = {
        "requests": len(all_rows),
        "input_tokens": sum(row["input_tokens"] for row in all_rows),
        "output_tokens": sum(row["output_tokens"] for row in all_rows),
        "cost_usd": sum(row["cost_usd"] for row in all_rows),
    }

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "sentence_mixed_jev_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    fields = list(all_rows[0])
    with (args.output / "sentence_mixed_jev_predictions.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    lines = [
        "# Jev 句子级人机混合散文检测结果",
        "",
        "本报告使用 `typesafe/jev-1.14-20261014`，主阈值固定为 0.50。语料为中英文各 100 篇，每篇约三分之一句子来自 GPT-4o-mini 整篇改写稿，其余句子保留人工原文。",
        "",
        "## 主要发现",
        "",
        f"- 整篇提交时，中文混合文章检出率为 {summary['article']['zh']['detection_rate']:.1%}，英文为 {summary['article']['en']['detection_rate']:.1%}。",
        f"- 逐句按0.50阈值分类时，合计AI句召回率为 {summary['sentence']['combined']['recall']:.1%}，人工句特异度为 {summary['sentence']['combined']['specificity']:.1%}，F1为 {summary['sentence']['combined']['f1']:.3f}。中文AI句召回率仅 {summary['sentence']['zh']['recall']:.1%}，英文为 {summary['sentence']['en']['recall']:.1%}。",
        f"- 排序定位明显强于固定阈值分类：合计篇内ROC-AUC均值为 {summary['localization']['combined']['mean_within_article_roc_auc']:.3f}，Top-k召回率均值为 {summary['localization']['combined']['mean_top_k_recall']:.1%}；{summary['localization']['combined']['ai_mean_probability_higher_rate']:.1%} 的文章中，真实AI句的平均概率高于人工句。",
        "- 因此，JEV能够提供有用的句子级可疑度排序，但不适合直接用0.50阈值完成精确逐句标注；中文尤其需要重新校准阈值或采用篇内排序。",
        "",
        "## 整篇检测",
        "",
        "| 语言 | 篇数 | 检出篇数 | 检出率 | 平均概率 | 中位概率 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文")):
        item = summary["article"][language]
        lines.append(
            f"| {label} | {item['n']} | {item['detected']} | {fmt(item['detection_rate'])} | {fmt(item['mean_probability'])} | {fmt(item['median_probability'])} |"
        )
    lines += [
        "",
        "## 逐句检测",
        "",
        "| 语言 | 句数 | 准确率 | AI召回率 | 人工句特异度 | 精确率 | F1 | ROC-AUC | AP |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文"), ("combined", "合计")):
        item = summary["sentence"][language]
        lines.append(
            f"| {label} | {item['n']} | {fmt(item['accuracy'])} | {fmt(item['recall'])} | {fmt(item['specificity'])} | {fmt(item['precision'])} | {fmt(item['f1'])} | {fmt(item['roc_auc'])} | {fmt(item['average_precision'])} |"
        )
    lines += [
        "",
        "混淆矩阵按 `TP / FP / TN / FN`：",
        "",
    ]
    for language, label in (("zh", "中文"), ("en", "英文"), ("combined", "合计")):
        item = summary["sentence"][language]
        lines.append(f"- {label}：{item['tp']} / {item['fp']} / {item['tn']} / {item['fn']}")
    lines += [
        "",
        "## 篇内句子定位",
        "",
        "`Top-k召回率`：每篇按Jev概率从高到低选出与真实AI句数量相同的k句，其中真实AI句所占比例。篇内ROC-AUC反映随机抽取一条AI句和一条人工句时，AI句获得更高概率的可能性。",
        "",
        "| 语言 | 篇内ROC-AUC均值 | Top-k召回率均值 | AI句平均概率高于人工句的文章比例 | 至少检出1条AI句 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文"), ("combined", "合计")):
        item = summary["localization"][language]
        lines.append(
            f"| {label} | {fmt(item['mean_within_article_roc_auc'])} | {fmt(item['mean_top_k_recall'])} | {fmt(item['ai_mean_probability_higher_rate'])} | {fmt(item['at_least_one_ai_sentence_detected_rate'])} |"
        )
    lines += [
        "",
        "## 概率分布",
        "",
        "| 语言 | AI句平均概率 | 人工句平均概率 | AI句中位概率 | 人工句中位概率 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文"), ("combined", "合计")):
        item = summary["sentence"][language]
        lines.append(
            f"| {label} | {fmt(item['mean_ai_probability'])} | {fmt(item['mean_human_probability'])} | {fmt(item['median_ai_probability'])} | {fmt(item['median_human_probability'])} |"
        )
    lines += [
        "",
        "## 费用",
        "",
        "| 层级 | 语言 | 请求数 | 输入token | 费用 |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for unit, unit_label in (("article", "整篇"), ("sentence", "逐句")):
        for language, language_label in (("zh", "中文"), ("en", "英文")):
            item = summary["cost"][f"{unit}_{language}"]
            lines.append(
                f"| {unit_label} | {language_label} | {item['requests']} | {item['input_tokens']} | ${item['cost_usd']:.6f} |"
            )
    total = summary["cost"]["total"]
    lines += [
        f"| 合计 | 中英文 | {total['requests']} | {total['input_tokens']} | ${total['cost_usd']:.6f} |",
        "",
        "## 解释限制",
        "",
        "逐句判断缺少上下文，短句、引语、固定表达会使检测难度显著增加。因此，逐句阈值分类适合评估细粒度定位能力，但不应直接替代整篇判断。ROC-AUC和篇内排序指标比单一0.50阈值更能反映模型是否掌握了定位信号。",
        "",
    ]
    (args.output / "SENTENCE_MIXED_JEV_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
