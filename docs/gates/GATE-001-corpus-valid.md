# GATE-001 — Corpus válido

**Status:** BLOCKED

## Objective

Establish one or more corpus snapshots whose provenance, integrity, scope, and reuse status are independently auditable.

## Evidence collected

The project identified Sefaria as a viable structured acquisition interface. Its current API documentation states that text versions can be retrieved through the v3 Texts endpoint and that version metadata can be queried separately.

The current Sefaria catalog identifies:

- `Vocalized Zohar, Israel 2013` — Hebrew, source attributed to nli.org.il, license currently unspecified in the catalog.
- `The Zohar; London, Soncino Press, 1933` — English translation, source attributed to nli.org.il, listed as Public Domain.

## Decision

No Zohar Hebrew text is stored in `data/raw/` at this stage.

The Hebrew candidate remains `BLOCKED_LICENSE` because the repository must not redistribute a source whose reuse status is unresolved.

The Soncino English translation is an eligible auxiliary candidate, but it has not yet been snapshotted and hashed in this repository. Therefore it cannot yet satisfy GATE-001.

## Required evidence before validation

1. Define the initial corpus scope.
2. Verify the reuse status of the selected primary-language edition.
3. Acquire an exact snapshot through a documented method.
4. Store the immutable RAW artifact.
5. Compute SHA-256 over the exact artifact.
6. Record retrieval timestamp in UTC.
7. Record edition/version/source metadata.
8. Record the segmentation basis separately from normalization.
9. Verify the manifest against the stored artifact.
10. Run an independent integrity check.

## What this gate does not establish

GATE-001 does not establish textual authenticity, historical authorship, semantic correctness, or superiority of one edition over another. It establishes only that the selected computational corpus is sufficiently identified and reproducible for subsequent computational analysis.
