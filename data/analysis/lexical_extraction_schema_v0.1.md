# Lexical extraction schema v0.1

Status: SPECIFICATION

Each E1 page record MUST contain:

```text
schema_version
cid
sequence
pageid
revid
page_title
source_path
source_sha256
api_endpoint
extraction_method
extractor_version
request_parameters_hash
extracted_path
extracted_sha256
retrieved_at_utc
status
reproducibility_status
diagnostics
dependencies
```

## `diagnostics`

```text
raw_template_count
expanded_template_count
unresolved_template_count
unresolved_template_samples
html_tag_count
link_count
reference_count
category_count
heading_count
empty_output
api_warnings
api_errors
```

## `dependencies`

Array of:

```text
title
namespace
pageid
revid
timestamp
sha1
retrieved_at_utc
status
```

## Status values

Page extraction:

- `PASS`
- `BLOCKED`
- `FAIL`

Reproducibility:

- `CONDITIONAL`
- `LOCKED`
- `BLOCKED`

`PASS + CONDITIONAL` is the expected status for the first E1 implementation. It must not be upgraded to `LOCKED` merely because dependency revision IDs were recorded.

## Invariants

1. `source_sha256` MUST equal the hash recorded in the immutable RAW snapshot manifest.
2. `extracted_sha256` MUST hash the exact bytes written to the E1 artifact.
3. `request_parameters_hash` MUST represent the canonicalized API request parameters excluding volatile transport headers.
4. `revid` MUST identify the source page revision used as the input context.
5. Any unresolved template MUST be represented in diagnostics; it MUST NOT be silently removed.
6. A page with unresolved lexical-affecting markup is `BLOCKED` for downstream lexical segmentation.
7. A dependency list without captured dependency content is `CONDITIONAL`, not `LOCKED`.
8. RAW files are never overwritten by E1.

## Traceability

The minimum chain is:

`SID candidate → E1 extracted_path → source_sha256 → RAW manifest record → pageid/revid`.

E1 does not create SIDs. It only creates an auditable derivative suitable for later normalization and segmentation.
