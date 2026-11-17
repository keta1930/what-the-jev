"""Analyze Jev detection and true block localization in one-AI-block essays."""

import csv
import json
import math
import os
import statistics
from pathlib import Path


EXPERIMENT = Path(os.environ.get("JEV_EXPERIMENT", Path(__file__).resolve().parents[2]))
DATA = EXPERIMENT / "data"
RESULT = EXPERIMENT / "result"
PREPARATION = EXPERIMENT / "preparation"
REPORT = Path(os.environ.get("JEV_REPORT_OUTPUT", EXPERIMENT / "report"))
ASSET = REPORT / "asset"
THRESHOLD = 0.50


def load_result(path):
    records = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["error"] is not None:
            raise ValueError(f"Unresolved error in {path.name}: {record['id']}")
        if record["id"] in records:
            raise ValueError(f"Duplicate result id: {record['id']}")
        response = record["response"]
        records[record["id"]] = {
            "probability": float(response["answers"]["ai_authorship"]["noul"]),
            "input_tokens": int(response["usage"]["input_tokens"]),
            "cost_usd": float(response["usage"]["cost"]),
            "model": response["model"],
        }
    return records


def wilson(successes, n, z=1.959963984540054):
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [center - margin, center + margin]


def roc_auc(positive, negative):
    wins = ties = 0
    for pos in positive:
        for neg in negative:
            wins += pos > neg
            ties += pos == neg
    return (wins + 0.5 * ties) / (len(positive) * len(negative))


def fmt(value):
    return f"{value:.3f}"


def main():
    ASSET.mkdir(parents=True, exist_ok=True)
    summary = {"threshold": THRESHOLD, "languages": {}, "cost": {}}
    output_rows = []
    total_cost = total_tokens = total_requests = 0

    for language in ("zh", "en"):
        prefix = "ZH" if language == "zh" else "EN"
        articles = json.loads((DATA / f"dataset.article-mixed.{language}.json").read_text(encoding="utf-8"))["samples"]
        blocks = json.loads((DATA / f"dataset.block-mixed.{language}.json").read_text(encoding="utf-8"))["samples"]
        mixed_article_results = load_result(RESULT / f"responses.noul.article-mixed.{language}.jsonl")
        mixed_block_results = load_result(RESULT / f"responses.noul.block-mixed.{language}.jsonl")
        paired_article_results = load_result(RESULT / f"responses.noul.article-human-rewritten.{language}.jsonl")
        if len(articles) != 100 or len(mixed_article_results) != 100:
            raise ValueError("Unexpected article count")
        if len(blocks) != 300 or len(mixed_block_results) != 300:
            raise ValueError("Unexpected block count")

        article_rows = []
        for sample in articles:
            source_id = sample["metadata"]["source_id"]
            target = int(sample["metadata"]["ai_block_index"])
            mixed = mixed_article_results[sample["id"]]["probability"]
            human = paired_article_results[f"{source_id}-human-article"]["probability"]
            full_ai = paired_article_results[f"{source_id}-ai-rewritten-article"]["probability"]
            article_rows.append({"source_id": source_id, "target_position": target, "mixed": mixed, "human": human, "full_ai": full_ai})
            output_rows.append({"language": language, "source_id": source_id, "unit": "article", "block_index": "", "target_position": target, "truth": True, "probability": mixed})

        by_source = {}
        for sample in blocks:
            source_id = sample["metadata"]["source_id"]
            index = int(sample["metadata"]["block_index"])
            target = int(sample["metadata"]["ai_block_index"])
            probability = mixed_block_results[sample["id"]]["probability"]
            row = {"block_index": index, "target_position": target, "truth": bool(sample["reference"]["ai_authorship"]), "probability": probability}
            by_source.setdefault(source_id, []).append(row)
            output_rows.append({"language": language, "source_id": source_id, "unit": "block", "block_index": index, "target_position": target, "truth": row["truth"], "probability": probability})

        source_rows = []
        for source_id, source_blocks in by_source.items():
            source_blocks.sort(key=lambda row: row["block_index"])
            target_row = next(row for row in source_blocks if row["truth"])
            other = [row for row in source_blocks if not row["truth"]]
            target_p = target_row["probability"]
            max_other = max(row["probability"] for row in other)
            strict_top = target_p > max_other
            top_or_tied = target_p >= max_other
            source_rows.append({
                "source_id": source_id,
                "target_position": target_row["target_position"],
                "target_probability": target_p,
                "max_human_probability": max_other,
                "strict_top": strict_top,
                "top_or_tied": top_or_tied,
                "target_detected": target_p >= THRESHOLD,
                "exact_at_threshold": target_p >= THRESHOLD and all(row["probability"] < THRESHOLD for row in other),
                "rank": 1 + sum(row["probability"] > target_p for row in other),
            })

        article_detected = sum(row["mixed"] >= THRESHOLD for row in article_rows)
        strict_top = sum(row["strict_top"] for row in source_rows)
        top_or_tied = sum(row["top_or_tied"] for row in source_rows)
        exact = sum(row["exact_at_threshold"] for row in source_rows)
        target_probs = [row["probability"] for rows in by_source.values() for row in rows if row["truth"]]
        human_probs = [row["probability"] for rows in by_source.values() for row in rows if not row["truth"]]
        block_false_positives = sum(p >= THRESHOLD for p in human_probs)
        lang_summary = {
            "article": {
                "n": 100,
                "detected": article_detected,
                "detection_rate": article_detected / 100,
                "detection_rate_95ci": wilson(article_detected, 100),
                "mean_probability": statistics.mean(row["mixed"] for row in article_rows),
                "median_probability": statistics.median(row["mixed"] for row in article_rows),
                "higher_than_original_human": sum(row["mixed"] > row["human"] for row in article_rows) / 100,
                "mean_increase_over_human": statistics.mean(row["mixed"] - row["human"] for row in article_rows),
                "lower_than_full_ai": sum(row["mixed"] < row["full_ai"] for row in article_rows) / 100,
                "by_position": {},
            },
            "localization": {
                "n": 100,
                "strict_top": strict_top,
                "strict_top_rate": strict_top / 100,
                "strict_top_95ci": wilson(strict_top, 100),
                "top_or_tied_rate": top_or_tied / 100,
                "mean_reciprocal_rank": statistics.mean(1 / row["rank"] for row in source_rows),
                "exact_at_threshold_rate": exact / 100,
                "target_block_detection_rate": sum(p >= THRESHOLD for p in target_probs) / 100,
                "human_block_false_positive_rate": block_false_positives / 200,
                "block_roc_auc": roc_auc(target_probs, human_probs),
                "mean_target_probability": statistics.mean(target_probs),
                "mean_human_probability": statistics.mean(human_probs),
                "by_position": {},
            },
        }
        for position in (1, 2, 3):
            ar = [row for row in article_rows if row["target_position"] == position]
            sr = [row for row in source_rows if row["target_position"] == position]
            lang_summary["article"]["by_position"][str(position)] = {
                "n": len(ar),
                "detection_rate": sum(row["mixed"] >= THRESHOLD for row in ar) / len(ar),
                "mean_probability": statistics.mean(row["mixed"] for row in ar),
            }
            lang_summary["localization"]["by_position"][str(position)] = {
                "n": len(sr),
                "strict_top_rate": sum(row["strict_top"] for row in sr) / len(sr),
                "top_or_tied_rate": sum(row["top_or_tied"] for row in sr) / len(sr),
                "target_detection_rate": sum(row["target_detected"] for row in sr) / len(sr),
                "mean_target_probability": statistics.mean(row["target_probability"] for row in sr),
            }
        summary["languages"][language] = lang_summary

        language_records = list(mixed_article_results.values()) + list(mixed_block_results.values())
        cost = sum(record["cost_usd"] for record in language_records)
        tokens = sum(record["input_tokens"] for record in language_records)
        summary["cost"][language] = {"requests": len(language_records), "input_tokens": tokens, "cost_usd": cost}
        total_cost += cost
        total_tokens += tokens
        total_requests += len(language_records)

    summary["cost"]["total"] = {"requests": total_requests, "input_tokens": total_tokens, "cost_usd": total_cost}
    combined_article_detected = sum(summary["languages"][lang]["article"]["detected"] for lang in ("zh", "en"))
    combined_strict_top = sum(summary["languages"][lang]["localization"]["strict_top"] for lang in ("zh", "en"))
    combined_target_detected = sum(
        round(summary["languages"][lang]["localization"]["target_block_detection_rate"] * 100)
        for lang in ("zh", "en")
    )
    combined_human_false_positives = sum(
        round(summary["languages"][lang]["localization"]["human_block_false_positive_rate"] * 200)
        for lang in ("zh", "en")
    )
    summary["combined"] = {
        "articles": 200,
        "article_detection_rate": combined_article_detected / 200,
        "article_detection_95ci": wilson(combined_article_detected, 200),
        "strict_localization_rate": combined_strict_top / 200,
        "strict_localization_95ci": wilson(combined_strict_top, 200),
        "target_block_detection_rate": combined_target_detected / 200,
        "human_block_false_positive_rate": combined_human_false_positives / 400,
    }
    generation_cost = {}
    for language in ("zh", "en"):
        audit_path = PREPARATION / "raw" / "mixed" / language / "audit_summary.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        generation_cost[language] = {
            "selected_cost_usd": float(audit["selected_cost_usd"]),
            "all_attempts_cost_usd": float(audit["all_attempts_cost_usd"]),
        }
    generation_cost["total"] = {
        "selected_cost_usd": sum(generation_cost[language]["selected_cost_usd"] for language in ("zh", "en")),
        "all_attempts_cost_usd": sum(generation_cost[language]["all_attempts_cost_usd"] for language in ("zh", "en")),
    }
    summary["generation_cost"] = generation_cost
    summary["mixed_phase_total_cost_usd"] = generation_cost["total"]["all_attempts_cost_usd"] + total_cost
    (ASSET / "mixed_jev_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (ASSET / "mixed_jev_predictions.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Jev 人机混合散文识别与定位结果",
        "",
        "每种语言 100 篇混合文章，每篇恰好一个 AI 改写块和两个未改动的人工块；AI 块位于开头、中间、结尾的数量为 34/33/33。主阈值为 0.50；定位主指标是 AI 块概率严格高于另外两个人工块。",
        "",
        "## 主要结果",
        "",
        "| 语言 | 混合整篇检出率 | AI 块严格排第一 | AI 块排第一或并列 | AI 块阈值检出率 | 人工块误报率 | 块级 ROC-AUC |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文")):
        a = summary["languages"][language]["article"]
        loc = summary["languages"][language]["localization"]
        lines.append(f"| {label} | {fmt(a['detection_rate'])} | {fmt(loc['strict_top_rate'])} | {fmt(loc['top_or_tied_rate'])} | {fmt(loc['target_block_detection_rate'])} | {fmt(loc['human_block_false_positive_rate'])} | {fmt(loc['block_roc_auc'])} |")
    combined = summary["combined"]
    lines += [
        "",
        "中英文合计 200 篇中，整篇检出 101 篇（50.5%，95% CI 43.6%–57.4%）；AI 块严格排第一 198 篇（99.0%，95% CI 96.4%–99.7%）。AI 块单独达到 0.50 阈值的比例为 83.0%，400 个人工块的误报率为 1.0%。",
    ]
    lines += ["", "## 按 AI 块位置", "", "| 语言 | 位置 | 样本数 | 整篇检出率 | 严格定位正确率 | AI 块阈值检出率 | AI 块平均概率 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for language, label in (("zh", "中文"), ("en", "英文")):
        for position, name in ((1, "开头"), (2, "中间"), (3, "结尾")):
            a = summary["languages"][language]["article"]["by_position"][str(position)]
            loc = summary["languages"][language]["localization"]["by_position"][str(position)]
            lines.append(f"| {label} | {name} | {a['n']} | {fmt(a['detection_rate'])} | {fmt(loc['strict_top_rate'])} | {fmt(loc['target_detection_rate'])} | {fmt(loc['mean_target_probability'])} |")
    lines += ["", "## 费用", "", "| 语言 | 请求数 | 输入 token | Jev 费用 |", "| --- | ---: | ---: | ---: |"]
    for language, label in (("zh", "中文"), ("en", "英文"), ("total", "合计")):
        cost = summary["cost"][language]
        lines.append(f"| {label} | {cost['requests']} | {cost['input_tokens']} | ${cost['cost_usd']:.6f} |")
    lines += [
        "",
        f"以上仅为 Jev 检测费。制作 200 篇混合样本的 GPT-4o-mini 全部改写尝试另耗 ${generation_cost['total']['all_attempts_cost_usd']:.6f}；因此本轮混合实验 API 总费用为 ${summary['mixed_phase_total_cost_usd']:.6f}，不含人工工作时间。",
    ]
    lines += [
        "",
        "## 结论与解释",
        "",
        "这些文章是人机混合文本：每篇保留两个原始人工块，只把一个块交给 GPT-4o-mini 改写。结果表明，若直接把整篇交给 Jev，约一半混合文章会漏检；若按三块分别检测并比较概率，Jev 几乎总能指出真正的 AI 改写块。因而本项目应把“分块检测 + 篇内排序”作为主流程，把整篇阈值判断作为辅助指标。",
        "",
        "整篇结果有明显位置效应：AI 块在开头时，中文整篇检出率为 0%，英文为 23.5%；在结尾时分别升至 66.7% 和 100%。这是本数据上的观察，不能在没有更多顺序实验前解释为 Jev 的固定机制。",
        "",
        "严格定位以每篇内部三块排序为准，因此不要求概率超过 0.50。`exact_at_threshold_rate` 则要求 AI 块达到 0.50 且另外两个人工块都低于 0.50，属于更严格的自动标记规则。",
        "",
        "本实验只使用 GPT-4o-mini 对一个块进行实质改写，结论不能直接外推到其他生成模型、人工后编辑、句子级混写或不同体裁。",
    ]
    (REPORT / "MIXED_JEV_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        import matplotlib.pyplot as plt
        labels = ["Overall", "Start", "Middle", "End"]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
        for axis, language in zip(axes, ("zh", "en")):
            a = summary["languages"][language]["article"]
            loc = summary["languages"][language]["localization"]
            article_rates = [a["detection_rate"]] + [a["by_position"][str(i)]["detection_rate"] for i in (1, 2, 3)]
            localization_rates = [loc["strict_top_rate"]] + [loc["by_position"][str(i)]["strict_top_rate"] for i in (1, 2, 3)]
            x = range(4)
            axis.bar([v - 0.18 for v in x], article_rates, width=0.36, label="Whole article detected")
            axis.bar([v + 0.18 for v in x], localization_rates, width=0.36, label="AI block ranked first")
            axis.set_xticks(list(x), labels)
            axis.set_ylim(0, 1.05)
            axis.set_title(language.upper())
            axis.set_ylabel("Rate")
            axis.grid(axis="y", alpha=0.25)
        axes[0].legend(loc="lower left")
        fig.tight_layout()
        fig.savefig(ASSET / "mixed_localization_rates.png", dpi=180)
        plt.close(fig)
    except ImportError:
        pass
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
