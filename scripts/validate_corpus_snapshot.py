#!/usr/bin/env python3
"""Validate an acquired Wikisource RAW snapshot without interpreting its text."""

from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

HEBREW_RANGES = ((0x0590, 0x05FF), (0xFB1D, 0xFB4F))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def has_hebrew(text: str) -> bool:
    return any(any(lo <= ord(ch) <= hi for lo, hi in HEBREW_RANGES) for ch in text)


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: validate_corpus_snapshot.py SNAPSHOT_DIR', file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    manifest_path = root / 'snapshot_manifest.json'
    if not manifest_path.exists():
        raise SystemExit('FAIL: snapshot_manifest.json is missing')

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    pages = manifest.get('pages', [])
    if not pages:
        raise SystemExit('FAIL: manifest contains no pages')
    if manifest.get('license') != 'CC BY-SA 4.0':
        raise SystemExit('FAIL: expected explicit CC BY-SA 4.0 license metadata')

    seen_sequences = set()
    seen_titles = set()
    failures: list[str] = []

    for page in pages:
        sequence = page['sequence']
        title = page['title']
        path = Path(page['path'])
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.exists():
            failures.append(f'missing file: {path}')
            continue
        if sequence in seen_sequences:
            failures.append(f'duplicate sequence: {sequence}')
        if title in seen_titles:
            failures.append(f'duplicate title: {title}')
        seen_sequences.add(sequence)
        seen_titles.add(title)
        actual_hash = sha256(path)
        if actual_hash != page['sha256']:
            failures.append(f'hash mismatch: {path}')
        if path.stat().st_size == 0:
            failures.append(f'empty file: {path}')

    if failures:
        for failure in failures:
            print(f'FAIL: {failure}', file=sys.stderr)
        return 1

    # Deterministic structural sample: first/last plus seeded random pages.
    indices = {0, len(pages) - 1}
    rng = random.Random(20260913)
    indices.update(rng.sample(range(len(pages)), min(8, len(pages))))
    sample = [pages[i] for i in sorted(indices)]
    sample_failures = []
    for page in sample:
        path = Path(page['path'])
        if not path.is_absolute():
            path = Path.cwd() / path
        text = path.read_text(encoding='utf-8')
        if not text.strip():
            sample_failures.append(f'blank sample: {path}')
        if not has_hebrew(text):
            sample_failures.append(f'no Hebrew-script characters in sample: {path}')

    report = {
        'schema_version': '1.0',
        'validation': 'PASS' if not sample_failures else 'FAIL',
        'page_count': len(pages),
        'manifest_sha256': sha256(manifest_path),
        'sample_seed': 20260913,
        'sample_sequences': [p['sequence'] for p in sample],
        'sample_failures': sample_failures,
        'checks': [
            'manifest exists',
            'explicit license metadata',
            'unique page sequence/title',
            'all files exist',
            'per-file SHA-256 matches manifest',
            'non-empty files',
            'deterministic structural sample contains Hebrew-script characters',
        ],
        'limitations': [
            'This validates acquisition integrity, not textual correctness against a historical witness.',
            'A Wikisource transcription remains a collaborative transcription rather than a critical edition.',
        ],
    }
    report_path = root / 'snapshot_validation.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    if sample_failures:
        for failure in sample_failures:
            print(f'FAIL: {failure}', file=sys.stderr)
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
