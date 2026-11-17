#!/usr/bin/env python3
"""Print what a plan leaves open: pending entries, choices made alone, skipped steps, follow-ups.

Each section prints only when it has items. With no items, print `Nothing is pending.`

Usage: sitrep.py <plan>
"""
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "update-plan", "scripts"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "write-to-file", "scripts"))
from check_plan import ENTRY, parse_steps  # noqa: E402
from layout import sections  # noqa: E402
from log_decision import log_path, read_log  # noqa: E402

RECOMMENDED = re.compile(r"^- ([A-Z]): .*\(recommended")


def open_entries(lines, span):
    """Returns each pending entry as a list of lines: its heading, then its body."""
    if span is None:
        return []
    entries = []
    for i in range(*span):
        if ENTRY.match(lines[i]):
            entries.append([lines[i]])
        elif entries and lines[i].strip():
            entries[-1].append(lines[i])
    return entries


def skipped_steps(lines, span):
    """Returns (title, reason) for each skipped step."""
    if span is None:
        return []
    found = []
    for step in parse_steps(lines, *span, lambda *a: None):
        if step.mark != "-":
            continue
        reason = next((b.strip()[len("- Skipped:"):].strip() for b in step.block if b.strip().startswith("- Skipped:")), "")
        found.append((f"{step.sid}. {step.title}", reason))
    return found


def follow_ups(lines, span):
    if span is None:
        return []
    return [lines[i].strip()[2:] for i in range(*span) if lines[i].startswith("- ")]


def main(argv):
    plan = argv[1]
    with open(plan) as f:
        lines = f.read().splitlines()
    found = sections(lines, 0)
    out = []

    entries = open_entries(lines, found.get("Pending Decisions"))
    if entries:
        out.append("## Open entries")
        for entry in entries:
            out.append("")
            out.append(entry[0].lstrip("# "))
            out.extend(entry[1:])
            rec = next((m.group(1) for l in entry if (m := RECOMMENDED.match(l))), None)
            if rec:
                out.append(f"Recommended: {rec}")

    try:
        rows = read_log(log_path(plan))
    except ValueError:
        rows = []
    if rows:
        out.append("## Choices made alone")
        for r in rows:
            out.append("")
            out.append(f"- Decision: {r['decision']}")
            out.append(f"  - Reason: {r['reason']}")
            out.append(f"  - Evidence: {r['evidence']}")
            out.append(f"  - Result: {r['result']}")

    skipped = skipped_steps(lines, found.get("Steps"))
    if skipped:
        out.append("## Skipped steps")
        out.extend(f"- {title} Skipped: {reason}" for title, reason in skipped)

    items = follow_ups(lines, found.get("Follow-ups"))
    if items:
        out.append("## Follow-ups")
        out.extend(f"- {i}" for i in items)

    print("\n".join(out) if out else "Nothing is pending.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
