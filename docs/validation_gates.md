# Validation gates

The project uses gates to prevent progression from implementation to scientific conclusion without evidence.

| Gate | Requirement | Current status |
|---|---|---|
| GATE-001 | Corpus válido | BLOCKED |
| GATE-002 | Segmentación reproducible | BLOCKED |
| GATE-003 | Esquema de anotación definido | BLOCKED |
| GATE-004 | Codificación validada | BLOCKED |
| GATE-005 | Modelo reproducible | BLOCKED |
| GATE-006 | Métricas calculables | BLOCKED |
| GATE-007 | Baseline establecido | BLOCKED |
| GATE-008 | Experimento ejecutable | BLOCKED |
| GATE-009 | Resultado reproducible | BLOCKED |
| GATE-010 | Conclusión auditable | BLOCKED |

## Rule

`IMPLEMENTED` does not mean `VALIDATED`.

A gate can advance only when its evidence is recorded in the repository or in a referenced reproducibility artifact. Missing evidence is reported as `BLOCKED`, `INCONCLUSIVE`, or `UNVERIFIED`, never inferred as success.

## Current evidence

`GATE-001` has a source registry and licensing/provenance policy, but no accepted RAW corpus snapshot. The gate therefore remains `BLOCKED`.

See `docs/gates/GATE-001-corpus-valid.md` for the evidence record and remaining acceptance criteria.

## Normalized offset validation

The normalized corpus has an independently validated offset-audit result:

- audit version: `NORMALIZED-OFFSETS-AUDIT-0.2`
- files audited: `1,721`
- records audited: `7,850`
- failed files: `0`
- errors: `0`
- warnings: `0`
- status: `PASS`

This evidence validates the normalized offset contract only. It does **not** constitute validation of `GATE-002`, because `GATE-002` requires a reproducible segmentation implementation and its associated tests and audit evidence.

The audit artifact is expected at `data/analysis/normalized_offsets_audit.json` in a reproducible working tree.

## GATE-002 acceptance evidence

`GATE-002` remains `BLOCKED` until all of the following are present and validated:

1. segmentation rules versioned in the repository;
2. a stable `SID` output contract;
3. a deterministic segmentation implementation;
4. tests covering the contract and failure conditions;
5. a reproducible segmentation run over the intended input;
6. an audit demonstrating traceability, ordering, uniqueness, and permitted offset behavior;
7. the resulting evidence recorded in the repository or a referenced reproducibility artifact.
