"""Compare a GPT baseline with Jev on the established mixed-text benchmark."""

from __future__ import annotations

import csv
import json
import math
import os
import statistics
from collections import Counter
from pathlib import Path


EXPERIMENT = Path(os.environ.get(
    "JEV_EXPERIMENT",
    r"C:\Users\asus\Desktop\Jev文章AI检测实验\what-the-jev\experiments\ai-writing-detection",
))
GPT_DIR = Path(os.environ.get(
    "GPT_BASELINE_OUTPUT",
    r"C:\Users\asus\Documents\ChatGPT\what-the-jev\gpt4omini_baseline_output",
))
GPT_TAG = os.environ.get("GPT_BASELINE_TAG", "gpt4omini")
GPT_LABEL = os.environ.get("GPT_BASELINE_LABEL", "GPT-4o-mini")
REPORT_STEM = os.environ.get("GPT_COMPARISON_STEM", f"JEV_VS_{GPT_TAG.upper()}")
REPORT = Path(os.environ.get(
    "GPT_COMPARISON_OUTPUT",
    r"C:\Users\asus\Documents\ChatGPT\what-the-jev\gpt4omini_comparison_output",
))
THRESHOLD = 0.5


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> list[float]:
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [center - margin, center + margin]


def roc_auc(positive: list[float], negative: list[float]) -> float:
    wins = ties = 0
    for pos in positive:
        for neg in negative:
            wins += pos > neg
            ties += pos == neg
    return (wins + 0.5 * ties) / (len(positive) * len(negative))


def load_gpt(path: Path) -> dict[str, dict]:
    records = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record.get("error") is not None:
            raise ValueError(f"unresolved error in {path}: {record['id']}")
        if record["id"] in records:
            raise ValueError(f"duplicate id in {path}: {record['id']}")
        records[record["id"]] = record
    return records


def evaluate_language(language: str) -> tuple[dict, list[dict]]:
    data = EXPERIMENT / "data"
    articles = json.loads((data / f"dataset.article-mixed.{language}.json").read_text(encoding="utf-8"))["samples"]
    blocks = json.loads((data / f"dataset.block-mixed.{language}.json").read_text(encoding="utf-8"))["samples"]
    article_results = load_gpt(GPT_DIR / f"responses.{GPT_TAG}.article-mixed.{language}.jsonl")
    block_results = load_gpt(GPT_DIR / f"responses.{GPT_TAG}.block-mixed.{language}.jsonl")
    if len(articles) != 100 or len(article_results) != 100:
        raise ValueError(f"article count mismatch for {language}")
    if len(blocks) != 300 or len(block_results) != 300:
        raise ValueError(f"block count mismatch for {language}")

    article_rows = []
    output_rows = []
    for sample in articles:
        probability = float(article_results[sample["id"]]["probability"])
        source_id = sample["metadata"]["source_id"]
        target = int(sample["metadata"]["ai_block_index"])
        article_rows.append({"source_id": source_id, "target": target, "probability": probability})
        output_rows.append({
            "method": GPT_TAG, "language": language, "source_id": source_id,
            "unit": "article", "block_index": "", "target_position": target,
            "truth": True, "probability": probability,
        })

    by_source: dict[str, list[dict]] = {}
    for sample in blocks:
        probability = float(block_results[sample["id"]]["probability"])
        source_id = sample["metadata"]["source_id"]
        index = int(sample["metadata"]["block_index"])
        target = int(sample["metadata"]["ai_block_index"])
        truth = bool(sample["reference"]["ai_authorship"])
        row = {"block_index": index, "target": target, "truth": truth, "probability": probability}
        by_source.setdefault(source_id, []).append(row)
        output_rows.append({
            "method": GPT_TAG, "language": language, "source_id": source_id,
            "unit": "block", "block_index": index, "target_position": target,
            "truth": truth, "probability": probability,
        })

    source_rows = []
    target_probs = []
    human_probs = []
    for source_id, rows in by_source.items():
        rows.sort(key=lambda row: row["block_index"])
        target_row = next(row for row in rows if row["truth"])
        humans = [row for row in rows if not row["truth"]]
        target_probability = target_row["probability"]
        max_human = max(row["probability"] for row in humans)
        target_probs.append(target_probability)
        human_probs.extend(row["probability"] for row in humans)
        source_rows.append({
            "source_id": source_id,
            "target": target_row["target"],
            "strict_top": target_probability > max_human,
            "top_or_tied": target_probability >= max_human,
            "exact_threshold": target_probability >= THRESHOLD and all(row["probability"] < THRESHOLD for row in humans),
            "target_detected": target_probability >= THRESHOLD,
        })

    article_detected = sum(row["probability"] >= THRESHOLD for row in article_rows)
    strict_top = sum(row["strict_top"] for row in source_rows)
    target_detected = sum(probability >= THRESHOLD for probability in target_probs)
    false_positives = sum(probability >= THRESHOLD for probability in human_probs)
    summary = {
        "article": {
            "n": 100,
            "detected": article_detected,
            "detection_rate": article_detected / 100,
            "detection_95ci": wilson(article_detected, 100),
            "mean_probability": statistics.mean(row["probability"] for row in article_rows),
        },
        "localization": {
            "n": 100,
            "strict_top": strict_top,
            "strict_top_rate": strict_top / 100,
            "strict_top_95ci": wilson(strict_top, 100),
            "top_or_tied_rate": sum(row["top_or_tied"] for row in source_rows) / 100,
            "exact_threshold_rate": sum(row["exact_threshold"] for row in source_rows) / 100,
            "target_block_detection_rate": target_detected / 100,
            "human_block_false_positive_rate": false_positives / 200,
            "block_accuracy": (target_detected + 200 - false_positives) / 300,
            "block_roc_auc": roc_auc(target_probs, human_probs),
            "mean_target_probability": statistics.mean(target_probs),
            "mean_human_probability": statistics.mean(human_probs),
            "by_position": {},
        },
        "output_distribution": {
            "article": dict(sorted(Counter(float(record["probability"]) for record in article_results.values()).items())),
            "block": dict(sorted(Counter(float(record["probability"]) for record in block_results.values()).items())),
        },
    }
    for position in (1, 2, 3):
        article_position = [row for row in article_rows if row["target"] == position]
        source_position = [row for row in source_rows if row["target"] == position]
        summary["article"].setdefault("by_position", {})[str(position)] = {
            "n": len(article_position),
            "detection_rate": sum(row["probability"] >= THRESHOLD for row in article_position) / len(article_position),
        }
        summary["localization"]["by_position"][str(position)] = {
            "n": len(source_position),
            "strict_top_rate": sum(row["strict_top"] for row in source_position) / len(source_position),
        }
    return summary, output_rows


def main() -> None:
    REPORT.mkdir(parents=True, exist_ok=True)
    asset = REPORT / "asset"
    asset.mkdir(parents=True, exist_ok=True)
    all_gpt_records = []
    for language in ("zh", "en"):
        for unit in ("article", "block"):
            all_gpt_records.extend(
                load_gpt(GPT_DIR / f"responses.{GPT_TAG}.{unit}-mixed.{language}.jsonl").values()
            )
    if len(all_gpt_records) != 800:
        raise ValueError(f"expected 800 GPT records, found {len(all_gpt_records)}")
    model_names = {record["model"] for record in all_gpt_records}
    if len(model_names) != 1:
        raise ValueError(f"mixed GPT models: {sorted(model_names)}")
    gpt_run = {
        "model": next(iter(model_names)),
        "total_cost_usd": sum(float(record.get("usage", {}).get("cost") or 0) for record in all_gpt_records),
        "total_prompt_tokens": sum(int(record.get("usage", {}).get("prompt_tokens") or 0) for record in all_gpt_records),
        "total_completion_tokens": sum(int(record.get("usage", {}).get("completion_tokens") or 0) for record in all_gpt_records),
    }
    jev = json.loads((EXPERIMENT / "report" / "asset" / "mixed_jev_summary.json").read_text(encoding="utf-8"))
    summary = {
        "threshold": THRESHOLD,
        "gpt_model": gpt_run["model"],
        "languages": {},
        "cost": {
            "jev_usd": float(jev["cost"]["total"]["cost_usd"]),
            "gpt_usd": float(gpt_run["total_cost_usd"]),
        },
    }
    prediction_rows = []
    for language in ("zh", "en"):
        language_summary, rows = evaluate_language(language)
        summary["languages"][language] = language_summary
        prediction_rows.extend(rows)

    summary["combined"] = {
        "article_detection_rate": sum(summary["languages"][lang]["article"]["detected"] for lang in ("zh", "en")) / 200,
        "strict_localization_rate": sum(summary["languages"][lang]["localization"]["strict_top"] for lang in ("zh", "en")) / 200,
        "target_block_detection_rate": sum(round(summary["languages"][lang]["localization"]["target_block_detection_rate"] * 100) for lang in ("zh", "en")) / 200,
        "human_block_false_positive_rate": sum(round(summary["languages"][lang]["localization"]["human_block_false_positive_rate"] * 200) for lang in ("zh", "en")) / 400,
    }
    summary["combined"]["block_accuracy"] = (
        summary["combined"]["target_block_detection_rate"] * 200
        + (1 - summary["combined"]["human_block_false_positive_rate"]) * 400
    ) / 600
    cost = summary["cost"]
    cost["gpt_to_jev_ratio"] = cost["gpt_usd"] / cost["jev_usd"]
    cost["jev_savings_fraction"] = 1 - cost["jev_usd"] / cost["gpt_usd"]
    cost["jev_per_1000_decisions_usd"] = cost["jev_usd"] / 800 * 1000
    cost["gpt_per_1000_decisions_usd"] = cost["gpt_usd"] / 800 * 1000

    (asset / f"jev_vs_{GPT_TAG}_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (asset / f"{GPT_TAG}_predictions.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(prediction_rows[0]))
        writer.writeheader()
        writer.writerows(prediction_rows)

    def pct(value: float) -> str:
        return f"{100 * value:.1f}%"

    lines = [
        f"# Jev 与 {GPT_LABEL} 人机混合文本检测对照",
        "",
        f"两种方法读取完全相同的中英文 200 篇混合文章及其 600 个文本块，共各做 800 次判断。阈值统一为 0.50；定位指标为每篇三个块中，真实 AI 块的概率严格高于两个人工块。{GPT_LABEL} 使用固定模型 `{gpt_run['model']}`、`temperature=0`。",
        "",
        "## 效果",
        "",
        "| 方法 | 语言 | 混合整篇检出率 | 块级准确率 | AI 块严格定位率 | AI 块阈值检出率 | 人工块误报率 | 块级 ROC-AUC |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for method in ("Jev", GPT_LABEL):
        for language, label in (("zh", "中文"), ("en", "英文")):
            if method == "Jev":
                article = jev["languages"][language]["article"]
                localization = jev["languages"][language]["localization"]
            else:
                article = summary["languages"][language]["article"]
                localization = summary["languages"][language]["localization"]
            block_accuracy = localization.get("block_accuracy")
            if block_accuracy is None:
                block_accuracy = (
                    localization["target_block_detection_rate"] * 100
                    + (1 - localization["human_block_false_positive_rate"]) * 200
                ) / 300
            lines.append(
                f"| {method} | {label} | {pct(article['detection_rate'])} | {pct(block_accuracy)} | "
                f"{pct(localization['strict_top_rate'])} | {pct(localization['target_block_detection_rate'])} | "
                f"{pct(localization['human_block_false_positive_rate'])} | {localization['block_roc_auc']:.3f} |"
            )
    jc = jev["combined"]
    gc = summary["combined"]
    jev_block_accuracy = (
        jc["target_block_detection_rate"] * 200
        + (1 - jc["human_block_false_positive_rate"]) * 400
    ) / 600
    lines += [
        "",
        "### 中英文合计",
        "",
        "| 方法 | 整篇检出率 | 块级准确率 | AI 块严格定位率 | AI 块阈值检出率 | 人工块误报率 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        f"| Jev | {pct(jc['article_detection_rate'])} | {pct(jev_block_accuracy)} | {pct(jc['strict_localization_rate'])} | {pct(jc['target_block_detection_rate'])} | {pct(jc['human_block_false_positive_rate'])} |",
        f"| {GPT_LABEL} | {pct(gc['article_detection_rate'])} | {pct(gc['block_accuracy'])} | {pct(gc['strict_localization_rate'])} | {pct(gc['target_block_detection_rate'])} | {pct(gc['human_block_false_positive_rate'])} |",
        "",
        "## 检测费用",
        "",
        "| 方法 | 判断数 | 实际费用 | 平均每次 | 每 1,000 次按本语料估算 |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| Jev | 800 | ${cost['jev_usd']:.6f} | ${cost['jev_usd']/800:.8f} | ${cost['jev_per_1000_decisions_usd']:.4f} |",
        f"| {GPT_LABEL} | 800 | ${cost['gpt_usd']:.6f} | ${cost['gpt_usd']/800:.8f} | ${cost['gpt_per_1000_decisions_usd']:.4f} |",
        "",
        f"在本批相同输入上，{GPT_LABEL} 的检测费用是 Jev 的 **{cost['gpt_to_jev_ratio']:.2f} 倍**；换言之，Jev 比 {GPT_LABEL} **节省 {100*cost['jev_savings_fraction']:.1f}%** 的检测费用。此处不计构建测试语料的改写费用。",
        "",
        f"## {GPT_LABEL} 输出行为",
        "",
        f"概率分布见汇总 JSON 的 `output_distribution`。本次 {GPT_LABEL} 使用标签加置信度协议，再把置信度换算为 AI 概率，以避免直接概率提示的边界坍缩。",
        "",
        "## 限制",
        "",
        f"混合语料中的 AI 块由 GPT-4o-mini 生成，而本次检测器是 {GPT_LABEL}，不存在同一模型自检，但仍只覆盖一种生成模型。该结果适合回答当前固定语料上的成本—效果比较，不能替代使用其他生成模型的外部验证。整篇混合集全部为阳性样本，因此整篇只报告检出率；人工误报率来自 400 个保持不变的人工块。",
    ]
    (REPORT / f"{REPORT_STEM}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        labels = ["Whole article", "AI block ranked first", "AI block >= 0.5", "Human-block specificity"]
        jev_values = [
            jc["article_detection_rate"], jc["strict_localization_rate"],
            jc["target_block_detection_rate"], 1 - jc["human_block_false_positive_rate"],
        ]
        gpt_values = [
            gc["article_detection_rate"], gc["strict_localization_rate"],
            gc["target_block_detection_rate"], 1 - gc["human_block_false_positive_rate"],
        ]
        x = list(range(len(labels)))
        fig, axis = plt.subplots(figsize=(10, 5))
        axis.bar([value - 0.19 for value in x], jev_values, width=0.38, label="Jev")
        axis.bar([value + 0.19 for value in x], gpt_values, width=0.38, label=GPT_LABEL)
        axis.set_xticks(x, labels)
        axis.set_ylim(0, 1.08)
        axis.set_ylabel("Rate")
        axis.grid(axis="y", alpha=0.25)
        axis.legend()
        fig.tight_layout()
        fig.savefig(asset / f"jev_vs_{GPT_TAG}.png", dpi=180)
        plt.close(fig)
    except ImportError:
        pass

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
