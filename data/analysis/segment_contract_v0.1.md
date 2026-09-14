# Segment Output Contract v0.1

**Contract:** `SID-CONTRACT-0.1`
**Status:** SPECIFICATION
**Upstream:** `SEGMENTATION-RULES-0.1`

## 1. Purpose

Define the stable output record for segmentation before implementation begins.

A `SID` identifies exactly one normalized input record in segmentation v0.1. It is an identifier for a structural segment, not an assertion about semantic or historical boundaries.

## 2. Output document

A segmentation output document MUST contain:

```text
schema_version
segmentation_version
input_normalization_version
offset_unit
encoding
source_normalized_path
segments
```

`segments` MUST be an ordered list.

## 3. Segment record

Each segment MUST contain:

| Field | Type | Requirement |
|---|---|---|
| `sid` | string | deterministic, unique within the corpus |
| `cid` | string | stable corpus identifier |
| `source_normalized_path` | string | repository-relative normalized source path |
| `sequence` | integer | source normalized-record sequence |
| `segment_index` | integer | zero-based output position within the source document |
| `raw_start` | integer | source RAW start offset |
| `raw_end` | integer | source RAW end offset |
| `raw_text` | string | exact source RAW substring |
| `normalized_text` | string | exact normalized record text |
| `offset_unit` | string | inherited from normalized input |
| `segmentation_version` | string | `SEGMENTATION-RULES-0.1` |
| `is_empty` | boolean | whether `normalized_text == ""` |

## 4. Identifier

The SID MUST be deterministic and independent of runtime state.

Recommended canonical form:

```text
SID:<CID>:<source-relative-path>:<sequence>
```

The implementation may use a filesystem-safe encoding of this logical identifier, but the mapping MUST be documented and stable.

No timestamp, random value, process ID, absolute filesystem path, or host-specific value may enter the SID.

## 5. CID

`cid` MUST identify the corpus snapshot from which the normalized source derives. The segmenter MUST NOT invent a new corpus identity per execution.

If the repository does not yet provide a stable CID in configuration or manifest data, implementation MUST fail or require an explicit configured CID rather than silently deriving one from the local environment.

## 6. Offset semantics

`raw_start` and `raw_end` are inherited from the normalized record and retain the upstream unit.

For the current corpus:

```text
offset_unit = unicode_codepoint_index
encoding    = UTF-8
```

The segmenter MUST NOT convert these values to byte offsets or normalized-text offsets.

## 7. Ordering

Segments MUST be emitted in the same order as normalized `records`.

Within one source document:

```text
segment_index = 0, 1, 2, ...
```

and source `sequence` MUST be strictly increasing for valid input.

## 8. Conservation invariants

For every valid normalized document:

```text
number_of_segments == number_of_records
```

and for every corresponding record `r` and segment `s`:

```text
s.sequence == r.sequence
s.raw_start == r.raw_start
s.raw_end == r.raw_end
s.raw_text == r.raw_text
s.normalized_text == r.normalized_text
```

No record may be silently omitted, merged, split, or rewritten.

## 9. Error conditions

The implementation MUST reject input when:

- `records` is absent or is not a list;
- a record is not an object;
- required source fields are absent;
- offsets are not integers;
- offsets are negative;
- `raw_end < raw_start`;
- `sequence` is not an integer;
- sequence order is not strictly increasing;
- `normalized_text` or `raw_text` is not a string;
- a deterministic SID would collide within the output.

Errors MUST be explicit and machine-readable.

## 10. Canonical serialization

JSON output MUST be UTF-8 and use the repository's canonical serialization policy. Key ordering, indentation, and trailing newline MUST be fixed by the implementation and covered by tests.

The same normalized input, configuration, and implementation version MUST produce byte-identical output.

## 11. Validation classification

This contract is a specification, not validation evidence.

The following states remain distinct:

- `SPECIFICATION`: contract defined;
- `IMPLEMENTED`: implementation exists;
- `TESTING`: tests executing;
- `VALIDATED`: implementation and corpus-level evidence satisfy the contract.

Only the last state can support closure of the relevant gate.
