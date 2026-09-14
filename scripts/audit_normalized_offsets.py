#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from zohar_corpus.normalization import normalize_text

EXPECTED_NORMALIZATION_VERSION = "NORMALIZATION-RULES-0.2"
EXPECTED_OFFSET_UNIT = "unicode_codepoint_index"
MANIFEST_NAME = "normalized_manifest.json"


def audit_record(record: object, record_index: int, raw_content: str | None) -> tuple[list[dict], list[dict]]:
    errors: list[dict] = []
    warnings: list[dict] = []
    if not isinstance(record, dict):
        return [{"record_index": record_index, "type": "RECORD_NOT_OBJECT"}], warnings

    required = {
        "raw_start", "raw_end", "raw_text", "normalized_text",
        "normalization_rule", "normalization_version", "offset_unit",
    }
    missing = sorted(required - set(record))
    if missing:
        return [{"record_index": record_index, "type": "MISSING_FIELDS", "fields": missing}], warnings

    start = record["raw_start"]
    end = record["raw_end"]
    raw_text = record["raw_text"]
    normalized_text = record["normalized_text"]

    if not isinstance(start, int) or not isinstance(end, int):
        errors.append({"record_index": record_index, "type": "INVALID_OFFSET_TYPE"})
        return errors, warnings
    if start < 0 or end < start:
        errors.append({"record_index": record_index, "type": "INVALID_OFFSET_RANGE", "raw_start": start, "raw_end": end})
    if not isinstance(raw_text, str):
        errors.append({"record_index": record_index, "type": "INVALID_RAW_TEXT_TYPE"})
        return errors, warnings
    if not isinstance(normalized_text, str):
        errors.append({"record_index": record_index, "type": "INVALID_NORMALIZED_TEXT_TYPE"})
        return errors, warnings

    if end - start != len(raw_text):
        errors.append({
            "record_index": record_index,
            "type": "RAW_TEXT_LENGTH_MISMATCH",
            "offset_length": end - start,
            "raw_text_length": len(raw_text),
        })

    if raw_content is not None:
        if end > len(raw_content):
            errors.append({
                "record_index": record_index,
                "type": "OFFSET_OUT_OF_BOUNDS",
                "raw_end": end,
                "raw_length": len(raw_content),
            })
        elif raw_content[start:end] != raw_text:
            errors.append({
                "record_index": record_index,
                "type": "RAW_OFFSET_CONTENT_MISMATCH",
                "raw_start": start,
                "raw_end": end,
            })

    if record["normalization_version"] != EXPECTED_NORMALIZATION_VERSION:
        errors.append({
            "record_index": record_index,
            "type": "NORMALIZATION_VERSION_MISMATCH",
            "actual": record["normalization_version"],
            "expected": EXPECTED_NORMALIZATION_VERSION,
        })
    if record["offset_unit"] != EXPECTED_OFFSET_UNIT:
        errors.append({
            "record_index": record_index,
            "type": "OFFSET_UNIT_MISMATCH",
            "actual": record["offset_unit"],
            "expected": EXPECTED_OFFSET_UNIT,
        })
    if record["normalization_rule"] != "NFC + whitespace":
        errors.append({
            "record_index": record_index,
            "type": "NORMALIZATION_RULE_MISMATCH",
            "actual": record["normalization_rule"],
            "expected": "NFC + whitespace",
        })

    if normalized_text != normalize_text(raw_text):
        errors.append({"record_index": record_index, "type": "NORMALIZED_TEXT_MISMATCH"})

    return errors, warnings


def audit_file(path: Path, repo_root: Path) -> dict:
    errors: list[dict] = []
    warnings: list[dict] = []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "INVALID_JSON", "error": str(exc)}], "warnings": [], "records": 0}

    if not isinstance(document, dict):
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "TOP_LEVEL_NOT_OBJECT"}], "warnings": [], "records": 0}

    records = document.get("records")
    if not isinstance(records, list):
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "RECORDS_NOT_LIST"}], "warnings": [], "records": 0}

    raw_path_value = document.get("raw_file")
    raw_content: str | None = None
    if not isinstance(raw_path_value, str) or not raw_path_value:
        errors.append({"type": "MISSING_RAW_FILE"})
    else:
        raw_path = repo_root / "data/raw/zohar/wikisource" / raw_path_value
        if not raw_path.exists():
            errors.append({"type": "RAW_FILE_NOT_FOUND", "raw_file": raw_path_value})
        else:
            try:
                raw_content = raw_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                errors.append({"type": "RAW_FILE_READ_ERROR", "raw_file": raw_path_value, "error": str(exc)})

    previous_end = None
    for index, record in enumerate(records):
        record_errors, record_warnings = audit_record(record, index, raw_content)
        errors.extend(record_errors)
        warnings.extend(record_warnings)
        if isinstance(record, dict) and isinstance(record.get("raw_end"), int):
            current_start = record.get("raw_start")
            if previous_end is not None and isinstance(current_start, int) and current_start < previous_end:
                warnings.append({"record_index": index, "type": "NON_MONOTONIC_OFFSET", "previous_end": previous_end, "raw_start": current_start})
            previous_end = record["raw_end"]

    if raw_content is not None:
        reconstructed = "".join(record.get("raw_text", "") for record in records if isinstance(record, dict))
        if reconstructed != raw_content:
            errors.append({"type": "RAW_RECONSTRUCTION_MISMATCH"})
        if records:
            last_end = records[-1].get("raw_end") if isinstance(records[-1], dict) else None
            if last_end != len(raw_content):
                errors.append({"type": "FINAL_OFFSET_MISMATCH", "final_offset": last_end, "raw_length": len(raw_content)})

    return {"file": str(path), "status": "PASS" if not errors else "FAIL", "errors": errors, "warnings": warnings, "records": len(records)}


def audit_directory(input_dir: Path, output: Path, repo_root: Path) -> dict:
    files = sorted(p for p in input_dir.glob("*.json") if p.name != MANIFEST_NAME)
    results = [audit_file(path, repo_root) for path in files]
    failed_files = [result for result in results if result["status"] != "PASS"]
    result = {
        "audit_version": "NORMALIZED-OFFSETS-AUDIT-0.2",
        "input_dir": str(input_dir),
        "total_files": len(results),
        "total_records": sum(r["records"] for r in results),
        "total_errors": sum(len(r["errors"]) for r in results),
        "total_warnings": sum(len(r["warnings"]) for r in results),
        "failed_files": len(failed_files),
        "status": "PASS" if not failed_files else "FAIL",
        "files": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit normalized corpus offsets against the current normalization schema.")
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = audit_directory(args.input_dir, args.output, Path.cwd())
    print(json.dumps({k: result[k] for k in ("audit_version", "status", "total_files", "total_records", "total_errors", "total_warnings", "failed_files")}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
