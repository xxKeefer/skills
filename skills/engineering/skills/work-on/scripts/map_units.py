#!/usr/bin/env python3
"""Read and tick the units of a map.

A unit is a heading `### [ ] N. Title` (or `### [x] N. Title` when ticked)
under the map's `## Units` heading, with a `Done:` line in its section. A split
unit is replaced by sub-units `### [ ] N.1. Title`, `### [ ] N.2. Title`; N is
then a dotted number such as `7.1`.

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
from typing import NamedTuple

UNIT = re.compile(r"^### \[([ x])\] (\d+(?:\.\d+)*)\. (.*)$")


class Unit(NamedTuple):
    index: int
    ticked: bool
    number: str
    title: str
    has_done: bool


class MalformedHeading(Exception):
    pass


def units(lines):
    """Yield a Unit for each unit heading under ## Units.

    Raise MalformedHeading with the 0-based line index when a `### [` heading
    under ## Units does not match the unit form.
    """
    in_units = False
    current = None
    for i, line in enumerate(lines):
        m = UNIT.match(line) if in_units else None
        closes = line.startswith("## ") or (in_units and line.startswith("### "))
        if closes and current:
            yield current
            current = None
        if line.startswith("## "):
            in_units = line.strip() == "## Units"
        elif not in_units:
            continue
        elif m:
            current = Unit(i, m.group(1) == "x", m.group(2), m.group(3).strip(), False)
        elif line.startswith("### ["):
            raise MalformedHeading(i)
        elif current and re.match(r"^\s*-?\s*Done:", line):
            current = current._replace(has_done=True)
    if current:
        yield current


def positive_int(value):
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be 1 or more, got {n}")
    return n


def cmd_next(path, batch):
    with open(path) as f:
        lines = f.read().splitlines()
    open_units = [u for u in units(lines) if not u.ticked]
    errors = [u for u in open_units if not u.has_done]
    for u in errors:
        print(
            f"error: {path}:{u.index + 1}: unit {u.number} has no Done: line. "
            "Fix: add a '- Done: <claim>' line under the heading.",
            file=sys.stderr,
        )
    if errors:
        return 1
    for u in open_units[:batch]:
        print(f"{u.number}\t{u.title}")
    return 0


def cmd_tick(path, number):
    with open(path) as f:
        text = f.read()
    lines = text.splitlines(keepends=True)
    match = [u for u in units([l.rstrip("\n") for l in lines]) if u.number == number]
    if not match:
        print(f"error: {path}: unit {number} does not exist.", file=sys.stderr)
        return 1
    i = match[0].index
    if match[0].ticked:
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
    p_next.add_argument("--batch", type=positive_int, default=5)
    p_tick = sub.add_parser("tick")
    p_tick.add_argument("map")
    p_tick.add_argument("number")
    args = parser.parse_args()
    try:
        if args.cmd == "next":
            return cmd_next(args.map, args.batch)
        return cmd_tick(args.map, args.number)
    except MalformedHeading as e:
        print(
            f"error: {args.map}:{e.args[0] + 1}: malformed unit heading. "
            "Fix: write it as '### [ ] N. Title'.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
