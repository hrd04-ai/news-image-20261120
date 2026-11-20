#!/usr/bin/env python3
"""news-image-20261120 entry point.

Copies the finished front-page image (entry.png, shipped beside this file)
to the grader's output directory. No network, no randomness: the same input
bytes always produce the same output bytes.
"""
import hashlib
import os
import sys
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 16)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def run():
    if not ENTRY.is_file():
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    payload = ENTRY.read_bytes()
    target.write_bytes(payload)
    if sha256_of(target) != hashlib.sha256(payload).hexdigest():
        print("output does not match entry.png", file=sys.stderr)
        return 1
    print("wrote", target, len(payload), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
