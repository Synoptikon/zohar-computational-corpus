# EXP-GATE004-LLM-CANDIDATE-0.1

## 1. Experiment identity

- EXP-ID: `EXP-GATE004-LLM-CANDIDATE-0.1`
- Status: `PLANNED`
- Parent gate: `GATE-004`
- Protocol: `ANNOTATION-PILOT-0.1`
- Schema: `ANNOTATION-SCHEMA-0.1`
- Vocabulary: `ANNOTATION-VOCABULARY-0.1`
- Guidelines: `ANNOTATION-GUIDELINES-0.1`
- Frozen CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- Frozen pilot size: `30`
- Frozen `selected_sid_sha256`: `715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d`
- Source pilot run: `34839232374`
- Source artifact: `gate004-annotation-package`

## 2. Purpose

This experiment formally separates the existing B output from the independent-human-annotator agreement experiment. B is designated as an LLM-assisted candidate-generation condition, not as an independent human annotator and not as ground truth.

The experiment evaluates whether the current annotation vocabulary and guidelines can be operationalized by an LLM as candidate generation, and whether those candidates can subsequently be reviewed by a human under the frozen protocol.

This experiment does not provide evidence of inter-annotator agreement and must not be merged with the human A/B agreement result.

## 3. Hypothesis

**HID:** `HID-GATE004-LLM-CANDIDATE-0.1`

**Description:** Given the frozen 30-SID pilot and the current annotation vocabulary/guidelines, an LLM can generate structurally valid annotation candidates that remain traceable to the source SID and preserve the annotation schema/provenance requirements.

**Prediction:** Candidate records will pass structural validation while remaining explicitly marked `source=llm` and `validation_status=CANDIDATE`.

**Variables:**

- `X`: frozen SID text input.
- `Y`: generated annotation candidate records.
- `V`: structural validation result.
- `C`: candidate provenance status.
- `H`: subsequent human review outcome.

**Data required:** the frozen 30 SID package, schema, vocabulary, guidelines, LLM model/version, prompt/context, raw outputs, normalized candidate JSON, and human review records.

**Model:** deterministic/reproducible candidate-generation procedure using a declared LLM configuration.

**Metric:** structural validity rate = valid candidate records / candidate records submitted to validation.

**Baseline:** zero automatic promotion to `ACCEPTED`; all LLM output starts as `source=llm`, `validation_status=CANDIDATE`.

**Falsification criterion:** the hypothesis is not supported if reproducible candidate generation cannot produce structurally valid records under the frozen schema, or if provenance/status cannot be preserved.

## 4. Model specification

- MID: `MID-GATE004-LLM-CANDIDATE-0.1`
- Objective: candidate generation only.
- Inputs: frozen SID text and frozen annotation specification.
- Transformation: LLM-assisted extraction constrained to `ENTITY`, `RELATION`, and `FEATURE`.
- Output: schema-valid candidate annotation records plus provenance.
- Assumptions: source text is unchanged; vocabulary and guidelines are frozen; LLM output is not ground truth.
- Parameters: model identifier/version, prompt, context, temperature and other generation parameters must be recorded for any confirmation run.
- Controls: abstention, schema validation, EID uniqueness, SID membership, provenance/status checks.
- Limitation: candidate generation does not establish agreement, semantic equivalence, historical validity, or theological validity.

## 5. Current B artifact classification

The existing `annotator_b.json` is reclassified for this experiment as:

- role: `LLM_CANDIDATE_GENERATOR`
- source: `llm`
- validation status: `CANDIDATE`
- independence class: `NOT_INDEPENDENT_HUMAN_ANNOTATOR`

The existing B artifact must not be used as the second human annotation in `GATE-004` agreement calculations.

## 6. Human review

A later human-review stage may transform individual candidates from `CANDIDATE` to a reviewed status only after explicit human inspection. Human review must preserve provenance and record the reviewer. A reviewed LLM candidate remains distinguishable from an independently originated human annotation.

## 7. Separation from GATE-004 agreement

The original pilot protocol requires at least two independent annotators to code the same frozen set without seeing each other's decisions. LLM output is explicitly excluded from serving as an independent human annotation unless a separate experiment specifies that comparison.

Therefore:

`human A vs human B` -> GATE-004 agreement evidence

`human A vs LLM candidate B` -> this experiment only; not human inter-annotator agreement

## 8. Required evidence for completion

A future execution must archive:

1. exact model identifier/version;
2. prompt and system/developer context used for candidate generation;
3. generation parameters;
4. frozen input package identity and hash;
5. raw LLM output;
6. normalized `annotator_b.json` candidate output;
7. structural validation report;
8. candidate-level provenance;
9. human review results, if performed;
10. reproducible run identifier.

## 9. Status

`PLANNED`

This document formalizes the separation. It does not retroactively convert the existing B candidates into validated evidence and does not advance `GATE-004` to `VALIDATED`.
