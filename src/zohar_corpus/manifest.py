from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from pathlib import Path


@dataclass(frozen=True)
class CorpusManifest:
    """Minimal provenance record for a corpus artifact."""

    cid: str
    source: str
    edition: str
    language: str
    version: str
    sha256: str
    normalization: str
    segmentation: str
    license: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest of a file without loading it fully into memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(manifest: CorpusManifest, path: str | Path) -> None:
    """Write a deterministic JSON manifest."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
