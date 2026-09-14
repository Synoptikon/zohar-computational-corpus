from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_annotations import validate_record


def test_valid_human_annotation() -> None:
    record = {
        "eid": "EID:SID:0001:0001",
        "sid": "SID:CID-ZOHAR-WIKISOURCE-MANTUA:0001:0",
        "annotation_type": "example_type",
        "value": "candidate",
        "source": "human",
        "annotator": "human:test",
        "annotation_version": "ANNOTATION-SCHEMA-0.1",
        "validation_status": "REVIEWED",
    }
    assert validate_record(record, 0) == []


def test_llm_annotation_must_start_as_candidate() -> None:
    record = {
        "eid": "EID:SID:0001:0001",
        "sid": "SID:CID-ZOHAR-WIKISOURCE-MANTUA:0001:0",
        "annotation_type": "example_type",
        "value": "candidate",
        "source": "llm",
        "annotator": "model:test@1",
        "annotation_version": "ANNOTATION-SCHEMA-0.1",
        "validation_status": "ACCEPTED",
    }
    errors = validate_record(record, 0)
    assert any(error["type"] == "LLM_MUST_START_AS_CANDIDATE" for error in errors)


def test_invalid_source_and_status_are_rejected() -> None:
    record = {
        "eid": "EID:SID:0001:0001",
        "sid": "SID:CID-ZOHAR-WIKISOURCE-MANTUA:0001:0",
        "annotation_type": "example_type",
        "value": {},
        "source": "unknown",
        "annotator": "human:test",
        "annotation_version": "ANNOTATION-SCHEMA-0.1",
        "validation_status": "UNKNOWN",
    }
    errors = validate_record(record, 0)
    error_types = {error["type"] for error in errors}
    assert "INVALID_SOURCE" in error_types
    assert "INVALID_VALIDATION_STATUS" in error_types


def test_schema_version_is_required() -> None:
    record = {
        "eid": "EID:SID:0001:0001",
        "sid": "SID:CID-ZOHAR-WIKISOURCE-MANTUA:0001:0",
        "annotation_type": "example_type",
        "value": True,
        "source": "rule",
        "annotator": "rule:test",
        "annotation_version": "ANNOTATION-SCHEMA-0.0",
        "validation_status": "CANDIDATE",
    }
    errors = validate_record(record, 0)
    assert any(error["type"] == "INVALID_SCHEMA_VERSION" for error in errors)
