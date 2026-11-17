#!/usr/bin/env python3
"""Append one choice to the decision log beside a plan.

The log is `decisions_<KEY>.tsv` for the plan `plan_<KEY>.md` or `handoff_<KEY>.md`. It has one header row and one
row for each choice. Print the log path. Exit 1 on an empty field or a plan name that does not
start with `plan_` or `handoff_`.

On an append, add `- Decision log: decisions_<KEY>.tsv` as the last line of the `## Progress`
section of the plan, when that section has no such line. A plan with no `## Progress` section
stays unchanged.

The `result` form sets the result of one row, counted from 1 with the header not counted. Exit 1
on a row out of range or an empty result.

Usage: log_decision.py <plan> --decision <text> --reason <text> --evidence <text> --result <text>
       log_decision.py result <plan> <row> --result <text>
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "write-to-file", "scripts"))
from layout import sections  # noqa: E402

COLUMNS = ["decision", "reason", "evidence", "result"]


def log_path(plan):
    """Returns the log path beside the plan, or raises ValueError when the name has no `plan_` or `handoff_` prefix."""
    name = os.path.basename(plan)
    prefix = next((p for p in ("plan_", "handoff_") if name.startswith(p)), None)
    if not (prefix and name.endswith(".md")):
        raise ValueError(f"plan file name `{name}` must start with `plan_` or `handoff_` and end with `.md`")
    return os.path.join(os.path.dirname(os.path.abspath(plan)), "decisions_" + name[len(prefix):-3] + ".tsv")


def clean(value):
    """Returns the field with each tab and line break changed to a space."""
    return re.sub(r"[\t\r\n]+", " ", value).strip()


def format_row(fields):
    return "\t".join(clean(f) for f in fields)


def read_log(path):
    """Returns the rows of the log as dicts, or an empty list when the log does not exist."""
    if not os.path.exists(path):
        return []
    with open(path) as f:
        lines = [l for l in f.read().split("\n") if l]
    rows = []
    for line in lines[1:]:
        parts = line.split("\t")
        parts += [""] * (len(COLUMNS) - len(parts))
        rows.append(dict(zip(COLUMNS, parts)))
    return rows


def link_log(plan, log):
    """Adds the decision log link as the last line of `## Progress`, unless that section has one."""
    if not os.path.exists(plan):
        return
    with open(plan) as f:
        lines = f.read().split("\n")
    span = sections(lines, 0).get("Progress")
    if span is None or any(l.startswith("- Decision log:") for l in lines[span[0]:span[1]]):
        return
    last = max((i for i in range(*span) if lines[i].strip()), default=span[0] - 1)
    lines.insert(last + 1, f"- Decision log: {os.path.basename(log)}")
    with open(plan, "w") as f:
        f.write("\n".join(lines))


def set_result(argv):
    parser = argparse.ArgumentParser(prog="log_decision.py result")
    parser.add_argument("plan")
    parser.add_argument("row", type=int)
    parser.add_argument("--result", required=True)
    args = parser.parse_args(argv)
    try:
        path = log_path(args.plan)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    if not clean(args.result):
        print("`--result` is empty. Fix: give the field a value.", file=sys.stderr)
        return 1
    rows = read_log(path)
    if not 1 <= args.row <= len(rows):
        print(f"row {args.row} is out of range. Fix: give a row from 1 to {len(rows)}.", file=sys.stderr)
        return 1
    rows[args.row - 1]["result"] = args.result
    with open(path, "w") as f:
        f.write("\t".join(COLUMNS) + "\n")
        for r in rows:
            f.write(format_row([r[c] for c in COLUMNS]) + "\n")
    print(path)
    return 0


def main():
    if sys.argv[1:2] == ["result"]:
        return set_result(sys.argv[2:])
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    for c in COLUMNS:
        parser.add_argument("--" + c, required=True)
    args = parser.parse_args()
    try:
        path = log_path(args.plan)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    fields = [getattr(args, c) for c in COLUMNS]
    for c, f in zip(COLUMNS, fields):
        if not clean(f):
            print(f"`--{c}` is empty. Fix: give the field a value.", file=sys.stderr)
            return 1
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("\t".join(COLUMNS) + "\n")
        f.write(format_row(fields) + "\n")
    link_log(args.plan, path)
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
