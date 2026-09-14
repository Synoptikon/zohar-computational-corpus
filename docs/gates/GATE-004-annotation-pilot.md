# GATE-004 — Annotation coding pilot

**Status:** IN_PROGRESS
**Gate:** `GATE-004`
**Pilot contract:** `ANNOTATION-PILOT-0.1`
**Vocabulary:** `ANNOTATION-VOCABULARY-0.1`
**Guidelines:** `ANNOTATION-GUIDELINES-0.1`
**Agreement:** `ANNOTATION-AGREEMENT-0.1`
**Disagreement classification:** `ANNOTATION-DISAGREEMENT-0.1`

## Objective

Determine whether independent annotators can apply the current structural annotation vocabulary and guidelines consistently to the same frozen SID sample.

## Implemented evidence

- `data/analysis/annotation_vocabulary_v0.1.md`
- `data/analysis/annotation_guidelines_v0.1.md`
- `data/analysis/annotation_pilot_protocol_v0.1.md`
- `data/analysis/annotation_agreement_v0.1.md`
- `scripts/select_annotation_pilot.py`
- `scripts/init_annotation_pilot.py`
- `scripts/compare_annotation_pilots.py`
- `scripts/classify_annotation_disagreements.py`
- `tests/test_select_annotation_pilot.py`
- `tests/test_init_annotation_pilot.py`
- `tests/test_compare_annotation_pilots.py`
- `tests/test_classify_annotation_disagreements.py`

## Deterministic selection

The pilot selector ranks each SID using the SHA-256 digest of its UTF-8 representation and selects the first records in ascending digest order.

Selection method:

`SHA256_SID_ASCENDING`

Pilot contract:

`ANNOTATION-PILOT-0.1`

Selector implementation version:

`SELECT-ANNOTATION-PILOT-0.2`

Default sample size:

`30`

The resulting artifact records:

- complete selected SID set;
- population size;
- CID;
- sample size;
- selector version;
- vocabulary version;
- guidelines version;
- per-SID selection hash;
- SHA-256 digest of the complete population SID set;
- SHA-256 digest of the selected SID set.

The population and selected-set digests make corpus drift detectable before annotation comparison. Re-running the selector against a changed SID population produces different freeze evidence rather than silently reusing an obsolete pilot.

## Independent annotation

`init_annotation_pilot.py` generates two empty annotation shells from the frozen pilot:

- `annotator_a.json`
- `annotator_b.json`

The shells preserve the frozen pilot metadata and SID set. They must be populated independently; neither annotator's decisions are input to the other's shell.

## Agreement comparison

`scripts/compare_annotation_pilots.py` implements `ANNOTATION-AGREEMENT-0.1`.

Comparison is performed at `SID` level using canonical signatures:

`(annotation_type, canonical(value), validation_status)`

`EID` is intentionally excluded from the agreement key because independent annotators may assign different local entity identifiers to an otherwise identical decision.

The comparator requires identical frozen-pilot metadata and identical SID sets. It rejects unannotated shells and produces:

`agreement_rate = agreements / total_SID`

This is exact structural agreement, not semantic validity and not an inferential statistic.

## Disagreement classification

`scripts/classify_annotation_disagreements.py` implements `ANNOTATION-DISAGREEMENT-0.1`.

For each SID it distinguishes:

- `AGREEMENT`
- `TYPE_MISMATCH`
- `VALUE_MISMATCH`
- `VALIDATION_STATUS_MISMATCH`
- `ABSTAIN_MISMATCH`

The classifier preserves both canonical annotation signatures for every disagreement. This creates an auditable bridge from the aggregate agreement rate to the individual SIDs requiring adjudication or guideline review.

No disagreement category is treated as semantic error automatically. Classification describes the structural difference between the two annotation outputs; adjudication remains a separate methodological step.

## Execution status

The selector implementation, fingerprint tests, independent-shell generator, agreement comparator, and disagreement classifier are committed. The real 7,850-SID pilot artifact has **not yet been executed in the project working tree** and therefore no frozen pilot evidence or agreement result is claimed here.

Expected execution:

```bash
python scripts/select_annotation_pilot.py \
  --input-dir data/segmented/zohar/wikisource \
  --output data/analysis/annotation_pilot.json \
  --sample-size 30

python scripts/init_annotation_pilot.py \
  --pilot data/analysis/annotation_pilot.json \
  --output-dir data/analysis/annotation_pilot_annotations
```

The resulting artifact must be preserved as the frozen pilot input before either annotator begins coding.

After independent coding and structural validation:

```bash
python scripts/compare_annotation_pilots.py \
  --annotator-a data/analysis/annotation_pilot_annotations/annotator_a.json \
  --annotator-b data/analysis/annotation_pilot_annotations/annotator_b.json \
  --output data/analysis/annotation_agreement.json

python scripts/classify_annotation_disagreements.py \
  --annotator-a data/analysis/annotation_pilot_annotations/annotator_a.json \
  --annotator-b data/analysis/annotation_pilot_annotations/annotator_b.json \
  --output data/analysis/annotation_disagreements.json
```

## Validation requirements

GATE-004 cannot be marked `VALIDATED` until all of the following exist:

1. frozen pilot selection;
2. two independent annotation records for the same frozen SIDs;
3. structural validation of both annotation sets;
4. reproducible agreement calculation;
5. disagreement classification;
6. documented changes, if any, to vocabulary or guidelines;
7. final rerun of structural validation.

LLM output is not independent human ground truth and remains `CANDIDATE` until reviewed under the annotation schema.

## Current limitation

The selector, integrity fingerprints, independent shells, agreement comparator, and disagreement classifier are implemented, but the real pilot has not yet been executed in the project working tree and no independent annotation agreement result has been produced. Therefore the gate remains `IN_PROGRESS`.
