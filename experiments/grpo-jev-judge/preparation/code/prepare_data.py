"""Build the JEV exam datasets from the prompts, rollouts, and judge choices."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "preparation/raw"
STANDARD = ROOT / "preparation/code/instruction.txt"
JUDGE_RESULT = RAW / "llm-judge-result.jsonl"

LAYOUTS = (
    ("data/dataset.json", False),
    ("data/dataset.criteria-text.json", True),
)

G = 8
QUESTION = "winner_overall"


def load_prompts(path):
    """Return {prompt_id: prompt text}."""
    prompts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            prompts[rec["id"]] = rec["prompt"]
    return prompts


def load_groups(path):
    """Return {prompt_id: thinkings ordered by sample_idx}."""
    groups = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("record") != "meta":
            groups.setdefault(rec["prompt_id"], []).append((rec["sample_idx"], rec["thinking"]))
    return {pid: [t for _, t in sorted(recs)] for pid, recs in groups.items()}


def load_choices(path):
    """Return {prompt_id: winning option key}."""
    choices = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec.get("error") is None and rec.get("choice"):
                choices[rec["prompt_id"]] = rec["choice"]
    return choices


def build_sample(pid, prompt_text, thinkings, standard, choice, responses_in_criteria):
    """Build one exam sample for the given layout, with the judge's choice as reference."""
    keys = [f"R{i + 1}" for i in range(len(thinkings))]
    if responses_in_criteria:
        state, criteria = {"prompt": prompt_text}, dict(zip(keys, thinkings))
    else:
        state, criteria = {"prompt": prompt_text, "responses": dict(zip(keys, thinkings))}, {k: f"responses.{k}" for k in keys}
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
        "reference": {QUESTION: {"choice": choice}},
    }


def main():
    """Write both exam datasets from the rollouts and judge choices."""
    standard = STANDARD.read_text(encoding="utf-8").strip()
    prompts = load_prompts(RAW / "prompts.jsonl")
    groups = load_groups(RAW / "rollouts.jsonl")
    choices = load_choices(JUDGE_RESULT)

    missing = [pid for pid in prompts if pid not in groups]
    short = [pid for pid, t in groups.items() if len(t) != G]
    if missing or short:
        raise SystemExit(f"incomplete data: missing groups {missing}; groups not of size {G}: {short}")
    unjudged = [pid for pid in prompts if pid not in choices]
    if unjudged:
        raise SystemExit(f"judge results missing for {len(unjudged)} prompts: {unjudged[:5]}")

    for out_name, responses_in_criteria in LAYOUTS:
        samples = [
            build_sample(pid, text, groups[pid], standard, choices[pid], responses_in_criteria)
            for pid, text in prompts.items()
        ]
        out = ROOT / out_name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps({"schema_version": 1, "samples": samples}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"{len(samples)} samples -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
