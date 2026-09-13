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
        edition="UNVERIFIED",
        language="UNVERIFIED",
        version="UNVERIFIED",
        sha256="UNVERIFIED",
        normalization="NFC + whitespace",
        segmentation="punctuation-v0",
        license="UNVERIFIED",
    )
    data = manifest.to_dict()
    assert data["cid"] == "CID-001"
    assert set(data) == {
        "cid", "source", "edition", "language", "version",
        "sha256", "normalization", "segmentation", "license",
    }
