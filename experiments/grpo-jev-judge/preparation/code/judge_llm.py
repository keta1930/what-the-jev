"""Judge each prompt's eight rollouts with an LLM and write the winner and rewards."""

import argparse
import json
import logging
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI

EXP = Path(__file__).resolve().parents[2]
DATA_DIR = EXP / "preparation/raw"
RESULT_FILE = DATA_DIR / "llm-judge-result.jsonl"
RESPONSE_FILE = DATA_DIR / "llm-judge-response.jsonl"
LOG_FILE = DATA_DIR / "llm-judge.log"
DEFAULT_STANDARD = EXP / "preparation/code/instruction.txt"

G = 8
WINNER_REWARD = 1.0


def setup_logging(log_path=None):
    """Return a logger writing to stdout and, when given, to a file as well."""
    logger = logging.getLogger("judge-llm")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_path:
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    for handler in handlers:
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


def load_prompts(path):
    """Return {prompt_id: (type, prompt text)}."""
    prompts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        prompts[rec["id"]] = (rec.get("type"), rec["prompt"])
    return prompts


def load_groups(path):
    """Return {prompt_id: thinkings ordered by sample_idx}."""
    groups = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("record") == "meta":
            continue
        groups.setdefault(rec["prompt_id"], []).append((rec["sample_idx"], rec["thinking"]))
    return {pid: [t for _, t in sorted(recs)] for pid, recs in groups.items()}


def load_state(out_path, keys):
    """Return judged ids, kept lines, and the raw line count, dropping failures and partial lines."""
    raw_lines = []
    if out_path.exists():
        raw_lines = [l for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    kept, done = [], set()
    for line in raw_lines:
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec.get("prompt_id"), str) and rec.get("error") is None and rec.get("choice") in keys:
            kept.append(json.dumps(rec, ensure_ascii=False))
            done.add(rec["prompt_id"])
    return done, kept, len(raw_lines)


def build_messages(std_text, prompt_text, thinkings):
    """Build the judge messages: standard as system, prompt and thinkings as user."""
    blocks = "\n\n".join(f"responses.R{i + 1}:\n{t}" for i, t in enumerate(thinkings))
    options = "、".join(f'"{k}"' for k in [f"R{i}" for i in range(1, len(thinkings) + 1)])
    example = '{"answer": "<选项>"}'
    user = (
        f"【题目】\n{prompt_text}\n\n"
        f"【八条思考】\n{blocks}\n\n"
        f"【回答格式】\n输出 JSON，只含一个字段 answer，其值必须是下列之一：{options}。\n"
        f"示例：{example}"
    )
    return [{"role": "system", "content": std_text}, {"role": "user", "content": user}]


def parse_answer(text, n):
    """Return the R<N> answer found in the text, or None."""
    keys = {f"R{i}" for i in range(1, n + 1)}
    if not text:
        return None
    candidates = [text.strip()]
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fence:
        candidates.insert(0, fence.group(1).strip())
    brace = re.search(r"\{.*\}", text, re.S)
    if brace:
        candidates.append(brace.group(0))
    for cand in candidates:
        try:
            obj = json.loads(cand)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("answer"), str):
            value = obj["answer"].strip()
            if value in keys:
                return value
            m = re.match(rf"R?\s*([1-{n}])$", value, re.I)
            if m:
                return f"R{int(m.group(1))}"
            return None
    m = re.search(rf"\bR\s*([1-{n}])\b", text, re.I)
    if m:
        return f"R{int(m.group(1))}"
    return None


def judge_one(client, args, messages):
    """Call the judge once, returning the raw response, the text, and the usage."""
    for attempt in range(1, args.retries + 1):
        try:
            resp = client.chat.completions.create(
                model=args.model,
                messages=messages,
                reasoning_effort=args.reasoning_effort,
                max_tokens=args.max_tokens,
            )
            usage = resp.usage
            return json.loads(resp.model_dump_json()), (resp.choices[0].message.content or "").strip(), {
                "input_tokens": getattr(usage, "prompt_tokens", None),
                "output_tokens": getattr(usage, "completion_tokens", None),
            }
        except Exception as exc:
            if attempt == args.retries:
                return None, None, {"type": type(exc).__name__, "message": str(exc)[:300]}
            time.sleep(2 ** attempt)
    return None, None, {"type": "unknown", "message": "unreachable"}


def append(path, rec):
    """Append one record and flush it to disk."""
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def main():
    """Judge the pending prompts and write the results."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--standard", default=str(DEFAULT_STANDARD), help="评判标准文件，与 JEV 用同一份")
    ap.add_argument("--prompts", default=str(DATA_DIR / "prompts.jsonl"))
    ap.add_argument("--rollouts", default=str(DATA_DIR / "rollouts.jsonl"))
    ap.add_argument("--out", default=str(RESULT_FILE), help="判好的结果")
    ap.add_argument("--response", action="store_true", help="另存判官原始响应，默认不存")
    ap.add_argument("--log", action="store_true", help="另存日志到文件，默认只打 stdout")
    ap.add_argument("--model", default="deepseek-flash")
    ap.add_argument("--base-url", default="https://api.deepseek.com")
    ap.add_argument("--reasoning-effort", default="max", choices=["low", "high", "max"])
    ap.add_argument("--max-tokens", type=int, default=393216, help="服务端上限 384K，开到顶以免思维链被截断")
    ap.add_argument("--concurrency", type=int, default=50)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--limit", type=int, default=None, help="只判前 N 组（小样验证用）")
    args = ap.parse_args()

    out_path = Path(args.out)
    response_path = RESPONSE_FILE if args.response else None
    log_path = LOG_FILE if args.log else None
    for p in (out_path, response_path, log_path):
        if p:
            p.parent.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(log_path)

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        logger.error("DEEPSEEK_API_KEY 未设置")
        sys.exit(2)

    std_text = Path(args.standard).read_text(encoding="utf-8").strip()
    prompts = load_prompts(Path(args.prompts))
    groups = load_groups(Path(args.rollouts))
    keys = {f"R{i}" for i in range(1, G + 1)}

    done, kept_lines, n_raw = load_state(out_path, keys)
    if len(kept_lines) != n_raw:
        tmp = out_path.with_suffix(".jsonl.tmp")
        tmp.write_text("\n".join(kept_lines) + ("\n" if kept_lines else ""), encoding="utf-8")
        os.replace(tmp, out_path)
        logger.info("resume repair: dropped %d lines (failed or partial), kept %d", n_raw - len(kept_lines), len(kept_lines))

    pending = [pid for pid in prompts if pid not in done and len(groups.get(pid, [])) == G]
    if args.limit:
        pending = pending[: args.limit]
    missing = [pid for pid in prompts if pid not in groups]
    bad_groups = [pid for pid, t in groups.items() if len(t) != G]
    logger.info(
        "run start: standard=%s | prompts=%d, rollouts=%d groups, already judged=%d, pending=%d | out=%s response=%s",
        Path(args.standard).name, len(prompts), len(groups), len(done), len(pending),
        out_path.name, response_path.name if response_path else "off",
    )
    logger.info(
        "model=%s @ %s | reasoning_effort=%s max_tokens=%d concurrency=%d retries=%d | missing=%d partial-groups=%d",
        args.model, args.base_url, args.reasoning_effort, args.max_tokens, args.concurrency, args.retries,
        len(missing), len(bad_groups),
    )

    client = OpenAI(api_key=api_key, base_url=args.base_url)
    lock = threading.Lock()
    t0 = time.time()
    stats = {"total": 0, "winner": 0, "invalid": 0, "error": 0, "in_tokens": 0, "out_tokens": 0}

    def work(pid):
        _, prompt_text = prompts[pid]
        raw, text, meta = judge_one(client, args, build_messages(std_text, prompt_text, groups[pid]))
        if text is None:
            choice, usage, error = None, None, meta
        else:
            choice = parse_answer(text, G)
            usage, error = meta, (None if choice else {"type": "unparsed", "message": text[:300]})
        raw_rec = {"prompt_id": pid, "response": raw, "error": error} if response_path else None
        rewards = [WINNER_REWARD if choice == f"R{i + 1}" else 0.0 for i in range(G)]
        rec = {
            "prompt_id": pid,
            "choice": choice,
            "sample_idx": (int(choice[1:]) - 1) if choice else None,
            "rewards": rewards,
            "usage": usage,
            "error": error,
        }
        with lock:
            if response_path:
                append(response_path, raw_rec)
            append(out_path, rec)
            stats["total"] += 1
            if error is None:
                stats["winner"] += 1
            elif error["type"] == "unparsed":
                stats["invalid"] += 1
            else:
                stats["error"] += 1
            if usage:
                stats["in_tokens"] += usage.get("input_tokens") or 0
                stats["out_tokens"] += usage.get("output_tokens") or 0
            n = stats["total"]
            elapsed = time.time() - t0
            eta = elapsed / n * (len(pending) - n)
            logger.info(
                "progress %d/%d groups | %s | %.0fs elapsed | %.1fs/group | ETA %.0fs | invalid=%d error=%d | %.0f tok in",
                n, len(pending), ("error:" + str(error["type"])) if error else f"choice={choice}",
                elapsed, elapsed / n, eta, stats["invalid"], stats["error"], stats["in_tokens"] / max(elapsed, 1),
            )

    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = [ex.submit(work, pid) for pid in pending]
        for fut in as_completed(futures):
            fut.result()

    logger.info(
        "run done: %d groups judged | winner=%d invalid=%d error=%d | tokens in=%d out=%d | total %.1fs",
        stats["total"], stats["winner"], stats["invalid"], stats["error"],
        stats["in_tokens"], stats["out_tokens"], time.time() - t0,
    )


if __name__ == "__main__":
    main()
