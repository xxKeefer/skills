#!/usr/bin/env python3
"""Check that a plan file has the plan layout.

Each error prints as `<path>:<line>: <problem>. Fix: <fix>.` The last line is
`open decisions: <n>`, the count of `### D`, `### B`, and `### N` entries under
`## Pending Decisions`. Exit 1 on any error, else exit 0.

Usage: check_plan.py <plan>
"""
import argparse
import os
import re
import sys
from typing import NamedTuple

sys.dont_write_bytecode = True
from layout import read_header, sections  # noqa: E402

HEADER_KEYS = ["doctype", "ticket", "worktree", "branch", "status", "goal"]
STATUSES = ["draft", "approved", "building", "done"]
STEP = re.compile(r"^- \[(.)\] \*\*(\S+?)\.\s+(.*?)\*\*")
NOT_BEHAVIOUR_KINDS = re.compile(r"\bKind: (docs|config|mechanical)\b")
NOT_BEHAVIOUR_TITLE = re.compile(r"(Test|Review|Push|Review fix \S+)\.")
ENTRY = re.compile(r"^### [DBN]\d+\b")


class Step(NamedTuple):
    index: int
    mark: str
    sid: str
    title: str
    block: list


def check_header(header, err):
    for key in HEADER_KEYS:
        if key not in header or header[key].value == "":
            err(1, f"header has no `{key}`", f"add `{key}:` to the YAML header")
    if "doctype" in header and header["doctype"].value not in ("", "plan"):
        value, line = header["doctype"]
        err(line, f"doctype `{value}` is not `plan`", "set `doctype: plan`")
    if "status" in header and header["status"].value not in [""] + STATUSES:
        value, line = header["status"]
        err(line, f"status `{value}` is not valid", "set it to one of " + ", ".join(STATUSES))
    # A done plan may outlive its worktree: /tidy-up removes it.
    done = "status" in header and header["status"].value == "done"
    if "worktree" in header and header["worktree"].value and not done:
        value, line = header["worktree"]
        if not os.path.isdir(os.path.expanduser(value)):
            err(line, f"worktree `{value}` does not exist", "set `worktree:` to the path of the step's worktree")


def parse_steps(lines, begin, end, err):
    """Return the steps in `## Steps`. A step block is the step line and its indented sub-lines."""
    steps = []
    current = None
    for i in range(begin, end):
        m = STEP.match(lines[i])
        if m:
            current = Step(i, m.group(1), m.group(2), m.group(3).strip(), [lines[i]])
            steps.append(current)
        elif current is not None and (lines[i].startswith((" ", "\t")) or lines[i].strip() == ""):
            current.block.append(lines[i])
        elif lines[i].startswith("- "):
            current = None
            if lines[i].startswith("- ["):
                err(i + 1, "step line is not in the step layout", "write it as `- [ ] **<id>. <title>.**`")
    if not steps:
        err(begin, "`## Steps` has no step", "add one `- [ ] **<id>. <title>.**` line for each step")
    return steps


def check_step(step, err):
    line = step.index + 1
    sid = step.sid
    body = "\n".join(step.block)
    subs = [b.strip() for b in step.block[1:]]
    if step.mark not in (" ", "x", "-"):
        err(line, f"step mark `[{step.mark}]` is not valid", "use `[ ]` open, `[x]` done, or `[-]` skipped")
    if step.mark == "-" and not any(s.startswith("- Skipped:") for s in subs):
        err(line, f"step {sid} is skipped with no reason", "add `  - Skipped: <reason>` under the step")
    if not any(s.startswith("- Done:") for s in subs):
        err(line, f"step {sid} has no done line", "add `  - Done: <line>` under the step")
    if NOT_BEHAVIOUR_KINDS.search(body) or NOT_BEHAVIOUR_TITLE.fullmatch(step.title):
        return
    if "Seam:" not in body:
        err(line, f"step {sid} changes behaviour and names no seam",
            "add `Seam: <seam>`, or `Kind: docs`, `Kind: config`, or `Kind: mechanical`")
    if "Conditions:" not in body:
        err(line, f"step {sid} changes behaviour and names no tests", "add `Conditions: <IDs>`")


def count_open(lines, span):
    if span is None:
        return 0
    begin, end = span
    return sum(1 for i in range(begin, end) if ENTRY.match(lines[i]))


def main(argv):
    parser = argparse.ArgumentParser(prog="check_plan.py", description="Check that a plan file has the plan layout.")
    parser.add_argument("plan")
    path = parser.parse_args(argv[1:]).plan
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
    if "Steps" not in found:
        err(len(lines) or 1, "no `## Steps` section", "add `## Steps` with one checkbox per step")
    else:
        for step in parse_steps(lines, *found["Steps"], err):
            check_step(step, err)
    for e in errors:
        print(e)
    print(f"open decisions: {count_open(lines, found.get('Pending Decisions'))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
