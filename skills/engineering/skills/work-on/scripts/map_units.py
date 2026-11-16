#!/usr/bin/env python3
"""Read and tick the units of a map.

A unit is a heading `### [ ] N. Title` (or `### [x] N. Title` when ticked)
under the map's `## Units` heading, with a `Done:` line in its section.

  next <map> [--batch 5]  One line per unit with no tick, in order,
                          `<N>\t<title>`, at most --batch lines. A unit with
                          no `Done:` line is an error that names its line.
  tick <map> <N>          Change `### [ ] N.` to `### [x] N.`. Exit 1 when
                          unit N does not exist or is already ticked.

Usage: map_units.py next <map> [--batch N] | tick <map> <N>
"""
import argparse
import re
import sys

UNIT = re.compile(r"^### \[([ x])\] (\d+)\. (.*)$")


def units(lines):
    """Yield (index, ticked, number, title, has_done) for each unit under ## Units."""
    in_units = False
    found = []
    for i, line in enumerate(lines):
        if line.startswith("## "):
            in_units = line.strip() == "## Units"
            continue
        if not in_units:
            continue
        m = UNIT.match(line)
        if m:
            found.append([i, m.group(1) == "x", int(m.group(2)), m.group(3).strip(), False])
        elif line.startswith("### "):
            found.append(None)
        elif found and found[-1] is not None and re.match(r"^\s*-?\s*Done:", line):
            found[-1][4] = True
    return [u for u in found if u is not None]


def cmd_next(path, batch):
    with open(path) as f:
        lines = f.read().splitlines()
    open_units = [u for u in units(lines) if not u[1]]
    errors = [u for u in open_units if not u[4]]
    for i, _, n, _, _ in errors:
        print(
            f"error: {path}:{i + 1}: unit {n} has no Done: line. "
            "Fix: add a '- Done: <claim>' line under the heading.",
            file=sys.stderr,
        )
    if errors:
        return 1
    for _, _, n, title, _ in open_units[:batch]:
        print(f"{n}\t{title}")
    return 0


def cmd_tick(path, number):
    with open(path) as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    match = [u for u in units([l.rstrip("\n") for l in lines]) if u[2] == number]
    if not match:
        print(f"error: {path}: unit {number} does not exist.", file=sys.stderr)
        return 1
    i, ticked = match[0][0], match[0][1]
    if ticked:
        print(f"error: {path}:{i + 1}: unit {number} is already ticked.", file=sys.stderr)
        return 1
    lines[i] = lines[i].replace("### [ ]", "### [x]", 1)
    with open(path, "w") as f:
        f.write("".join(lines))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Read and tick the units of a map.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_next = sub.add_parser("next")
    p_next.add_argument("map")
    p_next.add_argument("--batch", type=int, default=5)
    p_tick = sub.add_parser("tick")
    p_tick.add_argument("map")
    p_tick.add_argument("number", type=int)
    args = parser.parse_args()
    if args.cmd == "next":
        return cmd_next(args.map, args.batch)
    return cmd_tick(args.map, args.number)


if __name__ == "__main__":
    sys.exit(main())
