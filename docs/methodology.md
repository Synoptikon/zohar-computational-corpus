# Methodological pipeline

The project keeps the following layers separate:

`CORPUS → NORMALIZACIÓN → SEGMENTACIÓN → CODIFICACIÓN → REPRESENTACIÓN → MODELO → MÉTRICAS → EXPERIMENTO → VALIDACIÓN → RESULTADO → CONCLUSIÓN`

## Evidence classes

- **DATO:** material directly present in the corpus or generated deterministically from it.
- **ANOTACIÓN:** label or interpretation attached to data by an explicit procedure.
- **REGLA:** implementation rule used to transform or classify data.
- **HIPÓTESIS:** falsifiable proposition specified before confirmatory testing.
- **MODELO:** computational transformation or statistical model with documented assumptions.
- **RESULTADO:** output produced by an executed experiment.
- **INTERPRETACIÓN:** explanation proposed for a result.
- **CONCLUSIÓN:** claim that survives the defined validation criteria.

Exploratory findings must not be silently promoted to confirmatory evidence.

## Reproducibility

Raw corpus material must remain immutable. Transformations should produce distinct artifacts and record their configuration and provenance. Hashes should be recorded whenever source material is available.
