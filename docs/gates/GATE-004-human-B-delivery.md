# GATE-004 — Human B Delivery Control

This commit intentionally triggers `gate004-pilot-evidence` to regenerate the frozen annotation package from the verified pilot baseline.

Human B must receive only the generated `gate004-annotation-package` artifact and the frozen schema/vocabulary/guidelines. LLM candidate outputs from `EXP-GATE004-LLM-CANDIDATE-0.1` are excluded from the Human B workspace.

Frozen controls:
- CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- sample_size: `30`
- selected_sid_sha256: `715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d`
- schema: `ANNOTATION-SCHEMA-0.1`
- vocabulary: `ANNOTATION-VOCABULARY-0.1`
- guidelines: `ANNOTATION-GUIDELINES-0.1`

This file does not contain or expose any LLM candidate annotation.
