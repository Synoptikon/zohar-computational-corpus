from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_annotation_pilot_pair import validate_pair


def _shell(annotator: str) -> dict:
    return {
        "annotation_schema_version": "ANNOTATION-SCHEMA-0.1",
        "pilot_version": "ANNOTATION-PILOT-0.1",
        "selector_version": "SELECT-ANNOTATION-PILOT-0.2",
        "selection_method": "SHA256_SID_ASCENDING",
        "vocabulary_version": "ANNOTATION-VOCABULARY-0.1",
        "guidelines_version": "ANNOTATION-GUIDELINES-0.1",
        "cid": "CID-TEST",
        "population_size": 3,
        "sample_size": 2,
        "population_sid_sha256": "population",
        "selected_sid_sha256": "placeholder",
        "annotator": annotator,
        "status": "UNANNOTATED",
        "segments": [
            {"pilot_index": 0, "sid": "SID-001", "annotations": [], "abstain": False, "notes": ""},
            {"pilot_index": 1, "sid": "SID-002", "annotations": [], "abstain": False, "notes": ""},
        ],
    }


def _write_pair(tmp_path: Path) -> tuple[Path, Path]:
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    doc_a = _shell("annotator_a")
    doc_b = _shell("annotator_b")
    from scripts.validate_annotation_pilot_pair import sid_digest

    digest = sid_digest(["SID-001", "SID-002"])
    doc_a["selected_sid_sha256"] = digest
    doc_b["selected_sid_sha256"] = digest
    a.write_text(json.dumps(doc_a), encoding="utf-8")
    b.write_text(json.dumps(doc_b), encoding="utf-8")
    return a, b


def test_pair_passes_when_frozen_metadata_and_sids_match(tmp_path: Path) -> None:
    a, b = _write_pair(tmp_path)
    report = validate_pair(a, b, tmp_path / "report.json")
    assert report["status"] == "PASS"
    assert report["sample_size"] == 2
    assert report["errors"] == []


def test_pair_rejects_sid_set_mismatch(tmp_path: Path) -> None:
    a, b = _write_pair(tmp_path)
    doc = json.loads(b.read_text(encoding="utf-8"))
    doc["segments"][1]["sid"] = "SID-003"
    b.write_text(json.dumps(doc), encoding="utf-8")

    report = validate_pair(a, b, tmp_path / "report.json")
    assert report["status"] == "FAIL"
    assert any(error["type"] == "SID_SET_MISMATCH" for error in report["errors"])


def test_pair_rejects_metadata_mismatch(tmp_path: Path) -> None:
    a, b = _write_pair(tmp_path)
    doc = json.loads(b.read_text(encoding="utf-8"))
    doc["guidelines_version"] = "ANNOTATION-GUIDELINES-OTHER"
    b.write_text(json.dumps(doc), encoding="utf-8")

    report = validate_pair(a, b, tmp_path / "report.json")
    assert report["status"] == "FAIL"
    assert any(error["type"] == "METADATA_MISMATCH" for error in report["errors"])
