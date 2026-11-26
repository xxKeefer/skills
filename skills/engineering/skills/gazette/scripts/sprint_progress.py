#!/usr/bin/env python3
"""Reads a sprint's tickets as JSON on stdin and prints its progress bar as HTML, as a tracker's sprint progress counts it."""
import json
import sys

BUCKETS = [("done", "Done"), ("progress", "In progress"), ("todo", "Not started")]


def main():
    tickets = [t for t in json.load(sys.stdin)["tickets"] if not t.get("subtask")]
    pointed = any(t.get("points") for t in tickets)
    unit = "points" if pointed else "tickets"
    sums = {key: sum((t.get("points") or 0) if pointed else 1 for t in tickets if t["bucket"] == key) for key, _ in BUCKETS}
    total = sum(sums.values())
    share = {key: sums[key] / total * 100 if total else 0 for key, _ in BUCKETS}

    rects, x = [], 0.0
    for key, _ in BUCKETS:
        rects.append(f'<rect class="progress-{key}" x="{round(x, 1)}" width="{round(share[key], 1)}" height="6"/>')
        x += share[key]
    legend = "".join(f'<li><span class="progress-{key}">{label}</span> {round(share[key])}%</li>' for key, label in BUCKETS)
    print(f'<div class="progress"><p class="progress-head">{round(share["done"])}% done, {sums["done"]} of {total} {unit}</p>'
          f'<svg class="progress-bar" viewBox="0 0 100 6" preserveAspectRatio="none" role="img" '
          f'aria-label="Sprint progress: {round(share["done"])}% done">{"".join(rects)}</svg>'
          f'<ul class="progress-legend">{legend}</ul></div>')


if __name__ == "__main__":
    main()
