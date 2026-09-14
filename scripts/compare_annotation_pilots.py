#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

COMPARISON_VERSION = "ANNOTATION-AGREEMENT-0.1"


def _error(code: str, message: str, **context: object) -> ValueError:
    return ValueError(json.dumps({"type": code, "message": message, **context}, ensure_ascii=False, sort_keys=True))


def load_document(path: Path) -> dict[str, object]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _error("INVALID_JSON", "unable to read annotation document", path=str(path), error=str(exc)) from exc
    if not isinstance(document, dict):
        raise _error("DOCUMENT_NOT_OBJECT", "annotation document must be an object", path=str(path))
    if document.get("status") == "UNANNOTATED":
        raise _error("UNANNOTATED_INPUT", "annotation document has not been annotated", path=str(path))
    segments = document.get("segments")
    if not isinstance(segments, list) or not segments:
        raise _error("SEGMENTS_NOT_LIST", "annotation document must contain non-empty segments", path=str(path))
    return document


def metadata_fingerprint(document: dict[str, object]) -> dict[str, object]:
    return {
        key: document.get(key)
        for key in (
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
        )
    }


def canonical_value(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def annotation_signature(annotation: object) -> tuple[str, str, str]:
    if not isinstance(annotation, dict):
        raise _error("ANNOTATION_NOT_OBJECT", "annotation must be an object")
    annotation_type = annotation.get("annotation_type")
    if not isinstance(annotation_type, str) or not annotation_type:
        raise _error("INVALID_ANNOTATION_TYPE", "annotation_type must be a non-empty string")
    return (
        annotation_type,
        canonical_value(annotation.get("value")),
        str(annotation.get("validation_status", "")),
    )


def sid_map(document: dict[str, object]) -> dict[str, frozenset[tuple[str, str, str]]]:
    segments = document["segments"]
    assert isinstance(segments, list)
    result: dict[str, frozenset[tuple[str, str, str]]] = {}
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            raise _error("SEGMENT_NOT_OBJECT", "segment must be an object", index=index)
        sid = segment.get("sid")
        if not isinstance(sid, str) or not sid:
            raise _error("INVALID_SID", "segment must contain a non-empty sid", index=index)
        if sid in result:
            raise _error("SID_COLLISION", "duplicate SID in annotation document", sid=sid)
        annotations = segment.get("annotations")
        if not isinstance(annotations, list):
            raise _error("ANNOTATIONS_NOT_LIST", "segment annotations must be a list", sid=sid)
        abstain = bool(segment.get("abstain", False))
        signatures = {annotation_signature(item) for item in annotations}
        if abstain and signatures:
            raise _error("ABSTAIN_WITH_ANNOTATIONS", "abstention cannot coexist with annotations", sid=sid)
        if abstain:
            signatures = {("__ABSTAIN__", "true", "")}
        result[sid] = frozenset(signatures)
    return result


def compare_documents(a: dict[str, object], b: dict[str, object]) -> dict[str, object]:
    meta_a = metadata_fingerprint(a)
    meta_b = metadata_fingerprint(b)
    if meta_a != meta_b:
        raise _error("PILOT_METADATA_MISMATCH", "annotator documents do not share the same frozen pilot metadata")
    map_a = sid_map(a)
    map_b = sid_map(b)
    sids_a = set(map_a)
    sids_b = set(map_b)
    if sids_a != sids_b:
        raise _error("SID_SET_MISMATCH", "annotator documents do not contain the same SID set", only_a=sorted(sids_a - sids_b), only_b=sorted(sids_b - sids_a))
    total = len(sids_a)
    agreements = sum(map_a[sid] == map_b[sid] for sid in sids_a)
    disagreements = total - agreements
    agreement_rate = agreements / total if total else 0.0
    sid_payload = "\n".join(sorted(sids_a)).encode("utf-8")
    sid_sha256 = hashlib.sha256(sid_payload).hexdigest()
    return {
        "comparison_version": COMPARISON_VERSION,
        "pilot_version": a.get("pilot_version"),
        "sample_size": total,
        "sid_sha256": sid_sha256,
        "agreements": agreements,
        "disagreements": disagreements,
        "agreement_rate": agreement_rate,
        "status": "PASS" if disagreements == 0 else "DISAGREEMENT",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two independent annotation pilot documents.")
    parser.add_argument("--annotator-a", required=True)
    parser.add_argument("--annotator-b", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = compare_documents(load_document(Path(args.annotator_a)), load_document(Path(args.annotator_b)))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
