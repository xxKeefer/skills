#!/usr/bin/env python3
"""Check that a spec file has the spec layout.

Each error prints as `<path>:<line>: <problem>. Fix: <fix>.` The last line is
`open questions: <n>`, the count of `- ` items under `## Open questions`. Exit 1
on any error, else exit 0.

Usage: check_spec.py <spec>
"""
import argparse
import re
import string
import sys

sys.dont_write_bytecode = True
from layout import check_header, read_header, sections  # noqa: E402

HEADER_KEYS = ["doctype", "ticket", "status", "goal"]
STATUSES = ["draft", "confirmed"]
SECTIONS = ["Intent", "Decisions", "Acceptance criteria"]
AC = re.compile(r"^- \[[ x]\] \*\*([A-Z])\.\*\* \S.* → \S.*$")


def items(lines, span):
    if span is None:
        return 0
    return sum(1 for i in range(*span) if lines[i].startswith("- "))


def check_acs(lines, body, end, err):
    if items(lines, (body, end)) > 26:
        err(body, "`## Acceptance criteria` has more than 26 ACs", "split the spec")
        return
    seen = set()
    count = 0
    for i in range(body, end):
        if not lines[i].startswith("- "):
            continue
        expected = string.ascii_uppercase[count]
        count += 1
        m = AC.match(lines[i])
        if not m:
            err(i + 1, "AC is not in the AC layout", "write it as `- [ ] **A.** <action> → <expected>`")
            continue
        letter = m.group(1)
        if letter in seen:
            err(i + 1, f"AC letter `{letter}` is used twice", "give each AC its own letter")
        elif letter != expected:
            err(i + 1, f"AC letter `{letter}` is out of order", f"set it to `{expected}`")
        seen.add(letter)
    if count == 0:
        err(body, "`## Acceptance criteria` has no AC",
            "add one `- [ ] **A.** <action> → <expected>` line for each AC")


def main(argv):
    parser = argparse.ArgumentParser(prog="check_spec.py", description="Check that a spec file has the spec layout.")
    parser.add_argument("spec")
    path = parser.parse_args(argv[1:]).spec
    with open(path) as f:
        lines = f.read().splitlines()
    errors = []

    def err(line, problem, fix):
        errors.append(f"{path}:{line}: {problem}. Fix: {fix}.")

    header, body_start = read_header(lines)
    if header is None:
        err(1, "no YAML header", "add a `---` block with " + ", ".join(f"`{k}`" for k in HEADER_KEYS))
    else:
        check_header(header, err, "spec", HEADER_KEYS, STATUSES)
    found = sections(lines, body_start)
    for name in SECTIONS:
        if name not in found:
            err(len(lines) or 1, f"no `## {name}` section", f"add `## {name}`")
    if "Acceptance criteria" in found:
        check_acs(lines, *found["Acceptance criteria"], err)
    for e in errors:
        print(e)
    print(f"open questions: {items(lines, found.get('Open questions'))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
