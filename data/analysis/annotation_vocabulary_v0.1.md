# Annotation Vocabulary v0.1

**Contract:** `ANNOTATION-VOCABULARY-0.1`
**Status:** SPECIFICATION
**Upstream:** `ANNOTATION-SCHEMA-0.1`

## 1. Purpose

Define a deliberately minimal, domain-neutral registry of annotation types for the first coding pilot.

This vocabulary does **not** encode theological, historical, semantic, or philological truth. It defines only the structural class of an annotation. Domain-specific vocabularies require separate hypotheses and validation.

## 2. Controlled annotation types

| `annotation_type` | Meaning | Required value shape |
|---|---|---|
| `ENTITY` | annotation identifies a candidate entity mention or entity record associated with a segment | JSON object with a `label` string |
| `RELATION` | annotation identifies a candidate relation between annotation entities | JSON object with `relation_type`, `source_eid`, and `target_eid` strings |
| `FEATURE` | annotation records an explicitly defined observable feature of a segment | JSON object with `feature` and `value` |

These types are structural containers. Their presence does not assert that an entity, relation, or feature is historically or semantically true.

## 3. ENTITY

Minimum payload:

```json
{"label": "..."}
```

`label` is an annotation label, not a normalized historical identity unless a separate entity authority is defined.

## 4. RELATION

Minimum payload:

```json
{"relation_type": "...", "source_eid": "EID-...", "target_eid": "EID-..."}
```

A relation MUST reference annotation identifiers, not arbitrary text spans.

## 5. FEATURE

Minimum payload:

```json
{"feature": "...", "value": "..."}
```

The feature name and value require an additional controlled vocabulary before they can support substantive analysis.

## 6. Exclusions

Version 0.1 intentionally excludes substantive categories such as:

- theological concepts;
- mystical interpretations;
- historical attribution;
- author identity;
- semantic topics;
- claims about influence or causality.

No such category may be introduced into the pilot without a versioned vocabulary change and corresponding annotation guidelines.

## 7. Versioning

Changes to type meaning or required payload shape require a new vocabulary version. Existing annotations MUST retain the vocabulary version under which they were created.

## 8. Validation status

This document is a specification. It becomes `VALIDATED` only after fixtures and annotation guidelines demonstrate that independent coders can apply the types consistently under a defined pilot protocol.
