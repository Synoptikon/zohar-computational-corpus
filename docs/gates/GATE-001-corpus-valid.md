# GATE-001 — Corpus válido

**Status:** IN_PROGRESS / NOT VALIDATED

## Objective

Establish one or more corpus snapshots whose provenance, integrity, scope, and reuse status are independently auditable.

## Selected primary-language candidate

**CID:** `CID-ZOHAR-WIKISOURCE-MANTUA`

The Hebrew Wikisource edition documents the Mantua 1558 (5318) edition as the basis for its page numbering and exposes the Zohar in Hebrew/Aramaic. The source page states that its text is distributed under **Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)**.

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

## Current evidence — snapshot integrity

The RAW snapshot is now present in the repository and has been committed by GitHub Actions in commit `6235700797e34a9028bebf081b16e44a16cd5cd8` (`data: add verified Wikisource RAW snapshot`, 2026-09-14T08:28:54Z). The commit updates the immutable snapshot manifest and validation record, including the retrieval timestamp and manifest digest. fileciteturn9file0L3-L15

The committed validation artifact reports:

- `validation: PASS`
- `page_count: 1721`
- manifest SHA-256: `0d05ffc9f07322abd87362e286b7f92dc96bc152a63fecbb2f4fd248e306c24e`
- deterministic structural sample: 10 sequences
- `sample_failures: []`
- per-file SHA-256 verification included among the checks
- non-empty file verification included
- deterministic sample containing Hebrew-script characters included

The validator explicitly limits this evidence to acquisition integrity and states that it does not establish textual correctness against a historical witness. fileciteturn11file0L2-L2

The manifest records source, API, license, UTC-equivalent retrieval timestamp field, and `page_count: 1721`; it also begins the per-page sequence/title/pageid inventory. fileciteturn12file0L2-L2

## Corrected gate decision

The previous wording claiming that the snapshot had **not yet been acquired into `data/raw/`, hashed, and independently checked** is stale and has been corrected.

The repository now has auditable evidence for **acquisition and snapshot-level integrity**. This is necessary evidence for GATE-001 but is not, by itself, sufficient to close the gate.

## Remaining blocking evidence

1. **Independent integrity verification:** the committed validator result is evidence of the repository's validation procedure, but an independent second verification of the committed snapshot/manifest is not yet evidenced in the repository state inspected here.
2. **Transcription-quality audit:** a predefined sample methodology and error findings against an independent witness are not yet evidenced.
3. **Independent collation/provenance:** no committed collation against a digitized historical witness is yet evidenced.
4. **CI execution trace:** the current commit has no reported combined status checks through the available GitHub status endpoint; therefore no additional CI success is claimed solely from that endpoint.

## Required evidence before validation

1. Preserve the exact RAW snapshot.
2. Compute and record SHA-256 for every acquired page.
3. Record UTC retrieval timestamp.
4. Record the source revision/page identifiers where available.
5. Verify the manifest against the stored files.
6. Obtain and record an independent integrity check.
7. Perform an initial transcription-quality audit on a predefined sample.
8. Record the sample methodology and error findings.
9. Where feasible, perform an independent collation against a historical witness and document the result.
10. Do not normalize or segment RAW as evidence for this gate; downstream artifacts must remain separate.

## What this gate does not establish

GATE-001 does not establish textual authenticity, historical authorship, semantic correctness, superiority of the Mantua witness, or correctness of every Wikisource transcription.

It establishes only that the selected computational corpus is sufficiently identified, legally documented for the intended reuse, immutable at snapshot level, and reproducible enough to proceed to corpus-quality validation.
