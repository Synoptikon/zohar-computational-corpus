from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.init_annotation_pilot import build_annotation_shell, load_pilot


def _pilot() -> dict[str, object]:
    return {
        "pilot_version": "ANNOTATION-PILOT-0.1",
        "selector_version": "SELECT-ANNOTATION-PILOT-0.2",
        "selection_method": "SHA256_SID_ASCENDING",
        "vocabulary_version": "ANNOTATION-VOCABULARY-0.1",
        "guidelines_version": "ANNOTATION-GUIDELINES-0.1",
        "cid": "CID-ZOHAR-WIKISOURCE-MANTUA",
        "population_size": 7850,
        "sample_size": 2,
        "population_sid_sha256": "population-digest",
        "selected_sid_sha256": "selected-digest",
        "segments": [
            {"pilot_index": 1, "sid": "SID:1"},
            {"pilot_index": 2, "sid": "SID:2"},
        ],
    }


def test_annotation_shell_preserves_frozen_pilot_metadata() -> None:
    shell = build_annotation_shell(_pilot(), "annotator_a")
    assert shell["annotation_schema_version"] == "ANNOTATION-SCHEMA-0.1"
    assert shell["annotator"] == "annotator_a"
    assert shell["status"] == "UNANNOTATED"
    assert shell["selected_sid_sha256"] == "selected-digest"
    assert [item["sid"] for item in shell["segments"]] == ["SID:1", "SID:2"]
    assert all(item["annotations"] == [] for item in shell["segments"])
    assert all(item["abstain"] is False for item in shell["segments"])


def test_annotation_shell_allows_only_independent_pilot_annotators() -> None:
    with pytest.raises(ValueError, match="INVALID_ANNOTATOR"):
        build_annotation_shell(_pilot(), "annotator_c")


def test_load_pilot_rejects_duplicate_sid(tmp_path: Path) -> None:
    path = tmp_path / "pilot.json"
    document = _pilot()
    document["segments"] = [{"pilot_index": 1, "sid": "SID:1"}, {"pilot_index": 2, "sid": "SID:1"}]
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match="PILOT_SID_COLLISION"):
        load_pilot(path)
