from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_segments import audit_directory
from scripts.segment_corpus import segment_document


def test_segment_audit_passes_valid_output(tmp_path: Path) -> None:
    normalized = {
        "normalization_version": "NORMALIZATION-RULES-0.2",
        "offset_unit": "unicode_codepoint_index",
        "encoding": "UTF-8",
        "records": [
            {
                "sequence": 1,
                "raw_start": 0,
                "raw_end": 6,
                "raw_text": "alpha\n",
                "normalized_text": "alpha",
                "normalization_version": "NORMALIZATION-RULES-0.2",
                "offset_unit": "unicode_codepoint_index",
            }
        ],
    }
    segmented = segment_document(normalized, source_normalized_path="x.json", cid="CID:test")
    output_dir = tmp_path / "segments"
    output_dir.mkdir()
    (output_dir / "x.json").write_text(json.dumps(segmented, ensure_ascii=False), encoding="utf-8")

    report = audit_directory(output_dir, tmp_path / "audit.json")

    assert report["status"] == "PASS"
    assert report["total_files"] == 1
    assert report["total_segments"] == 1
    assert report["total_errors"] == 0


def test_segment_audit_detects_sid_collision(tmp_path: Path) -> None:
    output_dir = tmp_path / "segments"
    output_dir.mkdir()
    document = {
        "segmentation_version": "SEGMENTATION-RULES-0.1",
        "segments": [
            {
                "sid": "SID:CID:test:x:1",
                "cid": "CID:test",
                "source_normalized_path": "x.json",
                "sequence": 1,
                "segment_index": 0,
                "raw_start": 0,
                "raw_end": 1,
                "raw_text": "a",
                "normalized_text": "a",
                "offset_unit": "unicode_codepoint_index",
                "segmentation_version": "SEGMENTATION-RULES-0.1",
                "is_empty": False,
            },
            {
                "sid": "SID:CID:test:x:1",
                "cid": "CID:test",
                "source_normalized_path": "x.json",
                "sequence": 2,
                "segment_index": 1,
                "raw_start": 1,
                "raw_end": 2,
                "raw_text": "b",
                "normalized_text": "b",
                "offset_unit": "unicode_codepoint_index",
                "segmentation_version": "SEGMENTATION-RULES-0.1",
                "is_empty": False,
            },
        ],
    }
    (output_dir / "x.json").write_text(json.dumps(document), encoding="utf-8")

    report = audit_directory(output_dir, tmp_path / "audit.json")

    assert report["status"] == "FAIL"
    assert report["total_errors"] >= 1
    error_types = {error["type"] for error in report["files"][0]["errors"]}
    assert "SID_COLLISION" in error_types
