# Zohar Computational Corpus

Reproducible and auditable computational research framework for the Zohar corpus.

## Mission

Develop computational infrastructure for studying complex historical texts while separating observable data, annotations, implementation rules, models, experiments, results, and interpretations.

The project does not assume that a mathematical, cryptographic, linguistic, semantic, or metaphysical structure exists in the corpus. Its purpose is to determine which claims can be operationalized, measured, reproduced, and validated.

## Method

```text
CORPUS
  → NORMALIZACIÓN
  → SEGMENTACIÓN
  → CODIFICACIÓN
  → REPRESENTACIÓN
  → MODELO
  → MÉTRICAS
  → EXPERIMENTO
  → VALIDACIÓN
  → RESULTADO
  → CONCLUSIÓN
```

## Repository status

The repository is currently establishing the reproducibility foundation. The Zohar corpus itself is **NOT VERIFIED** in this repository yet, and no scientific finding should be inferred from the current code.

## Principles

- Preserve RAW data separately from transformed data.
- Record provenance, versions, hashes, and transformations when available.
- Treat LLM output as annotation candidates, not ground truth.
- Separate exploration from confirmation.
- Compare observations against appropriate baselines and null models.
- Never treat implementation as validation.
- Prefer falsifiable claims and auditable evidence.

## Validation

See [`docs/validation_gates.md`](docs/validation_gates.md) for the project gates and [`docs/methodology.md`](docs/methodology.md) for the methodological pipeline.
