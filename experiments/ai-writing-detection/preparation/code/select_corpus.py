"""Validate independently collected essays and package 100 per language.

Run after the three source manifests have been completed. No network or model calls.
"""

import csv
import hashlib
import re
import shutil
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "raw"
OUTPUT = Path(__file__).resolve().parents[1] / "clean" / "human"
SOURCES = {
    "zh": [ROOT / "chinese_kepub", ROOT / "chinese_other"],
    "en": [ROOT / "english"],
}
MIN_LENGTH = {"zh": 1200, "en": 800}
MAX_LENGTH = {"zh": 2200, "en": 1500}
MIN_BLOCK = {"zh": 350, "en": 250}
WORD = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def length(text, language):
    if language == "zh":
        return sum(not char.isspace() for char in text)
    return len(WORD.findall(text))


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def best_blocks(parts, language):
    sizes = [length(part, language) for part in parts]
    prefix = [0]
    for size in sizes:
        prefix.append(prefix[-1] + size)
    best = None
    for i in range(1, len(parts) - 1):
        for j in range(i + 1, len(parts)):
            blocks = [prefix[i], prefix[j] - prefix[i], prefix[-1] - prefix[j]]
            if min(blocks) < MIN_BLOCK[language]:
                continue
            candidate = (max(blocks) - min(blocks), -min(blocks), i, j, blocks)
            if best is None or candidate[:2] < best[:2]:
                best = candidate
    if best is None:
        return None
    return best[2], best[3], best[4]


def norm_title(value):
    value = unicodedata.normalize("NFKC", value).lower()
    return "".join(c for c in value if c.isalnum())


def source_rows(language):
    for source in SOURCES[language]:
        manifests = list(source.glob("*manifest*.csv"))
        if not manifests:
            raise FileNotFoundError(f"No manifest under {source}")
        if len(manifests) != 1:
            raise ValueError(f"More than one manifest under {source}: {manifests}")
        with manifests[0].open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                yield source, row


def collect(language):
    valid = []
    rejected = []
    seen_title = set()
    seen_body = set()
    for source, row in source_rows(language):
        title = (row.get("title") or "").strip()
        author = (row.get("author") or "").strip()
        url = (row.get("source_url") or "").strip()
        relpath = row.get("text_path") or row.get("path") or ""
        path = (source / relpath).resolve()
        reason = ""
        if not title or not author or not url or not relpath:
            reason = "missing metadata/path"
        elif not path.is_relative_to(source.resolve()) or not path.is_file():
            reason = "text file missing/outside source"
        else:
            text = path.read_text(encoding="utf-8-sig").strip()
            parts = paragraphs(text)
            n = length(text, language)
            blocks = best_blocks(parts, language) if len(parts) >= 6 else None
            key = (norm_title(author), norm_title(title))
            body_hash = hashlib.sha256("".join(text.split()).encode()).hexdigest()
            if not (MIN_LENGTH[language] <= n <= MAX_LENGTH[language]):
                reason = f"length {n}"
            elif len(parts) < 6:
                reason = f"paragraphs {len(parts)}"
            elif blocks is None:
                reason = "cannot make three minimum-length blocks"
            elif key in seen_title or body_hash in seen_body:
                reason = "duplicate title/author or body"
            else:
                seen_title.add(key)
                seen_body.add(body_hash)
                item = dict(row)
                item.update(
                    source_id=row.get("id", ""),
                    source_collection_dir=source.name,
                    title=title,
                    author=author,
                    source_url=url,
                    source_html_path=(
                        row.get("source_html_path")
                        or row.get("raw_html_path")
                        or (f"source_html/{row['id']}.html" if source.name == "chinese_kepub" else "")
                    ),
                    text_path=str(path),
                    length=n,
                    paragraphs=len(parts),
                    block_cuts=f"{blocks[0]},{blocks[1]}",
                    block_lengths=",".join(map(str, blocks[2])),
                    sha256=hashlib.sha256(text.encode()).hexdigest(),
                    language=language,
                )
                valid.append(item)
        if reason:
            rejected.append((str(source), title, author, url, reason))
    return valid, rejected


def select(items):
    by_author = Counter()
    selected = []
    remaining = list(items)
    while remaining and len(selected) < 100:
        remaining.sort(
            key=lambda item: (
                by_author[item["author"]],
                abs(item["length"] - (MIN_LENGTH[item["language"]] + MAX_LENGTH[item["language"]]) / 2),
                -item["paragraphs"],
                item["title"],
            )
        )
        pick = remaining.pop(0)
        selected.append(pick)
        by_author[pick["author"]] += 1
    return selected


def write_manifest(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fields = ["id", "source_id", "source_collection_dir", "language", "title", "author", "source_url", "collection", "publication_year", "length", "paragraphs", "block_cuts", "block_lengths", "sha256", "text_path", "source_html_path", "rights_note", "notes"]
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


for language in ("zh", "en"):
    valid, rejected = collect(language)
    chosen = select(valid)
    target = OUTPUT / language
    target.mkdir(parents=True, exist_ok=True)
    for number, row in enumerate(chosen, 1):
        row["id"] = f"{language.upper()}{number:03d}"
        destination = target / f"{row['id']}.txt"
        shutil.copyfile(row["text_path"], destination)
        row["text_path"] = f"{language}/{destination.name}"
    write_manifest(OUTPUT / f"manifest.{language}.csv", chosen)
    with (OUTPUT / f"rejected.{language}.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["source", "title", "author", "url", "reason"])
        writer.writerows(rejected)
    print(language, "eligible", len(valid), "selected", len(chosen), "rejected", len(rejected))
    print("authors", dict(Counter(item["author"] for item in chosen)))
    if len(chosen) != 100:
        raise SystemExit(f"Need 100 {language} essays, found {len(chosen)}")
