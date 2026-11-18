#!/usr/bin/env python3
"""Check that a findings file has the findings layout.

Each error prints as `<path>:<line>: <problem>. Fix: <fix>.` The last line is
`open points: <n>`, the count of `- ` items under `## Open points`. Exit 1 on
any error, else exit 0.

Usage: check_findings.py <findings>
"""
import argparse
import re
import sys

sys.dont_write_bytecode = True
from layout import check_header, read_header, sections  # noqa: E402

HEADER_KEYS = ["doctype", "ticket", "status"]
STATUSES = ["open", "answered", "consumed"]
SECTIONS = ["Question", "Answer", "Evidence", "Open points"]


COMMENT = re.compile(r"<!--.*?-->", re.S)


def items(lines, span):
    if span is None:
        return 0
    text = COMMENT.sub("", "\n".join(lines[span[0]:span[1]]))
    return sum(1 for line in text.splitlines() if line.startswith("- "))


def problems(lines):
    errors = []

    def err(line, problem, fix):
        errors.append((line, problem, fix))

    header, body_start = read_header(lines)
    if header is None:
        err(1, "no YAML header", "add a `---` block with " + ", ".join(f"`{k}`" for k in HEADER_KEYS))
    else:
        check_header(header, err, "findings", HEADER_KEYS, STATUSES)
    found = sections(lines, body_start)
    for name in SECTIONS:
        if name not in found:
            err(len(lines) or 1, f"no `## {name}` section", f"add `## {name}`")
    highest = -1
    for name, (begin, end) in found.items():
        if name not in SECTIONS:
            continue
        index = SECTIONS.index(name)
        if index < highest:
            err(begin, f"`## {name}` is out of order", "put the sections in the order " + ", ".join(f"`## {s}`" for s in SECTIONS))
        highest = max(highest, index)
        if not COMMENT.sub("", "\n".join(lines[begin:end])).strip():
            err(begin, f"`## {name}` has no body", "write text, or `none`")
    return errors, items(lines, found.get("Open points"))


def main(argv):
    parser = argparse.ArgumentParser(prog="check_findings.py", description="Check that a findings file has the findings layout.")
    parser.add_argument("findings")
    path = parser.parse_args(argv[1:]).findings
    with open(path) as f:
        lines = f.read().splitlines()
    errors, count = problems(lines)
    for line, problem, fix in errors:
        print(f"{path}:{line}: {problem}. Fix: {fix}.")
    print(f"open points: {count}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
