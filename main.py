#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the competition artifact: one code review comment, byte-identical every run.

The comment lives in entry.txt next to this file. We read it, trim trailing
newlines so the artifact is a single line with no stray whitespace, and write
it to $MAKEFUN_OUTPUT_DIR (or /output) as entry.txt.
"""

from __future__ import annotations

import os
import sys

# The comment is kept in a file of its own so the text is reviewable on its
# own terms, and so this program has nothing to decide at run time.
SOURCE_FILENAME = "entry.txt"
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_DIR_ENV = "MAKEFUN_OUTPUT_DIR"

# The gate: UTF-8 text, 1 to 140 characters, not only white space. The task
# also asks for a single line, so newlines are rejected here rather than
# silently rewritten -- a surprise in the source should fail loudly, not ship.
MAX_CHARS = 140


def read_comment() -> str:
    """Return the comment from the source file beside this script.

    Trailing newlines are trimmed so an editor adding one cannot change the
    artifact's bytes. Nothing else is touched.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, SOURCE_FILENAME), encoding="utf-8") as handle:
        return handle.read().strip("\r\n")


def gate_problem(text: str) -> str | None:
    """Describe why the text would fail the gate, or None if it passes."""
    if "\n" in text or "\r" in text:
        return "comment is not a single line"
    if not text.strip():
        return "comment is empty or only white space"
    if len(text) > MAX_CHARS:
        return f"comment is {len(text)} characters, limit {MAX_CHARS}"
    return None


def output_path() -> str:
    """Return the artifact path, creating its directory if it is missing."""
    out_dir = os.environ.get(OUTPUT_DIR_ENV) or DEFAULT_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, OUTPUT_FILENAME)


def main() -> int:
    text = read_comment()

    problem = gate_problem(text)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1

    path = output_path()
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))

    print(f"wrote {path} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
