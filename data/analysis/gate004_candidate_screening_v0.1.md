# GATE-004 Candidate Screening v0.1

**ID:** `GATE-004-SCREENING-0.1`
**Purpose:** operational intake and qualification record for selecting one independent human annotator B.
**Status:** IN_PROGRESS

## Candidate intake

Record only the minimum non-sensitive information required for selection:

- Candidate ID: `CAND-B-XXX`
- Hebrew reading level: `SELF-REPORTED`
- Aramaic reading level: `SELF-REPORTED`
- Relevant training/background: `SELF-REPORTED`
- Corpus / annotation / NLP experience: `SELF-REPORTED`
- Availability: `SELF-REPORTED`
- Proposed pilot compensation: `SELF-REPORTED`
- Independence protocol accepted: `YES/NO`
- LLM-candidate exclusion accepted: `YES/NO`

Do not store names, email addresses, telephone numbers, identity documents, addresses, or other unnecessary personal data in the repository.

## Screening gate

A candidate proceeds only if:

1. Advanced Hebrew reading competence is demonstrated or credibly documented.
2. The candidate can follow explicit annotation rules without adding interpretation.
3. The candidate can work with structured data or an equivalent annotation interface.
4. The candidate accepts the independence protocol.
5. The candidate accepts that LLM output is not ground truth.

## Qualification task

Before the official 30-SID pilot, provide a small qualification set composed exclusively of SIDs outside the frozen GATE-004 sample.

Qualification is recruitment evidence only. It must not be included in the official agreement calculation.

Record:

- qualification sample identifier/hash;
- qualification guideline/vocabulary versions;
- completion date;
- structural validity;
- rule-following assessment;
- qualification decision: `PASS`, `FAIL`, or `INCONCLUSIVE`.

Do not expose annotator A decisions or official GATE-004 results during qualification.

## Selection record

Selected candidate becomes:

- `annotator_b = HUMAN_INDEPENDENT`
- assignment date;
- assigned package version/hash;
- guidelines version;
- vocabulary version;
- completion date after annotation.

## Invalidity conditions

Recruitment/qualification is invalid if:

- the candidate saw A's decisions before freezing B;
- the candidate received LLM candidates as ground truth;
- the official 30-SID sample was changed;
- qualification used any official pilot SID;
- the final B package cannot be traced to the frozen pilot.

## Next sequence

`SCREENING → QUALIFICATION → SELECTION → B PACKAGE DELIVERY → B COMPLETE → STRUCTURAL VALIDATION → HASH/FREEZE → PAIR VALIDATION → AGREEMENT → AUDIT → GATE-004`
