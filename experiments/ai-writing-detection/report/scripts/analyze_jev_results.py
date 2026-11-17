"""Analyze Jev article and three-block AI-rewrite detection results."""

import csv
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path


EXPERIMENT = Path(__file__).resolve().parents[2]
DATA = EXPERIMENT / "data"
RESULT = EXPERIMENT / "result"
REPORT = EXPERIMENT / "report"
ASSET = REPORT / "asset"
THRESHOLD = 0.50


RUNS = [
    ("article", "zh", DATA / "dataset.article-human-rewritten.zh.json", RESULT / "responses.noul.article-human-rewritten.zh.jsonl"),
    ("article", "en", DATA / "dataset.article-human-rewritten.en.json", RESULT / "responses.noul.article-human-rewritten.en.jsonl"),
    ("block", "zh", DATA / "dataset.block-human-rewritten.zh.json", RESULT / "responses.noul.block-human-rewritten.zh.jsonl"),
    ("block", "en", DATA / "dataset.block-human-rewritten.en.json", RESULT / "responses.noul.block-human-rewritten.en.jsonl"),
]


def load_rows():
    rows = []
    for unit, language, dataset_path, result_path in RUNS:
        dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
        samples = {sample["id"]: sample for sample in dataset["samples"]}
        records = {}
        for line in result_path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            if record["id"] in records:
                raise ValueError(f"Duplicate result id: {record['id']}")
            if record["error"] is not None:
                raise ValueError(f"Unresolved result error: {record['id']}: {record['error']}")
            records[record["id"]] = record
        if set(samples) != set(records):
            raise ValueError(f"Dataset/result mismatch for {unit}/{language}")
        for sample_id, sample in samples.items():
            response = records[sample_id]["response"]
            probability = float(response["answers"]["ai_authorship"]["noul"])
            if not 0 <= probability <= 1:
                raise ValueError(f"Invalid probability: {sample_id}")
            usage = response["usage"]
            meta = sample["metadata"]
            rows.append({
                "id": sample_id,
                "unit": unit,
                "language": language,
                "source_id": meta["source_id"],
                "condition": meta["condition"],
                "block_index": meta.get("block_index"),
                "truth": bool(sample["reference"]["ai_authorship"]),
                "probability": probability,
                "predicted": probability >= THRESHOLD,
                "input_tokens": int(usage["input_tokens"]),
                "output_tokens": int(usage.get("output_tokens", 0)),
                "cost_usd": float(usage["cost"]),
                "model": response["model"],
                "provider": response["provider"],
            })
    return rows


def roc_auc(rows):
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
        average_rank = (position + position + (end - index) - 1) / 2
        rank_sum += average_rank * sum(label for _, label in ordered[index:end])
        position += end - index
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def safe_div(a, b):
    return a / b if b else None


def metrics(rows):
    tp = sum(row["truth"] and row["predicted"] for row in rows)
    tn = sum(not row["truth"] and not row["predicted"] for row in rows)
    fp = sum(not row["truth"] and row["predicted"] for row in rows)
    fn = sum(row["truth"] and not row["predicted"] for row in rows)
    sensitivity = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    precision = safe_div(tp, tp + fp)
    return {
        "n": len(rows), "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "accuracy": safe_div(tp + tn, len(rows)),
        "sensitivity": sensitivity,
        "specificity": specificity,
        "precision": precision,
        "f1": safe_div(2 * precision * sensitivity, precision + sensitivity) if precision is not None and sensitivity is not None and precision + sensitivity else None,
        "balanced_accuracy": (sensitivity + specificity) / 2,
        "roc_auc": roc_auc(rows),
        "brier": statistics.mean((row["probability"] - int(row["truth"])) ** 2 for row in rows),
        "mean_human_probability": statistics.mean(row["probability"] for row in rows if not row["truth"]),
        "mean_ai_probability": statistics.mean(row["probability"] for row in rows if row["truth"]),
        "median_human_probability": statistics.median(row["probability"] for row in rows if not row["truth"]),
        "median_ai_probability": statistics.median(row["probability"] for row in rows if row["truth"]),
    }


def percentile(values, q):
    values = sorted(values)
    at = (len(values) - 1) * q
    lo = math.floor(at)
    hi = math.ceil(at)
    return values[lo] if lo == hi else values[lo] * (hi - at) + values[hi] * (at - lo)


def cluster_bootstrap(rows, repetitions=2000):
    by_source = defaultdict(list)
    for row in rows:
        by_source[row["source_id"]].append(row)
    source_ids = sorted(by_source)
    rng = random.Random(20261026)
    fields = ("accuracy", "sensitivity", "specificity", "roc_auc")
    draws = {field: [] for field in fields}
    for _ in range(repetitions):
        sampled = []
        for source_id in rng.choices(source_ids, k=len(source_ids)):
            sampled.extend(by_source[source_id])
        current = metrics(sampled)
        for field in fields:
            draws[field].append(current[field])
    return {field: [percentile(draws[field], 0.025), percentile(draws[field], 0.975)] for field in fields}


def paired_summary(rows, unit):
    keyed = defaultdict(dict)
    for row in rows:
        key = (row["source_id"], row["block_index"] if unit == "block" else None)
        keyed[key][row["condition"]] = row
    deltas = []
    for pair in keyed.values():
        if set(pair) != {"human", "ai_rewritten"}:
            raise ValueError("Incomplete matched pair")
        deltas.append(pair["ai_rewritten"]["probability"] - pair["human"]["probability"])
    return {
        "pairs": len(deltas),
        "ai_probability_higher": sum(delta > 0 for delta in deltas) / len(deltas),
        "ties": sum(delta == 0 for delta in deltas) / len(deltas),
        "mean_probability_difference": statistics.mean(deltas),
        "median_probability_difference": statistics.median(deltas),
    }


def block_localization(rows):
    positions = {}
    for index in (1, 2, 3):
        subset = [row for row in rows if row["block_index"] == index]
        positions[str(index)] = metrics(subset)
    by_source = defaultdict(list)
    for row in rows:
        by_source[row["source_id"]].append(row)
    source_stats = {
        "all_three_ai_blocks_detected": 0,
        "at_least_one_ai_block_detected": 0,
        "majority_ai_blocks_detected": 0,
        "all_three_human_blocks_rejected": 0,
    }
    for source_rows in by_source.values():
        ai = [row for row in source_rows if row["truth"]]
        human = [row for row in source_rows if not row["truth"]]
        ai_hits = sum(row["predicted"] for row in ai)
        source_stats["all_three_ai_blocks_detected"] += ai_hits == 3
        source_stats["at_least_one_ai_block_detected"] += ai_hits >= 1
        source_stats["majority_ai_blocks_detected"] += ai_hits >= 2
        source_stats["all_three_human_blocks_rejected"] += all(not row["predicted"] for row in human)
    return {
        "positions": positions,
        "sources": len(by_source),
        **{key: value / len(by_source) for key, value in source_stats.items()},
    }


def fmt(value, digits=3):
    return f"{value:.{digits}f}"


def main():
    rows = load_rows()
    ASSET.mkdir(parents=True, exist_ok=True)
    prediction_path = ASSET / "jev_predictions.csv"
    fields = list(rows[0])
    with prediction_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    summary = {"threshold": THRESHOLD, "groups": {}, "cost": {}, "models": sorted({row["model"] for row in rows})}
    for unit in ("article", "block"):
        for language in ("zh", "en"):
            subset = [row for row in rows if row["unit"] == unit and row["language"] == language]
            key = f"{unit}_{language}"
            summary["groups"][key] = metrics(subset)
            summary["groups"][key]["cluster_bootstrap_95ci"] = cluster_bootstrap(subset)
            summary["groups"][key]["paired"] = paired_summary(subset, unit)
            if unit == "block":
                summary["groups"][key]["localization"] = block_localization(subset)
            summary["cost"][key] = {
                "requests": len(subset),
                "input_tokens": sum(row["input_tokens"] for row in subset),
                "cost_usd": sum(row["cost_usd"] for row in subset),
                "mean_cost_usd": statistics.mean(row["cost_usd"] for row in subset),
            }
    summary["cost"]["total"] = {
        "requests": len(rows),
        "input_tokens": sum(row["input_tokens"] for row in rows),
        "cost_usd": sum(row["cost_usd"] for row in rows),
        "mean_cost_usd": statistics.mean(row["cost_usd"] for row in rows),
    }
    (ASSET / "jev_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Jev 中英文散文 AI 改写识别结果",
        "",
        "本报告使用 `typesafe/jev-1.14-20261014`。主阈值在分析前固定为 0.50；ROC-AUC 不依赖阈值。置信区间以来源文章为簇进行 2,000 次 bootstrap。",
        "",
        "## 主要发现",
        "",
        "- 英文整篇识别准确率为 99.5%，100 篇 AI 改写仅漏判 1 篇，100 篇人工原文无误报；ROC-AUC 为 1.000。",
        "- 中文整篇 ROC-AUC 为 0.956，且每一组配对中 AI 改写文的概率都高于对应人工原文，说明排序信号很强；但在 0.50 阈值下只检出 52% 的 AI 改写，人工误报率为 1%。中文主要问题是阈值校准偏保守。",
        "- 英文块级准确率为 98.7%；95% 的来源文章三个 AI 块全部检出，100% 至少检出一个。",
        "- 中文块级 AI 检出率为 54.7%。开头、中间、结尾块分别为 65%、56%、43%；仅 23% 的来源文章三个 AI 块全部检出，84% 至少检出一个，存在明显的结尾块弱势。",
        "- 400 次整篇判断费用为 $0.032956；整篇加块级共 1,600 次判断，实际费用为 $0.078308。",
        "",
        "## 整篇识别",
        "",
        "| 语言 | 准确率 | AI 检出率 | 人工正确排除率 | ROC-AUC | TP / FP / TN / FN |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for language, name in (("zh", "中文"), ("en", "英文")):
        m = summary["groups"][f"article_{language}"]
        lines.append(f"| {name} | {fmt(m['accuracy'])} | {fmt(m['sensitivity'])} | {fmt(m['specificity'])} | {fmt(m['roc_auc'])} | {m['tp']} / {m['fp']} / {m['tn']} / {m['fn']} |")
    lines += ["", "## 三块识别", "", "| 语言 | 块级准确率 | AI 块检出率 | 人工块正确排除率 | ROC-AUC | 三个 AI 块全检出 | 至少检出一个 AI 块 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for language, name in (("zh", "中文"), ("en", "英文")):
        m = summary["groups"][f"block_{language}"]
        loc = m["localization"]
        lines.append(f"| {name} | {fmt(m['accuracy'])} | {fmt(m['sensitivity'])} | {fmt(m['specificity'])} | {fmt(m['roc_auc'])} | {fmt(loc['all_three_ai_blocks_detected'])} | {fmt(loc['at_least_one_ai_block_detected'])} |")
    lines += ["", "### 按位置", "", "| 语言 | 位置 | AI 块平均概率 | AI 块检出率 | 人工块平均概率 | 人工块误报率 |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for language, name in (("zh", "中文"), ("en", "英文")):
        for index in (1, 2, 3):
            m = summary["groups"][f"block_{language}"]["localization"]["positions"][str(index)]
            lines.append(f"| {name} | {index} | {fmt(m['mean_ai_probability'])} | {fmt(m['sensitivity'])} | {fmt(m['mean_human_probability'])} | {fmt(1-m['specificity'])} |")
    lines += ["", "## 实际费用", "", "| 范围 | 请求数 | 输入 token | 费用（美元） | 平均每次 |", "| --- | ---: | ---: | ---: | ---: |"]
    for key, label in (("article_zh", "中文整篇"), ("article_en", "英文整篇"), ("block_zh", "中文三块"), ("block_en", "英文三块"), ("total", "合计")):
        c = summary["cost"][key]
        lines.append(f"| {label} | {c['requests']} | {c['input_tokens']} | ${c['cost_usd']:.6f} | ${c['mean_cost_usd']:.8f} |")
    lines += [
        "",
        "## 解释边界",
        "",
        "这里的‘定位’是把完整人工文和完整 AI 改写文分别切成三个连续自然段块后，独立判断每个块。它衡量块级识别能力及开头、中间、结尾差异；由于本批文章没有人机混合真值，不能据此声称 Jev 已能在混合文章中准确指出唯一 AI 段。",
        "",
        "本结果只覆盖 GPT-4o-mini 对历史散文的实质改写。更换生成模型、体裁、年代或改写强度后，性能可能变化。",
    ]
    (REPORT / "JEV_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)
        for axis, unit, language in zip(axes.flat, ("article", "article", "block", "block"), ("zh", "en", "zh", "en")):
            subset = [row for row in rows if row["unit"] == unit and row["language"] == language]
            human = [row["probability"] for row in subset if not row["truth"]]
            ai = [row["probability"] for row in subset if row["truth"]]
            axis.hist(human, bins=20, range=(0, 1), alpha=0.62, label="Human")
            axis.hist(ai, bins=20, range=(0, 1), alpha=0.62, label="AI rewritten")
            axis.axvline(THRESHOLD, color="black", linestyle="--", linewidth=1)
            axis.set_title(f"{language.upper()} {unit}")
            axis.set_xlabel("Jev AI-authorship probability")
            axis.set_ylabel("Count")
        axes[0, 0].legend()
        fig.tight_layout()
        fig.savefig(ASSET / "jev_probability_distributions.png", dpi=180)
        plt.close(fig)
    except ImportError:
        pass
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
