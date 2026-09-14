# Validation gates

The project uses gates to prevent progression from implementation to scientific conclusion without evidence.

| Gate | Requirement | Current status |
|---|---|---|
| GATE-001 | Corpus válido | BLOCKED |
| GATE-002 | Segmentación reproducible | VALIDATED |
| GATE-003 | Esquema de anotación definido | VALIDATED |
| GATE-004 | Codificación validada | IN_PROGRESS |
| GATE-005 | Modelo reproducible | BLOCKED |
| GATE-006 | Métricas calculables | BLOCKED |
| GATE-007 | Baseline establecido | BLOCKED |
| GATE-008 | Experimento ejecutable | BLOCKED |
| GATE-009 | Resultado reproducible | BLOCKED |
| GATE-010 | Conclusión auditable | BLOCKED |

## Rule

`IMPLEMENTED` does not mean `VALIDATED`.

A gate can advance only when its evidence is recorded in the repository or in a referenced reproducibility artifact. Missing evidence is reported as `BLOCKED`, `INCONCLUSIVE`, or `UNVERIFIED`, never inferred as success.

## Current evidence

`GATE-001` has a source registry and licensing/provenance policy, but no accepted RAW corpus snapshot. The gate therefore remains `BLOCKED`.

See `docs/gates/GATE-001-corpus-valid.md` for the evidence record and remaining acceptance criteria.

## Normalized offset validation

The normalized corpus has an independently validated offset-audit result:

- audit version: `NORMALIZED-OFFSETS-AUDIT-0.2`
- files audited: `1,721`
- records audited: `7,850`
- failed files: `0`
- errors: `0`
- warnings: `0`
- status: `PASS`

This evidence validates the normalized offset contract only. It is upstream evidence and is distinct from `GATE-002`.

The audit artifact is expected at `data/analysis/normalized_offsets_audit.json` in a reproducible working tree.

## GATE-002 acceptance evidence

`GATE-002` is `VALIDATED` because all required evidence has been produced and recorded.

- segmentation rules: `data/analysis/segmentation_rules_v0.1.md`
- SID contract: `data/analysis/segment_contract_v0.1.md`
- implementation: `scripts/segment_corpus.py`
- tests: `tests/test_segment_corpus.py`
- corpus run: `data/segmented/zohar/wikisource/`
- audit: `data/analysis/segment_audit.json`
- evidence record: `docs/gates/GATE-002-segmentation-reproducible.md`

Corpus-level result:

```text
CID: CID-ZOHAR-WIKISOURCE-MANTUA
files: 1721
segments: 7850
failed_files: 0
total_errors: 0
status: PASS
```

## GATE-003 — Annotation schema

`GATE-003` is now `VALIDATED`.

The schema specification, validator, tests, and non-empty fixture have been implemented and executed in a reproducible working tree.

- specification: `data/analysis/annotation_schema_v0.1.md`
- validator: `scripts/validate_annotations.py`
- tests: `tests/test_validate_annotations.py`
- fixture: `tests/fixtures/annotations/valid_annotations.json`
- validation artifact: `data/analysis/annotation_validation.json`

Recorded execution evidence:

```text
pytest: 23 passed
validation_version: ANNOTATION-SCHEMA-0.1
status: PASS
total_files: 1
total_records: 3
total_errors: 0
failed_files: 0
```

This gate validates only the annotation contract and validator behavior. It does not validate substantive annotations or claims about the Zohar.

## GATE-004 — Coding validation

`GATE-004` is `IN_PROGRESS`.

The first coding layer has now been specified without introducing substantive theological or historical categories:

- vocabulary: `data/analysis/annotation_vocabulary_v0.1.md`
- guidelines: `data/analysis/annotation_guidelines_v0.1.md`

The pilot vocabulary defines only structural annotation classes: `ENTITY`, `RELATION`, and `FEATURE`.

GATE-004 must not be marked `VALIDATED` until a frozen pilot segment set has been independently annotated, disagreements have been measured and classified, and the resulting annotation records pass structural validation. LLM-generated annotations remain `CANDIDATE` until review.
