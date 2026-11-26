#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the competition artifact: one code review comment, byte-identical every run.

The comment lives in entry.txt next to this file. We read it, trim trailing
newlines so the artifact is a single line with no stray whitespace, and write
it to $MAKEFUN_OUTPUT_DIR (or /output) as entry.txt.
"""

import os
import sys

SOURCE = "entry.txt"
MAX_CHARS = 140


def comment() -> str:
    """Return the single-line comment held in the source file."""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, SOURCE), encoding="utf-8") as handle:
        text = handle.read()
    return text.strip("\r\n")


def main() -> int:
    text = comment()

    # The gate: UTF-8, one line, 1..140 characters, not only white space.
    if "\n" in text or "\r" in text:
        print("error: comment is not a single line", file=sys.stderr)
        return 1
    if not text.strip():
        print("error: comment is empty or only white space", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: comment is {len(text)} characters, limit {MAX_CHARS}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as handle:
        handle.write(text.encode("utf-8"))

    print(f"wrote {out_path} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
