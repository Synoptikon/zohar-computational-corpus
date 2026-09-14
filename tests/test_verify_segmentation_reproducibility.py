from __future__ import annotations

import json
from pathlib import Path

from scripts.verify_segmentation_reproducibility import compare_run_to_normalized, directory_hashes


def _write_document(path: Path, sequence: int = 1) -> None:
    path.write_text(
        json.dumps(
            {
                "normalization_version": "NORMALIZATION-RULES-0.2",
                "offset_unit": "unicode_codepoint_index",
                "encoding": "UTF-8",
                "records": [
                    {
                        "sequence": sequence,
                        "raw_start": 0,
                        "raw_end": 4,
                        "raw_text": "אבגד",
                        "normalized_text": "אבגד",
                        "normalization_version": "NORMALIZATION-RULES-0.2",
                        "offset_unit": "unicode_codepoint_index",
                    }
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_segment(path: Path, sequence: int = 1, text: str = "אבגד") -> None:
    path.write_text(
        json.dumps(
            {
                "schema_version": "SID-CONTRACT-0.1",
                "segmentation_version": "SEGMENTATION-RULES-0.1",
                "input_normalization_version": "NORMALIZATION-RULES-0.2",
                "offset_unit": "unicode_codepoint_index",
                "encoding": "UTF-8",
                "source_normalized_path": "data/normalized/zohar/wikisource/0001.json",
                "segments": [
                    {
                        "sid": "SID:CID-ZOHAR-WIKISOURCE-MANTUA:data/normalized/zohar/wikisource/0001.json:1",
                        "cid": "CID-ZOHAR-WIKISOURCE-MANTUA",
                        "source_normalized_path": "data/normalized/zohar/wikisource/0001.json",
                        "sequence": sequence,
                        "segment_index": 0,
                        "raw_start": 0,
                        "raw_end": 4,
                        "raw_text": text,
                        "normalized_text": text,
                        "offset_unit": "unicode_codepoint_index",
                        "segmentation_version": "SEGMENTATION-RULES-0.1",
                        "is_empty": text == "",
                    }
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def test_preservation_passes(tmp_path: Path) -> None:
    normalized = tmp_path / "normalized"
    run1 = tmp_path / "run1"
    normalized.mkdir()
    run1.mkdir()
    _write_document(normalized / "0001.json")
    _write_segment(run1 / "0001.json")

    report = compare_run_to_normalized(normalized, run1)
    assert report["status"] == "PASS"
    assert report["records"] == 1
    assert report["segments"] == 1


def test_preservation_detects_text_change(tmp_path: Path) -> None:
    normalized = tmp_path / "normalized"
    run1 = tmp_path / "run1"
    normalized.mkdir()
    run1.mkdir()
    _write_document(normalized / "0001.json")
    _write_segment(run1 / "0001.json", text="אבגX")

    report = compare_run_to_normalized(normalized, run1)
    assert report["status"] == "FAIL"
    assert any(error["type"] == "RECORD_SEGMENT_MISMATCH" for error in report["errors"])


def test_directory_hashes_are_stable(tmp_path: Path) -> None:
    root = tmp_path / "run"
    root.mkdir()
    _write_segment(root / "0001.json")
    assert directory_hashes(root) == directory_hashes(root)
