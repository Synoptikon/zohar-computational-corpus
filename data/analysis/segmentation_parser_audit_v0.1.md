# Segmentation Parser Audit v0.1

**Status:** BLOCKED FOR LEXICAL SEGMENTATION
**Date:** 2026-09-13

## Scope inspected

- `scripts/acquire_wikisource_zohar.py`
- `scripts/validate_corpus_snapshot.py`
- `src/zohar_corpus/normalization.py`
- `src/zohar_corpus/segmentation.py`
- representative RAW pages from `data/raw/zohar/wikisource/`

## Findings

### F-001 — Acquisition stores source wikitext, not resolved lexical text

The acquisition script retrieves `revision["slots"]["main"]["content"]` and writes that content verbatim to RAW. This is correct for provenance preservation.

However, representative pages such as `0004.txt` and `0005.txt` consist mainly of Zohar navigation/transclusion templates (`{{דף של זהר...}}`, `{{קטע זוהר...}}`). Therefore RAW cannot be passed directly to a lexical segmenter.

**Classification:** DATA / REPRESENTATION
**Severity:** CRITICAL for GATE-002 lexical segmentation; not an error in RAW acquisition.

### F-002 — Existing segmentation primitive is punctuation-based and Latin-centric

`src/zohar_corpus/segmentation.py` splits on `[.!?]` followed by whitespace. This is not suitable as the primary Zohar segmentation rule because it assumes punctuation that is not demonstrated to encode the required historical/textual boundaries.

**Classification:** METHODOLOGICAL / IMPLEMENTATION
**Severity:** HIGH

### F-003 — Existing normalization collapses whitespace

`normalize_text()` applies NFC normalization and then collapses all whitespace. This is acceptable as a named normalization primitive, but it destroys paragraph/newline structure needed for structural segmentation if applied before structural parsing.

**Classification:** TRANSFORMATION
**Severity:** HIGH

### F-004 — No offset-alignment layer exists

The current normalization API returns only a string. It does not provide an alignment map from normalized characters to source characters. Therefore a segmenter cannot honestly claim RAW-relative offsets after whitespace collapsing.

**Classification:** REPRODUCIBILITY / DATA MODEL
**Severity:** HIGH

### F-005 — No SID contract or segment artifact existed before this audit

The repository had segmentation-related primitives and tests but no implemented, auditable SID output contract. `segment_v0.1` now defines the required fields, but implementation is intentionally deferred until the extraction layer is specified.

**Classification:** SCHEMA
**Severity:** HIGH

## Decision

Do **not** implement `scripts/segment_corpus.py` against the current RAW files yet.

The correct next dependency is:

`RAW wikitext → controlled extraction/expansion derivative → normalization-with-alignment → structural segmentation → SID validation`

MediaWiki documents `action=expandtemplates` as a mechanism for expanding templates in wikitext. The project must record this as a derivative operation with its dependency characteristics rather than conflating the expanded result with RAW.

## Consequence for gates

- GATE-001 integrity evidence: **PASS for snapshot integrity checks**, but full GATE-001 remains not validated because textual-quality/collation evidence is still outstanding.
- GATE-002: **BLOCKED** until a controlled lexical extraction representation and offset policy exist.
- No scientific finding is affected by this audit.

## Required next implementation

1. Define `extraction_v0.1` and its provenance/dependency manifest.
2. Produce a small deterministic fixture from 3–10 representative pages.
3. Verify that lexical text can be recovered without silent loss.
4. Add normalization with alignment tracking.
5. Implement `scripts/segment_corpus.py` only after those prerequisites pass.
6. Add SID schema validation and conservation tests.
