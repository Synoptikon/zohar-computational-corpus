#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.compare_annotation_pilots import annotation_signature, load_document, metadata_fingerprint, sid_map

CLASSIFICATION_VERSION = "ANNOTATION-DISAGREEMENT-0.1"


def classify_signatures(a: frozenset[tuple[str, str, str]], b: frozenset[tuple[str, str, str]]) -> str:
    if a == b:
        return "AGREEMENT"
    if "__ABSTAIN__" in {item[0] for item in a} or "__ABSTAIN__" in {item[0] for item in b}:
        return "ABSTAIN_MISMATCH"
    types_a = {item[0] for item in a}
    types_b = {item[0] for item in b}
    if types_a != types_b:
        return "TYPE_MISMATCH"
    values_a = {(item[0], item[1]) for item in a}
    values_b = {(item[0], item[1]) for item in b}
    if values_a != values_b:
        return "VALUE_MISMATCH"
    return "VALIDATION_STATUS_MISMATCH"


def classify_documents(a: dict[str, object], b: dict[str, object]) -> dict[str, object]:
    if metadata_fingerprint(a) != metadata_fingerprint(b):
        raise ValueError("PILOT_METADATA_MISMATCH")
    map_a = sid_map(a)
    map_b = sid_map(b)
    if set(map_a) != set(map_b):
        raise ValueError("SID_SET_MISMATCH")

    disagreements: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    for sid in sorted(map_a):
        classification = classify_signatures(map_a[sid], map_b[sid])
        counts[classification] = counts.get(classification, 0) + 1
        if classification != "AGREEMENT":
            disagreements.append({
                "sid": sid,
                "classification": classification,
                "annotator_a": [list(item) for item in sorted(map_a[sid])],
                "annotator_b": [list(item) for item in sorted(map_b[sid])],
            })

    total = len(map_a)
    return {
        "classification_version": CLASSIFICATION_VERSION,
        "pilot_version": a.get("pilot_version"),
        "sample_size": total,
        "agreement_count": counts.get("AGREEMENT", 0),
        "disagreement_count": total - counts.get("AGREEMENT", 0),
        "agreement_rate": counts.get("AGREEMENT", 0) / total if total else 0.0,
        "classification_counts": dict(sorted(counts.items())),
        "disagreements": disagreements,
        "status": "PASS" if not disagreements else "DISAGREEMENT",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify disagreements between two independent annotation pilot documents.")
    parser.add_argument("--annotator-a", required=True)
    parser.add_argument("--annotator-b", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = classify_documents(load_document(Path(args.annotator_a)), load_document(Path(args.annotator_b)))
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
