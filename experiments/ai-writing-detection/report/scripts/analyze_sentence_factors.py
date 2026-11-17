#!/usr/bin/env python3
"""Descriptive factor analysis for Jev sentence-level mixed-text errors.

The script is fully local: it joins the frozen what-the-jev datasets with the
existing result JSONL files and never calls a model or an external API.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path


THRESHOLD = 0.50
WORD = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
ZH_CONTENT = re.compile(r"[\s\W_]+", re.UNICODE)
QUOTE = re.compile(r'["“”«»「」『』]')


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    at = (len(ordered) - 1) * q
    lo = math.floor(at)
    hi = math.ceil(at)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - at) + ordered[hi] * (at - lo)


def safe_div(a: float, b: float) -> float | None:
    return a / b if b else None


def metrics(rows: list[dict]) -> dict:
    ai = [row for row in rows if row["truth"]]
    human = [row for row in rows if not row["truth"]]
    tp = sum(row["predicted"] for row in ai)
    fp = sum(row["predicted"] for row in human)
    return {
        "n": len(rows),
        "n_ai": len(ai),
        "n_human": len(human),
        "mean_probability": statistics.mean(row["probability"] for row in rows) if rows else None,
        "mean_ai_probability": statistics.mean(row["probability"] for row in ai) if ai else None,
        "mean_human_probability": statistics.mean(row["probability"] for row in human) if human else None,
        "ai_recall": safe_div(tp, len(ai)),
        "ai_false_negative_rate": safe_div(len(ai) - tp, len(ai)),
        "human_false_positive_rate": safe_div(fp, len(human)),
        "human_specificity": safe_div(len(human) - fp, len(human)),
        "tp": tp,
        "fp": fp,
    }


def length_value(text: str, language: str) -> int:
    if language == "zh":
        return len(ZH_CONTENT.sub("", text))
    return len(WORD.findall(text))


def quote_or_dialogue(text: str) -> bool:
    stripped = text.lstrip()
    return bool(QUOTE.search(text)) or stripped.startswith(("—", "–", "- "))


def assign_four_bins(value: float, cuts: list[float], unit: str) -> str:
    q1, q2, q3 = cuts
    if value <= q1:
        return f"Q1 <= {q1:g} {unit}"
    if value <= q2:
        return f"Q2 ({q1:g}, {q2:g}] {unit}"
    if value <= q3:
        return f"Q3 ({q2:g}, {q3:g}] {unit}"
    return f"Q4 > {q3:g} {unit}"


def assign_score_bin(value: float, cuts: list[float]) -> str:
    low, high = cuts
    if value <= low:
        return f"low <= {low:.3f}"
    if value <= high:
        return f"middle ({low:.3f}, {high:.3f}]"
    return f"high > {high:.3f}"


def load_rows(experiment: Path, language: str) -> list[dict]:
    dataset_path = experiment / "data" / f"dataset.sentence-mixed.{language}.json"
    result_path = experiment / "result" / f"responses.noul.sentence-mixed.{language}.jsonl"
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
        raise ValueError(f"dataset/result ID mismatch: {language}")

    totals = defaultdict(int)
    for sample in samples.values():
        totals[sample["metadata"]["source_id"]] += 1
    rows = []
    for sample_id, sample in samples.items():
        metadata = sample["metadata"]
        response = records[sample_id]["response"]
        probability = float(response["answers"]["ai_authorship"]["noul"])
        truth = bool(sample["reference"]["ai_authorship"])
        sentence_index = int(metadata["sentence_index"])
        total = totals[metadata["source_id"]]
        position_index = min(2, ((sentence_index - 1) * 3) // total)
        rows.append(
            {
                "id": sample_id,
                "language": language,
                "source_id": metadata["source_id"],
                "truth": truth,
                "origin": metadata["origin"],
                "probability": probability,
                "predicted": probability >= THRESHOLD,
                "text": sample["input"]["state"],
                "sentence_index": sentence_index,
                "sentence_count": total,
                "relative_position": (sentence_index - 0.5) / total,
                "position_group": ("beginning", "middle", "ending")[position_index],
                "alignment_score": float(metadata["alignment_score"])
                if metadata.get("alignment_score") is not None
                else None,
            }
        )
    return rows


def grouped_metrics(rows: list[dict], factor: str, category_key: str) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[row[category_key]].append(row)
    output = []
    for category, subset in groups.items():
        output.append(
            {
                "factor": factor,
                "language": subset[0]["language"],
                "category": category,
                **metrics(subset),
            }
        )
    return output


def fmt(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def strongest_range(records: list[dict], field: str) -> tuple[str, float]:
    by_factor = defaultdict(list)
    for record in records:
        value = record[field]
        if value is not None:
            by_factor[(record["language"], record["factor"])].append(value)
    candidates = [
        (f"{language}/{factor}", max(values) - min(values))
        for (language, factor), values in by_factor.items()
        if len(values) >= 2
    ]
    return max(candidates, key=lambda item: item[1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    for language in ("zh", "en"):
        all_rows.extend(load_rows(args.experiment, language))

    length_cutpoints = {}
    score_cutpoints = {}
    for language in ("zh", "en"):
        subset = [row for row in all_rows if row["language"] == language]
        for row in subset:
            row["length"] = length_value(row["text"], language)
            row["quote_dialogue"] = "quote/dialogue" if quote_or_dialogue(row["text"]) else "no quote/dialogue"
        lengths = [row["length"] for row in subset]
        cuts = [quantile(lengths, q) for q in (0.25, 0.50, 0.75)]
        # Length is integral; retaining exact interpolated cuts keeps assignment
        # deterministic and documents the empirical quartiles.
        length_cutpoints[language] = cuts
        unit = "characters" if language == "zh" else "words"
        for row in subset:
            row["length_bin"] = assign_four_bins(row["length"], cuts, unit)
        scores = [row["alignment_score"] for row in subset if row["truth"] and row["alignment_score"] is not None]
        score_cuts = [quantile(scores, q) for q in (1 / 3, 2 / 3)]
        score_cutpoints[language] = score_cuts
        for row in subset:
            row["alignment_score_bin"] = (
                assign_score_bin(row["alignment_score"], score_cuts)
                if row["truth"] and row["alignment_score"] is not None
                else None
            )

    records: list[dict] = []
    overall = {}
    for language in ("zh", "en"):
        subset = [row for row in all_rows if row["language"] == language]
        overall[language] = metrics(subset)
        records.extend(grouped_metrics(subset, "sentence_length_quartile", "length_bin"))
        records.extend(grouped_metrics(subset, "quote_or_dialogue", "quote_dialogue"))
        records.extend(grouped_metrics(subset, "article_position_third", "position_group"))
        ai_with_score = [row for row in subset if row["truth"] and row["alignment_score"] is not None]
        records.extend(grouped_metrics(ai_with_score, "ai_alignment_score_tertile", "alignment_score_bin"))

    # Stable, human-readable ordering.
    factor_order = {
        "sentence_length_quartile": 0,
        "quote_or_dialogue": 1,
        "article_position_third": 2,
        "ai_alignment_score_tertile": 3,
    }
    language_order = {"zh": 0, "en": 1}
    def category_order(row: dict) -> int:
        category = row["category"]
        if row["factor"] == "sentence_length_quartile":
            return int(category[1])
        if row["factor"] == "quote_or_dialogue":
            return 0 if category == "no quote/dialogue" else 1
        if row["factor"] == "article_position_third":
            return {"beginning": 0, "middle": 1, "ending": 2}[category]
        return 0 if category.startswith("low") else 1 if category.startswith("middle") else 2

    records.sort(
        key=lambda row: (
            factor_order[row["factor"]],
            language_order[row["language"]],
            category_order(row),
        )
    )

    summary = {
        "threshold": THRESHOLD,
        "condition": "sentence_unit_mixed_gpt4o_mini_33pct",
        "external_api_called": False,
        "length_definition": {
            "zh": "count of Unicode word/content characters after removing whitespace and punctuation",
            "en": "regex word-token count",
        },
        "quote_dialogue_definition": "contains double quotation marks (straight/smart/CJK) or begins with a dialogue dash",
        "position_definition": "sentence ordinal divided into beginning/middle/ending thirds within each mixed article",
        "alignment_definition": "empirical tertiles among AI-origin sentences only; missing human alignment scores are excluded, never imputed",
        "length_cutpoints": length_cutpoints,
        "alignment_score_cutpoints": score_cutpoints,
        "overall": overall,
        "groups": records,
    }
    (args.output / "factor_analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    fieldnames = list(records[0])
    with (args.output / "factor_group_metrics.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    recall_range_name, recall_range = strongest_range(records, "ai_recall")
    fpr_range_name, fpr_range = strongest_range(records, "human_false_positive_rate")
    def select(language: str, factor: str) -> list[dict]:
        return [
            record
            for record in records
            if record["language"] == language and record["factor"] == factor
        ]

    zh_length = select("zh", "sentence_length_quartile")
    en_length = select("en", "sentence_length_quartile")
    zh_quote = select("zh", "quote_or_dialogue")
    en_quote = select("en", "quote_or_dialogue")
    zh_score = select("zh", "ai_alignment_score_tertile")
    en_score = select("en", "ai_alignment_score_tertile")
    lines = [
        "# JEV句子级误判因素分析",
        "",
        "本分析仅使用已经完成的JEV逐句结果，不调用任何API。主阈值固定为0.50。所有结果均为描述性分层结果，不应直接解释为因果效应。",
        "",
        "## 总体基线",
        "",
        "| 语言 | 句数 | AI句 | 人工句 | AI召回率 | 人工误报率 | AI平均概率 | 人工平均概率 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for language, label in (("zh", "中文"), ("en", "英文")):
        item = overall[language]
        lines.append(
            f"| {label} | {item['n']} | {item['n_ai']} | {item['n_human']} | {fmt(item['ai_recall'])} | {fmt(item['human_false_positive_rate'])} | {fmt(item['mean_ai_probability'])} | {fmt(item['mean_human_probability'])} |"
        )
    lines += [
        "",
        "## 主要观察",
        "",
        f"- 句长是最明显的误差因素。中文AI召回率从最短四分位的 {zh_length[0]['ai_recall']:.1%} 升至最长四分位的 {zh_length[-1]['ai_recall']:.1%}；英文从 {en_length[0]['ai_recall']:.1%} 升至 {en_length[-1]['ai_recall']:.1%}。",
        f"- 引语/对话更难识别：中文AI召回率由非引语的 {zh_quote[0]['ai_recall']:.1%} 降至 {zh_quote[1]['ai_recall']:.1%}，英文由 {en_quote[0]['ai_recall']:.1%} 降至 {en_quote[1]['ai_recall']:.1%}。",
        f"- 与人工原句越相似的AI改写越难检出。中文低/高对齐相似度组召回率为 {zh_score[0]['ai_recall']:.1%}/{zh_score[-1]['ai_recall']:.1%}；英文为 {en_score[0]['ai_recall']:.1%}/{en_score[-1]['ai_recall']:.1%}。",
        f"- 分层间AI召回率跨度最大的组合为 `{recall_range_name}`（跨度 {recall_range:.3f}）；人工误报率跨度最大的是 `{fpr_range_name}`（跨度 {fpr_range:.3f}）。",
        "- 对齐相似度只在AI句内部分析；人工句的缺失对齐分数没有填充为0。",
        "- 各分层同时报告样本量，极小分层不宜单独作强结论。",
        "",
    ]

    factor_titles = {
        "sentence_length_quartile": "句长四分位",
        "quote_or_dialogue": "引语或对话",
        "article_position_third": "篇内位置",
        "ai_alignment_score_tertile": "AI句对齐相似度三分位（仅AI句）",
    }
    for factor in factor_order:
        lines += [
            f"## {factor_titles[factor]}",
            "",
            "| 语言 | 分层 | 总数 | AI句 | 人工句 | AI召回率 | 人工误报率 | AI平均概率 | 人工平均概率 |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for record in [item for item in records if item["factor"] == factor]:
            language_label = "中文" if record["language"] == "zh" else "英文"
            lines.append(
                f"| {language_label} | {record['category']} | {record['n']} | {record['n_ai']} | {record['n_human']} | {fmt(record['ai_recall'])} | {fmt(record['human_false_positive_rate'])} | {fmt(record['mean_ai_probability'])} | {fmt(record['mean_human_probability'])} |"
            )
        lines.append("")

    lines += [
        "## 方法说明与限制",
        "",
        "- 句长分箱使用各语言全部句子的经验四分位数；中文长度去除空白和标点后计字符，英文按词计数。",
        "- 引语/对话以双引号类字符或句首对话破折号识别，属于保守的规则标注。",
        "- 篇内位置按每篇混合文章的句序等分为前、中、后三段。",
        "- AI对齐相似度按各语言AI句的经验三分位数分组。它反映AI句与被替换人工语义单元的表面相似程度，不等于改写质量。",
        "- 分层因素彼此相关，例如引语往往较短；本报告用于定位误差模式，不做因果归因。",
        "",
    ]
    (args.output / "FACTOR_ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"rows": len(all_rows), "groups": len(records), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
