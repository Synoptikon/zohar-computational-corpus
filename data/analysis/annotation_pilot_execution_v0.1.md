# Annotation Pilot Execution v0.1

**Contract:** `ANNOTATION-PILOT-EXECUTION-0.1`
**Upstream:** `ANNOTATION-PILOT-0.1`
**Schema:** `ANNOTATION-SCHEMA-0.1`
**Vocabulary:** `ANNOTATION-VOCABULARY-0.1`
**Guidelines:** `ANNOTATION-GUIDELINES-0.1`
**Status:** PROCEDURE

## Objective

Create two independent annotation shells from one frozen pilot artifact without exposing either annotator's decisions to the other before agreement is measured.

## Procedure

1. Execute the deterministic pilot selector against the validated segmented corpus.
2. Preserve `annotation_pilot.json` as the frozen pilot artifact.
3. Verify `population_sid_sha256` and `selected_sid_sha256`.
4. Initialize exactly two shells: `annotator_a.json` and `annotator_b.json`.
5. Verify both shells contain the same SID set and the same pilot provenance metadata.
6. Annotators work independently and do not modify pilot metadata.
7. Each annotation begins with the schema's required provenance fields and remains `CANDIDATE` until independently reviewed.
8. Abstention is represented explicitly where the guidelines require it.
9. Only after both annotation files are complete may agreement be calculated.

## Non-goals

This procedure does not establish semantic truth, historical identity, theological interpretation, or corpus-wide annotation quality.

## Integrity requirements

The following fields must be identical between annotator shells:

- `pilot_version`
- `selector_version`
- `selection_method`
- `vocabulary_version`
- `guidelines_version`
- `cid`
- `population_size`
- `sample_size`
- `population_sid_sha256`
- `selected_sid_sha256`
- ordered `SID` set

Only annotation content, abstention decisions, and annotator-specific notes may differ.

## Gate relation

Successful execution of this procedure is evidence for the implementation portion of `GATE-004`. It does not close the gate. Closure additionally requires independent annotations, structural validation, agreement analysis, disagreement classification, and a documented conclusion.
