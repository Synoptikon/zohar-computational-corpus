from __future__ import annotations

import unicodedata


def normalize_unicode(text: str) -> str:
    """Normalize Unicode representation without changing lexical content."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return unicodedata.normalize("NFC", text)


def normalize_whitespace(text: str) -> str:
    """Collapse whitespace runs and trim surrounding whitespace."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return " ".join(text.split())


def normalize_text(text: str) -> str:
    """Apply only documented, loss-minimizing normalization steps."""
    return normalize_whitespace(normalize_unicode(text))
