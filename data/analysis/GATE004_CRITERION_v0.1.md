# GATE-004 — Acceptance Criterion v0.1

**Gate:** `GATE-004`
**Contract:** `ANNOTATION-PILOT-0.1`
**Guidelines:** `ANNOTATION-GUIDELINES-0.1`
**Vocabulary:** `ANNOTATION-VOCABULARY-0.1`
**Agreement:** `ANNOTATION-AGREEMENT-0.1`
**Status:** `FORMALIZED / THRESHOLD_PENDING`

## 1. Objective

Define the decision protocol for GATE-004 before the independent A/B annotations are observed, without introducing a post-hoc acceptance threshold.

The gate asks whether independent annotators can apply the current structural annotation vocabulary and guidelines consistently to the same frozen 30-SID pilot.

## 2. Primary unit

The unit of comparison is `SID`.

For each SID, agreement is exact equality of the canonical annotation sets defined by `ANNOTATION-AGREEMENT-0.1`.

## 3. Primary metric

`agreement_rate = agreements / total_SID`

Range: `[0,1]`.

Interpretation: proportion of frozen SIDs for which the two annotation outputs are structurally identical under the canonical comparison rule.

This metric does not establish semantic validity, historical validity, causal interpretation, or correctness of the annotation vocabulary.

## 4. Preconditions

GATE-004 evaluation is permitted only if all of the following hold:

1. the pilot selection is frozen;
2. A and B contain the same 30 frozen SIDs;
3. both annotation documents are structurally valid;
4. annotator identities are distinct and correctly recorded;
5. no document remains `UNANNOTATED`;
6. the pair-integrity validator passes;
7. the agreement calculation is reproducible;
8. disagreements are classified and preserved;
9. any guideline/vocabulary changes are versioned rather than silently replacing v0.1;
10. final structural validation passes.

These preconditions derive from `docs/gates/GATE-004-annotation-pilot.md` and the existing annotation-agreement contract.

## 5. Acceptance threshold

**NO NUMERIC THRESHOLD IS CURRENTLY SPECIFIED IN THE VERIFIED PROJECT MATERIALS.**

Therefore this version deliberately does **not** invent a value for `theta`.

Let `theta` denote the acceptance threshold to be specified by the project protocol before A/B results are inspected.

Until `theta` is explicitly versioned and frozen:

`acceptance_decision = NOT_EVALUATED`

A measured agreement rate MUST NOT be converted into PASS/FAIL using an unstated or retrospectively selected threshold.

## 6. Decision rule after threshold registration

Once a threshold has been formally registered before inspecting the A/B result:

- if all preconditions pass and `agreement_rate >= theta`, the gate becomes `CANDIDATE_FOR_REVIEW`;
- if all preconditions pass and `agreement_rate < theta`, the gate becomes `NOT_SUPPORTED_BY_PILOT`;
- if any precondition fails, the gate remains `BLOCKED`;
- final `VALIDATED` status requires the complete evidence package and final structural validation described in the gate specification.

This rule separates the quantitative result from the final methodological gate decision.

## 7. Secondary evidence

The following are retained as diagnostics, not substitutes for the primary criterion:

- abstention agreement;
- disagreement count;
- disagreement classes (`TYPE_MISMATCH`, `VALUE_MISMATCH`, `VALIDATION_STATUS_MISMATCH`, `ABSTAIN_MISMATCH`);
- per-SID canonical signatures;
- guideline/vocabulary ambiguity identified during adjudication.

No secondary metric may be promoted to the primary acceptance criterion without a new versioned protocol.

## 8. Post-hoc change control

If the project changes `theta`, the primary metric, treatment of abstentions, or the decision rule after A/B results become visible, the change MUST be recorded as a new criterion version and the original result must remain preserved.

A retrospective change MUST NOT be presented as the original pre-registered criterion.

## 9. Current audit finding

`ANNOTATION-AGREEMENT-0.1` is implemented and explicitly states that it does not provide a threshold. `GATE-004-annotation-pilot.md` specifies the evidence required for validation but does not specify a numeric acceptance threshold.

Therefore the scientifically auditable state is:

`criterion = FORMALIZED`
`threshold = PENDING`
`acceptance_decision = NOT_EVALUATED`
`gate_004 = BLOCKED`

## 10. What this criterion does not demonstrate

Even if the gate is later validated, the result would not demonstrate that the Zohar has a particular semantic, theological, historical, mathematical, cryptographic, or metaphysical structure. It would establish only the specified level of annotation consistency for this pilot under the frozen protocol.
