#!/usr/bin/env python3
"""Move an old-layout plan into the plan layout, in place.

Moves the `Worktree:`, `Ticket:`, `Builds on:`, and `Merge:` lines into a YAML
header, and the goal, scope, and estimate into `## Goal`. Gives a Push step with
no done line one. A file that already has a header does not change.

Usage: migrate_plan.py <file>...
"""
import argparse
import json
import re
import sys

STEP = re.compile(r"^- \[(.)\] \*\*\S+?\.\s+(.*?)\*\*")
WORKTREE = re.compile(r"^Worktree:\s*(.+?)\.\s+Branch:\s*(.+?)\.?\s*$")
FIELD = re.compile(r"(?:^|(?<=\.)\s+)(Ticket|Spec|Goal|Scope|Estimate):\s*")
PUSH_DONE = "  - Done: the draft PR URL is in this line."


def scalar(value):
    if re.search(r": | #|^[-?:,\[\]{}#&*!|>'\"%@`]", value):
        return json.dumps(value)
    return value


def strip_period(value):
    return value.strip().rstrip(".").strip()


def parse_ticket(line):
    parts = FIELD.split(line)
    return {parts[i]: strip_period(parts[i + 1]) for i in range(1, len(parts) - 1, 2)}


def status_of(lines, approved):
    marks = [m.group(1) for m in map(STEP.match, lines) if m]
    if marks and all(m in "x-" for m in marks):
        return "done"
    if "x" in marks:
        return "building"
    return "approved" if approved else "draft"


def add_push_done(lines):
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        m = STEP.match(lines[i])
        i += 1
        if not m or not m.group(2).startswith("Push"):
            continue
        j = i
        while j < len(lines) and lines[j].startswith((" ", "\t")):
            j += 1
        out.extend(lines[i:j])
        if not any(l.strip().startswith("- Done:") for l in lines[i:j]):
            out.append(PUSH_DONE)
        i = j
    return out


def migrate(text):
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        return text
    header = {"doctype": "plan"}
    extra = {}
    goal_line = None
    body = []
    in_preamble = True
    for line in lines:
        if line.startswith("## "):
            in_preamble = False
        m = WORKTREE.match(line) if in_preamble else None
        if m:
            header["worktree"], header["branch"] = m.group(1).strip(), m.group(2).strip()
            continue
        if in_preamble and line.startswith("Ticket:"):
            fields = parse_ticket(line)
            header["ticket"] = fields.get("Ticket", "none").split(",")[0].strip()
            if "Goal" in fields:
                header["goal"] = fields["Goal"]
            if "Spec" in fields and fields["Spec"] != "none":
                extra["spec"] = fields["Spec"]
            rest = [f"{k}: {fields[k]}." for k in ("Scope", "Estimate") if k in fields]
            goal_line = " ".join(([fields["Goal"] + "."] if "Goal" in fields else []) + rest)
            body.append("## Goal")
            body.append("")
            body.append(goal_line)
            body.append("")
            continue
        if in_preamble and line.startswith("Builds on:"):
            value = strip_period(line[len("Builds on:"):])
            if value != "none":
                extra["builds_on"] = value
            continue
        if in_preamble and line.startswith("Merge:"):
            extra["merge"] = strip_period(line[len("Merge:"):])
            continue
        body.append(line)
    approved = any(l.startswith("Approval:") for l in lines)
    order = ["doctype", "ticket", "worktree", "branch"]
    out = ["---"]
    out += [f"{k}: {scalar(header[k])}" for k in order if k in header]
    out.append(f"status: {status_of(lines, approved)}")
    if "goal" in header:
        out.append(f"goal: {scalar(header['goal'])}")
    out += [f"{k}: {scalar(v)}" for k, v in extra.items()]
    out.append("---")
    out.append("")
    body = add_push_done(body)
    collapsed = []
    for line in body:
        if line.strip() == "" and collapsed and collapsed[-1].strip() == "":
            continue
        collapsed.append(line)
    return "\n".join(out + collapsed) + "\n"


def main(argv):
    parser = argparse.ArgumentParser(prog="migrate_plan.py", description="Move an old-layout plan into the plan layout, in place.")
    parser.add_argument("files", nargs="+")
    for path in parser.parse_args(argv[1:]).files:
        with open(path) as f:
            text = f.read()
        new = migrate(text)
        if new == text:
            print(f"{path}: no change")
            continue
        with open(path, "w") as f:
            f.write(new)
        print(f"{path}: migrated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
