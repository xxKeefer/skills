#!/usr/bin/env python3
"""Reads a sprint as JSON on stdin and prints its burndown chart as inline SVG."""
import json
import sys
from datetime import date, timedelta

W, H, LEFT, RIGHT, TOP, BOTTOM = 480, 180, 40, 12, 14, 28


def main():
    sprint = json.load(sys.stdin)
    start = date.fromisoformat(sprint["start"])
    end = date.fromisoformat(sprint["end"])
    today = min(date.fromisoformat(sprint["today"]), end)
    total = sprint["total"] or 1
    unit = sprint["unit"]
    days = (end - start).days + 1

    def x(i):
        return round(LEFT + i / days * (W - LEFT - RIGHT), 1)

    def y(v):
        return round(TOP + (1 - v / total) * (H - TOP - BOTTOM), 1)

    left = sprint["total"]
    actual = [(x(0), y(left))]
    for i in range((today - start).days + 1):
        day = start + timedelta(days=i)
        left -= sum(d["amount"] for d in sprint["done"] if date.fromisoformat(d["date"]) == day)
        actual.append((x(i + 1), y(left)))

    line = lambda pts: " ".join(f"{a},{b}" for a, b in pts)
    print(f'<svg class="burndown" viewBox="0 0 {W} {H}" role="img" aria-label="Sprint burndown: {left} {unit} left">'
          f'<line class="axis" x1="{LEFT}" y1="{H - BOTTOM}" x2="{W - RIGHT}" y2="{H - BOTTOM}"/>'
          f'<line class="axis" x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{H - BOTTOM}"/>'
          f'<text x="{LEFT - 6}" y="{TOP + 4}" text-anchor="end">{sprint["total"]}</text>'
          f'<text x="{LEFT - 6}" y="{H - BOTTOM}" text-anchor="end">0</text>'
          f'<text x="{LEFT}" y="{H - 8}">{start:%d %b}</text>'
          f'<text x="{W - RIGHT}" y="{H - 8}" text-anchor="end">{end:%d %b}</text>'
          f'<polyline class="ideal" points="{line([(x(0), y(sprint["total"])), (x(days), y(0))])}"/>'
          f'<polyline class="actual" points="{line(actual)}"/>'
          f'<text class="left" x="{actual[-1][0]}" y="{actual[-1][1] - 6}" text-anchor="end">{left} {unit} left</text>'
          f'</svg>')


if __name__ == "__main__":
    main()
