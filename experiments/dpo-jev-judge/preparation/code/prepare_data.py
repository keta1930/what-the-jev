#!/usr/bin/env python
"""生成 JEV 考卷：一对思考随机分派到 A、B 两个位置，按两种布局各出一份；LLM 判官偏好的一条进 reference。"""

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "preparation/raw"
STANDARD = ROOT / "preparation/code/instruction.txt"
PAIRS = RAW / "pairs.jsonl"

LAYOUTS = (
    ("data/dataset.json", False),
    ("data/dataset.criteria-text.json", True),
)

SEED = 20261009
QUESTION = "better"
OPTIONS = ("A", "B")


def load_pairs(path):
    """读偏好对，返回 [(prompt_id, 题目, chosen_idx, rejected_idx, chosen, rejected)]；meta 行跳过。"""
    pairs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("record") != "meta":
            pairs.append((rec["prompt_id"], rec["prompt"], rec["chosen_idx"], rec["rejected_idx"],
                          rec["chosen"], rec["rejected"]))
    return pairs


def build_sample(pid, prompt_text, texts, indices, answer, standard, responses_in_criteria):
    """一条考卷：两条思考落在 A、B，判据进 instructions，reference 指向 LLM 判官偏好的位置。"""
    responses = dict(zip(OPTIONS, texts))
    if responses_in_criteria:
        state, criteria = {"prompt": prompt_text}, responses
    else:
        state, criteria = {"prompt": prompt_text, "responses": responses}, {key: f"responses.{key}" for key in OPTIONS}
    return {
        "id": pid,
        "input": {
            "state": state,
            "questions": {
                QUESTION: {
                    "type": "choice",
                    "instructions": standard,
                    "criteria": criteria,
                }
            },
        },
        "reference": {QUESTION: {"choice": answer}},
        "metadata": {
            "chosen_idx": indices[0],
            "rejected_idx": indices[1],
            "option_to_idx": dict(zip(OPTIONS, indices)),
        },
    }


def write_dataset(path, samples):
    """写出数据集，两份布局各一份。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"schema_version": 1, "samples": samples}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    standard = STANDARD.read_text(encoding="utf-8").strip()
    pairs = load_pairs(PAIRS)
    if not pairs:
        raise SystemExit("没有读到偏好对")

    rng = random.Random(SEED)
    samples = {name: [] for name, _ in LAYOUTS}
    for pid, prompt_text, chosen_idx, rejected_idx, chosen, rejected in pairs:
        if rng.random() < 0.5:
            texts, indices, answer = (chosen, rejected), (chosen_idx, rejected_idx), OPTIONS[0]
        else:
            texts, indices, answer = (rejected, chosen), (rejected_idx, chosen_idx), OPTIONS[1]
        for name, responses_in_criteria in LAYOUTS:
            samples[name].append(build_sample(pid, prompt_text, texts, indices, answer, standard, responses_in_criteria))

    for name, _ in LAYOUTS:
        out = ROOT / name
        write_dataset(out, samples[name])
        print(f"{len(samples[name])} 条样本 -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
