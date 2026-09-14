from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.segment_corpus import (
    SEGMENTATION_VERSION,
    resolve_cid,
    segment_document,
    segment_file,
)


STABLE_CID = "CID-ZOHAR-WIKISOURCE-MANTUA"


def normalized_document() -> dict:
    return {
        "schema_version": "1.0",
        "normalization_version": "NORMALIZATION-RULES-0.2",
        "offset_unit": "unicode_codepoint_index",
        "encoding": "UTF-8",
        "raw_file": "0001.txt",
        "records": [
            {
                "sequence": 1,
                "raw_start": 0,
                "raw_end": 5,
                "raw_text": "alpha\n",
                "normalized_text": "alpha",
                "normalization_rule": "NFC + whitespace",
                "normalization_version": "NORMALIZATION-RULES-0.2",
                "offset_unit": "unicode_codepoint_index",
            },
            {
                "sequence": 2,
                "raw_start": 5,
                "raw_end": 10,
                "raw_text": "beta\n",
                "normalized_text": "beta",
                "normalization_rule": "NFC + whitespace",
                "normalization_version": "NORMALIZATION-RULES-0.2",
                "offset_unit": "unicode_codepoint_index",
            },
        ],
    }


def test_segment_document_preserves_records_and_offsets() -> None:
    result = segment_document(
        normalized_document(),
        source_normalized_path="data/normalized/zohar/wikisource/0001.json",
        cid=STABLE_CID,
    )

    assert result["schema_version"] == "SID-CONTRACT-0.1"
    assert result["segmentation_version"] == SEGMENTATION_VERSION
    assert len(result["segments"]) == 2
    assert result["segments"][0]["sequence"] == 1
    assert result["segments"][0]["raw_start"] == 0
    assert result["segments"][0]["raw_end"] == 5
    assert result["segments"][0]["normalized_text"] == "alpha"
    assert result["segments"][0]["sid"].startswith(f"SID:{STABLE_CID}:")
    assert result["segments"][0]["sid"].endswith(":1")


def test_segment_file_is_byte_stable(tmp_path: Path) -> None:
    input_path = tmp_path / "0001.json"
    output_a = tmp_path / "a.json"
    output_b = tmp_path / "b.json"
    input_path.write_text(
        json.dumps(normalized_document(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    segment_file(input_path, output_a, cid=STABLE_CID, repo_root=tmp_path)
    segment_file(input_path, output_b, cid=STABLE_CID, repo_root=tmp_path)

    assert output_a.read_bytes() == output_b.read_bytes()


def test_resolve_cid_reads_authoritative_source_manifest(tmp_path: Path) -> None:
    manifest = tmp_path / "source.json"
    manifest.write_text(json.dumps({"cid": STABLE_CID}) + "\n", encoding="utf-8")

    assert resolve_cid(cid=None, source_manifest=manifest) == STABLE_CID
    assert resolve_cid(cid=STABLE_CID, source_manifest=manifest) == STABLE_CID


def test_resolve_cid_rejects_mismatch(tmp_path: Path) -> None:
    manifest = tmp_path / "source.json"
    manifest.write_text(json.dumps({"cid": STABLE_CID}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="CID_MISMATCH"):
        resolve_cid(cid="CID-WRONG", source_manifest=manifest)


def test_segment_rejects_non_monotonic_sequence() -> None:
    document = normalized_document()
    document["records"][1]["sequence"] = 1

    with pytest.raises(ValueError, match="NON_MONOTONIC_SEQUENCE"):
        segment_document(document, source_normalized_path="x.json", cid=STABLE_CID)


def test_segment_rejects_offset_order_error() -> None:
    document = normalized_document()
    document["records"][0]["raw_end"] = -1

    with pytest.raises(ValueError, match="NEGATIVE_OFFSET"):
        segment_document(document, source_normalized_path="x.json", cid=STABLE_CID)
