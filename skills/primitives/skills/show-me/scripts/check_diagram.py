#!/usr/bin/env python3
"""Checks a text diagram: each character is one column wide, and each box has matching corners.

Usage: python3 check_diagram.py <file>   (use - to read stdin)
Prints ok and exits 0, or prints one line for each error and exits 1.
"""
import sys

ARROWS = "▲►▼◄"


def allowed(ch):
    return 0x20 <= ord(ch) <= 0x7E or 0x2500 <= ord(ch) <= 0x257F or ch in ARROWS


def check(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    errors = []
    for n, line in enumerate(lines, 1):
        for c, ch in enumerate(line, 1):
            if not allowed(ch):
                errors.append(f"line {n}, column {c}: U+{ord(ch):04X} is not one column wide")
    for n, line in enumerate(lines, 1):
        for c, ch in enumerate(line):
            if ch != "┌":
                continue
            right = line.find("┐", c + 1)
            if right == -1:
                errors.append(f"line {n}, column {c + 1}: no ┐ to the right of ┌")
                continue
            bottom = next(
                (m for m in range(n, len(lines)) if len(lines[m]) > c and lines[m][c] == "└"),
                None,
            )
            if bottom is None:
                errors.append(f"line {n}, column {c + 1}: no └ below ┌")
                continue
            row = lines[bottom]
            if len(row) <= right or row[right] != "┘":
                errors.append(f"line {n}, column {c + 1}: no ┘ under ┐ on line {bottom + 1}")
    return errors


def main():
    path = sys.argv[1]
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    errors = check(text)
    if errors:
        print("\n".join(errors))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
