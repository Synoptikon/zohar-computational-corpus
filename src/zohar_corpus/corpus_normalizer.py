from __future__ import annotations

import json
from pathlib import Path

from .normalization import normalize_text

NORMALIZATION_VERSION = "NORMALIZATION-RULES-0.2"
OFFSET_UNIT = "unicode_codepoint_index"
ENCODING = "UTF-8"
SCHEMA_VERSION = "1.0"


def normalize_raw_file(raw_path: str | Path, output_path: str | Path) -> dict:
    """Create a loss-traceable normalized representation of one RAW UTF-8 file.

    Each record preserves the exact RAW substring and its code-point offsets while
    storing the normalized form separately. The RAW text is never overwritten.
    """
    raw_path = Path(raw_path)
    output_path = Path(output_path)
    raw_text = raw_path.read_text(encoding=ENCODING)

    records: list[dict[str, object]] = []
    cursor = 0
    for sequence, raw_record in enumerate(raw_text.splitlines(keepends=True), start=1):
        start = cursor
        cursor += len(raw_record)
        records.append(
            {
                "sequence": sequence,
                "raw_start": start,
                "raw_end": cursor,
                "raw_text": raw_record,
                "normalized_text": normalize_text(raw_record),
                "normalization_rule": "NFC + whitespace",
                "normalization_version": NORMALIZATION_VERSION,
                "offset_unit": OFFSET_UNIT,
            }
        )

    if raw_text and not records:
        raise AssertionError("Non-empty RAW input produced no normalization records")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "normalization_version": NORMALIZATION_VERSION,
        "offset_unit": OFFSET_UNIT,
        "encoding": ENCODING,
        "raw_file": raw_path.name,
        "records": records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=ENCODING,
    )
    return payload
