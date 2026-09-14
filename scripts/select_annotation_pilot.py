#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PILOT_VERSION = "ANNOTATION-PILOT-0.1"
SELECTION_METHOD = "SHA256_SID_ASCENDING"
DEFAULT_SAMPLE_SIZE = 30


def _error(code: str, message: str, **context: object) -> ValueError:
    payload = {"type": code, "message": message, **context}
    return ValueError(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def load_sids(input_dir: Path) -> list[dict[str, object]]:
    files = sorted(p for p in input_dir.glob("*.json"))
    if not files:
        raise _error("NO_INPUT_FILES", "no segmented JSON files found", input_dir=str(input_dir))
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for path in files:
        with path.open(encoding="utf-8") as handle:
            document = json.load(handle)
        segments = document.get("segments") if isinstance(document, dict) else None
        if not isinstance(segments, list):
            raise _error("SEGMENTS_NOT_LIST", "segmented document must contain a segments list", path=str(path))
        for index, segment in enumerate(segments):
            if not isinstance(segment, dict):
                raise _error("SEGMENT_NOT_OBJECT", "segment must be an object", path=str(path), segment_index=index)
            sid = segment.get("sid")
            if not isinstance(sid, str) or not sid:
                raise _error("INVALID_SID", "segment must contain a non-empty sid", path=str(path), segment_index=index)
            if sid in seen:
                raise _error("SID_COLLISION", "SID must be unique across pilot input", sid=sid)
            seen.add(sid)
            records.append({
                "sid": sid,
                "cid": segment.get("cid"),
                "source_normalized_path": segment.get("source_normalized_path"),
                "sequence": segment.get("sequence"),
            })
    return records


def select_pilot(records: list[dict[str, object]], sample_size: int) -> list[dict[str, object]]:
    if sample_size < 1:
        raise _error("INVALID_SAMPLE_SIZE", "sample size must be >= 1", sample_size=sample_size)
    if sample_size > len(records):
        raise _error("SAMPLE_TOO_LARGE", "sample size exceeds available segments", sample_size=sample_size, available=len(records))
    ranked = sorted(
        records,
        key=lambda record: (
            hashlib.sha256(str(record["sid"]).encode("utf-8")).hexdigest(),
            str(record["sid"]),
        ),
    )
    selected = ranked[:sample_size]
    return [
        {
            "pilot_index": index + 1,
            **record,
            "selection_hash": hashlib.sha256(str(record["sid"]).encode("utf-8")).hexdigest(),
        }
        for index, record in enumerate(selected)
    ]


def build_pilot(input_dir: Path, sample_size: int) -> dict[str, object]:
    records = load_sids(input_dir)
    selected = select_pilot(records, sample_size)
    cids = {record["cid"] for record in selected if isinstance(record.get("cid"), str)}
    if len(cids) > 1:
        raise _error("MULTIPLE_CIDS", "pilot selection spans multiple CIDs", cids=sorted(cids))
    return {
        "pilot_version": PILOT_VERSION,
        "selection_method": SELECTION_METHOD,
        "sample_size": sample_size,
        "population_size": len(records),
        "cid": next(iter(cids), None),
        "segments": selected,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Select a deterministic annotation pilot from SID segments.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE)
    args = parser.parse_args()
    try:
        result = build_pilot(Path(args.input_dir), args.sample_size)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
