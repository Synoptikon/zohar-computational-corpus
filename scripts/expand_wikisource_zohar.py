#!/usr/bin/env python3
"""Expand Wikisource Zohar wikitext through the MediaWiki API.

E1 deliberately stores expanded wikitext as a derivative. It never mutates
RAW. Template dependency metadata is recorded, but dependency locking is not
claimed unless dependency content is separately captured and replayable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SCHEMA_VERSION = "0.1"
EXTRACTOR_VERSION = "0.1.0"
UNRESOLVED_TEMPLATE_RE = re.compile(r"\{\{", re.DOTALL)
TEMPLATE_END_RE = re.compile(r"\}\}", re.DOTALL)
HTML_TAG_RE = re.compile(r"<[^>]+>")
LINK_RE = re.compile(r"\[\[.*?\]\]", re.DOTALL)
REFERENCE_RE = re.compile(r"<\s*(?:ref|references)\b", re.I)
CATEGORY_RE = re.compile(r"\[\[\s*(?:קטגוריה|Category)\s*:", re.I)
HEADING_RE = re.compile(r"^\s*=+[^=].*?=+\s*$", re.MULTILINE)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_request_hash(params: dict[str, object]) -> str:
    canonical = urlencode(sorted((k, str(v)) for k, v in params.items()), doseq=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def api_call(endpoint: str, params: dict[str, object], timeout: int = 60) -> dict:
    payload = urlencode(params, doseq=True).encode("utf-8")
    request = Request(
        endpoint,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "zohar-computational-corpus/E1-0.1.0",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
    result = json.loads(raw.decode("utf-8"))
    if "error" in result:
        raise RuntimeError(json.dumps(result["error"], ensure_ascii=False))
    return result


def extract_expanded_wikitext(endpoint: str, title: str, revid: int, text: str) -> tuple[str, dict]:
    params = {
        "action": "expandtemplates",
        "format": "json",
        "formatversion": "2",
        "text": text,
        "title": title,
        "revid": revid,
        "prop": "wikitext",
    }
    result = api_call(endpoint, params)
    expand = result.get("expandtemplates", {})
    expanded = expand.get("wikitext")
    if expanded is None:
        raise RuntimeError("MediaWiki expandtemplates returned no wikitext")
    return expanded, {
        "api_warnings": result.get("warnings", {}),
        "request_parameters_hash": canonical_request_hash(params),
    }


def get_templates(endpoint: str, title: str, revid: int) -> list[dict]:
    params = {
        "action": "parse",
        "format": "json",
        "formatversion": "2",
        "oldid": revid,
        "prop": "templates",
    }
    result = api_call(endpoint, params)
    templates = result.get("parse", {}).get("templates", [])
    return templates if isinstance(templates, list) else []


def get_template_revision(endpoint: str, title: str) -> dict:
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "revisions",
        "titles": title,
        "rvprop": "ids|timestamp|sha1",
        "rvlimit": 1,
    }
    result = api_call(endpoint, params)
    pages = result.get("query", {}).get("pages", [])
    if not pages:
        return {"title": title, "status": "MISSING"}
    page = pages[0]
    revisions = page.get("revisions", [])
    if not revisions:
        return {
            "title": page.get("title", title),
            "pageid": page.get("pageid"),
            "status": "MISSING",
        }
    rev = revisions[0]
    return {
        "title": page.get("title", title),
        "pageid": page.get("pageid"),
        "revid": rev.get("revid"),
        "timestamp": rev.get("timestamp"),
        "sha1": rev.get("sha1"),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "RECORDED",
    }


def unique_template_titles(templates: list[dict]) -> list[str]:
    titles: list[str] = []
    seen: set[str] = set()
    for item in templates:
        title = item.get("title") if isinstance(item, dict) else None
        if title and title not in seen:
            seen.add(title)
            titles.append(title)
    return titles


def diagnostics(raw: str, expanded: str) -> dict:
    unresolved = [m.group(0) for m in UNRESOLVED_TEMPLATE_RE.finditer(expanded)]
    return {
        "raw_template_count": len(re.findall(r"\{\{", raw)),
        "expanded_template_count": len(re.findall(r"\{\{", raw)) - len(unresolved),
        "unresolved_template_count": len(unresolved),
        "unresolved_template_samples": unresolved[:10],
        "html_tag_count": len(HTML_TAG_RE.findall(expanded)),
        "link_count": len(LINK_RE.findall(expanded)),
        "reference_count": len(REFERENCE_RE.findall(expanded)),
        "category_count": len(CATEGORY_RE.findall(expanded)),
        "heading_count": len(HEADING_RE.findall(expanded)),
        "empty_output": not bool(expanded.strip()),
        "api_warnings": {},
        "api_errors": [],
    }


def selected_pages(pages: list[dict], sequences: set[int] | None, limit: int | None) -> list[dict]:
    result = [p for p in pages if sequences is None or p["sequence"] in sequences]
    if limit is not None:
        result = result[:limit]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/derived/zohar/extracted_e1"))
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--endpoint", default="https://he.wikisource.org/w/api.php")
    parser.add_argument("--sequence", type=int, action="append")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--sleep", type=float, default=0.1)
    args = parser.parse_args()

    manifest_path = args.manifest or (args.snapshot / "snapshot_manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages = selected_pages(manifest["pages"], set(args.sequence) if args.sequence else None, args.limit)
    args.output.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    blocked = 0
    failed = 0

    for page in pages:
        source = Path(page["path"])
        if not source.is_absolute():
            source = Path.cwd() / source
        actual_source_sha256 = sha256_file(source)
        if actual_source_sha256 != page["sha256"]:
            raise SystemExit(f"FAIL: source hash mismatch: {source}")

        raw = source.read_text(encoding="utf-8")
        retrieved_at = datetime.now(timezone.utc).isoformat()
        try:
            expanded, api_meta = extract_expanded_wikitext(
                args.endpoint, page["title"], page["revid"], raw
            )
            template_nodes = get_templates(args.endpoint, page["title"], page["revid"])
            dependencies = []
            for template_title in unique_template_titles(template_nodes):
                try:
                    dependencies.append(get_template_revision(args.endpoint, template_title))
                except Exception as exc:  # dependency metadata must not erase the E1 artifact
                    dependencies.append({"title": template_title, "status": "MISSING", "error": str(exc)})
                time.sleep(args.sleep)

            diag = diagnostics(raw, expanded)
            diag["api_warnings"] = api_meta.get("api_warnings", {})
            status = "BLOCKED" if diag["unresolved_template_count"] else "PASS"
            blocked += status == "BLOCKED"

            target = args.output / source.name
            target.write_text(expanded, encoding="utf-8", newline="\n")
            records.append({
                "schema_version": SCHEMA_VERSION,
                "cid": manifest.get("cid", "UNASSIGNED"),
                "sequence": page["sequence"],
                "pageid": page["pageid"],
                "revid": page["revid"],
                "page_title": page["title"],
                "source_path": str(source),
                "source_sha256": actual_source_sha256,
                "api_endpoint": args.endpoint,
                "extraction_method": "E1_MEDIAVIKI_EXPANDTEMPLATES",
                "extractor_version": EXTRACTOR_VERSION,
                "request_parameters_hash": api_meta["request_parameters_hash"],
                "extracted_path": str(target),
                "extracted_sha256": sha256_file(target),
                "retrieved_at_utc": retrieved_at,
                "status": status,
                "reproducibility_status": "CONDITIONAL",
                "diagnostics": diag,
                "dependencies": dependencies,
            })
        except Exception as exc:
            failed += 1
            records.append({
                "schema_version": SCHEMA_VERSION,
                "cid": manifest.get("cid", "UNASSIGNED"),
                "sequence": page["sequence"],
                "pageid": page["pageid"],
                "revid": page["revid"],
                "page_title": page["title"],
                "source_path": str(source),
                "source_sha256": actual_source_sha256,
                "api_endpoint": args.endpoint,
                "extraction_method": "E1_MEDIAVIKI_EXPANDTEMPLATES",
                "extractor_version": EXTRACTOR_VERSION,
                "retrieved_at_utc": retrieved_at,
                "status": "FAIL",
                "reproducibility_status": "BLOCKED",
                "diagnostics": {"api_errors": [str(exc)]},
                "dependencies": [],
            })
        time.sleep(args.sleep)

    output_manifest = args.output / "extraction_manifest.json"
    output_manifest.write_text(
        json.dumps({
            "schema_version": SCHEMA_VERSION,
            "extractor_version": EXTRACTOR_VERSION,
            "source_manifest": str(manifest_path),
            "api_endpoint": args.endpoint,
            "page_count": len(records),
            "blocked_count": blocked,
            "failed_count": failed,
            "records": records,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Processed {len(records)} pages; blocked={blocked}; failed={failed}")
    print(f"Manifest: {output_manifest}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
