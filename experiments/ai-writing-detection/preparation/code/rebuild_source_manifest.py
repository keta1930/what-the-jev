"""Rebuild the experiment's combined source manifest from selected essays."""

import csv
from pathlib import Path


PREPARATION = Path(__file__).resolve().parents[1]
SELECTED = PREPARATION / "clean" / "human"
rows = []
for language in ("zh", "en"):
    with (SELECTED / f"manifest.{language}.csv").open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            row["text_path"] = "clean/human/" + row["text_path"].replace("\\", "/")
            if row.get("source_html_path"):
                row["source_html_path"] = "raw/" + row["source_collection_dir"] + "/" + row["source_html_path"].replace("\\", "/")
            rows.append(row)
if len(rows) != 200:
    raise ValueError(f"Expected 200 selected essays, got {len(rows)}")
with (PREPARATION / "source_manifest.csv").open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(PREPARATION / "source_manifest.csv", len(rows))
