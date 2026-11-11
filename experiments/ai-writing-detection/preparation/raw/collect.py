"""Collect independently attributable public Chinese prose chapters from kepub.net.

This only reads public HTML. It never requests gated text, API endpoints, or downloads.
"""

import concurrent.futures
import csv
import hashlib
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


HERE = Path(__file__).resolve().parent
ROOT = "https://www.kepub.net"
COLLECTIONS = {
    "700533": ("周作人", "雨天的书"),
    "773303": ("周作人", "药味集"),
    "705452": ("周作人", "木片集"),
    "764089": ("许地山", "许地山散文集"),
    "23392": ("老舍", "老舍散文集"),
    "23393": ("老舍", "八方风雨"),
    "23394": ("老舍", "老舍幽默诗文集"),
    "11263": ("老舍", "老牛破车"),
    "708966": ("萧红", "萧红散文集"),
}


def get(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def links_for_collection(item):
    book_id, (author, collection) = item
    soup = BeautifulSoup(get(f"{ROOT}/book/{book_id}"), "html.parser")
    links = []
    seen = set()
    for link in soup.select("a[href]"):
        href = link.get("href", "")
        if not re.match(r"^/book/\d+/\d+", href):
            continue
        if href in seen:
            continue
        seen.add(href)
        title = link.get_text(" ", strip=True)
        if not title or title in ("Start Reading", "Recently Updated", "下一章", "上一章"):
            continue
        links.append((author, collection, title, urljoin(ROOT, href)))
    return links


def yu_singles():
    soup = BeautifulSoup(get(f"{ROOT}/author/10105"), "html.parser")
    links = []
    seen = set()
    for link in soup.select("a[href]"):
        href = link.get("href", "")
        if not re.fullmatch(r"/book/\d+", href) or href in seen:
            continue
        seen.add(href)
        title = link.get_text(" ", strip=True)
        if not title or title in ("Book Details", "Start Reading"):
            continue
        # Novel and story collections precede the short prose entries on this page.
        if re.match(r"/book/21[67]\d\d", href):
            links.append(("郁达夫", "郁达夫散文集 / 单篇", title, urljoin(ROOT, href)))
    return links


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    batches = list(pool.map(links_for_collection, COLLECTIONS.items()))
catalog = [row for batch in batches for row in batch] + yu_singles()
catalog = list(dict.fromkeys(catalog))
with (HERE / "catalog.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["author", "collection", "title", "source_url"])
    writer.writerows(catalog)
print("catalog", len(catalog))
for author in sorted({x[0] for x in catalog}):
    print(author, sum(x[0] == author for x in catalog))
