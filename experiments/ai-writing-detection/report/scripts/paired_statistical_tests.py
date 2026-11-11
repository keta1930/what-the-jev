"""Paired, article-clustered statistical comparisons for mixed-text detectors."""

from __future__ import annotations

import csv
import json
import math
import os
from collections import defaultdict
from pathlib import Path

import numpy as np


EXPERIMENT = Path(os.environ.get(
    "JEV_EXPERIMENT",
    r"C:\Users\asus\Desktop\Jev文章AI检测实验\what-the-jev\experiments\ai-writing-detection",
))
OUT = Path(os.environ.get(
    "PAIRED_STATS_OUTPUT",
    r"C:\Users\asus\Documents\ChatGPT\what-the-jev\paired_stats_output",
))
ASSET = EXPERIMENT / "report" / "asset"
THRESHOLD = 0.5
BOOTSTRAPS = 20_000
AUC_BOOTSTRAPS = 4_000
SEED = 20261027

METHODS = {
    "jev": ASSET / "mixed_jev_predictions.csv",
    "gpt4omini": ASSET / "gpt4omini_predictions.csv",
    "gpt56luna": ASSET / "gpt56luna_predictions.csv",
}
LABELS = {"jev": "Jev 1.14", "gpt4omini": "GPT-4o-mini", "gpt56luna": "GPT-5.6 Luna"}

METRIC_LABELS = {
    "article_detection": "整篇检出率",
    "block_accuracy": "块级准确率",
    "strict_localization": "AI 块严格定位率",
    "target_detection": "AI 块阈值检出率",
    "human_specificity": "人工块正确排除率",
}


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def load_predictions(path: Path) -> dict[tuple[str, str, str, str], dict]:
    records = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["language"], row["source_id"], row["unit"], row["block_index"])
            if key in records:
                raise ValueError(f"duplicate prediction key in {path}: {key}")
            records[key] = {
                "language": row["language"],
                "source_id": row["source_id"],
                "unit": row["unit"],
                "block_index": int(row["block_index"]) if row["block_index"] else None,
                "target_position": int(row["target_position"]),
                "truth": parse_bool(row["truth"]),
                "probability": float(row["probability"]),
            }
    if len(records) != 800:
        raise ValueError(f"expected 800 rows in {path}, found {len(records)}")
    return records


def build_method(records: dict) -> dict:
    by_source = defaultdict(lambda: {"article": None, "blocks": []})
    for row in records.values():
        key = (row["language"], row["source_id"])
        if row["unit"] == "article":
            by_source[key]["article"] = row
        else:
            by_source[key]["blocks"].append(row)
    if len(by_source) != 200:
        raise ValueError(f"expected 200 sources, found {len(by_source)}")

    result = {}
    for key, group in by_source.items():
        blocks = sorted(group["blocks"], key=lambda row: row["block_index"])
        if group["article"] is None or len(blocks) != 3:
            raise ValueError(f"incomplete source: {key}")
        targets = [row for row in blocks if row["truth"]]
        humans = [row for row in blocks if not row["truth"]]
        if len(targets) != 1 or len(humans) != 2:
            raise ValueError(f"invalid truth composition: {key}")
        target = targets[0]
        target_p = target["probability"]
        human_ps = [row["probability"] for row in humans]
        block_correct = [
            (row["probability"] >= THRESHOLD) == row["truth"] for row in blocks
        ]
        result[key] = {
            "article_detection": int(group["article"]["probability"] >= THRESHOLD),
            "strict_localization": int(target_p > max(human_ps)),
            "target_detection": int(target_p >= THRESHOLD),
            "block_correct": np.asarray(block_correct, dtype=np.int8),
            "block_accuracy_count": int(sum(block_correct)),
            "human_correct": np.asarray([p < THRESHOLD for p in human_ps], dtype=np.int8),
            "human_specificity_count": int(sum(p < THRESHOLD for p in human_ps)),
            "target_probability": target_p,
            "human_probabilities": np.asarray(human_ps, dtype=float),
        }
    return result


def exact_cluster_signflip_p(differences: np.ndarray) -> float:
    nonzero = [int(value) for value in differences if value != 0]
    if not nonzero:
        return 1.0
    observed = abs(sum(nonzero))
    counts = {0: 1}
    for value in nonzero:
        updated = defaultdict(int)
        magnitude = abs(value)
        for total, count in counts.items():
            updated[total + magnitude] += count
            updated[total - magnitude] += count
        counts = dict(updated)
    extreme = sum(count for total, count in counts.items() if abs(total) >= observed)
    return extreme / (2 ** len(nonzero))


def paired_bootstrap_ci(
    diff_zh: np.ndarray,
    diff_en: np.ndarray,
    denominator_per_source: int,
    iterations: int = BOOTSTRAPS,
    seed_offset: int = 0,
) -> list[float]:
    rng = np.random.default_rng(SEED + seed_offset)
    indices_zh = rng.integers(0, len(diff_zh), size=(iterations, len(diff_zh)))
    indices_en = rng.integers(0, len(diff_en), size=(iterations, len(diff_en)))
    deltas = (
        diff_zh[indices_zh].sum(axis=1) + diff_en[indices_en].sum(axis=1)
    ) / ((len(diff_zh) + len(diff_en)) * denominator_per_source)
    return [float(np.quantile(deltas, 0.025)), float(np.quantile(deltas, 0.975))]


def fast_auc(positive: np.ndarray, negative: np.ndarray) -> float:
    values = np.concatenate([positive, negative])
    labels = np.concatenate([
        np.ones(len(positive), dtype=np.int8), np.zeros(len(negative), dtype=np.int8)
    ])
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and sorted_values[end] == sorted_values[start]:
            end += 1
        average_rank = (start + 1 + end) / 2
        ranks[order[start:end]] = average_rank
        start = end
    n_pos, n_neg = len(positive), len(negative)
    return float((ranks[labels == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def auc_difference(method_a: dict, method_b: dict, keys_zh: list, keys_en: list, seed_offset: int) -> dict:
    keys = keys_zh + keys_en
    a_target = np.asarray([method_a[key]["target_probability"] for key in keys], dtype=float)
    b_target = np.asarray([method_b[key]["target_probability"] for key in keys], dtype=float)
    a_human = np.asarray([method_a[key]["human_probabilities"] for key in keys], dtype=float)
    b_human = np.asarray([method_b[key]["human_probabilities"] for key in keys], dtype=float)
    auc_a = fast_auc(a_target, a_human.reshape(-1))
    auc_b = fast_auc(b_target, b_human.reshape(-1))
    rng = np.random.default_rng(SEED + seed_offset)
    differences = np.empty(AUC_BOOTSTRAPS, dtype=float)
    for iteration in range(AUC_BOOTSTRAPS):
        zh_idx = rng.integers(0, len(keys_zh), len(keys_zh))
        en_idx = rng.integers(0, len(keys_en), len(keys_en)) + len(keys_zh)
        idx = np.concatenate([zh_idx, en_idx])
        differences[iteration] = (
            fast_auc(a_target[idx], a_human[idx].reshape(-1))
            - fast_auc(b_target[idx], b_human[idx].reshape(-1))
        )
    return {
        "jev_auc": auc_a,
        "other_auc": auc_b,
        "difference": auc_a - auc_b,
        "difference_95ci": [float(np.quantile(differences, 0.025)), float(np.quantile(differences, 0.975))],
        "bootstrap_iterations": AUC_BOOTSTRAPS,
    }


def binary_pair_counts(a: np.ndarray, b: np.ndarray) -> dict:
    return {
        "both_correct": int(np.sum((a == 1) & (b == 1))),
        "jev_only_correct": int(np.sum((a == 1) & (b == 0))),
        "other_only_correct": int(np.sum((a == 0) & (b == 1))),
        "both_wrong": int(np.sum((a == 0) & (b == 0))),
    }


def compare_methods(jev: dict, other: dict, other_key: str, seed_offset: int) -> dict:
    keys_zh = sorted(key for key in jev if key[0] == "zh")
    keys_en = sorted(key for key in jev if key[0] == "en")
    keys = keys_zh + keys_en
    if set(keys) != set(other):
        raise ValueError(f"source mismatch for {other_key}")

    metric_specs = {
        "article_detection": ("article_detection", 1),
        "block_accuracy": ("block_accuracy_count", 3),
        "strict_localization": ("strict_localization", 1),
        "target_detection": ("target_detection", 1),
        "human_specificity": ("human_specificity_count", 2),
    }
    metrics = {}
    for index, (metric, (field, denominator)) in enumerate(metric_specs.items()):
        a = np.asarray([jev[key][field] for key in keys], dtype=np.int16)
        b = np.asarray([other[key][field] for key in keys], dtype=np.int16)
        diff = a - b
        diff_zh = diff[: len(keys_zh)]
        diff_en = diff[len(keys_zh) :]
        metric_result = {
            "jev_rate": float(a.sum() / (len(keys) * denominator)),
            "other_rate": float(b.sum() / (len(keys) * denominator)),
            "difference": float(diff.sum() / (len(keys) * denominator)),
            "difference_95ci": paired_bootstrap_ci(diff_zh, diff_en, denominator, seed_offset=seed_offset + index),
            "cluster_exact_p": exact_cluster_signflip_p(diff),
            "cluster_count": len(keys),
            "denominator_per_cluster": denominator,
        }
        if metric == "block_accuracy":
            individual_a = np.concatenate([jev[key]["block_correct"] for key in keys])
            individual_b = np.concatenate([other[key]["block_correct"] for key in keys])
        elif metric == "human_specificity":
            individual_a = np.concatenate([jev[key]["human_correct"] for key in keys])
            individual_b = np.concatenate([other[key]["human_correct"] for key in keys])
        else:
            individual_a, individual_b = a, b
        metric_result["paired_counts"] = binary_pair_counts(individual_a, individual_b)
        metrics[metric] = metric_result

    return {
        "other_method": other_key,
        "n_articles": 200,
        "n_blocks": 600,
        "metrics": metrics,
        "block_auc": auc_difference(jev, other, keys_zh, keys_en, seed_offset + 100),
    }


def holm_adjust(comparisons: dict) -> None:
    tests = []
    for comparison_key, comparison in comparisons.items():
        for metric_key, metric in comparison["metrics"].items():
            tests.append((metric["cluster_exact_p"], comparison_key, metric_key))
    tests.sort()
    running = 0.0
    m = len(tests)
    for rank, (p_value, comparison_key, metric_key) in enumerate(tests):
        adjusted = min(1.0, (m - rank) * p_value)
        running = max(running, adjusted)
        comparisons[comparison_key]["metrics"][metric_key]["holm_p"] = running


def p_text(value: float) -> str:
    if value < 0.0001:
        return "<0.0001"
    return f"{value:.4f}"


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def pp(value: float) -> str:
    return f"{100 * value:+.1f} pp"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    loaded = {key: build_method(load_predictions(path)) for key, path in METHODS.items()}
    comparisons = {
        "jev_vs_gpt4omini": compare_methods(loaded["jev"], loaded["gpt4omini"], "gpt4omini", 1000),
        "jev_vs_gpt56luna": compare_methods(loaded["jev"], loaded["gpt56luna"], "gpt56luna", 2000),
    }
    holm_adjust(comparisons)

    jev_cost = json.loads((ASSET / "mixed_jev_summary.json").read_text(encoding="utf-8"))["cost"]["total"]["cost_usd"]
    gpt4_cost = json.loads((EXPERIMENT / "result" / "gpt4omini" / "run_summary.json").read_text(encoding="utf-8"))["total_cost_usd"]
    gpt56_cost = json.loads((EXPERIMENT / "result" / "gpt56luna" / "run_summary.json").read_text(encoding="utf-8"))["total_cost_usd"]
    summary = {
        "threshold": THRESHOLD,
        "bootstrap_iterations": BOOTSTRAPS,
        "auc_bootstrap_iterations": AUC_BOOTSTRAPS,
        "bootstrap_design": "stratified by language; resampling unit is source article with all three blocks",
        "p_value_design": "exact paired cluster sign-flip; Holm correction across 10 binary primary/secondary tests",
        "cost_usd": {"jev": jev_cost, "gpt4omini": gpt4_cost, "gpt56luna": gpt56_cost},
        "comparisons": comparisons,
    }
    (OUT / "paired_statistical_tests.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Jev 与 GPT 基线的配对统计检验",
        "",
        "Jev、GPT-4o-mini、GPT-5.6 Luna 判断完全相同的 200 篇混合文章及 600 个文本块。所有差值均定义为 `Jev − GPT`；正值表示 Jev 更高，负值表示 GPT 更高。95% 置信区间采用按语言分层、以整篇文章为聚类单位的配对 bootstrap（20,000 次），同一篇的三个块始终共同抽样。P 值采用文章聚类的精确配对符号翻转检验；单文章二元指标等价于精确 McNemar 检验。10 个二元检验统一使用 Holm 校正。",
        "",
        "## 合并中英文结果",
        "",
        "| 配对 | 指标 | Jev | GPT | 差值（Jev−GPT） | 差值 95% CI | 原始 p | Holm p |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for comparison_key in ("jev_vs_gpt4omini", "jev_vs_gpt56luna"):
        comparison = comparisons[comparison_key]
        other_key = comparison["other_method"]
        pair_label = f"Jev vs {LABELS[other_key]}"
        for metric_key in ("article_detection", "block_accuracy", "strict_localization", "target_detection", "human_specificity"):
            metric = comparison["metrics"][metric_key]
            ci = metric["difference_95ci"]
            lines.append(
                f"| {pair_label} | {METRIC_LABELS[metric_key]} | {pct(metric['jev_rate'])} | "
                f"{pct(metric['other_rate'])} | {pp(metric['difference'])} | "
                f"[{pp(ci[0])}, {pp(ci[1])}] | {p_text(metric['cluster_exact_p'])} | {p_text(metric['holm_p'])} |"
            )
        auc = comparison["block_auc"]
        ci = auc["difference_95ci"]
        lines.append(
            f"| {pair_label} | 块级 ROC-AUC | {auc['jev_auc']:.3f} | {auc['other_auc']:.3f} | "
            f"{auc['difference']:+.3f} | [{ci[0]:+.3f}, {ci[1]:+.3f}] | — | — |"
        )

    lines += [
        "",
        "## 配对不一致计数",
        "",
        "下表给出两种方法作答不一致的方向；块级准确率以 600 个块计，人工块正确排除率以 400 个人工块计，其显著性检验仍按文章聚类。",
        "",
        "| 配对 | 指标 | 仅 Jev 正确 | 仅 GPT 正确 |",
        "| --- | --- | ---: | ---: |",
    ]
    for comparison_key in ("jev_vs_gpt4omini", "jev_vs_gpt56luna"):
        comparison = comparisons[comparison_key]
        pair_label = f"Jev vs {LABELS[comparison['other_method']]}"
        for metric_key in ("article_detection", "block_accuracy", "strict_localization", "target_detection", "human_specificity"):
            counts = comparison["metrics"][metric_key]["paired_counts"]
            lines.append(
                f"| {pair_label} | {METRIC_LABELS[metric_key]} | {counts['jev_only_correct']} | {counts['other_only_correct']} |"
            )

    c4 = comparisons["jev_vs_gpt4omini"]
    c56 = comparisons["jev_vs_gpt56luna"]
    lines += [
        "",
        "## 解释",
        "",
        "### Jev 与 GPT-4o-mini",
        "",
        "Jev 在整篇检出率、块级准确率、AI 块定位、AI 块阈值检出和人工块正确排除上均具有大幅且经 Holm 校正后仍显著的优势。GPT-4o-mini 的直接概率提示发生边界坍缩，因此这一比较反映的是该模型与该提示协议组合的实际表现。",
        "",
        "### Jev 与 GPT-5.6 Luna",
        "",
        "GPT-5.6 Luna 的整篇检出率比 Jev 高 22.0 个百分点，校正后仍显著。Jev 的 AI 块阈值检出率高 9.0 个百分点，校正后仍显著。Jev 的块级准确率高 2.3 个百分点：未校正的聚类检验 p=0.0436，普通 95% bootstrap 区间为 +0.3 至 +4.3 个百分点，但经过 10 项 Holm 多重比较校正后 p=0.1307，不能按 0.05 水平认定为显著。严格定位率差 1.5 个百分点、人工块正确排除率差 −1.0 个百分点，均不显著；块级 ROC-AUC 差为 0.001，bootstrap 区间跨 0，也没有可辨别差异。",
        "",
        "统计显著不等于实际重要。费用不是抽样估计：同样 800 次判断，Jev 为 "
        f"`${jev_cost:.6f}`，GPT-4o-mini 为 `${gpt4_cost:.6f}`，GPT-5.6 Luna 为 `${gpt56_cost:.6f}`。",
        "",
        "## 限制",
        "",
        "整篇混合文章全部为阳性，因此整篇指标只能比较检出率，不能计算包含人工阴性文章的整篇特异度或完整准确率。混合语料只由 GPT-4o-mini 生成，尚未覆盖其他生成模型和句子级混写。GPT-4o-mini 与 GPT-5.6 Luna 使用不同的概率提取协议，因此二者之间不能作纯模型能力归因。",
    ]
    (OUT / "PAIRED_STATISTICAL_TESTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
