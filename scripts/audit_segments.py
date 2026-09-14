#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SEGMENTATION_VERSION = "SEGMENTATION-RULES-0.1"
REQUIRED_SEGMENT_FIELDS = {
    "sid",
    "cid",
    "source_normalized_path",
    "sequence",
    "segment_index",
    "raw_start",
    "raw_end",
    "raw_text",
    "normalized_text",
    "offset_unit",
    "segmentation_version",
    "is_empty",
}


def audit_file(path: Path) -> dict:
    errors: list[dict] = []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "INVALID_JSON", "error": str(exc)}], "segments": 0}

    if not isinstance(document, dict):
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "TOP_LEVEL_NOT_OBJECT"}], "segments": 0}

    if document.get("segmentation_version") != SEGMENTATION_VERSION:
        errors.append({"type": "INVALID_SEGMENTATION_VERSION", "value": document.get("segmentation_version")})

    segments = document.get("segments")
    if not isinstance(segments, list):
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "SEGMENTS_NOT_LIST"}], "segments": 0}

    seen_sids: set[str] = set()
    previous_sequence: int | None = None

    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            errors.append({"type": "SEGMENT_NOT_OBJECT", "segment_index": index})
            continue

        missing = REQUIRED_SEGMENT_FIELDS - set(segment)
        if missing:
            errors.append({"type": "MISSING_FIELDS", "segment_index": index, "fields": sorted(missing)})
            continue

        sid = segment["sid"]
        sequence = segment["sequence"]
        segment_index = segment["segment_index"]
        start = segment["raw_start"]
        end = segment["raw_end"]

        if not isinstance(sid, str) or not sid:
            errors.append({"type": "INVALID_SID", "segment_index": index})
        elif sid in seen_sids:
            errors.append({"type": "SID_COLLISION", "segment_index": index, "sid": sid})
        else:
            seen_sids.add(sid)

        if segment_index != index:
            errors.append({"type": "SEGMENT_INDEX_MISMATCH", "segment_index": index, "value": segment_index})
        if not isinstance(sequence, int) or isinstance(sequence, bool):
            errors.append({"type": "INVALID_SEQUENCE", "segment_index": index})
        elif previous_sequence is not None and sequence <= previous_sequence:
            errors.append({"type": "NON_MONOTONIC_SEQUENCE", "segment_index": index, "sequence": sequence})
        else:
            previous_sequence = sequence

        if not isinstance(start, int) or not isinstance(end, int):
            errors.append({"type": "INVALID_OFFSET_TYPE", "segment_index": index})
        elif start < 0 or end < start:
            errors.append({"type": "INVALID_OFFSET_ORDER", "segment_index": index, "raw_start": start, "raw_end": end})

        if not isinstance(segment["raw_text"], str) or not isinstance(segment["normalized_text"], str):
            errors.append({"type": "INVALID_TEXT_TYPE", "segment_index": index})

        if segment["is_empty"] != (segment["normalized_text"] == ""):
            errors.append({"type": "EMPTY_FLAG_MISMATCH", "segment_index": index})

    return {
        "file": str(path),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "segments": len(segments),
    }


def audit_directory(input_dir: Path, output_path: Path) -> dict:
    files = sorted(input_dir.glob("*.json"))
    results = [audit_file(path) for path in files]
    report = {
        "audit_version": "SEGMENT-AUDIT-0.1",
        "input_dir": str(input_dir),
        "total_files": len(results),
        "failed_files": sum(result["status"] != "PASS" for result in results),
        "total_segments": sum(result["segments"] for result in results),
        "total_errors": sum(len(result["errors"]) for result in results),
        "status": "PASS" if all(result["status"] == "PASS" for result in results) else "FAIL",
        "files": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit SID segmentation output.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = audit_directory(Path(args.input_dir), Path(args.output))
    print(json.dumps({k: v for k, v in report.items() if k != "files"}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
