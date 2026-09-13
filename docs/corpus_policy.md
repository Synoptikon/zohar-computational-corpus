# Corpus provenance and licensing policy

## Purpose

GATE-001 requires a corpus snapshot whose provenance, edition, version, retrieval method, integrity hash, segmentation basis, and reuse status can be audited.

The repository must never silently mix editions, translations, revisions, or licensing regimes.

## Required provenance fields

Every ingested corpus artifact must record:

- `cid`: stable corpus identifier
- `source`: institution or provider
- `source_url`: canonical source URL or API endpoint
- `edition`: bibliographic edition
- `language`: ISO language code where applicable
- `version`: provider version or revision identifier
- `retrieved_at`: UTC timestamp of acquisition
- `sha256`: SHA-256 hash of the exact stored artifact
- `format`: storage format
- `license`: explicit reuse status
- `license_evidence_url`: URL supporting the license determination
- `raw_path`: immutable RAW artifact path
- `normalization`: transformation identifier, or `NONE`
- `segmentation`: segmentation scheme identifier, or `NONE`

## Source separation

The project distinguishes at minimum:

1. **Primary-language corpus** — Hebrew/Aramaic source text intended for linguistic analysis.
2. **Translation corpus** — translations used for comparative or auxiliary experiments.
3. **Metadata** — bibliographic and structural information that does not constitute corpus text.

These layers must not be merged into a single text field.

## Current source assessment

Sefaria provides a structured API for text retrieval and exposes version metadata. Its documentation states that individual text versions can have different copyright statuses, including public domain, Creative Commons, or unverified status. Therefore license status must be evaluated per version, not inferred from the platform as a whole.

For the Zohar, the Sefaria catalog currently identifies **Vocalized Zohar, Israel 2013** as a Hebrew source whose license is not specified in the catalog. This source is therefore **BLOCKED for redistribution in this repository until its reuse status is independently verified**.

The catalog identifies **The Zohar; London, Soncino Press, 1933** as an English translation with Public Domain status. It may be used as an auxiliary translation corpus subject to recording the exact retrieved snapshot and provenance.

## No-license-bypass rule

A source with unknown or unresolved licensing must not be copied into `data/raw/` merely because an API makes it technically accessible.

The project may store metadata describing such a source, but not redistribute the underlying text until reuse is verified.

## Snapshot rule

A live API response is not itself a reproducible corpus. Any accepted corpus must be snapshotted locally and hashed. Re-running an API request later is a new acquisition and must receive a new provenance record if the returned content differs.

## GATE-001 acceptance criteria

GATE-001 can be marked `VALIDATED` only when:

- a defined corpus scope exists;
- every included artifact has complete provenance;
- the exact stored bytes have a SHA-256 hash;
- licensing/reuse status is documented;
- RAW is immutable;
- the acquisition process is reproducible;
- no unverified source has been silently included;
- the corpus manifest matches the stored artifacts.

Until all criteria are satisfied, GATE-001 remains `BLOCKED` or `TESTING`.
