# GATE-004 — Independent Human B Annotation

This branch is reserved exclusively for the second independent human annotation.

- Frozen CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- Frozen pilot size: `30`
- Frozen `selected_sid_sha256`: `715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d`
- Source pilot run: `34839232374`
- Source artifact: `gate004-annotation-package`

## Independence rule

The human annotator must not inspect or reuse the LLM candidate decisions from `EXP-GATE004-LLM-CANDIDATE-0.1` before completing the independent annotation.

The resulting `annotator_b.json` must be generated from the frozen package, schema, vocabulary and guidelines only, and must preserve human provenance.

This branch is not evidence of annotation completion until `annotator_b.json` is supplied and structurally validated.
