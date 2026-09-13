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
import random
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://he.wikisource.org/w/api.php"
SOURCE_URL = "https://he.wikisource.org/wiki/ספר_הזהר"
ROOT_CATEGORIES = [
    "קטגוריה:זהר חלק א",
    "קטגוריה:זהר חלק ב",
    "קטגוריה:זהר חלק ג",
]
USER_AGENT = "zohar-computational-corpus/0.2 (reproducible research acquisition)"
MAX_TITLES_PER_REQUEST = 50
MAX_RETRIES = 6


def api(params: dict[str, str]) -> dict:
    query = urlencode({"format": "json", "formatversion": "2", **params})
    url = f"{API}?{query}"
    for attempt in range(MAX_RETRIES):
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(req, timeout=60) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code != 429 or attempt == MAX_RETRIES - 1:
                raise
            retry_after = exc.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                delay = float(retry_after)
            else:
                delay = min(60.0, 2.0 ** attempt) + random.uniform(0.0, 0.5)
            time.sleep(delay)

    raise RuntimeError("unreachable: API retry loop exhausted")


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

    for subcategory in sorted(set(subcategories)):
        pages.extend(category_pages(subcategory))

    return sorted(set(pages))


def fetch_revisions(titles: list[str]) -> dict[str, dict]:
    """Fetch one latest revision per title using MediaWiki's batched title API."""
    revisions: dict[str, dict] = {}
    for start in range(0, len(titles), MAX_TITLES_PER_REQUEST):
        batch = titles[start : start + MAX_TITLES_PER_REQUEST]
        data = api(
            {
                "action": "query",
                "prop": "revisions",
                "titles": "|".join(batch),
                "rvprop": "content|ids|timestamp",
                "rvslots": "main",
                "rvlimit": "1",
            }
        )
        for page in data["query"]["pages"]:
            if "revisions" not in page:
                raise RuntimeError(f"No revision returned for page {page.get('title')!r}")
            revision = page["revisions"][0]
            revisions[page["title"]] = {
                "pageid": page["pageid"],
                "revid": revision["revid"],
                "revision_timestamp": revision["timestamp"],
                "wikitext": revision["slots"]["main"]["content"],
            }
        time.sleep(0.25)
    missing = sorted(set(titles) - set(revisions))
    if missing:
        raise RuntimeError(f"Missing revisions for {len(missing)} pages: {missing[:10]}")
    return revisions


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw/zohar/wikisource"))
    parser.add_argument("--delay", type=float, default=0.1, help="Legacy per-page delay; retained for CLI compatibility.")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    titles = sorted({title for category in ROOT_CATEGORIES for title in category_pages(category)})
    revisions = fetch_revisions(titles)

    for index, title in enumerate(titles, start=1):
        revision = revisions[title]
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
        if args.delay:
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
