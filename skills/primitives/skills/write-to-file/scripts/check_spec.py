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

HEADER_KEYS = ["doctype", "ticket", "status", "goal"]
STATUSES = ["draft", "confirmed"]
SECTIONS = ["Intent", "Decisions", "Acceptance criteria"]
AC = re.compile(r"^- \[[ x]\] \*\*([A-Z])\.\*\* \S.* → \S.*$")


def read_header(lines):
    """Return ({key: (value, line)}, end index) or (None, 0) when there is no header."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    header = {}
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            return header, i + 1
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            header[m.group(1)] = (m.group(2).strip().strip("\"'"), i + 1)
    return None, 0


def sections(lines, start):
    """Map each `## ` heading to its (heading index, end index)."""
    found = {}
    name, begin = None, None
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            if name is not None:
                found[name] = (begin, i)
            name, begin = lines[i][3:].strip(), i
    if name is not None:
        found[name] = (begin, len(lines))
    return found


def check_header(header, err):
    for key in HEADER_KEYS:
        if key not in header or header[key][0] == "":
            err(1, f"header has no `{key}`", f"add `{key}:` to the YAML header")
    if "doctype" in header and header["doctype"][0] not in ("", "spec"):
        value, line = header["doctype"]
        err(line, f"doctype `{value}` is not `spec`", "set `doctype: spec`")
    if "status" in header and header["status"][0] not in [""] + STATUSES:
        value, line = header["status"]
        err(line, f"status `{value}` is not valid", "set it to one of " + ", ".join(STATUSES))


def check_acs(lines, heading, end, err):
    seen = set()
    count = 0
    for i in range(heading + 1, end):
        if not lines[i].startswith("- "):
            continue
        m = AC.match(lines[i])
        if not m:
            err(i + 1, "AC is not in the AC layout", "write it as `- [ ] **A.** <action> → <expected>`")
            continue
        letter = m.group(1)
        expected = string.ascii_uppercase[count] if count < 26 else "?"
        count += 1
        if letter in seen:
            err(i + 1, f"AC letter `{letter}` is used twice", "give each AC its own letter")
        elif letter != expected:
            err(i + 1, f"AC letter `{letter}` is out of order", f"set it to `{expected}`")
        seen.add(letter)
    if count == 0:
        err(heading + 1, "`## Acceptance criteria` has no AC",
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
