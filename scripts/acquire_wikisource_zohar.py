#!/usr/bin/env python3
"""Acquire the Hebrew/Aramaic Zohar transcription from Hebrew Wikisource.

The script creates a deterministic local snapshot from the MediaWiki API.
It does not normalize, segment, annotate, or interpret the text.

The acquired material is licensed by Wikisource under CC BY-SA 4.0; retain
source attribution and license metadata with every redistributed snapshot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://he.wikisource.org/w/api.php"
SOURCE_URL = "https://he.wikisource.org/wiki/ספר_הזהר"
ROOT_CATEGORIES = [
    "קטגוריה:זהר חלק א",
    "קטגוריה:זהר חלק ב",
    "קטגוריה:זהר חלק ג",
]


def api(params: dict[str, str]) -> dict:
    query = urlencode({"format": "json", "formatversion": "2", **params})
    req = Request(
        f"{API}?{query}",
        headers={"User-Agent": "zohar-computational-corpus/0.1"},
    )
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def category_pages(category: str) -> list[str]:
    pages: list[str] = []
    subcategories: list[str] = []
    cont: dict[str, str] = {}

    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmtype": "page|subcat",
            "cmlimit": "500",
            **cont,
        }
        data = api(params)
        for item in data["query"]["categorymembers"]:
            title = item["title"]
            if item["ns"] == 0:
                pages.append(title)
            elif item["ns"] == 14:
                subcategories.append(title)
        if "continue" not in data:
            break
        cont = data["continue"]

    for subcategory in subcategories:
        pages.extend(category_pages(subcategory))

    return sorted(set(pages))


def fetch_revision(title: str) -> dict:
    data = api(
        {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "content|ids|timestamp",
            "rvslots": "main",
            "rvlimit": "1",
        }
    )
    page = data["query"]["pages"][0]
    revision = page["revisions"][0]
    return {
        "pageid": page["pageid"],
        "revid": revision["revid"],
        "revision_timestamp": revision["timestamp"],
        "wikitext": revision["slots"]["main"]["content"],
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw/zohar/wikisource"))
    parser.add_argument("--delay", type=float, default=0.1)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    titles = sorted({title for category in ROOT_CATEGORIES for title in category_pages(category)})

    for index, title in enumerate(titles, start=1):
        revision = fetch_revision(title)
        relative = f"{index:04d}.txt"
        target = args.output / relative
        target.write_text(revision["wikitext"], encoding="utf-8", newline="\n")
        manifest.append(
            {
                "sequence": index,
                "title": title,
                "pageid": revision["pageid"],
                "revid": revision["revid"],
                "revision_timestamp": revision["revision_timestamp"],
                "source_url": f"https://he.wikisource.org/wiki/{title.replace(' ', '_')}",
                "path": str(target),
                "sha256": sha256(target),
            }
        )
        time.sleep(args.delay)

    manifest_path = args.output / "snapshot_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "source": SOURCE_URL,
                "api": API,
                "license": "CC BY-SA 4.0",
                "retrieved_at_unix": int(time.time()),
                "page_count": len(manifest),
                "pages": manifest,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Acquired {len(manifest)} pages into {args.output}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
