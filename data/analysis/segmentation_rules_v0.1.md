# Segmentation Rules v0.1

**Status:** SPECIFICATION / NOT IMPLEMENTED
**Version:** `segmentation_rules_v0.1`
**Scope:** primary Zohar corpus snapshot, Hebrew/Aramaic Wikisource source

## 1. Objective

Define a deterministic segmentation policy that converts a validated, non-RAW derivative into stable segment records without silently altering the source text.

Segmentation is an implementation rule. It does **not** assert that the resulting units correspond to historical, semantic, or authorial sentence boundaries.

## 2. Input layers

The pipeline MUST preserve:

`RAW → NORMALIZED → SEGMENTED`

- `RAW`: exact acquired Wikisource wikitext; immutable and never overwritten.
- `NORMALIZED`: explicit derivative produced by a named normalization version.
- `SEGMENTED`: records derived from NORMALIZED with provenance back to RAW.

The current acquisition snapshot contains MediaWiki wikitext. Several Zohar pages are template/transclusion wrappers rather than lexical text. Therefore v0.1 MUST NOT treat raw wikitext template bodies as the textual unit for linguistic segmentation.

## 3. Unit of segmentation

Primary unit: **document-page block** corresponding to one source page/revision after controlled expansion/extraction.

Secondary unit: **text paragraph** where paragraph boundaries are explicitly recoverable from the derivative representation.

Sentence segmentation is NOT part of v0.1. The existing punctuation splitter is an implementation primitive only and is not an accepted Zohar sentence model.

Each segment MUST have:

- stable `SID`;
- `CID`;
- source page identifier;
- source revision identifier when available;
- source byte/character offsets when the transformation preserves an offset mapping;
- segment ordinal within the parent source unit;
- exact segment text;
- normalization identifier;
- segmentation-rule version;
- provenance status.

## 4. Headers

Markdown/MediaWiki headings are structural metadata, not textual content by default.

Rules:

1. Detect heading syntax before whitespace normalization.
2. Preserve heading text in metadata (`heading_path`, `heading_level`, `heading_text`).
3. Do not merge heading text into a prose segment unless a later experiment explicitly requires it.
4. A heading creates a structural boundary for subsequent paragraph segments.
5. Unrecognized heading-like markup is retained as residual markup rather than silently interpreted.

## 5. References

Reference markup such as `<ref>...</ref>`, `<references/>`, footnote markers, and citation templates MUST NOT be silently deleted from RAW.

For SEGMENTED output:

- inline reference markup is excluded from lexical text by default;
- reference payload is stored separately when extractable;
- reference presence is recorded as an annotation flag;
- unresolved reference markup is retained in `markup_residual`.

## 6. Variants

Variant readings and editorial alternatives such as parenthetical `נ"א` material MUST be preserved in RAW and NORMALIZED representations.

v0.1 does not resolve variants into a single canonical reading.

If a variant can be structurally identified, represent it as an annotation with:

- `variant_type`;
- `surface_text`;
- `variant_text`;
- offsets relative to the source derivative.

If identification is uncertain, retain the surface text and mark the structure as unresolved.

## 7. Page breaks and folio references

Page/folio markers such as `דף א א`, `א ע"א`, or equivalent source navigation markup are structural metadata.

They MUST:

- be preserved in provenance metadata when recoverable;
- define a boundary when they represent a source-page transition;
- never be converted into arbitrary sentence boundaries;
- retain the original surface form.

A segment MUST NOT cross a verified source-page boundary unless the representation explicitly models a multi-page segment.

## 8. Markup residual

Unknown or unsupported MediaWiki markup MUST NOT be silently stripped.

Each segment may contain `markup_residual`, a list of unresolved spans with:

- markup type: `UNKNOWN`, `TEMPLATE`, `LINK`, `TAG`, `PARSER_FUNCTION`, `OTHER`;
- start/end offsets;
- exact surface text.

A segment with unresolved markup is valid for structural analysis but is NOT automatically valid for lexical/statistical analysis.

## 9. Offsets

Offsets are measured against the immediate input representation named by the record.

Required convention:

- `start_offset`: zero-based inclusive;
- `end_offset`: zero-based exclusive;
- `offset_unit`: `UNICODE_CODEPOINT` for v0.1.

Byte offsets MUST NOT be inferred from character offsets.

If a normalization step changes character count and no deterministic alignment map exists, lexical offsets MUST be set to `null` and the record marked `offset_status: UNAVAILABLE`.

## 10. Conservation criterion

Segmentation MUST be conservative.

A transformation is acceptable only when every output character can be classified as one of:

1. preserved lexical/source text;
2. normalized representation with an explicit rule;
3. structural markup represented in metadata;
4. excluded markup represented in `markup_residual` or a reference/variant annotation.

Unclassified deletion is a validation failure.

## 11. Template/transclusion rule

The current RAW snapshot demonstrates that some pages consist primarily of templates such as `{{דף של זהר|...}}` and `{{קטע זוהר|...}}`. These wrappers do not themselves constitute the lexical corpus.

Therefore v0.1 requires a preceding **controlled extraction/expansion layer** that records the exact source page, revision and extraction method. The segmenter MUST refuse lexical segmentation when the input remains unresolved template-only wikitext.

MediaWiki's `action=expandtemplates` can expand wikitext, but the resulting derivative has dependency on the MediaWiki template environment; this dependency MUST be recorded rather than treated as equivalent to the immutable RAW snapshot.

## 12. Determinism

Given identical:

- RAW snapshot;
- extraction configuration;
- normalization version;
- segmentation version;

segmentation MUST produce byte-identical serialized output, apart from explicitly documented serialization metadata such as run timestamp.

## 13. Rejection conditions

The segmenter MUST fail closed when:

- input provenance is missing;
- source revision cannot be identified where required;
- template-only content is presented as lexical text;
- offsets are claimed without an alignment basis;
- unsupported markup is deleted without annotation;
- output SIDs are duplicated;
- source order cannot be established deterministically.

## 14. Non-goals

v0.1 does not establish:

- historical sentence boundaries;
- semantic units;
- authorship boundaries;
- textual superiority of the Wikisource witness;
- linguistic equivalence between Hebrew and Aramaic passages;
- correctness of any later interpretation.
