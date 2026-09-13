from __future__ import annotations

import re

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def segment_sentences(text: str) -> list[str]:
    """Segment text using a deterministic punctuation rule.

    This is an implementation primitive, not a claim that punctuation reflects
    historical or semantic sentence boundaries in the source corpus.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = text.strip()
    if not cleaned:
        return []
    return [part for part in _SENTENCE_END.split(cleaned) if part]
