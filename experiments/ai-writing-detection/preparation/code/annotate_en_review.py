"""Record the limited human review decisions for flagged English rewrites."""

import json

import rewrite_en as rw


REVIEWS = {
    "EN005": {
        "reviewed_quote_overlap": True,
        "review_note": "High lexical 5-gram overlap is concentrated in preserved poems and song titles quoted inside the prose; surrounding narration is substantively rephrased.",
    },
    "EN052": {
        "reviewed_quote_overlap": True,
        "review_note": "High lexical 5-gram overlap is concentrated in preserved literary quotations and cited verse; surrounding narration is substantively rephrased.",
    },
    "EN087": {
        "approved_exception": True,
        "review_note": "779-word closest saved model output retained after two targeted length retries; 21 words below the corpus hard minimum, within source ±20%, all 8 paragraphs intact.",
    },
}


def main():
    for sample_id, updates in REVIEWS.items():
        path = rw.RAW_DIR / f"{sample_id}.json"
        meta = json.loads(path.read_text(encoding="utf-8"))
        if meta["source_id"] != sample_id:
            raise ValueError(f"ID mismatch in {path}")
        meta.update(updates)
        rw.save_json(path, meta)
        print(f"{sample_id}: review recorded")


if __name__ == "__main__":
    main()
