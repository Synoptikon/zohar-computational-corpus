# Segmentation Rules v0.1

**Status:** SPECIFICATION
**Version:** `SEGMENTATION-RULES-0.1`
**Scope:** normalized Zohar corpus produced by `src/zohar_corpus/corpus_normalizer.py`

## 1. Objective

Define a deterministic, auditable first segmentation layer without introducing semantic or historical interpretations that are not represented in the current corpus schema.

This version defines the segment as a reproducible structural unit derived from one normalized record. It is intentionally conservative: semantic sections, folio boundaries, headings, references, variants, and other editorial structures are not inferred unless they are explicitly present in the input record or a later annotation layer.

## 2. Input contract

The segmentation input is a normalized JSON document with:

- top-level `schema_version`;
- top-level `normalization_version`;
- top-level `offset_unit`;
- top-level `encoding`;
- top-level `raw_file`;
- `records`, a list ordered by source sequence.

Each normalized record currently provides:

- `sequence`;
- `raw_start`;
- `raw_end`;
- `raw_text`;
- `normalized_text`;
- `normalization_rule`;
- `normalization_version`;
- `offset_unit`.

The current normalizer uses UTF-8 input and Unicode code-point indices for offsets. Normalization is NFC followed by whitespace collapse and trimming. These properties are inherited by segmentation and are not redefined by the segmenter.

## 3. Segmentation unit

### 3.1 Unit definition

In v0.1, **one normalized record = one segment candidate**.

The segment boundary is therefore the boundary of one item in `records`. The segmenter MUST preserve record order and MUST NOT merge or split records in v0.1.

This is a structural rule, not a claim that each record is a linguistic, semantic, paragraph, folio, or historical unit.

### 3.2 Empty records

Records are not discarded silently.

If a normalized record has an empty `normalized_text`, the segmenter MUST preserve the record as a segment with an explicit `is_empty` value in the output contract. Whether empty segments are included in downstream linguistic analyses is a later analytical decision.

### 3.3 Newlines

The normalized record retains its exact `raw_text`, including the source line ending. Segmentation boundaries are inherited from the normalized record sequence and are not recomputed from rendered text.

## 4. Headers

No semantic header detection is performed in v0.1.

A record is not classified as a header merely because it is short, uppercase, visually isolated, or contains punctuation. Such heuristics would introduce an unvalidated annotation rule.

A future header layer must define an explicit rule, provenance, test fixtures, and validation before being incorporated into the segmentation contract.

## 5. References

References are preserved as text. No reference extraction or semantic linking is performed by the v0.1 segmenter.

Reference extraction belongs to a later annotation layer unless the corpus schema is extended with explicit source annotations.

## 6. Variants

No variant normalization or conflation is performed by segmentation.

The segmenter MUST preserve the normalized representation produced upstream. Variant handling requires a separate, versioned annotation rule.

## 7. Page breaks and folio markers

No page or folio boundaries are inferred in v0.1.

If such markers occur literally in the normalized input, they remain part of the segment text. Removing, interpreting, or converting them requires an explicit rule and provenance.

## 8. Residual markup

The segmenter MUST NOT silently remove markup.

Markup that survives normalization remains part of `normalized_text` unless a future version explicitly defines a markup transformation. Residual markup should therefore be measurable as input data rather than hidden during segmentation.

## 9. Offsets and traceability

The segment output MUST retain the source record's raw offsets:

- `raw_start`;
- `raw_end`;
- `raw_path` or an equivalent stable source identifier;
- source sequence.

Offsets use the upstream `offset_unit`. For the current normalized corpus this is `unicode_codepoint_index`.

The segmenter MUST NOT reinterpret offsets as byte offsets or normalized-text offsets.

A segment's raw span must remain traceable to the exact substring represented by the source record.

## 10. Conservation criterion

Segmentation v0.1 is lossless with respect to the normalized records if:

1. every input record produces exactly one output segment;
2. record order is preserved;
3. `raw_text`, `raw_start`, and `raw_end` are preserved;
4. `normalized_text` is preserved exactly;
5. no record is silently discarded, merged, or split.

This is a structural conservation criterion. It does not assert semantic completeness.

## 11. Determinism

For identical normalized input and identical segmentation-rule version, the segmenter MUST produce byte-stable JSON output after applying the repository's canonical serialization policy.

The segment identifier must be deterministic and derived only from stable source identity and segment position. Runtime timestamps, random values, host paths, and process identifiers MUST NOT affect a `SID`.

## 12. Error policy

The segmenter MUST fail explicitly when required input fields are missing or have invalid types.

It MUST NOT silently repair malformed normalized records.

At minimum, validation must detect:

- missing `records` list;
- non-object records;
- missing `sequence`;
- invalid offset types;
- negative offsets;
- `raw_end < raw_start`;
- invalid `normalized_text` type;
- duplicate or non-monotonic source sequence within a file.

## 13. Non-goals

Segmentation v0.1 does not establish:

- semantic paragraph boundaries;
- historical authorship boundaries;
- folio or page reconstruction;
- linguistic units;
- named entities;
- references or citations as relations;
- thematic units;
- mystical or metaphysical categories.

Those require independent specifications and validation.

## 14. Required validation artifacts

Before `GATE-002` can be marked `VALIDATED`, the repository must contain:

- this versioned rule specification;
- a stable SID contract;
- the segmentation implementation;
- deterministic fixtures and tests;
- a corpus-level segmentation run;
- a segmentation audit report;
- evidence that the run is reproducible.

`IMPLEMENTED` alone is insufficient for gate closure.
