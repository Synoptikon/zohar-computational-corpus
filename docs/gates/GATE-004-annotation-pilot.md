# GATE-004 — Annotation coding pilot

**Status:** IN_PROGRESS
**Gate:** `GATE-004`
**Pilot contract:** `ANNOTATION-PILOT-0.1`
**Vocabulary:** `ANNOTATION-VOCABULARY-0.1`
**Guidelines:** `ANNOTATION-GUIDELINES-0.1`

## Objective

Determine whether independent annotators can apply the current structural annotation vocabulary and guidelines consistently to the same frozen SID sample.

## Implemented evidence

- `data/analysis/annotation_vocabulary_v0.1.md`
- `data/analysis/annotation_guidelines_v0.1.md`
- `data/analysis/annotation_pilot_protocol_v0.1.md`
- `scripts/select_annotation_pilot.py`
- `tests/test_select_annotation_pilot.py`

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

## Execution status

The selector implementation and its fingerprint tests are committed. The real 7,850-SID pilot artifact has **not yet been executed in the project working tree** and therefore no frozen pilot evidence is claimed here.

Expected execution:

```bash
python scripts/select_annotation_pilot.py \
  --input-dir data/segmented/zohar/wikisource \
  --output data/analysis/annotation_pilot.json \
  --sample-size 30
```

The resulting artifact must be preserved as the frozen pilot input before either annotator begins coding.

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

The selector and protocol are implemented, including corpus-drift fingerprints, but the pilot has not yet been executed in the project working tree and no independent annotation agreement result has been produced. Therefore the gate remains `IN_PROGRESS`.
