from __future__ import annotations

import hashlib
import json
from pathlib import Path

from zohar_corpus.corpus_normalizer import normalize_raw_file

NORMALIZATION_VERSION = "NORMALIZATION-RULES-0.2"
OFFSET_UNIT = "unicode_codepoint_index"
ENCODING = "UTF-8"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_snapshot_manifest(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Snapshot manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_raw_against_snapshot(raw_files: list[Path], snapshot_manifest: dict) -> None:
    expected = {
        Path(entry["path"]).name: entry["sha256"]
        for entry in snapshot_manifest["pages"]
    }
    actual_names = {path.name for path in raw_files}
    if actual_names != set(expected):
        missing = sorted(set(expected) - actual_names)
        unexpected = sorted(actual_names - set(expected))
        raise ValueError(
            "RAW/SNAPSHOT file-set mismatch; "
            f"missing={missing[:10]}, unexpected={unexpected[:10]}"
        )

    for raw_path in raw_files:
        actual_sha256 = sha256_file(raw_path)
        expected_sha256 = expected[raw_path.name]
        if actual_sha256 != expected_sha256:
            raise ValueError(
                f"RAW SHA-256 mismatch: {raw_path}; "
                f"expected={expected_sha256}; actual={actual_sha256}"
            )


def normalize_corpus(
    raw_dir: str | Path,
    output_dir: str | Path,
    manifest_path: str | Path,
    snapshot_manifest_path: str | Path,
) -> dict:
    raw_dir = Path(raw_dir)
    output_dir = Path(output_dir)
    manifest_path = Path(manifest_path)
    snapshot_manifest_path = Path(snapshot_manifest_path)

    raw_files = sorted(raw_dir.glob("*.txt"))
    if not raw_files:
        raise ValueError(f"No RAW files found in {raw_dir}")

    snapshot_manifest = load_snapshot_manifest(snapshot_manifest_path)
    validate_raw_against_snapshot(raw_files, snapshot_manifest)

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for raw_path in raw_files:
        output_path = output_dir / f"{raw_path.stem}.json"
        payload = normalize_raw_file(raw_path, output_path)
        reconstructed = "".join(record["raw_text"] for record in payload["records"])
        raw_text = raw_path.read_text(encoding=ENCODING)
        if reconstructed != raw_text:
            raise ValueError(f"RAW reconstruction failed: {raw_path}")
        entries.append(
            {
                "raw_file": raw_path.name,
                "raw_sha256": sha256_file(raw_path),
                "normalized_file": output_path.name,
                "normalized_sha256": sha256_file(output_path),
                "record_count": len(payload["records"]),
                "normalization_version": NORMALIZATION_VERSION,
            }
        )

    manifest = {
        "schema_version": "1.0",
        "normalization_version": NORMALIZATION_VERSION,
        "offset_unit": OFFSET_UNIT,
        "encoding": ENCODING,
        "raw_file_count": len(raw_files),
        "entries": entries,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=ENCODING,
    )
    return manifest


if __name__ == "__main__":
    normalize_corpus(
        "data/raw/zohar/wikisource",
        "data/normalized/zohar/wikisource",
        "data/normalized/zohar/wikisource/normalized_manifest.json",
        "data/raw/zohar/wikisource/snapshot_manifest.json",
    )
