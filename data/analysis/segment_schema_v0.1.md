# SID Segment Contract v0.1

**Status:** SPECIFICATION / NOT IMPLEMENTED
**Schema ID:** `segment_v0.1`

## 1. Purpose

Define the minimum auditable contract for a computational segment (`SID`). The contract separates source identity, provenance, structure, text, offsets, and unresolved markup.

## 2. Stable identifiers

### CID — Corpus identifier

Identifies the corpus snapshot or corpus family.

Example: `CID-ZOHAR-WIKISOURCE-MANTUA`

### SID — Segment identifier

Deterministic identifier derived from the corpus identifier, source page/revision and segment ordinal. The implementation MUST specify the exact canonical serialization before generating SIDs.

Recommended canonical input:

`CID | pageid | revid | segment_ordinal | segmentation_version`

Recommended representation:

`SID-ZOHAR-<base32(sha256(canonical_input))[:20]>`

The hash is an identifier, not a content claim.

## 3. Required fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `sid` | string | yes | Stable segment identifier |
| `cid` | string | yes | Corpus identifier |
| `page_sequence` | integer | yes | Deterministic sequence from snapshot manifest |
| `pageid` | integer | yes | MediaWiki page identifier |
| `revid` | integer | yes | Source revision identifier |
| `source_title` | string | yes | Original source page title |
| `segment_ordinal` | integer | yes | 1-based ordinal within source unit |
| `segment_type` | enum | yes | `HEADER`, `PARAGRAPH`, `TEXT_BLOCK`, `STRUCTURAL_ONLY` |
| `text` | string | yes | Segment text after declared normalization |
| `normalization_version` | string | yes | Exact normalization contract |
| `segmentation_version` | string | yes | Exact segmentation contract |
| `source_path` | string | yes | RAW snapshot path |
| `source_sha256` | string | yes | SHA-256 of source RAW file |
| `offset_start` | integer/null | yes | Zero-based inclusive offset |
| `offset_end` | integer/null | yes | Zero-based exclusive offset |
| `offset_unit` | enum | yes | `UNICODE_CODEPOINT` or `NONE` |
| `offset_status` | enum | yes | `AVAILABLE`, `UNAVAILABLE`, `NOT_APPLICABLE` |
| `heading_path` | array | yes | Structural heading context |
| `folio` | object/null | yes | Source folio metadata when recoverable |
| `references` | array | yes | Extracted reference annotations |
| `variants` | array | yes | Extracted variant annotations |
| `markup_residual` | array | yes | Unsupported/unresolved markup spans |
| `provenance_status` | enum | yes | Provenance confidence/status |

## 4. Enumerations

### `segment_type`

- `HEADER`: structural heading only.
- `PARAGRAPH`: paragraph-level lexical content.
- `TEXT_BLOCK`: lexical block where paragraph semantics cannot be established reliably.
- `STRUCTURAL_ONLY`: source structure with no lexical payload.

### `offset_status`

- `AVAILABLE`: deterministic alignment exists.
- `UNAVAILABLE`: source alignment was lost by a documented transformation.
- `NOT_APPLICABLE`: structural-only record.

### `provenance_status`

- `RAW_DIRECT`: direct mapping to RAW.
- `DERIVED_EXACT`: deterministic derivative with recorded transformation.
- `DERIVED_EXTERNAL_DEPENDENCY`: derivative depends on external rendering/template state.
- `UNRESOLVED`: provenance insufficient for lexical analysis.

## 5. Folio object

When available:

```json
{
  "volume": "I",
  "daf": "א",
  "side": "א",
  "surface": "דף א א",
  "source": "explicit|derived|unresolved"
}
```

No conversion from Hebrew folio notation to numeric coordinates is required in v0.1.

## 6. Reference object

```json
{
  "type": "footnote|reference|citation|unknown",
  "surface_text": "...",
  "start_offset": 0,
  "end_offset": 0,
  "status": "resolved|unresolved"
}
```

## 7. Variant object

```json
{
  "variant_type": "editorial|reading|unknown",
  "surface_text": "...",
  "variant_text": "...",
  "start_offset": 0,
  "end_offset": 0,
  "status": "resolved|candidate|unresolved"
}
```

## 8. Markup residual object

```json
{
  "markup_type": "TEMPLATE|LINK|TAG|PARSER_FUNCTION|OTHER",
  "surface_text": "...",
  "start_offset": 0,
  "end_offset": 0,
  "status": "unresolved"
}
```

## 9. Invariants

1. `sid` is unique within the corpus snapshot.
2. `segment_ordinal` is contiguous within each source unit unless an explicit rejected/omitted record is documented.
3. `source_sha256` matches the RAW manifest.
4. `revid` and `pageid` match the RAW manifest.
5. `offset_start < offset_end` when `offset_status=AVAILABLE`.
6. `text` is never silently replaced by an interpretation or translation.
7. Unsupported markup is never silently deleted.
8. Source order is deterministic.
9. Serialization order is deterministic.

## 10. Canonical serialization

The implementation MUST serialize fields in the schema order above and use UTF-8 JSON with:

- `ensure_ascii=false`;
- sorted object keys disabled in favor of schema order;
- newline-delimited records for large corpora;
- final newline in every artifact.

The exact serializer implementation becomes part of the model/version manifest.

## 11. Validation status

This contract is **SPECIFICATION / NOT IMPLEMENTED** until a validator and at least one fixture are committed and executed successfully.
