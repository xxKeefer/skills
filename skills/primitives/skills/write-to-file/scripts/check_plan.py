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
from layout import DECISION_COLUMNS, check_header, read_header, sections  # noqa: E402

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


def check_worktree(header, err):
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


def check_decision_log(path, lines, found, err):
    name = os.path.basename(path)
    m = re.match(r"(?:plan|handoff)_(.+)\.md$", name)
    if not m:
        return
    log_name = f"decisions_{m.group(1)}.tsv"
    log_path = os.path.join(os.path.dirname(os.path.abspath(path)), log_name)
    if not os.path.exists(log_path):
        return
    with open(log_path) as f:
        header = f.readline().rstrip("\n").split("\t")
    if header != DECISION_COLUMNS:
        err(1, f"{log_name} has the header `{' '.join(header)}`",
            f"write each row with `log_decision.py`, under the header `{' '.join(DECISION_COLUMNS)}`")
    begin, end = found.get("Progress", (len(lines), len(lines)))
    if not any(lines[i].startswith("- Decision log:") for i in range(begin, end)):
        err(begin or 1, "`## Progress` has no `Decision log:` line", f"add `- Decision log: {log_name}`")


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
        check_header(header, err, "plan", HEADER_KEYS, STATUSES)
        check_worktree(header, err)
    found = sections(lines, body_start)
    seen = set()
    for i in range(body_start, len(lines)):
        if lines[i].startswith("## "):
            name = lines[i][3:].strip()
            if name in seen:
                err(i + 1, f"section `## {name}` appears twice", "merge the two sections into one")
            seen.add(name)
    if "Steps" not in found:
        err(len(lines) or 1, "no `## Steps` section", "add `## Steps` with one checkbox per step")
    else:
        for step in parse_steps(lines, *found["Steps"], err):
            check_step(step, err)
    check_decision_log(path, lines, found, err)
    for e in errors:
        print(e)
    print(f"open decisions: {count_open(lines, found.get('Pending Decisions'))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
