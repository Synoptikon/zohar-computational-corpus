#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PAIR_VALIDATION_VERSION = "ANNOTATION-PILOT-PAIR-VALIDATION-0.1"
REQUIRED_METADATA = {
    "annotation_schema_version",
    "pilot_version",
    "selector_version",
    "selection_method",
    "vocabulary_version",
    "guidelines_version",
    "cid",
    "population_size",
    "sample_size",
    "population_sid_sha256",
    "selected_sid_sha256",
}
ALLOWED_ANNOTATORS = {"annotator_a", "annotator_b"}


def load_document(path: Path) -> dict:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(json.dumps({"type": "INVALID_JSON", "file": str(path), "error": str(exc)})) from exc
    if not isinstance(document, dict):
        raise ValueError(json.dumps({"type": "TOP_LEVEL_NOT_OBJECT", "file": str(path)}))
    return document


def sid_digest(sids: list[str]) -> str:
    payload = "\n".join(sorted(sids)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def inspect_document(document: dict, path: Path) -> tuple[list[dict], list[str]]:
    errors: list[dict] = []
    segments = document.get("segments")
    if not isinstance(segments, list) or not segments:
        errors.append({"type": "INVALID_SEGMENTS", "file": str(path)})
        return errors, []

    annotator = document.get("annotator")
    if annotator not in ALLOWED_ANNOTATORS:
        errors.append({"type": "INVALID_ANNOTATOR", "file": str(path), "value": annotator})

    missing = REQUIRED_METADATA - set(document)
    if missing:
        errors.append({"type": "MISSING_METADATA", "file": str(path), "fields": sorted(missing)})

    sids: list[str] = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict) or not isinstance(segment.get("sid"), str) or not segment["sid"]:
            errors.append({"type": "INVALID_SEGMENT", "file": str(path), "index": index})
            continue
        sids.append(segment["sid"])
        if not isinstance(segment.get("annotations"), list):
            errors.append({"type": "ANNOTATIONS_NOT_LIST", "file": str(path), "index": index})
        if not isinstance(segment.get("abstain"), bool):
            errors.append({"type": "ABSTAIN_NOT_BOOLEAN", "file": str(path), "index": index})

    if len(sids) != len(set(sids)):
        errors.append({"type": "SID_COLLISION", "file": str(path)})

    return errors, sids


def validate_pair(path_a: Path, path_b: Path, output_path: Path) -> dict:
    errors: list[dict] = []
    try:
        doc_a = load_document(path_a)
        doc_b = load_document(path_b)
    except ValueError as exc:
        try:
            error = json.loads(str(exc))
        except json.JSONDecodeError:
            error = {"type": "INVALID_DOCUMENT", "message": str(exc)}
        errors.append(error)
        report = {"validation_version": PAIR_VALIDATION_VERSION, "status": "FAIL", "errors": errors}
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return report

    errors_a, sids_a = inspect_document(doc_a, path_a)
    errors_b, sids_b = inspect_document(doc_b, path_b)
    errors.extend(errors_a + errors_b)

    if doc_a.get("annotator") == doc_b.get("annotator"):
        errors.append({"type": "ANNOTATOR_COLLISION", "annotator": doc_a.get("annotator")})
    if doc_a.get("annotator") != "annotator_a" or doc_b.get("annotator") != "annotator_b":
        errors.append({"type": "ANNOTATOR_PAIR_ORDER", "expected": ["annotator_a", "annotator_b"]})

    for field in sorted(REQUIRED_METADATA):
        if doc_a.get(field) != doc_b.get(field):
            errors.append({"type": "METADATA_MISMATCH", "field": field, "annotator_a": doc_a.get(field), "annotator_b": doc_b.get(field)})

    if sids_a != sids_b:
        errors.append({
            "type": "SID_SET_MISMATCH",
            "only_in_annotator_a": sorted(set(sids_a) - set(sids_b)),
            "only_in_annotator_b": sorted(set(sids_b) - set(sids_a)),
        })

    expected_digest = doc_a.get("selected_sid_sha256")
    actual_digest = sid_digest(sids_a)
    if expected_digest != actual_digest:
        errors.append({"type": "SELECTED_SID_DIGEST_MISMATCH", "expected": expected_digest, "actual": actual_digest})

    report = {
        "validation_version": PAIR_VALIDATION_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "annotator_a": str(path_a),
        "annotator_b": str(path_b),
        "sample_size": len(sids_a),
        "sid_count_a": len(sids_a),
        "sid_count_b": len(sids_b),
        "selected_sid_sha256": actual_digest,
        "errors": errors,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate two independent annotation shells against the same frozen pilot.")
    parser.add_argument("--annotator-a", required=True)
    parser.add_argument("--annotator-b", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = validate_pair(Path(args.annotator_a), Path(args.annotator_b), Path(args.output))
    print(json.dumps({k: v for k, v in report.items() if k != "errors"}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
