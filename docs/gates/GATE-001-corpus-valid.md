# GATE-001 — Corpus válido

**Status:** IN_PROGRESS / NOT VALIDATED

## Objective

Establish one or more corpus snapshots whose provenance, integrity, scope, and reuse status are independently auditable.

## Selected primary-language candidate

**CID:** `CID-ZOHAR-WIKISOURCE-MANTUA`

The Hebrew Wikisource edition documents the Mantua 1558 (5318) edition as the basis for its page numbering and exposes the Zohar in Hebrew/Aramaic. The source page currently states that its text is distributed under **Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)**.

Source:
https://he.wikisource.org/wiki/ספר_הזהר

The corpus scope for the first snapshot is deliberately limited to:

- Zohar Part I — Genesis
- Zohar Part II — Exodus
- Zohar Part III — Leviticus, Numbers and Deuteronomy

Tikunei Zohar and Zohar Chadash remain separate auxiliary corpora and are not silently mixed into the primary corpus.

## Acquisition

Acquisition is implemented through:

`scripts/acquire_wikisource_zohar.py`

The script uses the Hebrew Wikisource MediaWiki API, recursively traverses the three selected Zohar categories, retrieves page wikitext, writes UTF-8 RAW files, and produces a per-page SHA-256 manifest.

No normalization, segmentation, annotation, embedding, or interpretation is performed during acquisition.

## License status

**VERIFIED_AT_SOURCE:** CC BY-SA 4.0 for the Wikisource text layer.

Redistribution must preserve attribution and the applicable ShareAlike requirements.

This does not mean that the Wikisource transcription is a critical edition or that every transcription is independently verified. Textual quality remains a separate validation problem.

## Provenance status

**DOCUMENTED_BUT_NOT_YET_INDEPENDENTLY_COLLATION_VALIDATED**

Wikisource identifies the Mantua edition as the basis for page numbering, but the repository does not yet have an independent collation against a digitized historical witness.

A National Library of Israel digitized Zohar witness is available as an independent provenance/reference candidate and can be used for future collation. Its individual use conditions must be recorded separately from the Wikisource license.

## Current decision

The primary-language source is now **license-eligible for acquisition**, but GATE-001 remains **NOT VALIDATED** because the immutable snapshot has not yet been acquired into `data/raw/`, hashed, and independently checked in this repository.

## Required evidence before validation

1. Execute the acquisition script.
2. Preserve the exact RAW snapshot.
3. Compute and record SHA-256 for every acquired page.
4. Record UTC retrieval timestamp.
5. Record the source revision/page identifiers where available.
6. Verify the manifest against the stored files.
7. Run an independent integrity check.
8. Perform an initial transcription-quality audit on a predefined sample.
9. Record the sample methodology and error findings.
10. Do not normalize or segment RAW during this gate.

## What this gate does not establish

GATE-001 does not establish textual authenticity, historical authorship, semantic correctness, superiority of the Mantua witness, or correctness of every Wikisource transcription.

It establishes only that the selected computational corpus is sufficiently identified, legally documented for the intended reuse, immutable at snapshot level, and reproducible enough to proceed to corpus-quality validation.
