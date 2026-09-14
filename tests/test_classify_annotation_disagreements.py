from __future__ import annotations

from scripts.classify_annotation_disagreements import classify_documents
from tests.test_compare_annotation_pilots import annotation, make_document


def test_classifies_agreement_and_value_mismatch() -> None:
    a = make_document(
        "annotator_a",
        {
            "SID-1": [annotation("ENTITY", {"label": "x"})],
            "SID-2": [],
        },
    )
    b = make_document(
        "annotator_b",
        {
            "SID-1": [annotation("ENTITY", {"label": "y"})],
            "SID-2": [],
        },
    )
    result = classify_documents(a, b)
    assert result["sample_size"] == 2
    assert result["agreement_count"] == 1
    assert result["disagreement_count"] == 1
    assert result["classification_counts"] == {"AGREEMENT": 1, "VALUE_MISMATCH": 1}
    assert result["disagreements"][0]["sid"] == "SID-1"


def test_classifies_type_mismatch() -> None:
    a = make_document("annotator_a", {"SID-1": [annotation("ENTITY", {"label": "x"})]})
    b = make_document("annotator_b", {"SID-1": [annotation("RELATION", {"label": "x"})]})
    result = classify_documents(a, b)
    assert result["classification_counts"] == {"TYPE_MISMATCH": 1}


def test_classifies_validation_status_mismatch() -> None:
    a = make_document("annotator_a", {"SID-1": [annotation("ENTITY", {"label": "x"})]})
    b = make_document("annotator_b", {"SID-1": [annotation("ENTITY", {"label": "x"})]})
    b["segments"][0]["annotations"][0]["validation_status"] = "CANDIDATE"
    result = classify_documents(a, b)
    assert result["classification_counts"] == {"VALIDATION_STATUS_MISMATCH": 1}


def test_classifies_abstention_mismatch() -> None:
    a = make_document("annotator_a", {"SID-1": []})
    b = make_document("annotator_b", {"SID-1": []})
    b["segments"][0]["abstain"] = True
    result = classify_documents(a, b)
    assert result["classification_counts"] == {"ABSTAIN_MISMATCH": 1}
