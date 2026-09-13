from pathlib import Path

import pytest

from zohar_corpus.manifest import CorpusManifest, sha256_file


def make_manifest() -> CorpusManifest:
    return CorpusManifest(
        cid="CID-TEST",
        source="test",
        source_url="https://example.org/source",
        edition="test edition",
        language="he",
        version="1",
        retrieved_at="2026-09-13T00:00:00Z",
        sha256="0" * 64,
        format="txt",
        license="Public Domain",
        license_evidence_url="https://example.org/license",
        raw_path="data/raw/test.txt",
        normalization="NONE",
        segmentation="NONE",
    )


def test_manifest_accepts_complete_provenance() -> None:
    make_manifest().validate()


def test_manifest_rejects_missing_required_field() -> None:
    manifest = make_manifest()
    invalid = CorpusManifest(**{**manifest.to_dict(), "source_url": ""})

    with pytest.raises(ValueError, match="source_url"):
        invalid.validate()


def test_manifest_rejects_invalid_sha256() -> None:
    manifest = make_manifest()
    invalid = CorpusManifest(**{**manifest.to_dict(), "sha256": "not-a-hash"})

    with pytest.raises(ValueError, match="sha256"):
        invalid.validate()


def test_sha256_file(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("zohar\n", encoding="utf-8")

    assert sha256_file(path) == "1fa6e97b3fc1df83235651afbc7c1ca9cc38542503a3d3f4d04306c997824f90"
