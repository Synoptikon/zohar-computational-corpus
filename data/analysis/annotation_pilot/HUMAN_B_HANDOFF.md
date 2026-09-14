# GATE-004 — Human B Independent Annotation Handoff

## Purpose
This workspace is for the independent human B annotation required for GATE-004.

## Frozen package
- CID: CID-ZOHAR-WIKISOURCE-MANTUA
- sample_size: 30
- selected_sid_sha256: 715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d
- annotation schema: ANNOTATION-SCHEMA-0.1
- vocabulary: ANNOTATION-VOCABULARY-0.1
- guidelines: ANNOTATION-GUIDELINES-0.1

## Independence rule
Do not inspect, copy, compare against, or derive decisions from any LLM candidate output or Human A annotations before submitting the completed Human B annotation.

## Required input
Use only the frozen 30-SID package plus the schema, vocabulary, and guidelines.

## Required output
Create/update `annotator_b.json` with Human B decisions only. Preserve all frozen pilot metadata. Use human provenance and the controlled validation states defined by the schema. Abstention is permitted where evidence is insufficient.

## Completion gate
Do not run pair validation or agreement until the completed Human B file is committed. GitHub Actions will then perform structural validation and the downstream comparison chain.

## Status
BLOCKED_PENDING_HUMAN_B
