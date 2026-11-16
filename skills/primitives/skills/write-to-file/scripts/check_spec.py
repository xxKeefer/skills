#!/usr/bin/env python3
"""Check that a spec file has the spec layout.

Each error prints as `<path>:<line>: <problem>. Fix: <fix>.` Exit 1 on any
error, else exit 0.

Usage: check_spec.py <spec>
"""
import argparse
import re
import string
import sys

sys.dont_write_bytecode = True
from layout import read_header, sections  # noqa: E402

HEADER_KEYS = ["doctype", "ticket", "status", "goal"]
STATUSES = ["draft", "confirmed"]
SECTIONS = ["Intent", "Decisions", "Acceptance criteria"]
AC = re.compile(r"^- \[[ x]\] \*\*([A-Z])\.\*\* \S.* → \S.*$")


def check_header(header, err):
    for key in HEADER_KEYS:
        if key not in header or header[key].value == "":
            err(1, f"header has no `{key}`", f"add `{key}:` to the YAML header")
    if "doctype" in header and header["doctype"].value not in ("", "spec"):
        value, line = header["doctype"]
        err(line, f"doctype `{value}` is not `spec`", "set `doctype: spec`")
    if "status" in header and header["status"].value not in [""] + STATUSES:
        value, line = header["status"]
        err(line, f"status `{value}` is not valid", "set it to one of " + ", ".join(STATUSES))


def check_acs(lines, body, end, err):
    seen = set()
    count = 0
    for i in range(body, end):
        if not lines[i].startswith("- "):
            continue
        expected = string.ascii_uppercase[count] if count < 26 else "?"
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
        check_header(header, err)
    found = sections(lines, body_start)
    for name in SECTIONS:
        if name not in found:
            err(len(lines) or 1, f"no `## {name}` section", f"add `## {name}`")
    if "Acceptance criteria" in found:
        check_acs(lines, *found["Acceptance criteria"], err)
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
