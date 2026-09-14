from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.compare_annotation_pilots import compare_documents, load_document


def make_document(annotator: str, annotations_by_sid: dict[str, list[dict]]) -> dict:
    return {
        "annotation_schema_version": "ANNOTATION-SCHEMA-0.1",
        "pilot_version": "ANNOTATION-PILOT-0.1",
        "selector_version": "SELECT-ANNOTATION-PILOT-0.2",
        "selection_method": "SHA256_SID_ASCENDING",
        "vocabulary_version": "ANNOTATION-VOCABULARY-0.1",
        "guidelines_version": "ANNOTATION-GUIDELINES-0.1",
        "cid": "CID-ZOHAR-WIKISOURCE-MANTUA",
        "population_size": 100,
        "sample_size": 2,
        "population_sid_sha256": "population",
        "selected_sid_sha256": "selected",
        "annotator": annotator,
        "status": "ANNOTATED",
        "segments": [
            {"pilot_index": i + 1, "sid": sid, "annotations": annotations, "abstain": False, "notes": ""}
            for i, (sid, annotations) in enumerate(sorted(annotations_by_sid.items()))
        ],
    }


def annotation(annotation_type: str, value: object) -> dict:
    return {
        "eid": "EID:test",
        "sid": "SID:test",
        "annotation_type": annotation_type,
        "value": value,
        "source": "human",
        "annotator": "human:test",
        "annotation_version": "ANNOTATION-SCHEMA-0.1",
        "validation_status": "REVIEWED",
    }


def test_identical_annotations_have_full_exact_agreement() -> None:
    data = {"SID-1": [annotation("ENTITY", {"label": "x"})], "SID-2": []}
    result = compare_documents(make_document("annotator_a", data), make_document("annotator_b", data))
    assert result["status"] == "PASS"
    assert result["agreements"] == 2
    assert result["disagreements"] == 0
    assert result["agreement_rate"] == 1.0


def test_different_annotations_are_reported_as_disagreement() -> None:
    a = {"SID-1": [annotation("ENTITY", {"label": "x"})]}
    b = {"SID-1": [annotation("ENTITY", {"label": "y"})]}
    result = compare_documents(make_document("annotator_a", a), make_document("annotator_b", b))
    assert result["status"] == "DISAGREEMENT"
    assert result["agreements"] == 0
    assert result["disagreements"] == 1
    assert result["agreement_rate"] == 0.0


def test_mismatched_pilot_metadata_is_rejected() -> None:
    a = make_document("annotator_a", {"SID-1": []})
    b = make_document("annotator_b", {"SID-1": []})
    b["selected_sid_sha256"] = "different"
    with pytest.raises(ValueError, match="PILOT_METADATA_MISMATCH"):
        compare_documents(a, b)


def test_mismatched_sid_sets_are_rejected() -> None:
    a = make_document("annotator_a", {"SID-1": []})
    b = make_document("annotator_b", {"SID-2": []})
    with pytest.raises(ValueError, match="SID_SET_MISMATCH"):
        compare_documents(a, b)


def test_unannotated_document_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "a.json"
    document = make_document("annotator_a", {"SID-1": []})
    document["status"] = "UNANNOTATED"
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match="UNANNOTATED_INPUT"):
        load_document(path)
