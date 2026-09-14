# GATE-002 — Segmentación reproducible

**Status:** `VALIDATED`

## Scope

This gate validates the deterministic transformation from the normalized corpus to the `SID-CONTRACT-0.1` representation. It does not validate semantic, historical, linguistic, theological, or mathematical interpretations of the segments.

## Acceptance criteria

| Criterion | Evidence | Status |
|---|---|---|
| Versioned segmentation rules | `data/analysis/segmentation_rules_v0.1.md` | PASS |
| Stable SID contract | `data/analysis/segment_contract_v0.1.md` | PASS |
| Deterministic implementation | `scripts/segment_corpus.py` | PASS |
| Contract/failure tests | `tests/test_segment_corpus.py` | PASS |
| Reproducible corpus run | `data/segmented/zohar/wikisource/` | PASS |
| Segment audit | `data/analysis/segment_audit.json` | PASS |
| Evidence recorded | This document | PASS |

## Corpus execution

- CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- input directory: `data/normalized/zohar/wikisource`
- output directory: `data/segmented/zohar/wikisource`
- files: `1,721`
- segments: `7,850`
- schema version: `SID-CONTRACT-0.1`
- segmentation version: `SEGMENTATION-RULES-0.1`

## Audit result

Audit version: `SEGMENT-AUDIT-0.1`

```text
status: PASS
failed_files: 0
total_files: 1721
total_segments: 7850
total_errors: 0
```

## Test result

The repository test suite completed successfully during the validation run:

```text
21 passed
```

## Interpretation boundary

This gate establishes reproducibility and structural traceability of the segmentation transformation. It does not establish that one normalized record is a semantically ideal unit, nor does it support any substantive interpretation of the Zohar.

## Reproducibility command

```bash
python scripts/segment_corpus.py \
  --input-dir data/normalized/zohar/wikisource \
  --output-dir data/segmented/zohar/wikisource \
  --repo-root .

python scripts/audit_segments.py \
  --input-dir data/segmented/zohar/wikisource \
  --output data/analysis/segment_audit.json
```
