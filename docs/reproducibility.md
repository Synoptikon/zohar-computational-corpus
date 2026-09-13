# Reproducibility protocol

Every corpus acquisition must be reproducible from a declared source, version, retrieval method, configuration, and timestamp.

## Acquisition record

An acquisition record must contain:

- CID
- source and canonical URL
- edition/version
- API endpoint if applicable
- request parameters
- retrieval timestamp (UTC)
- response/storage format
- exact stored artifact path
- SHA-256 of the artifact
- license and license evidence
- software version used for acquisition

## Deterministic storage

The exact acquired bytes become the RAW artifact. Normalization and segmentation operate on copies and must never overwrite RAW.

## Re-acquisition

A later acquisition is a separate event. If the bytes differ, it receives a new hash and must not silently replace the earlier snapshot.

## Validation

A corpus snapshot is accepted only after an independent check recomputes its SHA-256 and confirms that the manifest matches the stored artifact.
