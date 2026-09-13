import json
from pathlib import Path


REQUIRED_PAGE_FIELDS = {
    "sequence",
    "title",
    "pageid",
    "revid",
    "revision_timestamp",
    "source_url",
    "path",
    "sha256",
}


def test_wikisource_manifest_schema():
    manifest_path = Path("data/raw/zohar/wikisource/snapshot_manifest.json")
    if not manifest_path.exists():
        # Acquisition is intentionally not run during ordinary unit tests.
        return

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert data["license"] == "CC BY-SA 4.0"
    assert data["page_count"] == len(data["pages"])

    sequences = [page["sequence"] for page in data["pages"]]
    assert sequences == list(range(1, len(sequences) + 1))

    for page in data["pages"]:
        assert REQUIRED_PAGE_FIELDS <= page.keys()
        assert len(page["sha256"]) == 64
        assert page["source_url"].startswith("https://he.wikisource.org/wiki/")
