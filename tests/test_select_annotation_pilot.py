from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.select_annotation_pilot import build_pilot, sid_population_digest


def _write_segment_file(path: Path, sids: list[str]) -> None:
    path.write_text(
        json.dumps(
            {
                "segments": [
                    {
                        "sid": sid,
                        "cid": "CID-ZOHAR-WIKISOURCE-MANTUA",
                        "source_normalized_path": "data/normalized/zohar/wikisource/0001.json",
                        "sequence": index + 1,
                    }
                    for index, sid in enumerate(sids)
                ]
            }
        ),
        encoding="utf-8",
    )


def test_pilot_selection_is_deterministic(tmp_path: Path) -> None:
    input_dir = tmp_path / "segmented"
    input_dir.mkdir()
    sids = [f"SID:CID-ZOHAR-WIKISOURCE-MANTUA:test:{index}" for index in range(1, 11)]
    _write_segment_file(input_dir / "0001.json", sids)

    first = build_pilot(input_dir, 4)
    second = build_pilot(input_dir, 4)

    assert first == second
    assert first["pilot_version"] == "ANNOTATION-PILOT-0.1"
    assert first["selector_version"] == "SELECT-ANNOTATION-PILOT-0.2"
    assert first["selection_method"] == "SHA256_SID_ASCENDING"
    assert first["vocabulary_version"] == "ANNOTATION-VOCABULARY-0.1"
    assert first["guidelines_version"] == "ANNOTATION-GUIDELINES-0.1"
    assert first["population_size"] == 10
    assert first["sample_size"] == 4
    assert first["population_sid_sha256"] == sid_population_digest(sids)
    selected_sids = [record["sid"] for record in first["segments"]]
    assert first["selected_sid_sha256"] == sid_population_digest(selected_sids)
    assert len(set(selected_sids)) == 4


def test_population_digest_is_order_independent() -> None:
    sids = ["SID:b", "SID:a", "SID:c"]
    expected = hashlib.sha256("SID:a\nSID:b\nSID:c".encode("utf-8")).hexdigest()
    assert sid_population_digest(sids) == expected
    assert sid_population_digest(list(reversed(sids))) == expected


def test_pilot_rejects_duplicate_sid(tmp_path: Path) -> None:
    input_dir = tmp_path / "segmented"
    input_dir.mkdir()
    sid = "SID:CID-ZOHAR-WIKISOURCE-MANTUA:test:1"
    _write_segment_file(input_dir / "0001.json", [sid])
    _write_segment_file(input_dir / "0002.json", [sid])

    with pytest.raises(ValueError, match="SID_COLLISION"):
        build_pilot(input_dir, 1)


def test_pilot_rejects_sample_larger_than_population(tmp_path: Path) -> None:
    input_dir = tmp_path / "segmented"
    input_dir.mkdir()
    _write_segment_file(
        input_dir / "0001.json",
        ["SID:CID-ZOHAR-WIKISOURCE-MANTUA:test:1"],
    )

    with pytest.raises(ValueError, match="SAMPLE_TOO_LARGE"):
        build_pilot(input_dir, 2)
