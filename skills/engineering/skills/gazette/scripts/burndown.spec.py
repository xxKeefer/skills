#!/usr/bin/env python3
"""Tests for burndown.py. Run: python3 burndown.spec.py"""
import json
import os
import re
import subprocess
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "burndown.py")
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
SPRINT = {"start": "2026-11-17", "end": "2026-11-20", "today": "2026-11-19", "total": 10, "unit": "points",
          "done": [{"date": "2026-11-18", "amount": 4}, {"date": "2026-11-20", "amount": 6}]}


def run(sprint):
    return subprocess.run(["python3", SCRIPT], input=json.dumps(sprint), capture_output=True, text=True, env=ENV)


def points(svg, cls):
    found = re.search(rf'<polyline class="{cls}" points="([^"]+)"', svg).group(1)
    return [tuple(float(n) for n in p.split(",")) for p in found.split()]


class Burndown(unittest.TestCase):
    def test_draws_the_ideal_line_from_the_total_to_zero(self):
        ideal = points(run(SPRINT).stdout, "ideal")
        actual = points(run(SPRINT).stdout, "actual")
        self.assertEqual(ideal[0], actual[0])
        self.assertGreater(ideal[-1][1], ideal[0][1])

    def test_ends_the_actual_line_today_with_the_amount_left(self):
        svg = run(SPRINT).stdout
        actual = points(svg, "actual")
        self.assertEqual(len(actual), 4)
        self.assertEqual(actual[1][1], actual[0][1])
        self.assertGreater(actual[2][1], actual[1][1])
        self.assertIn("6 points left", svg)

    def test_stops_the_actual_line_at_the_sprint_end(self):
        svg = run({**SPRINT, "today": "2026-11-30"}).stdout
        self.assertEqual(len(points(svg, "actual")), 5)
        self.assertIn("0 points left", svg)

    def test_has_no_inline_style(self):
        self.assertNotIn("style=", run(SPRINT).stdout)


if __name__ == "__main__":
    unittest.main()
