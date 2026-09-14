#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "ANNOTATION-SCHEMA-0.1"
PILOT_INIT_VERSION = "ANNOTATION-PILOT-INIT-0.1"
ALLOWED_ANNOTATORS = {"annotator_a", "annotator_b"}


def _error(code: str, message: str, **context: object) -> ValueError:
    return ValueError(json.dumps({"type": code, "message": message, **context}, ensure_ascii=False, sort_keys=True))


def load_pilot(path: Path) -> dict[str, object]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise _error("INVALID_PILOT", "unable to read pilot artifact", path=str(path), error=str(exc)) from exc
    if not isinstance(document, dict):
        raise _error("PILOT_NOT_OBJECT", "pilot artifact must be an object")
    segments = document.get("segments")
    if not isinstance(segments, list) or not segments:
        raise _error("EMPTY_PILOT", "pilot artifact must contain non-empty segments")
    sids: list[str] = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict) or not isinstance(segment.get("sid"), str) or not segment["sid"]:
            raise _error("INVALID_PILOT_SEGMENT", "pilot segment must contain a non-empty sid", index=index)
        sids.append(segment["sid"])
    if len(sids) != len(set(sids)):
        raise _error("PILOT_SID_COLLISION", "pilot artifact contains duplicate SID values")
    return document


def build_annotation_shell(pilot: dict[str, object], annotator: str) -> dict[str, object]:
    if annotator not in ALLOWED_ANNOTATORS:
        raise _error("INVALID_ANNOTATOR", "annotator must be annotator_a or annotator_b", annotator=annotator)
    segments = pilot["segments"]
    assert isinstance(segments, list)
    return {
        "annotation_schema_version": SCHEMA_VERSION,
        "pilot_init_version": PILOT_INIT_VERSION,
        "pilot_version": pilot.get("pilot_version"),
        "selector_version": pilot.get("selector_version"),
        "selection_method": pilot.get("selection_method"),
        "vocabulary_version": pilot.get("vocabulary_version"),
        "guidelines_version": pilot.get("guidelines_version"),
        "cid": pilot.get("cid"),
        "population_size": pilot.get("population_size"),
        "sample_size": pilot.get("sample_size"),
        "population_sid_sha256": pilot.get("population_sid_sha256"),
        "selected_sid_sha256": pilot.get("selected_sid_sha256"),
        "annotator": annotator,
        "status": "UNANNOTATED",
        "segments": [
            {
                "pilot_index": segment.get("pilot_index"),
                "sid": segment["sid"],
                "annotations": [],
                "abstain": False,
                "notes": "",
            }
            for segment in segments
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize independent annotation shells from a frozen pilot.")
    parser.add_argument("--pilot", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        pilot = load_pilot(Path(args.pilot))
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for annotator in sorted(ALLOWED_ANNOTATORS):
            output = output_dir / f"{annotator}.json"
            output.write_text(
                json.dumps(build_annotation_shell(pilot, annotator), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "PASS", "annotators": sorted(ALLOWED_ANNOTATORS)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
