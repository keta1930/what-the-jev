"""Make the final Chinese corpus use one frozen rewrite prompt and keep every attempt."""

import csv
import hashlib
import json
import math
import shutil
import sys
import time

import generate_rewrites_zh as gen
from repair_rewrites_zh import quality


def expected_payload(source, retry_flags=()):
    system = gen.SYSTEM + gen.script_instruction(source)
    if "simplified_traditional_shift" in retry_flags:
        system += "【字形约束】全文逐字沿用原文的简繁用字类型，不得转换字形。"
    if "outside_corpus_length_range" in retry_flags or "length_outside_20pct" in retry_flags:
        n = gen.visible_length(source)
        lower = max(1200, math.ceil(0.8 * n))
        upper = min(2200, math.floor(1.2 * n))
        system += f"【长度约束】最终正文不计空白的可见字符必须介于 {lower} 与 {upper} 之间。"
    if "fewer_than_6_paragraphs" in retry_flags:
        system += f"【段落约束】至少六个自然段，尽量保留原文 {gen.paragraph_count(source)} 个自然段的组织。"
    if "high_5gram_overlap" in retry_flags:
        system += "【重写约束】除人名、书名和必要直接引文外，不连续复用原文五字以上的短句，重新组织每段措辞。"
    return {
        "model": gen.MODEL,
        "temperature": gen.TEMPERATURE,
        "top_p": gen.TOP_P,
        "max_tokens": gen.MAX_TOKENS,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": gen.USER.format(body=source)},
        ],
    }


def attempt(source_id, payload, key, number):
    request_path = gen.OUT / f"{source_id}.final{number}.request.json"
    response_path = gen.OUT / f"{source_id}.final{number}.response.json"
    if request_path.exists():
        payload = json.loads(request_path.read_text(encoding="utf-8"))
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
        raise ValueError(f"{source_id}: final{number} invalid response")
    output = choices[0]["message"]["content"].strip()
    return output, response, request_path, response_path


def score(flags):
    weight = {
        "simplified_traditional_shift": 5,
        "outside_corpus_length_range": 4,
        "fewer_than_6_paragraphs": 4,
        "high_5gram_overlap": 3,
        "length_outside_20pct": 1,
    }
    return sum(weight.get(flag, 2) for flag in flags)


def save_selected(source_id, source, output, response, request_path, response_path, old_record):
    record_path = gen.OUT / f"{source_id}.json"
    text_path = gen.TEXT_OUT / f"{source_id}.txt"
    old_request = gen.PREP / old_record["request_path"]
    old_response = gen.PREP / old_record["response_path"]
    history = list(old_record.get("attempt_history", []))
    if old_request != request_path or old_response != response_path:
        archive_record = gen.OUT / f"{source_id}.prior{len(history)+1}.record.json"
        archive_text = gen.OUT / f"{source_id}.prior{len(history)+1}.txt"
        if not archive_record.exists():
            shutil.copy2(record_path, archive_record)
        if not archive_text.exists():
            shutil.copy2(text_path, archive_text)
        history.append({
            "request_path": old_record["request_path"],
            "response_path": old_record["response_path"],
            "record_path": str(archive_record.relative_to(gen.PREP)),
            "output_path": str(archive_text.relative_to(gen.PREP)),
            "cost_usd": old_record["cost_usd"],
        })
    flags, overlap = quality(source, output)
    gen.atomic_text(text_path, output)
    cost, cost_source = gen.get_cost(response)
    new = dict(old_record)
    selected_request = json.loads(request_path.read_text(encoding="utf-8"))
    selected_system = selected_request["messages"][0]["content"]
    new.update({
        "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        "model": gen.MODEL,
        "model_returned": response.get("model"),
        "temperature": gen.TEMPERATURE,
        "top_p": gen.TOP_P,
        "max_tokens": gen.MAX_TOKENS,
        "prompt": {"system": selected_system, "user_template": gen.USER},
        "core_prompt": expected_payload(source)["messages"][0]["content"],
        "targeted_script_retry": "【字形约束】" in selected_system,
        "targeted_length_retry": "【长度约束】" in selected_system,
        "targeted_paragraph_retry": "【段落约束】" in selected_system,
        "targeted_overlap_retry": "【重写约束】" in selected_system,
        "request_path": str(request_path.relative_to(gen.PREP)),
        "response_path": str(response_path.relative_to(gen.PREP)),
        "output_visible_characters": gen.visible_length(output),
        "output_paragraphs": gen.paragraph_count(output),
        "finish_reason": (response.get("choices") or [{}])[0].get("finish_reason"),
        "usage": response.get("usage"),
        "cost_usd": cost,
        "cost_source": cost_source,
        "quality_checks": {
            "flags": flags,
            "length_within_20pct": "length_outside_20pct" not in flags,
            "length_within_corpus_range": "outside_corpus_length_range" not in flags,
            "at_least_6_paragraphs": "fewer_than_6_paragraphs" not in flags,
            "fivegram_overlap": overlap,
        },
        "attempt_history": history,
    })
    gen.atomic_json(record_path, new)


def main():
    key = gen.os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is absent")
    rows = [r for r in csv.DictReader(gen.MANIFEST.open(encoding="utf-8-sig", newline="")) if r["language"] == "zh"]
    replaced = 0
    errors = 0
    for row in rows:
        source_id = row["id"]
        source = (gen.PREP / row["text_path"]).read_text(encoding="utf-8-sig").strip()
        payload = expected_payload(source)
        record_path = gen.OUT / f"{source_id}.json"
        text_path = gen.TEXT_OUT / f"{source_id}.txt"
        if not record_path.exists() or not text_path.exists():
            print(source_id, "MISSING current record or text", flush=True)
            errors += 1
            continue
        old_record = json.loads(record_path.read_text(encoding="utf-8"))
        current_request = json.loads((gen.PREP / old_record["request_path"]).read_text(encoding="utf-8"))
        old_output = text_path.read_text(encoding="utf-8").strip()
        old_flags, _ = quality(source, old_output)
        if current_request == payload and not old_flags:
            continue
        must_replace = current_request != payload
        best = None
        retry_flags = old_flags if not must_replace else ()
        for number in range(1, 4):
            try:
                result = attempt(source_id, expected_payload(source, retry_flags), key, number)
                errors = 0
                candidate, response, request_path, response_path = result
                flags, _ = quality(source, candidate)
                if best is None or score(flags) < score(best[0]):
                    best = (flags, candidate, response, request_path, response_path)
                if not flags:
                    break
                retry_flags = flags
            except Exception as exc:
                print(source_id, "attempt error", type(exc).__name__, str(exc), flush=True)
                errors += 1
                if errors >= 3:
                    raise SystemExit("Stopped after three errors") from exc
                time.sleep(5 * errors)
                break
        if best is None:
            continue
        flags, output, response, request_path, response_path = best
        if must_replace or score(flags) < score(old_flags):
            save_selected(source_id, source, output, response, request_path, response_path, old_record)
            replaced += 1
        print(source_id, "replaced" if must_replace or score(flags) < score(old_flags) else "retained", "flags=", flags, "total=", round(gen.all_spend(), 6), flush=True)
    print("replaced", replaced, "errors", errors, "total_spend", gen.all_spend(), flush=True)


if __name__ == "__main__":
    main()
