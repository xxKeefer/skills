#!/usr/bin/env python3
"""List the deprecated skills that are due for deletion.

A skill is due when its `deprecated:` date is more than 30 days before today.
Output: one line per due skill, `<name>\t<deprecated date>\t<days>\t<count>`,
oldest first. The count comes from the skill tally (0 when the skill or the
tally file is missing). A deprecated skill with no `deprecated:` key gives an
error line on stderr and exit 1.

Usage: due.py [--root <repo>] [--tally <file>] [--today YYYY-MM-DD]
"""
import argparse
import datetime
import glob
import json
import os
import sys

GRACE_DAYS = 30
DEFAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 5))


def tally_path():
    return os.environ.get("SKILL_TALLY_FILE", os.path.expanduser("~/.claude/skill-tally.json"))


def read_tally(path):
    try:
        with open(path) as f:
            tally = json.load(f)
    except (OSError, ValueError):
        return {}
    return tally if isinstance(tally, dict) else {}


def deprecated_date(skill_md):
    with open(skill_md) as f:
        lines = f.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        key, _, value = line.partition(":")
        if key.strip() == "deprecated" and value.strip():
            return datetime.date.fromisoformat(value.strip().strip("'\""))
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--tally", default=tally_path())
    parser.add_argument("--today", type=datetime.date.fromisoformat, default=datetime.date.today())
    args = parser.parse_args()

    tally = read_tally(args.tally)
    pattern = os.path.join(args.root, "skills", "deprecated", "skills", "*", "SKILL.md")
    due = []
    failed = False
    for skill_md in sorted(glob.glob(pattern)):
        date = deprecated_date(skill_md)
        if date is None:
            print(
                f"error: {skill_md}: no deprecated: key. Fix: add deprecated: YYYY-MM-DD to the frontmatter.",
                file=sys.stderr,
            )
            failed = True
            continue
        days = (args.today - date).days
        if days > GRACE_DAYS:
            name = os.path.basename(os.path.dirname(skill_md))
            due.append((date, name, days, tally.get(name, 0)))

    for date, name, days, count in sorted(due):
        print(f"{name}\t{date.isoformat()}\t{days}\t{count}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
