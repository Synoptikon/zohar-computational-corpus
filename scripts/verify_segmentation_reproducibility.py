#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SEGMENTATION_VERSION = "SEGMENTATION-RULES-0.1"
OUTPUT_SCHEMA_VERSION = "SID-CONTRACT-0.1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*.json"))
        if path.is_file()
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compare_run_to_normalized(normalized_dir: Path, segment_dir: Path) -> dict:
    errors: list[dict] = []
    normalized_files = sorted(
        path for path in normalized_dir.glob("*.json") if path.name != "normalized_manifest.json"
    )
    segment_files = sorted(segment_dir.glob("*.json"))
    normalized_names = {path.name for path in normalized_files}
    segment_names = {path.name for path in segment_files}

    for name in sorted(normalized_names - segment_names):
        errors.append({"type": "MISSING_SEGMENT_FILE", "file": name})
    for name in sorted(segment_names - normalized_names):
        errors.append({"type": "UNEXPECTED_SEGMENT_FILE", "file": name})

    records = 0
    segments = 0
    for normalized_path in normalized_files:
        segment_path = segment_dir / normalized_path.name
        if not segment_path.exists():
            continue
        normalized = load_json(normalized_path)
        segmented = load_json(segment_path)
        source_records = normalized.get("records")
        output_segments = segmented.get("segments")
        if not isinstance(source_records, list) or not isinstance(output_segments, list):
            errors.append({"type": "INVALID_STRUCTURE", "file": normalized_path.name})
            continue

        records += len(source_records)
        segments += len(output_segments)
        if segmented.get("schema_version") != OUTPUT_SCHEMA_VERSION:
            errors.append({"type": "INVALID_SCHEMA_VERSION", "file": normalized_path.name})
        if segmented.get("segmentation_version") != SEGMENTATION_VERSION:
            errors.append({"type": "INVALID_SEGMENTATION_VERSION", "file": normalized_path.name})
        if len(source_records) != len(output_segments):
            errors.append({
                "type": "RECORD_SEGMENT_COUNT_MISMATCH",
                "file": normalized_path.name,
                "records": len(source_records),
                "segments": len(output_segments),
            })
            continue

        for index, (record, segment) in enumerate(zip(source_records, output_segments)):
            checks = {
                "sequence": record.get("sequence") == segment.get("sequence"),
                "raw_start": record.get("raw_start") == segment.get("raw_start"),
                "raw_end": record.get("raw_end") == segment.get("raw_end"),
                "raw_text": record.get("raw_text") == segment.get("raw_text"),
                "normalized_text": record.get("normalized_text") == segment.get("normalized_text"),
                "offset_unit": record.get("offset_unit") == segment.get("offset_unit"),
            }
            for field, ok in checks.items():
                if not ok:
                    errors.append({
                        "type": "RECORD_SEGMENT_MISMATCH",
                        "file": normalized_path.name,
                        "segment_index": index,
                        "field": field,
                    })

    return {
        "normalized_files": len(normalized_files),
        "segment_files": len(segment_files),
        "records": records,
        "segments": segments,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify GATE-002 segmentation preservation and byte reproducibility.")
    parser.add_argument("--normalized-dir", required=True)
    parser.add_argument("--run1-dir", required=True)
    parser.add_argument("--run2-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    normalized_dir = Path(args.normalized_dir)
    run1_dir = Path(args.run1_dir)
    run2_dir = Path(args.run2_dir)

    run1 = compare_run_to_normalized(normalized_dir, run1_dir)
    run2 = compare_run_to_normalized(normalized_dir, run2_dir)
    hashes1 = directory_hashes(run1_dir)
    hashes2 = directory_hashes(run2_dir)
    same_file_set = set(hashes1) == set(hashes2)
    hash_mismatches = sorted(
        name for name in set(hashes1) | set(hashes2) if hashes1.get(name) != hashes2.get(name)
    )
    byte_identical = same_file_set and not hash_mismatches

    report = {
        "audit_version": "SEGMENT-REPRO-AUDIT-0.1",
        "segmentation_version": SEGMENTATION_VERSION,
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "run1": run1,
        "run2": run2,
        "reproducibility": {
            "file_sets_identical": same_file_set,
            "hash_mismatches": hash_mismatches,
            "byte_identical": byte_identical,
            "run1_sha256": hashes1,
            "run2_sha256": hashes2,
        },
        "status": "PASS" if run1["status"] == "PASS" and run2["status"] == "PASS" and byte_identical else "FAIL",
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "records": run1["records"],
        "segments": run1["segments"],
        "byte_identical": byte_identical,
        "hash_mismatches": len(hash_mismatches),
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
