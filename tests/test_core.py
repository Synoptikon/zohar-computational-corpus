from zohar_corpus.manifest import CorpusManifest
from zohar_corpus.normalization import normalize_text
from zohar_corpus.segmentation import segment_sentences


def test_normalize_text_is_deterministic():
    assert normalize_text("  A\n\tB  ") == "A B"
    assert normalize_text("e\u0301") == "é"


def test_segment_sentences_is_deterministic():
    assert segment_sentences("Uno. Dos! Tres?") == ["Uno.", "Dos!", "Tres?"]
    assert segment_sentences("") == []


def test_manifest_has_required_provenance_fields():
    manifest = CorpusManifest(
        cid="CID-001",
        source="UNVERIFIED",
        source_url="UNVERIFIED",
        edition="UNVERIFIED",
        language="UNVERIFIED",
        version="UNVERIFIED",
        retrieved_at="UNVERIFIED",
        sha256="0" * 64,
        format="text/plain",
        license="UNVERIFIED",
        license_evidence_url="UNVERIFIED",
        raw_path="data/raw/example.txt",
        normalization="NFC + whitespace",
        segmentation="punctuation-v0",
    )
    data = manifest.to_dict()
    assert data["cid"] == "CID-001"
    assert set(data) == {
        "cid", "source", "source_url", "edition", "language", "version",
        "retrieved_at", "sha256", "format", "license", "license_evidence_url",
        "raw_path", "normalization", "segmentation",
    }
    manifest.validate()
