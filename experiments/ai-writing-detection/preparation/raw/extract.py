"""Extract qualifying prose from the public chapter pages listed in catalog.csv."""

import argparse
import concurrent.futures
import csv
import hashlib
import html
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


HERE = Path(__file__).resolve().parent
RAW = HERE / "source_html"
TEXT = HERE / "texts"
RAW.mkdir(exist_ok=True)
TEXT.mkdir(exist_ok=True)


def visible_length(value):
    return sum(not character.isspace() for character in value)


def block_sizes(paragraphs):
    sizes = [visible_length(p) for p in paragraphs]
    target = sum(sizes) / 3
    choices = []
    for i in range(1, len(sizes) - 1):
        for j in range(i + 1, len(sizes)):
            parts = (sum(sizes[:i]), sum(sizes[i:j]), sum(sizes[j:]))
            choices.append((sum((x - target) ** 2 for x in parts), parts))
    return min(choices)[1] if choices else (0, 0, 0)


def extract(row):
    url = row["source_url"]
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as error:
        return (row, [], "network:" + str(error)[:80], b"")
    soup = BeautifulSoup(response.content, "html.parser")
    node = soup.select_one("#content")
    if node is None:
        return (row, [], "no_content", response.content)
    markup = node.decode_contents()
    markup = re.sub(r"(?:<br\s*/?>\s*){2,}", "\n\n", markup, flags=re.I)
    markup = re.sub(r"<br\s*/?>", "\n", markup, flags=re.I)
    markup = re.sub(r"</p>\s*<p[^>]*>", "\n\n", markup, flags=re.I)
    body = BeautifulSoup(markup, "html.parser").get_text()
    body = html.unescape(body)
    paragraphs = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n+", body)]
    paragraphs = [part for part in paragraphs if part]
    while paragraphs and (paragraphs[0] == row["title"] or paragraphs[0].startswith("作者：")):
        paragraphs.pop(0)
    while paragraphs and (
        paragraphs[-1].startswith(("原载", "首刊", "（本篇", "(本篇", "本篇", "作者："))
        or re.fullmatch(r"(?:[12][0-9]{3}|一九[一二三四五六七八九零〇]{2})年.*", paragraphs[-1])
    ):
        paragraphs.pop()
    if len(paragraphs) == 1 and visible_length(paragraphs[0]) > 1000:
        return (row, paragraphs, "no_paragraph_boundaries", response.content)
    if any(term in " ".join(paragraphs[-2:]) for term in ("本章为付费", "请订阅后阅读", "开通VIP继续")):
        return (row, paragraphs, "paywalled", response.content)
    return (row, paragraphs, "ok", response.content)


parser = argparse.ArgumentParser()
parser.add_argument("--authors", nargs="+", default=["周作人", "许地山", "郁达夫", "老舍", "萧红"])
args = parser.parse_args()
catalog = list(csv.DictReader((HERE / "catalog.csv").open(encoding="utf-8-sig")))
catalog = [r for r in catalog if r["author"] in args.authors]
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for row, paragraphs, status, raw in pool.map(extract, catalog):
        size = visible_length("".join(paragraphs))
        blocks = block_sizes(paragraphs)
        results.append((row, paragraphs, status, raw, size, blocks))

with (HERE / "screening.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["author", "collection", "title", "source_url", "length", "paragraphs", "block_sizes", "status"])
    for row, paragraphs, status, raw, size, blocks in results:
        writer.writerow([row["author"], row["collection"], row["title"], row["source_url"], size, len(paragraphs), "/".join(map(str, blocks)), status])

selected = []
seen = set()
for row, paragraphs, status, raw, size, blocks in results:
    if status != "ok" or not 1200 <= size <= 2200 or len(paragraphs) < 6 or min(blocks) < 350:
        continue
    if re.search(r"(?:自序|附录|目录|跋$|序$|译|小说|诗选|童话|话剧|剧本)", row["title"]):
        continue
    fingerprint = hashlib.sha256("".join(paragraphs).encode("utf-8")).hexdigest()
    key = (row["author"], re.sub(r"[\W_]+", "", row["title"]))
    if fingerprint in seen or key in seen:
        continue
    seen.update((fingerprint, key))
    id_ = f"K{len(selected)+1:03d}"
    text_path = f"texts/{id_}.txt"
    (HERE / text_path).write_text("\n\n".join(paragraphs) + "\n", encoding="utf-8")
    (RAW / f"{id_}.html").write_bytes(raw)
    selected.append((id_, row["title"], row["author"], row["source_url"], text_path, size, len(paragraphs), row["collection"], "Public chapter page; site rights statement requires source review", "3-block sizes " + "/".join(map(str, blocks))))

with (HERE / "all_qualified.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "title", "author", "source_url", "text_path", "length", "paragraphs", "collection", "rights_note", "notes"])
    writer.writerows(selected)
print("screened", len(results), "qualified", len(selected))
for author in sorted({row[2] for row in selected}):
    print(author, sum(row[2] == author for row in selected))
