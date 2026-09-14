# Lexical extraction protocol v0.1

Status: SPECIFICATION
Layer: `RAW → EXTRACTED-E1`

## Objective

Recover lexical-bearing wikitext from the immutable RAW snapshot by using the Wikisource MediaWiki parser, while preserving provenance and making the resulting derivative independently hashable.

This protocol does **not** claim that the resulting text is a critical-edition witness or historically authentic text. It is a computational derivative of a specific Wikisource revision under a recorded MediaWiki parser/template environment.

## Inputs

- `snapshot_manifest.json`
- RAW page wikitext
- `pageid`
- `revid`
- page title when available
- Wikisource API endpoint

## Extraction method E1

For each RAW page:

1. Verify `sha256(RAW)` against `snapshot_manifest.json`.
2. Read the exact UTF-8 RAW wikitext.
3. Submit that wikitext to `action=expandtemplates` with the source `revid` and page title.
4. Request expanded wikitext, not HTML.
5. Preserve line breaks and whitespace returned by the API.
6. Store the expanded output byte-for-byte as the E1 derivative.
7. Hash the E1 output with SHA-256.
8. Separately inspect the source revision through `action=parse` with `oldid` and `prop=templates` to enumerate transcluded templates.
9. Record dependency metadata for each discovered template where revision metadata is obtainable.
10. Mark dependency reproducibility as `CONDITIONAL` unless all template dependencies are themselves captured and replayable.

MediaWiki documents `action=expandtemplates` as the API operation that expands all templates in supplied wikitext and returns expanded wikitext. `action=parse` can inspect a specific revision and report the templates used by that revision. These operations are therefore used as explicit extraction primitives rather than inferred local regex substitutions.

## Why E1 is not yet declared fully reproducible

The page `revid` identifies the source page revision, but template transclusions are external dependencies. A later rerun may produce different output if a transcluded template has changed. Therefore:

- the **stored E1 artifact** is reproducible by hash;
- the **regeneration process** is only conditionally reproducible until template dependencies are captured and replayable;
- no E1 result may be labelled `FULLY_REGENERABLE` without dependency-lock evidence.

This distinction is mandatory.

## Dependency record

For each template, record when available:

- template title
- namespace
- pageid
- revision id
- revision timestamp
- revision SHA-1 reported by MediaWiki
- retrieval timestamp
- API endpoint

Dependency status:

- `RECORDED` — dependency metadata obtained;
- `MISSING` — dependency could not be resolved;
- `UNPINNED` — metadata exists but expansion cannot yet be replayed locally from the captured dependency;
- `LOCKED` — dependency content is captured and the expansion can be replayed;
- `BLOCKED` — unresolved dependency prevents lexical validation.

## Postconditions

E1 may be `PASS` only when:

- RAW hash matches the acquisition manifest;
- API response is valid;
- expanded output is non-empty when lexical content is expected;
- the output is hashed;
- all unresolved template constructs are reported;
- dependency metadata is recorded;
- source and derivative identifiers are linked.

`PASS` means successful extraction, **not** historical or semantic validation.

## Lexical residuals

E1 does not silently strip all MediaWiki markup. Remaining constructs are classified after expansion:

- `LEXICAL_TEXT`
- `HEADING`
- `LINK_MARKUP`
- `REFERENCE_MARKUP`
- `CATEGORY_MARKUP`
- `HTML_MARKUP`
- `UNRESOLVED_TEMPLATE`
- `OTHER_UNKNOWN_MARKUP`

Any `UNRESOLVED_TEMPLATE` or `OTHER_UNKNOWN_MARKUP` affecting the lexical body blocks downstream lexical segmentation for that page.

## Determinism

The E1 derivative itself is deterministic as an artifact: identical output bytes must produce the same SHA-256. Regeneration determinism requires identical source bytes, identical extractor version/configuration, identical API/parser behavior, and identical template dependency state.

## Non-goals

- no semantic interpretation;
- no normalization that collapses structural whitespace;
- no segmentation into SIDs;
- no claim of textual authenticity;
- no silent deletion of unresolved markup;
- no substitution of a local regex expander for MediaWiki's parser.

## Acceptance fixture

Before running the full corpus, E1 must be tested on a deterministic fixture of 3–10 pages containing at minimum:

1. a direct/transcluded Zohar text page;
2. a page with headings/navigation;
3. a page containing references or residual markup;
4. preferably one index-like page with navigation templates.

The fixture must record page sequence, pageid, revid, source hash and expected extraction status.
