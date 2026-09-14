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
| Contract/failure tests | `tests/test_segment_corpus.py` + GATE-002 run | PASS |
| Reproducible corpus run | GitHub Actions run `34827311687` | PASS |
| Normalized offset audit | `artifacts/audit_normalized_offsets.json` | PASS |
| Segment audit RUN 1 | `artifacts/audit_segments_run1.json` | PASS |
| Segment audit RUN 2 | `artifacts/audit_segments_run2.json` | PASS |
| Preservation/reproducibility audit | `artifacts/segment_reproducibility.json` | PASS |
| Execution manifest | `artifacts/gate002_execution_manifest.json` | PASS |
| Evidence artifact | GitHub artifact `10340860869` | PASS |

## Corpus execution

- CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- input directory: `data/normalized/zohar/wikisource`
- RUN 1 output directory: `data/segments/zohar/wikisource`
- RUN 2 output directory: `artifacts/segmentation-run2`
- files: `1,721`
- normalized records: `7,850`
- RUN 1 segments: `7,850`
- RUN 2 segments: `7,850`
- schema version: `SID-CONTRACT-0.1`
- segmentation version: `SEGMENTATION-RULES-0.1`

## Audit result

### Normalized offsets

```text
status: PASS
failed_files: 0
total_files: 1721
total_records: 7850
total_errors: 0
total_warnings: 0
```

### Segment audits

RUN 1 and RUN 2 both returned:

```text
status: PASS
failed_files: 0
total_files: 1721
total_segments: 7850
total_errors: 0
```

### Reproducibility

```text
status: PASS
records: 7850
segments: 7850
file_sets_identical: true
byte_identical: true
hash_mismatches: 0
```

Evidence SHA-256 recorded by the execution manifest:

```text
c1d6381ba437aa695093fabf1f6c0a637e775896e77b50ac956bed8bc5c380b7
```

GitHub Actions artifact ZIP:

```text
artifact_id: 10340860869
artifact_sha256: 66c8c441451e6a63bbbd91559e25ad8f7e41f337b90ce00d493d5d7b2c6f3d70
```

## Test result

The GATE-002 validation run completed:

```text
49 passed in 0.16s
```

## Interpretation boundary

This gate establishes reproducibility and structural traceability of the segmentation transformation. It does not establish that one normalized record is a semantically ideal unit, nor does it support any substantive interpretation of the Zohar.

## Reproducibility command

```bash
python scripts/normalize_corpus.py
python scripts/audit_normalized_offsets.py \
  --input-dir data/normalized/zohar/wikisource \
  --output artifacts/audit_normalized_offsets.json

python scripts/segment_corpus.py \
  --input-dir data/normalized/zohar/wikisource \
  --output-dir data/segments/zohar/wikisource \
  --source-manifest data/sources/zohar_primary_wikisource.json \
  --repo-root .

python scripts/audit_segments.py \
  --input-dir data/segments/zohar/wikisource \
  --output artifacts/audit_segments_run1.json

python scripts/segment_corpus.py \
  --input-dir data/normalized/zohar/wikisource \
  --output-dir artifacts/segmentation-run2 \
  --source-manifest data/sources/zohar_primary_wikisource.json \
  --repo-root .

python scripts/audit_segments.py \
  --input-dir artifacts/segmentation-run2 \
  --output artifacts/audit_segments_run2.json

python scripts/verify_segmentation_reproducibility.py \
  --normalized-dir data/normalized/zohar/wikisource \
  --run1-dir data/segments/zohar/wikisource \
  --run2-dir artifacts/segmentation-run2 \
  --output artifacts/segment_reproducibility.json
```

## Validation record

- Workflow: `gate002-reproducibility`
- Run ID: `34827311687`
- Validation commit: `5796bce8ec6fe274c8951c4cf6d3fbbe1023635e`
- Branch commit containing implementation: `69a8f110b74d45ed73749380398dd1fd1928fbda`
- Artifact ID: `10340860869`
- Artifact SHA-256: `66c8c441451e6a63bbbd91559e25ad8f7e41f337b90ce00d493d5d7b2c6f3d70`

**Decision:** `GATE-002 = VALIDATED`.
