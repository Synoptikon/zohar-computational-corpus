from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_normalized_offsets import audit_directory
from src.zohar_corpus.corpus_normalizer import normalize_raw_file


def test_audit_passes_normalized_corpus_and_excludes_manifest(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data/raw/zohar/wikisource"
    normalized_dir = tmp_path / "data/normalized/zohar/wikisource"
    raw_dir.mkdir(parents=True)
    normalized_dir.mkdir(parents=True)

    raw = raw_dir / "0001.txt"
    raw.write_text("e\u0301 {{תבנית}} אבג\nsecond line\n", encoding="utf-8")
    normalize_raw_file(raw, normalized_dir / "0001.json")

    (normalized_dir / "normalized_manifest.json").write_text(
        json.dumps({"raw_file_count": 1}), encoding="utf-8"
    )

    output = tmp_path / "audit.json"
    result = audit_directory(normalized_dir, output, tmp_path)

    assert result["status"] == "PASS"
    assert result["total_files"] == 1
    assert result["total_errors"] == 0
    assert result["failed_files"] == 0
    assert result["files"][0]["records"] == 2


def test_audit_detects_raw_offset_corruption(tmp_path: Path) -> None:
    raw_dir = tmp_path / "data/raw/zohar/wikisource"
    normalized_dir = tmp_path / "data/normalized/zohar/wikisource"
    raw_dir.mkdir(parents=True)
    normalized_dir.mkdir(parents=True)

    raw = raw_dir / "0001.txt"
    raw.write_text("alpha\nbeta\n", encoding="utf-8")
    output_file = normalized_dir / "0001.json"
    normalize_raw_file(raw, output_file)

    document = json.loads(output_file.read_text(encoding="utf-8"))
    document["records"][0]["raw_end"] += 1
    output_file.write_text(json.dumps(document), encoding="utf-8")

    result = audit_directory(normalized_dir, tmp_path / "audit.json", tmp_path)

    assert result["status"] == "FAIL"
    assert result["total_errors"] >= 1
    error_types = {error["type"] for error in result["files"][0]["errors"]}
    assert "RAW_TEXT_LENGTH_MISMATCH" in error_types or "RAW_OFFSET_CONTENT_MISMATCH" in error_types
