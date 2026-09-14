# GATE-003 — Esquema de anotación

**Status:** `VALIDATED`

## Scope

This gate validates the machine-readable annotation contract and validator behavior. It does not validate substantive annotations, semantic categories, historical claims, theological interpretation, or model truth.

## Acceptance criteria

| Criterion | Evidence | Status |
|---|---|---|
| Annotation schema specification | `data/analysis/annotation_schema_v0.1.md` | PASS |
| Validator implementation | `scripts/validate_annotations.py` | PASS |
| Validator tests | `tests/test_validate_annotations.py` | PASS |
| Non-empty fixture | `tests/fixtures/annotations/valid_annotations.json` | PASS |
| Reproducible validation run | GitHub Actions run `34827461313` | PASS |
| Validation artifact | `annotation_validation.json` in artifact `10340384910` | PASS |
| Execution manifest | `gate003_execution_manifest.json` in artifact `10340384910` | PASS |

## Validation result

```text
validation_version: ANNOTATION-SCHEMA-0.1
status: PASS
total_files: 1
total_records: 3
total_errors: 0
failed_files: 0
pytest: 6 passed
```

Evidence SHA-256:

```text
9bb6d305091c8798b22a90ebf9d77c1395f31cc1a81b124c0bce30f9da5296d4
```

GitHub Actions artifact:

```text
artifact_id: 10340384910
artifact_sha256: c520545e0c145f4f44c1e927b1ac9e8c0e8ec057e57460553ccca8bb17cfeab1
```

## Interpretation boundary

`VALIDATED` applies only to the schema contract and validator behavior. The fixture is a structural test fixture, not a scientifically validated annotation corpus. Substantive annotation vocabularies and coding guidelines remain downstream work under GATE-004.

## Validation record

- Workflow: `gate003-annotation-schema`
- Run ID: `34827461313`
- Commit: `f57ce4503e68eae519deac749d7241dcc2bb8a89`
- Artifact ID: `10340384910`
- Artifact SHA-256: `c520545e0c145f4f44c1e927b1ac9e8c0e8ec057e57460553ccca8bb17cfeab1`

**Decision:** `GATE-003 = VALIDATED`.
