#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "ANNOTATION-SCHEMA-0.1"
REQUIRED_FIELDS = {
    "eid",
    "sid",
    "annotation_type",
    "value",
    "source",
    "annotator",
    "annotation_version",
    "validation_status",
}
ALLOWED_SOURCES = {"human", "rule", "llm", "import"}
ALLOWED_STATUSES = {"CANDIDATE", "REVIEWED", "ACCEPTED", "REJECTED", "SUPERSEDED"}


def validate_record(record: object, index: int) -> list[dict]:
    errors: list[dict] = []
    if not isinstance(record, dict):
        return [{"type": "ANNOTATION_NOT_OBJECT", "record_index": index}]

    missing = REQUIRED_FIELDS - set(record)
    if missing:
        return [{"type": "MISSING_FIELDS", "record_index": index, "fields": sorted(missing)}]

    for field in ("eid", "sid", "annotation_type", "annotator", "annotation_version", "validation_status"):
        if not isinstance(record[field], str) or not record[field]:
            errors.append({"type": "INVALID_STRING_FIELD", "record_index": index, "field": field})

    if record["source"] not in ALLOWED_SOURCES:
        errors.append({"type": "INVALID_SOURCE", "record_index": index, "value": record["source"]})
    if record["validation_status"] not in ALLOWED_STATUSES:
        errors.append({"type": "INVALID_VALIDATION_STATUS", "record_index": index, "value": record["validation_status"]})
    if record["annotation_version"] != SCHEMA_VERSION:
        errors.append({"type": "INVALID_SCHEMA_VERSION", "record_index": index, "value": record["annotation_version"]})

    if record["source"] == "llm" and record["validation_status"] != "CANDIDATE":
        errors.append({"type": "LLM_MUST_START_AS_CANDIDATE", "record_index": index})

    if "confidence" in record and not isinstance(record["confidence"], (int, float)):
        errors.append({"type": "INVALID_CONFIDENCE_TYPE", "record_index": index})

    return errors


def validate_document(path: Path) -> dict:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "INVALID_JSON", "error": str(exc)}], "records": 0}

    if not isinstance(document, dict):
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "TOP_LEVEL_NOT_OBJECT"}], "records": 0}

    annotations = document.get("annotations")
    if not isinstance(annotations, list):
        return {"file": str(path), "status": "ERROR", "errors": [{"type": "ANNOTATIONS_NOT_LIST"}], "records": 0}

    errors: list[dict] = []
    seen: set[str] = set()
    for index, record in enumerate(annotations):
        record_errors = validate_record(record, index)
        errors.extend(record_errors)
        if isinstance(record, dict) and isinstance(record.get("eid"), str):
            if record["eid"] in seen:
                errors.append({"type": "EID_COLLISION", "record_index": index, "eid": record["eid"]})
            seen.add(record["eid"])

    return {"file": str(path), "status": "PASS" if not errors else "FAIL", "errors": errors, "records": len(annotations)}


def validate_directory(input_dir: Path, output_path: Path) -> dict:
    files = sorted(input_dir.glob("*.json"))
    results = [validate_document(path) for path in files]
    report = {
        "validation_version": SCHEMA_VERSION,
        "input_dir": str(input_dir),
        "total_files": len(results),
        "failed_files": sum(result["status"] != "PASS" for result in results),
        "total_records": sum(result["records"] for result in results),
        "total_errors": sum(len(result["errors"]) for result in results),
        "status": "PASS" if all(result["status"] == "PASS" for result in results) else "FAIL",
        "files": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate annotation records against ANNOTATION-SCHEMA-0.1.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = validate_directory(Path(args.input_dir), Path(args.output))
    print(json.dumps({k: v for k, v in report.items() if k != "files"}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
