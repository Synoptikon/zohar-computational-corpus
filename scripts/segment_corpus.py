#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SEGMENTATION_VERSION = "SEGMENTATION-RULES-0.1"
OUTPUT_SCHEMA_VERSION = "SID-CONTRACT-0.1"
DEFAULT_SOURCE_MANIFEST = "data/sources/zohar_primary_wikisource.json"

REQUIRED_RECORD_FIELDS = {
    "sequence",
    "raw_start",
    "raw_end",
    "raw_text",
    "normalized_text",
    "normalization_version",
    "offset_unit",
}


def _error(code: str, message: str, **context: object) -> ValueError:
    payload = {"type": code, "message": message, **context}
    return ValueError(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _validate_record(record: object, index: int, previous_sequence: int | None) -> int:
    if not isinstance(record, dict):
        raise _error("RECORD_NOT_OBJECT", "normalized record must be an object", record_index=index)

    missing = REQUIRED_RECORD_FIELDS - set(record)
    if missing:
        raise _error(
            "MISSING_FIELDS",
            "normalized record is missing required fields",
            record_index=index,
            fields=sorted(missing),
        )

    sequence = record["sequence"]
    raw_start = record["raw_start"]
    raw_end = record["raw_end"]
    raw_text = record["raw_text"]
    normalized_text = record["normalized_text"]

    if not isinstance(sequence, int) or isinstance(sequence, bool):
        raise _error("INVALID_SEQUENCE_TYPE", "sequence must be an integer", record_index=index)
    if previous_sequence is not None and sequence <= previous_sequence:
        raise _error(
            "NON_MONOTONIC_SEQUENCE",
            "sequence must be strictly increasing",
            record_index=index,
            previous_sequence=previous_sequence,
            sequence=sequence,
        )
    if not isinstance(raw_start, int) or isinstance(raw_start, bool):
        raise _error("INVALID_OFFSET_TYPE", "raw_start must be an integer", record_index=index)
    if not isinstance(raw_end, int) or isinstance(raw_end, bool):
        raise _error("INVALID_OFFSET_TYPE", "raw_end must be an integer", record_index=index)
    if raw_start < 0 or raw_end < 0:
        raise _error("NEGATIVE_OFFSET", "offsets must be non-negative", record_index=index)
    if raw_end < raw_start:
        raise _error("OFFSET_ORDER", "raw_end must be >= raw_start", record_index=index)
    if not isinstance(raw_text, str):
        raise _error("INVALID_RAW_TEXT_TYPE", "raw_text must be a string", record_index=index)
    if not isinstance(normalized_text, str):
        raise _error(
            "INVALID_NORMALIZED_TEXT_TYPE",
            "normalized_text must be a string",
            record_index=index,
        )

    return sequence


def load_manifest_cid(manifest_path: Path) -> str:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _error("SOURCE_MANIFEST_INVALID", "cannot read source manifest", path=str(manifest_path)) from exc

    cid = manifest.get("cid") if isinstance(manifest, dict) else None
    if not isinstance(cid, str) or not cid.strip():
        raise _error("SOURCE_MANIFEST_CID_MISSING", "source manifest must contain a non-empty cid", path=str(manifest_path))
    return cid


def resolve_cid(*, cid: str | None, source_manifest: Path) -> str:
    manifest_cid = load_manifest_cid(source_manifest)
    if cid is not None and cid != manifest_cid:
        raise _error(
            "CID_MISMATCH",
            "explicit cid does not match the authoritative source manifest",
            explicit_cid=cid,
            manifest_cid=manifest_cid,
            source_manifest=str(source_manifest),
        )
    return manifest_cid


def segment_document(
    document: dict,
    *,
    source_normalized_path: str,
    cid: str,
) -> dict:
    if not isinstance(document, dict):
        raise _error("TOP_LEVEL_NOT_OBJECT", "normalized document must be an object")

    records = document.get("records")
    if not isinstance(records, list):
        raise _error("RECORDS_NOT_LIST", "normalized document records must be a list")
    if not isinstance(cid, str) or not cid.strip():
        raise _error("INVALID_CID", "cid must be a non-empty string")

    normalization_version = document.get("normalization_version")
    offset_unit = document.get("offset_unit")
    encoding = document.get("encoding")
    if not isinstance(normalization_version, str):
        raise _error("MISSING_NORMALIZATION_VERSION", "normalization_version must be a string")
    if not isinstance(offset_unit, str):
        raise _error("MISSING_OFFSET_UNIT", "offset_unit must be a string")
    if not isinstance(encoding, str):
        raise _error("MISSING_ENCODING", "encoding must be a string")

    segments: list[dict[str, object]] = []
    previous_sequence: int | None = None

    for segment_index, record in enumerate(records):
        sequence = _validate_record(record, segment_index, previous_sequence)
        previous_sequence = sequence

        sid = f"SID:{cid}:{source_normalized_path}:{sequence}"
        segments.append(
            {
                "sid": sid,
                "cid": cid,
                "source_normalized_path": source_normalized_path,
                "sequence": sequence,
                "segment_index": segment_index,
                "raw_start": record["raw_start"],
                "raw_end": record["raw_end"],
                "raw_text": record["raw_text"],
                "normalized_text": record["normalized_text"],
                "offset_unit": record["offset_unit"],
                "segmentation_version": SEGMENTATION_VERSION,
                "is_empty": record["normalized_text"] == "",
            }
        )

    sids = [segment["sid"] for segment in segments]
    if len(sids) != len(set(sids)):
        raise _error("SID_COLLISION", "segment identifiers must be unique")

    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "segmentation_version": SEGMENTATION_VERSION,
        "input_normalization_version": normalization_version,
        "offset_unit": offset_unit,
        "encoding": encoding,
        "source_normalized_path": source_normalized_path,
        "segments": segments,
    }


def segment_file(input_path: Path, output_path: Path, *, cid: str, repo_root: Path) -> dict:
    with input_path.open(encoding="utf-8") as handle:
        document = json.load(handle)

    source_path = input_path.resolve().relative_to(repo_root.resolve()).as_posix()
    result = segment_document(document, source_normalized_path=source_path, cid=cid)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def segment_directory(input_dir: Path, output_dir: Path, *, cid: str, repo_root: Path) -> dict:
    files = sorted(p for p in input_dir.glob("*.json") if p.name != "normalized_manifest.json")
    if not files:
        raise _error("NO_INPUT_FILES", "no normalized JSON files found", input_dir=str(input_dir))

    results = []
    for input_path in files:
        output_path = output_dir / input_path.name
        results.append(segment_file(input_path, output_path, cid=cid, repo_root=repo_root))

    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "segmentation_version": SEGMENTATION_VERSION,
        "cid": cid,
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "files": len(results),
        "segments": sum(len(result["segments"]) for result in results),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create deterministic SID segments from normalized Zohar JSON.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--cid", default=None)
    parser.add_argument("--source-manifest", default=DEFAULT_SOURCE_MANIFEST)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    try:
        cid = resolve_cid(cid=args.cid, source_manifest=repo_root / args.source_manifest)
        result = segment_directory(
            Path(args.input_dir),
            Path(args.output_dir),
            cid=cid,
            repo_root=repo_root,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
