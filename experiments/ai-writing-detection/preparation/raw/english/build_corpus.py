"""Extract and validate individual public-domain essays from saved Gutenberg HTML."""

import csv
import hashlib
import re
import shutil
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
SOURCE_DIRS = [ROOT / "source_html", ROOT.parent / "01-原始数据"]
BOOKS = {
    386: ("Robert Louis Stevenson", "Virginibus Puerisque, and Other Papers", 1881),
    5803: ("A. A. Milne", "Not That It Matters", 1919),
    10675: ("A. G. Gardiner", "Pebbles on the Shore", 1916),
    34462: ("E. V. Lucas", "Adventures and Enthusiasms", 1920),
    8092: ("G. K. Chesterton", "Tremendous Trifles", 1909),
    11505: ("G. K. Chesterton", "All Things Considered", 1908),
    38280: ("various", "Modern Essays", 1921),
    38245: ("various", "Atlantic Classics, Second Series", 1918),
    66831: ("various", "Modern Essays and Stories", 1922),
}
WORD = re.compile(r"\b[\w’'-]+\b")
MILNE = {
    "The Pleasure of Writing", "My Library", "Superstition", "The Charm of Golf",
    "Goldfish", "Saturday to Monday", "The Pond", "Our Learned Friends",
    "A Christmas Number", "The Unfairness of Things", "Daffodils", "A Household Book",
    "Lunch", "The Friend of Man", "The Diary Habit", "Midsummer Day",
    "At the Bookstall", "A Day at Lord's", "By the Sea", "Signs of Character",
    "Intellectual Snobbery", "A Question of Form", "The Label", "The Profession",
}
GARDINER = {
    "ON CHOOSING A NAME", "ON LETTER-WRITING", "ON READING IN BED", "ON CATS AND DOGS",
    "ON SEEING VISIONS", "THE VILLAGE AND THE WAR", "ON RUMOUR", "ON UMBRELLA MORALS",
    "ON TALKING TO ONE'S SELF", "ON SEEING OURSELVES", "ON THE ENGLISH SPIRIT",
    "ON FALLING IN LOVE", "ON A BIT OF SEAWEED", "ON LIVING AGAIN", "TU-WHIT, TU-WHOO!",
    "ON POINTS OF VIEW", "ON BEER AND PORCELAIN", "ON A CASE OF CONSCIENCE",
    "ON THE DISLIKE OF LAWYERS", "ON THE CHEERFULNESS OF THE BLIND",
    "ON THOUGHTS AT FIFTY", "THE ONE-EYED CAT", "IN PRAISE OF WALKING",
    "ON A HAWTHORN HEDGE",
}
CHESTERTON_SKIP = {"The Secret of a Train", "A Tragedy of Twopence"}
CHESTERTON_EXTRA = {"ON RUNNING AFTER ONE’S HAT", "ANONYMITY AND FURTHER COUNSELS"}
ANTHOLOGY = {
    "THE MARKET By William Mcfee",
    "AMERICA AND THE ENGLISH TRADITION By Harry Morgan Ayres",
    "ON LYING AWAKE AT NIGHT By Stewart Edward White",
    "A WOODLAND VALENTINE By Marian Storm",
    "WINTER MIST By Robert Palfrey Utter",
}


def word_count(text):
    return len(WORD.findall(text))


def clean_paragraph(value):
    value = re.sub(r"\[Pg\s*\d+\]", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def chapter_paragraphs(heading, book_id):
    if heading.parent.name == "div" and "chapter" in heading.parent.get("class", []):
        nodes = heading.parent.find_all("p")
    else:
        nodes = []
        for sibling in heading.next_siblings:
            if getattr(sibling, "name", None) == "h2":
                break
            if getattr(sibling, "name", None):
                if book_id == 38280 and ("blockquot" in sibling.get("class", []) or any(x.startswith("fig") for x in sibling.get("class", []))):
                    continue
                if sibling.name == "p":
                    nodes.append(sibling)
                else:
                    nodes.extend(sibling.find_all("p"))
    return [p for node in nodes if (p := clean_paragraph(node.get_text(" ", strip=True)))]


def split_three(paragraphs):
    lens = [word_count(p) for p in paragraphs]
    n = len(lens)
    if n < 6:
        return None
    running = [0]
    for length in lens:
        running.append(running[-1] + length)
    target = running[-1] / 3
    choices = []
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            blocks = (running[i], running[j] - running[i], running[n] - running[j])
            if min(blocks) >= 250:
                choices.append((sum((x - target) ** 2 for x in blocks), i, j, blocks))
    return min(choices) if choices else None


def load_book(book_id):
    for directory in SOURCE_DIRS:
        path = directory / f"pg{book_id}.html"
        if path.exists():
            break
    else:
        raise FileNotFoundError(book_id)
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    if book_id == 5803:
        for heading in soup.find_all("p"):
            if "margin-top: 4em" not in heading.get("style", ""):
                continue
            title = re.sub(r"\s+", " ", heading.get_text(" ", strip=True))
            paragraphs = []
            for sibling in heading.next_siblings:
                if getattr(sibling, "name", None) == "p" and "margin-top: 4em" in sibling.get("style", ""):
                    break
                if getattr(sibling, "name", None) == "p":
                    value = clean_paragraph(sibling.get_text(" ", strip=True))
                    if value:
                        paragraphs.append(value)
            words = sum(word_count(p) for p in paragraphs)
            split = split_three(paragraphs)
            if 800 <= words <= 1500 and split:
                yield title, paragraphs, words, split
        return
    for heading in soup.find_all("h2"):
        title = re.sub(r"\s+", " ", heading.get_text(" ", strip=True))
        if book_id == 34462 and re.fullmatch(r"[IVXLCDM]+", title):
            continue
        paragraphs = chapter_paragraphs(heading, book_id)
        words = sum(word_count(p) for p in paragraphs)
        if 800 <= words <= 1500 and len(paragraphs) >= 6:
            split = split_three(paragraphs)
            if split:
                yield title, paragraphs, words, split


if __name__ == "__main__":
    chosen = []
    for book_id in BOOKS:
        rows = list(load_book(book_id))
        for title, paragraphs, words, split in rows:
            use = (
                book_id == 386
                or book_id == 5803 and title in MILNE
                or book_id == 10675 and title in GARDINER
                or book_id == 34462 and title != "WHAT THE SUN DID NOT SEE—FOR FAR TOO LONG"
                or book_id == 8092 and not any(title.endswith(x) for x in CHESTERTON_SKIP)
                or book_id == 11505 and title in CHESTERTON_EXTRA
                or book_id == 38280 and title in ANTHOLOGY
            )
            if use:
                chosen.append((book_id, title, paragraphs, words, split))
    if len(chosen) != 100:
        raise RuntimeError(f"Expected 100 selected essays, got {len(chosen)}")

    source_dir = ROOT / "source_html"
    source_dir.mkdir(exist_ok=True)
    text_dir = ROOT / "texts"
    text_dir.mkdir(exist_ok=True)
    for book_id in {row[0] for row in chosen}:
        target = source_dir / f"pg{book_id}.html"
        if not target.exists():
            shutil.copy2(ROOT.parent / "01-原始数据" / target.name, target)

    output = []
    for index, (book_id, title, paragraphs, words, split) in enumerate(chosen, start=1):
        essay_id = f"E{index:03d}"
        author, collection, year = BOOKS[book_id]
        if book_id == 38280:
            title, author = title.rsplit(" By ", 1)
        if book_id == 8092:
            title = re.sub(r"^[IVXLCDM]+\.\s*", "", title)
        body = "\n\n".join(paragraphs) + "\n"
        path = text_dir / f"{essay_id}.txt"
        path.write_text(body, encoding="utf-8")
        url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html"
        output.append({
            "id": essay_id,
            "title": title,
            "author": author,
            "source_url": url,
            "text_path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "length": words,
            "paragraphs": len(paragraphs),
            "block1_words": split[3][0],
            "block2_words": split[3][1],
            "block3_words": split[3][2],
            "block_cut_after_paragraphs": f"{split[1]},{split[2]}",
            "collection": collection,
            "publication_year": year,
            "book_id": book_id,
            "source_html_path": f"source_html/pg{book_id}.html",
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "rights_note": "Project Gutenberg marks the ebook public domain in the USA; local reuse rules may differ.",
            "notes": "Body only; natural paragraphs retained. Collection year is not necessarily first publication year; PG 386 transcribes an 1897 edition and PG 11505 a 1915 edition.",
        })
    if len({(x["author"].casefold(), x["title"].casefold()) for x in output}) != 100:
        raise RuntimeError("Duplicate author/title")
    if len({x["sha256"] for x in output}) != 100:
        raise RuntimeError("Duplicate text")
    fields = list(output[0])
    with (ROOT / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    print("selected", len(output))
    print("authors", dict(Counter(row["author"] for row in output)))
    print("books", dict(Counter(row["book_id"] for row in output)))
