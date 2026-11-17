"""Collect public modern Chinese essays from XY Bookstore and Kepub.

The output is a research candidate set; each essay keeps its source URL.
"""

from __future__ import annotations

import concurrent.futures
import csv
import hashlib
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT.parent / "xybookstore_prose_catalog.csv"
HEADERS = {"User-Agent": "JevEssayResearch/1.0 (source verification)"}
HTML_CACHE = ROOT / "source_html"
HTML_CACHE.mkdir(exist_ok=True)


def get(url: str) -> BeautifulSoup:
    cache = HTML_CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".html")
    if cache.exists():
        return BeautifulSoup(cache.read_bytes(), "html.parser")
    for attempt in range(4):
        try:
            response = requests.get(url, timeout=30, headers=HEADERS)
            response.raise_for_status()
            cache.write_bytes(response.content)
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(1 + attempt)


def clean(paragraphs):
    return [re.sub(r"\s+", " ", x).strip() for x in paragraphs if x and x.strip()]


def visible_length(paragraphs):
    return sum(len(re.sub(r"\s", "", p)) for p in paragraphs)


def three_blocks_possible(paragraphs, minimum=350):
    cumulative = [0]
    for paragraph in paragraphs:
        cumulative.append(cumulative[-1] + len(re.sub(r"\s", "", paragraph)))
    n = len(paragraphs)
    return any(
        cumulative[i] >= minimum and cumulative[j] - cumulative[i] >= minimum and cumulative[n] - cumulative[j] >= minimum
        for i in range(1, n - 1)
        for j in range(i + 1, n)
    )


def xy_row(row):
    card = row["card_text"]
    label = card.removeprefix("散文 ")
    title, author = label.rsplit(" ", 1)
    url = row["url"].replace("/book/", "/read/") + "?variant=simplified"
    article = get(url).select_one("article.reader-article")
    if article is None:
        return None
    paragraphs = clean(p.get_text(" ", strip=True) for p in article.select("p"))
    while paragraphs and (paragraphs[0] in ("散文", title) or paragraphs[0].startswith("作者：") or re.fullmatch(r"\d{4}年.*", paragraphs[0])):
        paragraphs.pop(0)
    while paragraphs and (paragraphs[-1].startswith(("原载", "本文", "出处：")) or re.fullmatch(r"\d{4}年.*", paragraphs[-1])):
        paragraphs.pop()
    paragraphs = [p for p in paragraphs if not (
        p in ("版本信息", "本作品收录于《朝花夕拾》", "◇")
        or p.startswith(("这份文献应全部或部分使用传统汉字", "一般而言，文献应保留其底本", "署名「"))
        or re.match(r"^[（(]原载", p)
    )]
    while paragraphs and len(paragraphs[0]) < 10 and paragraphs[0] != title:
        paragraphs.pop(0)
    while paragraphs and (re.fullmatch(r"[一二三四五六七八九十〇零0-9０-９]{1,4}年.*", paragraphs[-1]) or re.fullmatch(r"[一二三四五六七八九十〇零0-9０-９]+月[一二三四五六七八九十〇零0-9０-９]+日[。.]?", paragraphs[-1])):
        paragraphs.pop()
    return dict(title=title, author=author, source_url=url, collection="栖页书屋现代散文", paragraphs=paragraphs,
                rights_note="原作者公有领域；站点标注维基文库校录/CC BY-SA 4.0，需保留来源与许可", source="xy")


def kepub_index(collection_id, author):
    soup = get(f"https://www.kepub.net/book/{collection_id}")
    rows = []
    seen = set()
    for link in soup.select('a[href^="/book/"]'):
        href = link.get("href", "")
        if href in seen:
            continue
        title = link.get_text(" ", strip=True)
        if title in ("下一章", "上一章", "开始阅读", "Start Reading") or title.startswith("Recently Updated"):
            continue
        if "collectionNo=" + str(collection_id) not in href and not re.fullmatch(rf"/book/{collection_id}/\d+", href):
            continue
        seen.add(href)
        rows.append((title, author, urljoin("https://www.kepub.net", href)))
    return rows


def kepub_row(info):
    title, author, url = info
    content = get(url).select_one("#content")
    if content is None:
        return None
    # Chapter HTML varies: bare text with double <br>, <p> blocks,
    # or a mixture (e.g. bare text followed by a dated footer in <p>).
    html = content.decode_contents()
    html = re.sub(r"(?:<br\s*/?>\s*){2,}", "\n\n", html, flags=re.I)
    html = re.sub(r"</p\s*>", "\n\n", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    paragraphs = clean(BeautifulSoup(html, "html.parser").get_text().split("\n\n"))
    while paragraphs and paragraphs[0] in (title, author, "作者：" + author):
        paragraphs.pop(0)
    while paragraphs and (paragraphs[-1].startswith(("原载", "本文", "出处：")) or re.fullmatch(r"\d{4}年.*", paragraphs[-1])):
        paragraphs.pop()
    paragraphs = [p for p in paragraphs if not re.fullmatch(r"(?:【[一二三四五六七八九十]+】|◇)", p)]
    while paragraphs and (
        ("原载" in paragraphs[-1] and len(paragraphs[-1]) < 100)
        or re.fullmatch(r"[一二三四五六七八九十〇零0-9０-９]{1,4}年.*", paragraphs[-1])
        or re.fullmatch(r"[一二三四五六七八九十〇零0-9０-９]+月[一二三四五六七八九十〇零0-9０-９]+日[。.]?", paragraphs[-1])
    ):
        paragraphs.pop()
    return dict(title=title, author=author, source_url=url, collection="可阅文学网散文集", paragraphs=paragraphs,
                rights_note="作者作品为公有领域；此处为可阅文学网公开阅读页，保留来源链接", source="kepub")


catalog = list(csv.DictReader(CATALOG.open(encoding="utf-8-sig")))
xy_candidates = [row for row in catalog if any(row["card_text"].endswith(name) for name in ("朱自清", "徐志摩", "鲁迅"))]
kepub_candidates = kepub_index(714836, "朱自清") + kepub_index(796968, "徐志摩")
for book_id in (11070, 11072, 11068, 11059, 11061, 11074):
    kepub_candidates += kepub_index(book_id, "鲁迅")
print("catalog", len(xy_candidates), len(kepub_candidates), flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    xy = [r for r in pool.map(xy_row, xy_candidates) if r]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    kp = [r for r in pool.map(kepub_row, kepub_candidates) if r]

seen = set()
all_rows = []
for row in xy + kp:
    title = re.sub(r"[\W_]", "", row["title"])
    key = (row["author"], title)
    if key in seen:
        continue
    seen.add(key)
    row["length"] = visible_length(row["paragraphs"])
    row["paragraph_count"] = len(row["paragraphs"])
    row["three_blocks"] = three_blocks_possible(row["paragraphs"])
    all_rows.append(row)

with (ROOT / "candidates.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["title", "author", "source_url", "source", "length", "paragraphs", "three_blocks"])
    for row in all_rows:
        writer.writerow([row["title"], row["author"], row["source_url"], row["source"], row["length"], row["paragraph_count"], row["three_blocks"]])

qualifiers = [r for r in all_rows if 1200 <= r["length"] <= 2200 and r["paragraph_count"] >= 6 and r["three_blocks"]]
print("unique", len(all_rows), "mechanically qualified", len(qualifiers), flush=True)
for row in qualifiers:
    print(row["source"], row["author"], row["title"], row["length"], row["paragraph_count"], flush=True)

import pickle
(ROOT / "candidates.pkl").write_bytes(pickle.dumps(all_rows))
