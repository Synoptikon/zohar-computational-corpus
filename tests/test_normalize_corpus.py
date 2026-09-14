from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.normalize_corpus import normalize_corpus


def write_snapshot_manifest(path: Path, raw_file: Path, sha256: str) -> None:
    manifest = {
        "schema_version": "1.0",
        "license": "CC BY-SA 4.0",
        "page_count": 1,
        "pages": [
            {
                "sequence": 1,
                "title": "test",
                "pageid": 1,
                "revid": 1,
                "revision_timestamp": "2026-01-01T00:00:00Z",
                "source_url": "https://example.invalid/test",
                "path": str(raw_file),
                "sha256": sha256,
            }
        ],
    }
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_normalize_corpus_creates_manifest(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "normalized"
    manifest_path = output_dir / "normalized_manifest.json"
    snapshot_path = tmp_path / "snapshot_manifest.json"
    raw_dir.mkdir()
    raw_file = raw_dir / "0001.txt"
    raw_file.write_text("e\u0301 {{תבנית}} אבג\n", encoding="utf-8")
    sha256 = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    write_snapshot_manifest(snapshot_path, raw_file, sha256)

    manifest = normalize_corpus(raw_dir, output_dir, manifest_path, snapshot_path)

    assert manifest["raw_file_count"] == 1
    assert len(manifest["entries"]) == 1
    assert manifest["offset_unit"] == "unicode_codepoint_index"
    output = output_dir / "0001.json"
    assert output.exists()
    parsed = json.loads(output.read_text(encoding="utf-8"))
    reconstructed = "".join(record["raw_text"] for record in parsed["records"])
    assert reconstructed == raw_file.read_text(encoding="utf-8")


def test_normalize_corpus_rejects_modified_raw(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "normalized"
    snapshot_path = tmp_path / "snapshot_manifest.json"
    raw_dir.mkdir()
    raw_file = raw_dir / "0001.txt"
    raw_file.write_text("original\n", encoding="utf-8")
    sha256 = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    write_snapshot_manifest(snapshot_path, raw_file, sha256)
    raw_file.write_text("modified\n", encoding="utf-8")

    with pytest.raises(ValueError, match="RAW SHA-256 mismatch"):
        normalize_corpus(raw_dir, output_dir, output_dir / "normalized_manifest.json", snapshot_path)


def test_normalize_corpus_rejects_file_set_mismatch(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "normalized"
    snapshot_path = tmp_path / "snapshot_manifest.json"
    raw_dir.mkdir()
    raw_file = raw_dir / "0001.txt"
    raw_file.write_text("test\n", encoding="utf-8")
    sha256 = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    write_snapshot_manifest(snapshot_path, raw_file, sha256)
    (raw_dir / "0002.txt").write_text("extra\n", encoding="utf-8")

    with pytest.raises(ValueError, match="file-set mismatch"):
        normalize_corpus(raw_dir, output_dir, output_dir / "normalized_manifest.json", snapshot_path)
