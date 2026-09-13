from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path


@dataclass(frozen=True)
class CorpusManifest:
    """Immutable provenance record for one exact corpus artifact."""

    cid: str
    source: str
    source_url: str
    edition: str
    language: str
    version: str
    retrieved_at: str
    sha256: str
    format: str
    license: str
    license_evidence_url: str
    raw_path: str
    normalization: str
    segmentation: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def validate(self) -> None:
        """Validate required provenance fields without inspecting corpus semantics."""
        required = self.to_dict()
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing required provenance fields: {', '.join(missing)}")

        if len(self.sha256) != 64:
            raise ValueError("sha256 must contain exactly 64 hexadecimal characters")
        try:
            int(self.sha256, 16)
        except ValueError as exc:
            raise ValueError("sha256 must be hexadecimal") from exc


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest of a file without loading it fully into memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(manifest: CorpusManifest, path: str | Path) -> None:
    """Write a deterministic JSON manifest after validating provenance."""
    manifest.validate()
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
