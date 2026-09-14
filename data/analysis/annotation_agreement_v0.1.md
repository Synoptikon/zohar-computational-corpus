# Annotation agreement v0.1

## Objetivo

Comparar dos anotaciones independientes sobre el mismo piloto congelado sin confundir acuerdo estructural con validez semántica.

## Unidad

La unidad de comparación es `SID`.

Para cada `SID`, la decisión se representa como el conjunto de firmas:

`(annotation_type, canonical(value), validation_status)`

El `EID` no participa en la comparación porque puede ser distinto entre anotadores aunque la decisión sobre el segmento sea equivalente.

## Requisitos previos

1. Ambos documentos deben proceder del mismo piloto congelado.
2. Los metadatos del piloto deben coincidir.
3. Los conjuntos de `SID` deben coincidir exactamente.
4. Ningún documento puede conservar `status: UNANNOTATED`.
5. La abstención se representa como una decisión explícita y no puede coexistir con anotaciones en el mismo segmento.

## Métrica

`agreement_rate = agreements / total_SID`

Un acuerdo significa igualdad exacta de los conjuntos de firmas canónicas para un `SID`.

## Interpretación

- `1.0`: acuerdo exacto en todos los SID comparados.
- `0.0`: desacuerdo en todos los SID comparados.
- valores intermedios: proporción de SID con decisiones idénticas.

La métrica no demuestra calidad semántica, validez histórica ni corrección de las categorías.

## Limitaciones

Esta versión mide acuerdo exacto por SID. No calcula todavía Cohen's kappa, Krippendorff's alpha ni acuerdo parcial. Esas métricas requieren una definición previa de la unidad estadística y de cómo tratar multilabel, abstenciones y categorías ordinales.

## Estado

`ANNOTATION-AGREEMENT-0.1` — IMPLEMENTED, PENDING REAL PILOT DATA.
