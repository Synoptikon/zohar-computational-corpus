# Annotation Guidelines v0.1

**Contract:** `ANNOTATION-GUIDELINES-0.1`
**Vocabulary:** `ANNOTATION-VOCABULARY-0.1`
**Status:** SPECIFICATION

## 1. Scope

These guidelines define the first coding pilot for the three structural annotation types `ENTITY`, `RELATION`, and `FEATURE`.

The pilot is intentionally conservative. Annotators must record only what is operationally supported by the supplied segment and the current vocabulary. Interpretation, historical attribution, and inferred meaning are out of scope.

## 2. General decision procedure

For each candidate annotation:

1. Identify the target `SID`.
2. Determine whether the observation is directly supported by the supplied segment or by another explicitly permitted annotation record.
3. Select exactly one structural `annotation_type`.
4. Populate only the fields required by that type.
5. Record provenance in the schema fields.
6. Use `CANDIDATE` when the annotation has not completed independent review.
7. If the evidence is insufficient, do not create the annotation.

## 3. ENTITY

Use `ENTITY` only when the segment contains a candidate entity mention that can be delimited or identified from the supplied text under the pilot protocol.

Do not infer identity, authorship, historical existence, theological status, or canonical equivalence.

Minimum payload:

```json
{"label": "..."}
```

If two mentions could refer to the same entity but that identity is not explicitly established by the protocol, annotate them separately.

## 4. RELATION

Use `RELATION` only when a relation is explicitly represented by the annotation protocol and both endpoint `EID`s already exist.

Do not infer causal, historical, theological, or semantic relations merely because two entities co-occur.

Minimum payload:

```json
{"relation_type": "...", "source_eid": "EID-...", "target_eid": "EID-..."}
```

## 5. FEATURE

Use `FEATURE` only for an observable property for which the feature name and value have been defined in a versioned sub-vocabulary.

Do not use `FEATURE` as a free-form field for interpretation.

Minimum payload:

```json
{"feature": "...", "value": "..."}
```

## 6. Abstention

Annotators MUST abstain when:

- the evidence is ambiguous under the current guidelines;
- the required vocabulary is not defined;
- the proposed annotation requires historical or theological inference;
- the target cannot be traced to a stable `SID`;
- a relation endpoint cannot be traced to an existing `EID`.

Abstention is a valid outcome and is not treated as missing work.

## 7. Independence

For the validation pilot, independent annotators must work from the same frozen segment set and versioned guidelines without seeing each other's decisions before agreement is measured.

## 8. LLM annotations

LLM output is an annotation candidate only. It MUST be stored with `source=llm` and `validation_status=CANDIDATE` and must undergo the same review process before acceptance.

## 9. Change control

Any change to a definition, inclusion criterion, exclusion criterion, or required payload shape requires a new guidelines version. Changes made after observing pilot results must be recorded rather than silently replacing this version.

## 10. Validation target

These guidelines are `SPECIFICATION` until a pilot demonstrates that independent coders can apply them consistently and that disagreements can be classified as guideline ambiguity, evidence ambiguity, or annotation error.
