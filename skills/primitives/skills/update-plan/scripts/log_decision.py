#!/usr/bin/env python3
"""Append one choice to the decision log beside a plan.

The log is `decisions_<KEY>.tsv` for the plan `plan_<KEY>.md`. It has one header row and one
row for each choice. Print the log path. Exit 1 on an empty field or a plan name that does not
start with `plan_`.

Usage: log_decision.py <plan> --decision <text> --reason <text> --evidence <text> --result <text>
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True

COLUMNS = ["decision", "reason", "evidence", "result"]


def log_path(plan):
    """Returns the log path beside the plan, or raises ValueError when the name has no `plan_` prefix."""
    name = os.path.basename(plan)
    if not (name.startswith("plan_") and name.endswith(".md")):
        raise ValueError(f"plan file name `{name}` must start with `plan_` and end with `.md`")
    return os.path.join(os.path.dirname(os.path.abspath(plan)), "decisions_" + name[5:-3] + ".tsv")


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


def main():
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
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
