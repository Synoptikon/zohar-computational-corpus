#!/usr/bin/env python3
"""Create an auditable extraction derivative from the immutable RAW snapshot.

This first implementation deliberately performs conservative extraction only:
it classifies MediaWiki constructs and preserves unresolved markup instead of
silently deleting it. Template expansion is not guessed locally.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SCHEMA_VERSION = "0.1"
EXTRACTOR_VERSION = "0.1.0"
TEMPLATE_RE = re.compile(r"\{\{.*?\}\}", re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
LINK_RE = re.compile(r"\[\[.*?\]\]", re.DOTALL)
CATEGORY_RE = re.compile(r"\[\[קטגוריה:.*?\]\]", re.DOTALL)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(text: str) -> dict:
    templates = TEMPLATE_RE.findall(text)
    links = LINK_RE.findall(text)
    categories = CATEGORY_RE.findall(text)
    tags = TAG_RE.findall(text)
    references = [tag for tag in tags if re.search(r"references?|ref", tag, re.I)]
    navigation = [item for item in templates if any(k in item for k in ("סרגל", "ניווט", "תוכן עניינים", "דף של זהר"))]
    unknown_templates = [item for item in templates if item not in navigation and "קטע זוהר" not in item]
    return {
        "template_count": len(templates),
        "link_count": len(links),
        "tag_count": len(tags),
        "reference_count": len(references),
        "category_count": len(categories),
        "navigation_count": len(navigation),
        "unknown_markup_count": len(unknown_templates),
        "unknown_markup_samples": unknown_templates[:10],
    }


def extract(text: str) -> tuple[str, dict]:
    diagnostics = classify(text)
    # Conservative mode: preserve unresolved templates and markup verbatim.
    # This makes the derivative auditable but intentionally does not claim to
    # recover lexical text. A later E1 implementation must resolve templates.
    return text, diagnostics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/derived/zohar/extracted"))
    parser.add_argument("--manifest", type=Path, default=None)
    args = parser.parse_args()

    manifest_path = args.manifest or (args.snapshot / "snapshot_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)

    records = []
    blocked = 0
    for page in manifest["pages"]:
        source = Path(page["path"])
        if not source.is_absolute():
            source = Path.cwd() / source
        actual = sha256(source)
        if actual != page["sha256"]:
            raise SystemExit(f"FAIL: source hash mismatch: {source}")
        text = source.read_text(encoding="utf-8")
        extracted, diagnostics = extract(text)
        status = "BLOCKED" if diagnostics["unknown_markup_count"] else "PASS"
        blocked += status == "BLOCKED"
        target = args.output / source.name
        target.write_text(extracted, encoding="utf-8", newline="\n")
        records.append({
            "schema_version": SCHEMA_VERSION,
            "cid": "CID-ZOHAR-WIKISOURCE-MANTUA",
            "sequence": page["sequence"],
            "pageid": page["pageid"],
            "revid": page["revid"],
            "source_path": str(source),
            "source_sha256": actual,
            "extraction_method": "E0_CONSERVATIVE_CLASSIFY",
            "extractor_version": EXTRACTOR_VERSION,
            "extracted_path": str(target),
            "extracted_sha256": sha256(target),
            "diagnostics": diagnostics,
            "status": status,
        })

    output_manifest = args.output / "extraction_manifest.json"
    output_manifest.write_text(json.dumps({
        "schema_version": SCHEMA_VERSION,
        "extractor_version": EXTRACTOR_VERSION,
        "source_manifest": str(manifest_path),
        "page_count": len(records),
        "blocked_count": blocked,
        "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Processed {len(records)} pages; blocked={blocked}")
    print(f"Manifest: {output_manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
