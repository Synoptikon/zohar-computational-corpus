# GATE-004 Human Annotator Recruitment v0.1

**ID:** `GATE-004-RECRUITMENT-0.1`
**Status:** PLANNED / BLOCKED
**Purpose:** obtain a second independent human annotator without contaminating the frozen 30-SID pilot.

## 1. Role

One independent human annotator is required in addition to the project annotator. The person will annotate the same frozen 30-SID pilot using `ANNOTATION-GUIDELINES-0.1` and `ANNOTATION-VOCABULARY-0.1`.

## 2. Minimum competence

- Advanced reading competence in Hebrew.
- Ability to follow explicit annotation rules without adding interpretation.
- Ability to edit/return JSON or use an equivalent structured annotation interface.
- Ability to work independently and preserve stable `SID` identifiers.

## 3. Preferred competence

- Hebrew and Aramaic.
- Linguistics, philology, Jewish studies, Semitic languages, corpus annotation, NLP or related training.
- Experience with textual annotation or data labeling.

Zohar specialization is preferred but is not mandatory when the annotation task is fully operationalized.

## 4. Independence requirements

The selected annotator MUST NOT see the first annotator's decisions before freezing their own annotation. They MUST NOT receive LLM candidate decisions as ground truth. The recruitment/screening process MUST NOT expose the official 30-SID decisions before the real annotation begins.

## 5. Screening

Candidate screening must record:

- Hebrew proficiency;
- Aramaic proficiency;
- relevant academic/training background;
- prior annotation/corpus/NLP experience;
- availability;
- proposed compensation;
- acceptance of the independence protocol.

## 6. Pilot qualification

Before the official 30-SID pilot, candidates should complete a small qualification task using segments outside the frozen GATE-004 sample. Qualification decisions MUST NOT alter the official sample.

Qualification is an operational recruitment test, not evidence for inter-annotator agreement.

## 7. Delivery

After selection, deliver only the B package and the applicable guidelines/vocabulary. Do not deliver A's annotations, agreement results, LLM candidates, hypotheses, or downstream analyses.

## 8. Acceptance record

The project must record the selected annotator as an independent human participant, the date of assignment, package version/hash, guideline version, vocabulary version, and completion date. Personal data should be minimized.

## 9. Post-annotation sequence

`B COMPLETE → STRUCTURAL VALIDATION → HASH/FREEZE → PAIR VALIDATION → AGREEMENT → DISAGREEMENT CLASSIFICATION → AUDIT → GATE-004 DECISION`

## 10. Failure conditions

Recruitment is invalid if the candidate has seen the other annotator's decisions, if the official sample was changed, if LLM output was used as independent ground truth, or if the package cannot be traced to the frozen pilot.

## 11. Current blocker

`BLOCKED: SECOND HUMAN ANNOTATOR NOT YET RECRUITED.`

No agreement metric or GATE-004 closure may be inferred from the absence of annotations.
