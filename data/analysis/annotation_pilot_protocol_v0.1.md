# Annotation Pilot Protocol v0.1

**Contract:** `ANNOTATION-PILOT-0.1`
**Vocabulary:** `ANNOTATION-VOCABULARY-0.1`
**Guidelines:** `ANNOTATION-GUIDELINES-0.1`
**Status:** SPECIFICATION

## 1. Objective

Evaluate whether independent coders can apply the current annotation vocabulary and guidelines consistently to the same frozen set of SID records.

The pilot is a validation experiment. It does not establish semantic, historical, theological, or causal claims about the Zohar.

## 2. Population

The population is the complete output of `SID-CONTRACT-0.1` generated from the validated normalized corpus.

The population is identified by stable `SID` values. The pilot must not depend on filesystem traversal order, manual selection, or annotator preference.

## 3. Deterministic selection

The pilot selector ranks every available `SID` by the hexadecimal SHA-256 digest of its UTF-8 representation, ascending, with the SID itself as a deterministic tie-breaker.

Selection method identifier:

`SHA256_SID_ASCENDING`

Default pilot size:

`30` segments.

The selected set is frozen by recording the complete selected SID list and each selection hash in the pilot artifact.

A different sample size is a different experiment configuration and must be recorded explicitly.

## 4. Inputs

Required:

- segmented SID JSON files;
- authoritative CID embedded in the SID records;
- `ANNOTATION-VOCABULARY-0.1`;
- `ANNOTATION-GUIDELINES-0.1`.

The pilot must fail on duplicate SID values or insufficient population size.

## 5. Independent annotation

At least two independent annotators should code the same frozen pilot set without seeing each other's decisions before agreement is calculated.

Each annotator records provenance through the annotation schema. Abstention is a valid outcome and must not be silently converted into an annotation.

LLM-generated output is treated as `source=llm` and `validation_status=CANDIDATE`; it is not a substitute for an independent human annotation unless a separate experiment explicitly specifies that comparison.

## 6. Freeze rule

The selected SID set, vocabulary version, guideline version, selector version, and pilot sample size must be fixed before comparison of annotator decisions.

Changes made after observing disagreements must be recorded as a new version or protocol revision. The original pilot remains immutable evidence.

## 7. Agreement analysis

Agreement must be computed only after the independent annotation records are frozen.

At minimum, report:

- number of pilot SIDs;
- number of annotations per annotator;
- abstentions per annotator;
- exact agreement counts where applicable;
- disagreement counts;
- disagreement classification: guideline ambiguity, evidence ambiguity, or annotation error.

A chance-corrected agreement metric may be added only when its assumptions and unit of analysis are explicitly defined.

No threshold is declared in v0.1 for substantive acceptance. The first pilot is intended to expose ambiguity in the protocol before a quantitative acceptance threshold is frozen.

## 8. Gate criterion

`GATE-004` cannot be marked `VALIDATED` merely because the selector runs or because annotations validate structurally.

Validation requires:

1. frozen pilot selection;
2. independent annotations;
3. reproducible annotation artifacts;
4. agreement calculation;
5. disagreement classification;
6. documented protocol changes, if any;
7. rerun of structural validation on the pilot annotations.

Until these conditions are met, the gate remains `IN_PROGRESS`.
