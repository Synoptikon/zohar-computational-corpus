# Validation gates

The project uses gates to prevent progression from implementation to scientific conclusion without evidence.

| Gate | Requirement | Initial status |
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
