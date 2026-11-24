#!/usr/bin/env python3
"""Alien Field Notes: The Two Day Earth Review -- make.fun entry.

One line, written by the program itself to /output/entry.txt. Nothing
but the standard library is used.

An alien tourist files a two-day trip report on Earth, and the thing
that sticks is the self-checkout: the locals wave their groceries at a
beeping box, pay the box, then bag it all themselves -- and nobody finds
this strange except the visitor. The report closes the way a real review
would, with stars and a promise to orbit again.
"""

import os
import sys

ENTRY = "Two-day trip report: the locals wave their groceries at a beeping box, pay the box, then bag it themselves. Five stars; would orbit again."

OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.txt"
LOWER_BOUND = 1
UPPER_BOUND = 200


def problems_with(text):
    """List every way the entry can fail the kit's gate, as messages."""
    if not isinstance(text, str):
        return ["entry is not text"]
    problems = []
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8")
    if not LOWER_BOUND <= len(text) <= UPPER_BOUND:
        problems.append(
            "entry runs %d characters; the gate allows %d-%d"
            % (len(text), LOWER_BOUND, UPPER_BOUND)
        )
    if not text.strip():
        problems.append("entry is blank")
    if any(ch in text for ch in "\r\n"):
        problems.append("entry spans more than one line")
    return problems


def fail(problems):
    """Report each problem on stderr and exit nonzero."""
    for problem in problems:
        print("GATE FAILED: %s" % problem, file=sys.stderr)
    return 1


def write_entry():
    """Gate the entry, write it out, then prove the disk copy matches."""
    problems = problems_with(ENTRY)
    if problems:
        return fail(problems)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != ENTRY:
        return fail(["read-back differs from the entry"])
    if problems_with(stored):
        return fail(["written file fails the gates"])
    print("OK: wrote %s (%d characters, 1 line)" % (path, len(stored)))
    return 0


if __name__ == "__main__":
    sys.exit(write_entry())
