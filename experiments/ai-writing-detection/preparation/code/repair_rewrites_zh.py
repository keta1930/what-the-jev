"""Targeted Chinese rewrite repairs; preserves first requests and responses."""

import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

import generate_rewrites_zh as gen
from quality_rewrites_zh import grams, script_fraction


def quality(source, output):
    ns, no = gen.visible_length(source), gen.visible_length(output)
    ps, po = script_fraction(source), script_fraction(output)
    source_grams, output_grams = grams(source), grams(output)
    overlap = len(source_grams & output_grams) / len(output_grams) if output_grams else 0
    flags = []
    if not 1200 <= no <= 2200:
        flags.append("outside_corpus_length_range")
    if not 0.8 * ns <= no <= 1.2 * ns:
        flags.append("length_outside_20pct")
    if gen.paragraph_count(output) < 6:
        flags.append("fewer_than_6_paragraphs")
    if ps is not None and po is not None and abs(ps - po) > 0.3:
        flags.append("simplified_traditional_shift")
    if overlap > 0.5:
        flags.append("high_5gram_overlap")
    return flags, overlap


def main(ids):
    key = gen.os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is absent")
    rows = {row["id"]: row for row in csv.DictReader(gen.MANIFEST.open(encoding="utf-8-sig", newline="")) if row["language"] == "zh"}
    for source_id in ids:
        row = rows[source_id]
        source = (gen.PREP / row["text_path"]).read_text(encoding="utf-8-sig").strip()
        text_path = gen.TEXT_OUT / f"{source_id}.txt"
        record_path = gen.OUT / f"{source_id}.json"
        old = text_path.read_text(encoding="utf-8").strip()
        old_record = json.loads(record_path.read_text(encoding="utf-8"))
        old_flags, old_overlap = quality(source, old)
        if not old_flags:
            print(source_id, "already valid, skip", flush=True)
            continue
        request_path = gen.OUT / f"{source_id}.retry2.request.json"
        response_path = gen.OUT / f"{source_id}.retry2.response.json"
        system = gen.SYSTEM + gen.script_instruction(source)
        if "simplified_traditional_shift" in old_flags:
            system += " 特别注意：上一版把原文字形改错了。请严格沿用原文用字，通篇不能发生简繁转换。"
        if "high_5gram_overlap" in old_flags:
            system += " 特别注意：上一版与原文过于相似。除人名、书名和必要直接引文外，不要保留连续的原文词句；在保持事实准确的前提下重新组织每一段表达。"
        payload = {
            "model": gen.MODEL,
            "temperature": gen.TEMPERATURE,
            "top_p": gen.TOP_P,
            "max_tokens": gen.MAX_TOKENS,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": gen.USER.format(body=source)},
            ],
        }
        if request_path.exists():
            saved = json.loads(request_path.read_text(encoding="utf-8"))
            if saved != payload:
                raise ValueError(f"{source_id}: retry request mismatch")
        else:
            gen.atomic_json(request_path, payload)
        if response_path.exists():
            response = json.loads(response_path.read_text(encoding="utf-8"))
        else:
            if gen.all_spend() + 0.005 > gen.BUDGET_USD:
                raise RuntimeError("Chinese generation budget would be exceeded")
            response = gen.call(payload, key)
            gen.atomic_json(response_path, response)
        choices = response.get("choices") or []
        if not choices or not isinstance((choices[0].get("message") or {}).get("content"), str):
            raise ValueError(f"{source_id}: retry response invalid")
        output = choices[0]["message"]["content"].strip()
        new_flags, new_overlap = quality(source, output)
        print(source_id, "old", old_flags, round(old_overlap, 3), "new", new_flags, round(new_overlap, 3), flush=True)
        if len(new_flags) >= len(old_flags):
            continue
        attempt1_record = gen.OUT / f"{source_id}.attempt1.record.json"
        attempt1_text = gen.OUT / f"{source_id}.attempt1.txt"
        if not attempt1_record.exists():
            shutil.copy2(record_path, attempt1_record)
        if not attempt1_text.exists():
            shutil.copy2(text_path, attempt1_text)
        gen.atomic_text(text_path, output)
        cost, cost_source = gen.get_cost(response)
        record = dict(old_record)
        record.update({
            "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
            "request_path": str(request_path.relative_to(gen.PREP)),
            "response_path": str(response_path.relative_to(gen.PREP)),
            "prompt": {"system": system, "user_template": gen.USER},
            "output_visible_characters": gen.visible_length(output),
            "output_paragraphs": gen.paragraph_count(output),
            "finish_reason": choices[0].get("finish_reason"),
            "usage": response.get("usage"),
            "cost_usd": cost,
            "cost_source": cost_source,
            "quality_checks": {
                "flags": new_flags,
                "length_within_20pct": "length_outside_20pct" not in new_flags,
                "length_within_corpus_range": "outside_corpus_length_range" not in new_flags,
                "at_least_6_paragraphs": "fewer_than_6_paragraphs" not in new_flags,
                "fivegram_overlap": new_overlap,
            },
            "prior_record_path": str(attempt1_record.relative_to(gen.PREP)),
            "prior_output_path": str(attempt1_text.relative_to(gen.PREP)),
        })
        gen.atomic_json(record_path, record)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python repair_rewrites_zh.py ZH002 [ZH004 ...]")
    main(sys.argv[1:])
