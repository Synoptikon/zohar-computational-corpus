# EXP-GATE004-LLM-CANDIDATE-0.1 — Execution 001

- EXP-ID: `EXP-GATE004-LLM-CANDIDATE-0.1`
- Execution ID: `EXP-GATE004-LLM-CANDIDATE-0.1-E001`
- Date: `2026-09-14`
- Status: `INCONCLUSIVE`
- Parent gate: `GATE-004`
- Frozen pilot run: `34839232374`
- Frozen artifact: `gate004-annotation-package`
- Artifact ID: `10345512559`
- Artifact digest: `sha256:a39f6bb3e7a7dce3c509ff84963c1e1c11c8b2cb16a1989caa9b12230c4c0ab8`
- CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- sample_size: `30`
- selected_sid_sha256: `715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d`

## Model

- model identifier: `GPT-5.6 Luna`
- model version/date recorded by output provenance: `2026-09-14`
- role: `LLM_CANDIDATE_GENERATOR`

## Prompt

System/project constraint: operate under `ANNOTATION-SCHEMA-0.1`, `ANNOTATION-VOCABULARY-0.1`, and `ANNOTATION-GUIDELINES-0.1`. Treat the frozen 30-SID package as immutable input. For each SID, identify only explicit, text-supported candidates permitted by the vocabulary (`ENTITY`, `RELATION`, `FEATURE`). If evidence is insufficient or requires unsupported inference, abstain. Emit candidate records only; do not promote any record to `ACCEPTED`. Preserve SID provenance and mark every generated record `source=llm`, `validation_status=CANDIDATE`.

## Input

Frozen source package identified by the artifact digest above. Input identity is the 30-SID set with the recorded `selected_sid_sha256`.

## Generation parameters

- temperature: `NOT_EXPOSED_BY_CHATGPT_RUNTIME`
- top_p: `NOT_EXPOSED_BY_CHATGPT_RUNTIME`
- max_tokens: `NOT_EXPOSED_BY_CHATGPT_RUNTIME`
- seed: `NOT_AVAILABLE`
- other sampling parameters: `NOT_EXPOSED`

## Output

Normalized candidate output: `data/analysis/annotation_pilot_annotations/annotator_b.json`

Output blob SHA: `c3f2b3b89acfcf010a82d5fd2fddc347e4196aa5`

Observed result:
- 30 SID records processed
- 28 abstentions
- 2 non-abstaining SID records
- 5 candidate `ENTITY` records
- 0 `RELATION`
- 0 `FEATURE`
- all generated records use `source=llm`
- all generated records use `validation_status=CANDIDATE`

## Validation

Structural validation checks:
- schema version: PASS
- SID membership: PASS
- selected SID set: PASS
- EID uniqueness: PASS
- provenance/status constraints: PASS
- automatic promotion to ACCEPTED: NONE

Structural validity rate: `1.0` for submitted candidate records (5/5).

## Interpretation

The structural prediction is supported for this execution: candidate records were produced and preserved as LLM candidates under the frozen schema. This is not evidence of semantic correctness, human agreement, historical validity, or theological validity.

## Reproducibility limitation

This execution is not fully reproducible at the sampling level because the ChatGPT runtime does not expose all generation parameters (temperature, top_p, seed, token limits). Therefore the execution remains `INCONCLUSIVE` for the stronger reproducibility criterion. A future API-backed confirmation run must record the complete generation configuration.

## Separation rule

This execution MUST NOT be included in human inter-annotator agreement. The existing B artifact remains an LLM candidate condition. GATE-004 requires a separate independent human B annotation.
