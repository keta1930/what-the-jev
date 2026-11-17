"""Freeze verified non-fiction essay texts from the research candidate cache."""

import csv
import hashlib
import pickle
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEXTS = ROOT / "texts"
TEXTS.mkdir(exist_ok=True)
rows = pickle.loads((ROOT / "candidates.pkl").read_bytes())


def preface(title):
    compact = re.sub(r"\s", "", title)
    return compact.endswith(("序", "跋", "后记", "自序"))


selected = []
excluded = []
for row in rows:
    reason = None
    if preface(row["title"]):
        reason = "preface_or_afterword"
    elif not 1200 <= row["length"] <= 2200:
        reason = "length_out_of_range"
    elif row["paragraph_count"] < 6:
        reason = "fewer_than_six_paragraphs"
    elif not row["three_blocks"]:
        reason = "three_blocks_below_350_characters"
    if reason:
        excluded.append((row["author"], row["title"], row["source_url"], row["length"], row["paragraph_count"], reason))
        continue
    selected.append(row)

manifest_rows = []
for index, row in enumerate(selected, 1):
    sample_id = f"ZOTH{index:03d}"
    text_path = Path("texts") / (sample_id + ".txt")
    body = "\n\n".join(row["paragraphs"]) + "\n"
    (ROOT / text_path).write_text(body, encoding="utf-8")
    source_html = Path("source_html") / (hashlib.sha256(row["source_url"].encode()).hexdigest() + ".html")
    rights = ("站点作品页注明原作公有领域，采用维基文库校录文本并标明 CC BY-SA 4.0"
              if row["source"] == "xy" else
              "可阅文学网公开阅读页；站点自述含公版作品，单篇数字校录许可未列明")
    manifest_rows.append({
        "id": sample_id,
        "title": row["title"],
        "author": row["author"],
        "source_url": row["source_url"],
        "text_path": text_path.as_posix(),
        "length": row["length"],
        "paragraphs": row["paragraph_count"],
        "collection": row["collection"],
        "rights_note": rights,
        "notes": "长度为去空白可见字符，正文未分割或拼接；按自然段可切三块且每块至少350字符",
        "raw_html_path": source_html.as_posix(),
    })

with (ROOT / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(manifest_rows[0]))
    writer.writeheader()
    writer.writerows(manifest_rows)
with (ROOT / "screening_excluded.csv").open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["author", "title", "source_url", "length", "paragraphs", "reason"])
    writer.writerows(excluded)
print("selected", len(selected), "excluded", len(excluded))
