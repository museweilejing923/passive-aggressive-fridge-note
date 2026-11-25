"""Fridge-note entry writer.

One fixed passive-aggressive note from a fridge that has had enough.
Every run writes the same bytes to /output/entry.txt: no arguments,
no clock, no network, no randomness.
"""

import os
import string
import sys

SENTENCE = "You have opened me 14 times in the last hour and eaten nothing. I am not a window. I am a fridge with feelings."
CEILING = 200
CLOSERS = ".!?"


def abort(reason):
    sys.stderr.write("rejected: " + reason + "\n")
    raise SystemExit(1)


def has_triple_repeat(line):
    """True when one character shows up three times in a row.

    A tripled letter ("feeeelings") is a typo, not emphasis,
    so notes that repeat a character three times are refused.
    """
    previous = ""
    streak = 0
    for mark in line:
        streak = streak + 1 if mark == previous else 1
        previous = mark
        if streak >= 3:
            return True
    return False


def screen(line):
    if not line.strip():
        abort("the note is blank")
    if len(line) > CEILING:
        abort("the note is longer than 200 characters")
    if any(code < 32 or code == 127 for code in map(ord, line)):
        abort("the note contains a control character")
    if line.strip() != line or "  " in line or "\n" in line:
        abort("the note has ragged edges, a double space, or a line break")
    if line[-1] not in CLOSERS:
        abort("the note does not end with . ! or ?")
    if all(mark in string.punctuation for mark in line):
        abort("the note is punctuation only")
    if line.isdigit():
        abort("the note is digits only")
    if not any(mark.isalpha() for mark in line):
        abort("the note has no letters")
    if "fridge" not in line.casefold():
        abort("the note never says fridge")
    if has_triple_repeat(line):
        abort("the note repeats one character three times in a row")


def emit():
    screen(SENTENCE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as out:
        out.write(SENTENCE + "\n")


if __name__ == "__main__":
    emit()
