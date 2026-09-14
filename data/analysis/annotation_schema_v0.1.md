# Annotation Schema v0.1

**Contract:** `ANNOTATION-SCHEMA-0.1`
**Status:** SPECIFICATION
**Upstream:** `SID-CONTRACT-0.1`

## 1. Purpose

Define the minimum machine-readable contract for annotations attached to stable `SID` segments without encoding an interpretation as ground truth.

An annotation is metadata about a segment or relation. It is not equivalent to the source text, a model output, or a historical interpretation.

## 2. Required record

Each annotation record MUST contain:

| Field | Type | Requirement |
|---|---|---|
| `eid` | string | stable annotation/entity identifier |
| `sid` | string | existing segment identifier |
| `annotation_type` | string | controlled type identifier defined by a future annotation vocabulary |
| `value` | JSON value | annotation payload |
| `source` | string | provenance of the annotation, e.g. `human`, `rule`, `llm` |
| `annotator` | string | annotator/model identifier; `human:<id>` or `model:<name>@<version>` |
| `annotation_version` | string | `ANNOTATION-SCHEMA-0.1` |
| `validation_status` | string | controlled lifecycle state |

## 3. Optional provenance fields

An implementation MAY include:

- `rid`: stable relation identifier when the annotation represents a relation;
- `target_eid`: target annotation/entity identifier for a relation;
- `confidence`: numeric confidence supplied by the annotator/model, only when its scale is explicitly defined;
- `rationale`: concise machine-readable or human rationale;
- `created_at`: provenance timestamp; it MUST NOT affect identity;
- `source_reference`: reference to an external or internal source used during annotation.

Optional fields MUST NOT silently change the meaning of required fields.

## 4. Controlled values

`source` MUST be one of:

```text
human
rule
llm
import
```

`validation_status` MUST be one of:

```text
CANDIDATE
REVIEWED
ACCEPTED
REJECTED
SUPERSEDED
```

`annotation_type` is intentionally not populated with substantive Zohar categories in v0.1. Domain vocabularies require a separate specification and validation process.

## 5. LLM rule

An LLM-generated annotation MUST initially use:

```text
source = "llm"
validation_status = "CANDIDATE"
```

An LLM output MUST NOT be promoted automatically to `ACCEPTED`.

The provenance record SHOULD identify model name/version, prompt/version, and relevant execution parameters in an associated reproducibility artifact.

## 6. Identity

`eid` MUST be deterministic for the same annotation identity and MUST NOT contain timestamps, process IDs, absolute paths, or host-specific state.

`rid`, when present, MUST likewise be deterministic.

The annotation identifier does not replace `SID`; annotations remain downstream objects.

## 7. Separation of layers

The following distinctions are mandatory:

```text
source text      != annotation
annotation       != model output
model output     != validation
validation       != interpretation
```

No annotation field may be interpreted as a claim about historical truth merely because it is present in the corpus.

## 8. Validation states

The annotation lifecycle is:

```text
CANDIDATE → REVIEWED → ACCEPTED
                    ↘ REJECTED
ACCEPTED → SUPERSEDED
```

`CANDIDATE` is the default state for newly generated annotations.

## 9. Scope of v0.1

This contract defines record structure and provenance only. It does not define:

- semantic categories for the Zohar;
- historical attribution;
- linguistic truth labels;
- theological interpretation;
- model truth;
- agreement thresholds;
- statistical significance.

Those require separate hypotheses, vocabularies, annotation guidelines, and validation experiments.

## 10. Validation classification

This document is a specification. A schema can be syntax-validated without its substantive annotations being scientifically validated.

States remain distinct:

- `SPECIFICATION`: contract defined;
- `IMPLEMENTED`: validator/tooling exists;
- `TESTING`: tests executing;
- `VALIDATED`: schema contract and validator tests pass.

`VALIDATED` here applies only to the schema contract, not to any future annotation claims.
