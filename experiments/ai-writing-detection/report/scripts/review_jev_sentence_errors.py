#!/usr/bin/env python3
"""Select deterministic diagnostic cases from Jev sentence predictions.

No model or external API is called. Cases are probability extrema within four
predefined outcome classes, separately for Chinese and English.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


THRESHOLD = 0.50
CASE_TYPES = (
    "high_confidence_false_positive",
    "low_confidence_false_negative",
    "high_confidence_true_positive",
    "low_confidence_true_negative",
)


def lexical_features(text: str, language: str) -> dict:
    if language == "zh":
        units = [char for char in text if "\u4e00" <= char <= "\u9fff"]
        length = len(units)
        length_bin = "very_short" if length < 8 else "short" if length < 20 else "medium" if length < 45 else "long"
        first_person = bool(re.search(r"我|我们|本人|笔者", text))
        connective = bool(re.search(r"因此|然而|不过|所以|但是|此外|总之|其实|显然|于是", text))
    else:
        units = re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE)
        length = len(units)
        length_bin = "very_short" if length < 5 else "short" if length < 12 else "medium" if length < 25 else "long"
        first_person = bool(re.search(r"\b(?:I|we|me|us|my|our|mine|ours)\b", text, flags=re.I))
        connective = bool(re.search(r"\b(?:however|therefore|thus|but|yet|moreover|indeed|nevertheless|so|then)\b", text, flags=re.I))
    quote_or_dialogue = bool(re.search(r"[\"“”‘’「」『』]", text))
    question_or_exclamation = bool(re.search(r"[?!？！]", text))
    numeric_or_reference = bool(re.search(r"\d", text))
    punctuation_count = len(re.findall(r"[^\w\s\u4e00-\u9fff]", text, flags=re.UNICODE))
    punctuation_heavy = punctuation_count >= max(4, length // 4)
    flags = []
    if length_bin in {"very_short", "short"}:
        flags.append(length_bin)
    if quote_or_dialogue:
        flags.append("quote_or_dialogue")
    if question_or_exclamation:
        flags.append("question_or_exclamation")
    if numeric_or_reference:
        flags.append("numeric_or_reference")
    if first_person:
        flags.append("first_person")
    if connective:
        flags.append("connective")
    if punctuation_heavy:
        flags.append("punctuation_heavy")
    if not flags:
        flags.append("no_rule_flag")
    return {
        "length_units": length,
        "length_bin": length_bin,
        "quote_or_dialogue": quote_or_dialogue,
        "question_or_exclamation": question_or_exclamation,
        "numeric_or_reference": numeric_or_reference,
        "first_person": first_person,
        "connective": connective,
        "punctuation_heavy": punctuation_heavy,
        "phenomenon_flags": ";".join(flags),
    }


def load_language(experiment: Path, language: str) -> list[dict]:
    dataset_path = experiment / "data" / f"dataset.sentence-mixed.{language}.json"
    result_path = experiment / "result" / f"responses.noul.sentence-mixed.{language}.jsonl"
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
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
        raise ValueError(f"dataset/result mismatch for {language}")
    rows = []
    for sample_id, sample in samples.items():
        metadata = sample["metadata"]
        response = records[sample_id]["response"]
        probability = float(response["answers"]["ai_authorship"]["noul"])
        truth = bool(sample["reference"]["ai_authorship"])
        predicted = probability >= THRESHOLD
        text = sample["input"]["state"]
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        if text_hash != metadata["output_sha256"]:
            raise ValueError(f"source text hash mismatch: {sample_id}")
        if not truth and predicted:
            case_type = "high_confidence_false_positive"
        elif truth and not predicted:
            case_type = "low_confidence_false_negative"
        elif truth and predicted:
            case_type = "high_confidence_true_positive"
        else:
            case_type = "low_confidence_true_negative"
        row = {
            "id": sample_id,
            "language": language,
            "case_type": case_type,
            "source_id": metadata["source_id"],
            "sentence_index": metadata["sentence_index"],
            "paragraph_index": metadata["paragraph_index"],
            "truth_origin": metadata["origin"],
            "truth_ai": truth,
            "jev_probability": probability,
            "predicted_ai_at_0_50": predicted,
            "text": text,
            "output_sha256": metadata["output_sha256"],
            "source_human_sha256": metadata.get("source_human_sha256"),
            "source_ai_sha256": metadata.get("source_ai_sha256"),
            "source_human_sentence_index": metadata.get("source_human_sentence_index"),
            "source_ai_sentence_index": metadata.get("source_ai_sentence_index"),
            "alignment_score": metadata.get("alignment_score"),
            "jev_model": response["model"],
        }
        row.update(lexical_features(row["text"], language))
        rows.append(row)
    return rows


def select_cases(rows: list[dict], per_group: int) -> list[dict]:
    selected = []
    for language in ("zh", "en"):
        for case_type in CASE_TYPES:
            candidates = [row for row in rows if row["language"] == language and row["case_type"] == case_type]
            reverse = case_type in {"high_confidence_false_positive", "high_confidence_true_positive"}
            candidates.sort(
                key=lambda row: (
                    -row["jev_probability"] if reverse else row["jev_probability"],
                    row["id"],
                )
            )
            for rank, row in enumerate(candidates[:per_group], 1):
                selected.append({**row, "selection_rank": rank, "candidate_count": len(candidates)})
    return selected


def write_markdown(path: Path, selected: list[dict], per_group: int) -> None:
    by_group: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in selected:
        by_group[(row["language"], row["case_type"])].append(row)
    labels = {
        "high_confidence_false_positive": "高置信误报人工句",
        "low_confidence_false_negative": "低置信漏检AI句",
        "high_confidence_true_positive": "正确高置信AI句",
        "low_confidence_true_negative": "正确低置信人工句",
    }
    lines = [
        "# Jev逐句检测典型错误案例抽查",
        "",
        "## 方法",
        "",
        f"以0.50为固定阈值，中英文分别在四个结果类别中抽取最多{per_group}条。高置信类别按Jev概率从高到低选择，低置信类别按概率从低到高选择；同分按样本ID排序。因此选择规则确定且可复现，不依赖人工主观挑选。",
        "",
        "这些样本是各类别的概率极端案例，用于诊断而非估计总体比例。语言现象由简单可复现规则编码，属于探索性定性分析，不能解释因果。完整80条案例见CSV/JSON。",
        "",
        "## 样本构成",
        "",
        "| 语言 | 类别 | 候选总数 | 抽查数 | 概率范围 |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for language, language_label in (("zh", "中文"), ("en", "英文")):
        for case_type in CASE_TYPES:
            group = by_group[(language, case_type)]
            candidate_count = group[0]["candidate_count"] if group else 0
            probabilities = [row["jev_probability"] for row in group]
            range_text = f"{min(probabilities):.2f}–{max(probabilities):.2f}" if probabilities else "—"
            lines.append(f"| {language_label} | {labels[case_type]} | {candidate_count} | {len(group)} | {range_text} |")

    lines += ["", "## 规则化语言现象汇总", "", "一个案例可同时具有多个标签。", ""]
    flag_names = ("very_short", "short", "quote_or_dialogue", "question_or_exclamation", "numeric_or_reference", "first_person", "connective", "punctuation_heavy", "no_rule_flag")
    lines += ["| 语言 | 类别 | " + " | ".join(flag_names) + " |", "| --- | --- | " + " | ".join("---:" for _ in flag_names) + " |"]
    for language, language_label in (("zh", "中文"), ("en", "英文")):
        for case_type in CASE_TYPES:
            counter = Counter(flag for row in by_group[(language, case_type)] for flag in row["phenomenon_flags"].split(";"))
            lines.append(
                f"| {language_label} | {labels[case_type]} | "
                + " | ".join(str(counter[name]) for name in flag_names)
                + " |"
            )

    lines += ["", "## 案例预览", "", "下表每组显示概率最极端的前3条；完整案例及哈希见附件。", ""]
    for language, language_label in (("zh", "中文"), ("en", "英文")):
        for case_type in CASE_TYPES:
            lines += [f"### {language_label}：{labels[case_type]}", "", "| ID | 概率 | 现象标签 | 句子 |", "| --- | ---: | --- | --- |"]
            for row in by_group[(language, case_type)][:3]:
                preview = row["text"].replace("|", "\\|").replace("\n", " ")
                if len(preview) > 160:
                    preview = preview[:157] + "…"
                lines.append(f"| {row['id']} | {row['jev_probability']:.2f} | {row['phenomenon_flags']} | {preview} |")
            lines.append("")

    lines += [
        "## 探索性观察",
        "",
        "- 极端错误并不只发生在短句；长句和普通陈述句也会进入高置信误报或低置信漏检组，说明错误不能由句长单独解释。",
        "- 引语、问句、第一人称、连接词等现象在不同类别均出现，需结合全量分层统计判断其总体关联，不能仅凭本抽查推断。",
        "- 中文漏检组的低概率极端案例说明部分GPT-4o-mini改写句在表面风格上仍非常接近人工原文；英文高置信误报则提示规范、流畅或概括式措辞也可能被Jev视为AI特征。",
        "- 本抽查适合展示模型错误形态；关于各因素是否系统性影响检测，应以实验2的全量分层结果为准。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-group", type=int, default=10)
    args = parser.parse_args()
    rows = []
    for language in ("zh", "en"):
        rows.extend(load_language(args.experiment, language))
    selected = select_cases(rows, args.per_group)
    args.output.mkdir(parents=True, exist_ok=True)
    fieldnames = list(selected[0])
    with (args.output / "jev_sentence_error_cases.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(selected)
    (args.output / "jev_sentence_error_cases.json").write_text(
        json.dumps(selected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(args.output / "ERROR_CASE_REVIEW.md", selected, args.per_group)
    summary = {
        "threshold": THRESHOLD,
        "selection": "probability extrema within four outcome classes; deterministic ID tie-break",
        "per_group_target": args.per_group,
        "selected_total": len(selected),
        "groups": [
            {
                "language": language,
                "case_type": case_type,
                "selected": len([row for row in selected if row["language"] == language and row["case_type"] == case_type]),
                "candidate_count": next((row["candidate_count"] for row in selected if row["language"] == language and row["case_type"] == case_type), 0),
            }
            for language in ("zh", "en")
            for case_type in CASE_TYPES
        ],
        "external_api_called": False,
    }
    (args.output / "error_case_review_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
