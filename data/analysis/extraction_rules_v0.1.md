# Controlled Extraction Rules v0.1

**Status:** SPECIFICATION
**Layer:** RAW → EXTRACTED
**Objective:** derive lexical/structural text from MediaWiki wikitext without modifying or overwriting RAW.

## 1. Inputs

- RAW snapshot directory: `data/raw/zohar/wikisource/`
- `snapshot_manifest.json`
- MediaWiki page identifiers and revision identifiers recorded by acquisition.

## 2. Immutable-source rule

RAW files are never edited by extraction. Extraction creates a separate derivative tree.

Pipeline:

`RAW → EXTRACTED → NORMALIZED → SEGMENTED`

## 3. Extraction modes

### E0 — RAW passthrough

Preserve exact wikitext. No lexical interpretation.

### E1 — Template expansion

Resolve MediaWiki templates using the source MediaWiki expansion mechanism where reproducibly available.

Record:

- source pageid
- source revid
- extraction method
- endpoint/tool version
- retrieval timestamp UTC
- output hash
- source hash

### E2 — Controlled markup stripping

After expansion, remove only explicitly classified presentation markup. Never remove unknown markup silently.

Every removed construct must be classified as one of:

- navigation
- category
- reference
- formatting
- citation
- structural wrapper
- unknown

Unknown constructs cause `BLOCKED` status for lexical extraction rather than automatic deletion.

## 4. Text conservation

Extraction must expose enough metadata to determine which source constructs generated each output span.

For each derivative page record:

`source_sha256 → extracted_sha256`

and extraction diagnostics including counts of templates, links, tags, references, unknown constructs and empty outputs.

## 5. Structural preservation

Do not collapse whitespace, paragraphs, line breaks, folio markers, or headings during extraction unless the rule explicitly identifies them as non-text markup.

Whitespace normalization belongs to a later layer.

## 6. Fixture requirement

Before corpus-wide execution, build a deterministic fixture containing at least 3 and preferably 10 representative pages covering:

- a page with transclusion
- a page with headings/navigation
- a page containing references
- a page containing markup residual
- beginning, middle and end corpus positions

The fixture must be versioned and accompanied by expected extraction diagnostics.

## 7. Acceptance criteria

Extraction may advance only if:

1. every fixture input has a recorded source hash;
2. every fixture output has a recorded derivative hash;
3. extraction method and version are recorded;
4. unknown markup is surfaced, not silently discarded;
5. source/output relationships are auditable;
6. extraction is deterministic for the same source revision and configuration;
7. RAW remains byte-identical.

## 8. Non-claims

Successful extraction does not establish textual authenticity, historical correctness, semantic equivalence, or transcription accuracy.

It establishes only that a reproducible derivative representation has been generated under documented rules.
