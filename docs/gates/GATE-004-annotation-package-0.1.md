# GATE-004 — Annotation Package 0.1

## Purpose

This package freezes the 30-SID pilot for two independent annotators. It is a data-collection package, not evidence of agreement.

## Frozen identity

- CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- Population: `7,850` SID
- Pilot: `30` SID
- Selector: `SELECT-ANNOTATION-PILOT-0.2`
- Selection method: `SHA256_SID_ASCENDING`
- `selected_sid_sha256`: `715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d`
- Guidelines: `ANNOTATION-GUIDELINES-0.1`
- Vocabulary: `ANNOTATION-VOCABULARY-0.1`
- Annotation schema: `ANNOTATION-SCHEMA-0.1`

## Independence protocol

1. Annotator A and Annotator B must work independently.
2. They must not exchange decisions, labels, examples, disagreement information, or intermediate results before both annotations are frozen.
3. Both annotators receive exactly the same 30-SID context.
4. The SID set and pilot metadata must not be changed.
5. If evidence is insufficient, use the abstention mechanism defined by the guidelines.
6. LLM assistance is permitted only as candidate generation; `source=llm` must remain `validation_status=CANDIDATE` until human review. LLM output is not an independent ground truth.

## Package contents

The GitHub Actions artifact `gate004-annotation-package` contains:

- `manifest.json` — frozen pilot identity and provenance;
- `annotator_a.json` — A's independent annotation workspace;
- `annotator_b.json` — B's independent annotation workspace;
- `segments/` — the 30 frozen segment records, including `raw_text` and `normalized_text`.

## Submission

After both annotators finish, place the two completed JSON documents at:

- `data/analysis/annotation_pilot_annotations/annotator_a.json`
- `data/analysis/annotation_pilot_annotations/annotator_b.json`

Do not replace the pilot metadata or SID set.

## Automatic comparison chain

A GitHub Actions workflow executes automatically when the annotation files change:

`validate_annotations → validate_pair → compare → classify_disagreements → evidence`

The comparison uses exact annotation signatures. It reports agreement rate and disagreement classes; it does not claim semantic equivalence or historical validity.

`pair validation PASS` is not agreement evidence.
