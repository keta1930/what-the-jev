"""Select preference pairs from the grpo-jev-judge judge results."""

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT.parent / "grpo-jev-judge/preparation/raw"
PAIRS = ROOT / "preparation/raw/pairs.jsonl"
SEED = 20261008


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


def load_winners(path):
    """Return {prompt_id: winning sample_idx}."""
    winners = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec.get("error") is None and rec.get("sample_idx") is not None:
                winners[rec["prompt_id"]] = rec["sample_idx"]
    return winners


def main():
    """Write the preference pairs drawn from the judge results."""
    prompts = load_prompts(SOURCE / "prompts.jsonl")
    groups = load_groups(SOURCE / "rollouts.jsonl")
    winners = load_winners(SOURCE / "llm-judge-result.jsonl")

    missing = [pid for pid in prompts if pid not in groups or pid not in winners]
    if missing:
        raise SystemExit(f"源数据不齐，缺组或缺标注 {len(missing)} 条：{missing[:5]}")

    rng = random.Random(SEED)
    records = []
    for pid, prompt_text in prompts.items():
        thinkings = groups[pid]
        chosen_idx = winners[pid]
        rejected_idx = rng.choice([i for i in range(len(thinkings)) if i != chosen_idx])
        records.append({
            "prompt_id": pid,
            "prompt": prompt_text,
            "chosen_idx": chosen_idx,
            "rejected_idx": rejected_idx,
            "chosen": thinkings[chosen_idx],
            "rejected": thinkings[rejected_idx],
        })

    meta = {
        "record": "meta",
        "source": "experiments/grpo-jev-judge/preparation/raw/{prompts,rollouts,llm-judge-result}.jsonl",
        "seed": SEED,
        "groups": len(records),
        "rule": "chosen = LLM 判官选中的那条，rejected = 其余七条中随机一条",
    }
    lines = [json.dumps(meta, ensure_ascii=False)] + [json.dumps(r, ensure_ascii=False) for r in records]
    PAIRS.parent.mkdir(parents=True, exist_ok=True)
    PAIRS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(records)} 对偏好 -> {PAIRS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
