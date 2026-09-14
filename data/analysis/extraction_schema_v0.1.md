# Extraction Artifact Schema v0.1

**Status:** SPECIFICATION

## Artifact

Each extracted page is represented by one record. The record is a derivative of exactly one RAW page revision.

### Required fields

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | string | Extraction schema version |
| `cid` | string | Corpus identifier |
| `sequence` | integer | Stable acquisition sequence |
| `pageid` | integer | MediaWiki page ID |
| `revid` | integer | Source revision ID |
| `source_path` | string | RAW path |
| `source_sha256` | string | SHA-256 of exact RAW bytes |
| `extraction_method` | string | E0/E1/E2 or composed method |
| `extractor_version` | string | Implementation version |
| `extracted_path` | string | Derivative path |
| `extracted_sha256` | string | SHA-256 of derivative bytes |
| `retrieved_at_utc` | string | Derivative retrieval/execution timestamp |
| `diagnostics` | object | Counts and unresolved constructs |
| `status` | enum | `PASS`, `BLOCKED`, `FAIL` |

## Diagnostics

Required counters/collections:

- `template_count`
- `link_count`
- `tag_count`
- `reference_count`
- `category_count`
- `navigation_count`
- `unknown_markup_count`
- `unknown_markup_samples`
- `empty_output`
- `warnings`

## Provenance invariant

`source_sha256` must match the SHA-256 recorded by the RAW snapshot manifest before extraction is accepted.

## Determinism invariant

Given identical RAW bytes and identical extractor version/configuration, the extracted bytes and deterministic diagnostics must be identical. Execution timestamps are metadata and are excluded from content-hash determinism.

## Status rules

- `PASS`: no unknown markup and all required provenance/integrity checks succeed.
- `BLOCKED`: unknown/unresolved markup prevents a defensible lexical representation.
- `FAIL`: source integrity mismatch, missing required fields, non-deterministic output, or other implementation failure.

## Non-goals

This schema does not assert that extracted text is historically authentic or semantically equivalent to an edition. It only describes a reproducible computational derivative.
