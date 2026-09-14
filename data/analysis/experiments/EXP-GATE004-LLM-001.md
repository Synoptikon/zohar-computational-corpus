# EXP-GATE004-LLM-001

## Estado
REGISTERED — NOT CONFIRMATORY

## Propósito
Registrar formalmente la salida de `annotator_b.json` como un experimento separado de anotación asistida por LLM y no como una segunda anotación humana independiente.

## Relación con GATE-004
- Gate: GATE-004
- Pilot run: `34839232374`
- Artifact: `gate004-annotation-package`
- Artifact ID: `10345512559`
- CID: `CID-ZOHAR-WIKISOURCE-MANTUA`
- sample_size: `30`
- selected_sid_sha256: `715dc83c2336857c4a3fe07844033305f4a7ee6f86a2fea4e47d5c236d0bd05d`
- A/B package metadata remains frozen.

## Rol de B
`B` deja de interpretarse como `independent human annotator`.

La salida se clasifica como `LLM ANNOTATION CANDIDATE`.

Esto impide utilizar A-vs-B como evidencia de inter-annotator agreement humano.

## Provenance
- source: `llm`
- validation_status: `CANDIDATE`
- annotation schema: `ANNOTATION-SCHEMA-0.1`
- model: `GPT-5.6 Luna`
- model version/date: `2026-09-14`

## Datos producidos
`annotator_b.json` contiene candidatos de anotación sobre el mismo conjunto congelado de 30 SID. La salida requiere validación humana antes de cualquier estado `ACCEPTED`.

## Hipótesis experimental
**HID: HID-GATE004-LLM-001**

Evaluar si un LLM puede producir anotaciones estructurales compatibles con el esquema y vocabulario v0.1 sobre el conjunto piloto congelado.

### Predicción
La salida podrá pasar validación estructural del esquema cuando las decisiones se limiten al vocabulario permitido y las abstenciones se utilicen ante evidencia insuficiente.

### Variables
- `schema_valid`: booleano; validación estructural del JSON.
- `candidate_count`: número de anotaciones con `validation_status=CANDIDATE`.
- `abstention_count`: número de SID sin anotaciones candidatas.
- `vocabulary_compliance`: booleano; uso exclusivo de tipos permitidos.

### Baseline
No establecido todavía. Este experimento es descriptivo/validatorio y no demuestra superioridad sobre un baseline humano.

### Criterio de falsación
El experimento no puede considerarse apoyado si la salida no cumple el contrato estructural o utiliza categorías fuera del vocabulario aprobado.

## Qué NO demuestra
- No demuestra inter-annotator agreement humano.
- No demuestra equivalencia entre LLM y anotador humano.
- No demuestra validez histórica, teológica o semántica de las entidades.
- No demuestra causalidad.
- No permite convertir automáticamente candidatos LLM en ground truth.

## Estado científico
`EN_EVALUACIÓN`

## Bloqueos
1. El prompt completo y su configuración de inferencia deben registrarse para reproducibilidad completa si se pretende repetir el experimento.
2. La validación humana de los candidatos sigue pendiente.
3. No ejecutar `agreement` A-vs-B como agreement humano.

## Siguiente acción
Ejecutar validación específica del experimento LLM:

`annotator_b.json → schema validation → vocabulary validation → provenance audit → human review → resultado EXP-GATE004-LLM-001`
