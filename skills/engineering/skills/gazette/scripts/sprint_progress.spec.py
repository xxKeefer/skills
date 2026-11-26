#!/usr/bin/env python3
"""Tests for sprint_progress.py. Run: python3 sprint_progress.spec.py"""
import json
import os
import re
import subprocess
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "sprint_progress.py")
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
SPRINT = [
    *[{"points": p, "bucket": "done"} for p in (5, 2, 3, 2, 3, 3, 5, 3, 3, 3, 3, 3, 1, 3, 5, 1, 2, 3, 2, 2)],
    *[{"points": p, "bucket": "progress"} for p in (5, 3, 3, 2, 3, 5)],
    {"points": 3, "bucket": "todo"},
    {"points": 3, "bucket": "progress", "subtask": True},
    {"points": 2, "bucket": "progress", "subtask": True},
    {"points": None, "bucket": "todo"},
]


def run(tickets):
    return subprocess.run(["python3", SCRIPT], input=json.dumps({"tickets": tickets}), capture_output=True, text=True, env=ENV)


def widths(html):
    return {cls: float(w) for cls, w in re.findall(r'<rect class="progress-(\w+)" x="[\d.]+" width="([\d.]+)"', html)}


class SprintProgress(unittest.TestCase):
    def test_matches_the_sprint_progress_that_the_tracker_shows(self):
        html = run(SPRINT).stdout
        self.assertIn("70% done", html)
        self.assertIn("Done</span> 70%", html)
        self.assertIn("In progress</span> 26%", html)
        self.assertIn("Not started</span> 4%", html)
        self.assertIn("57 of 81 points", html)

    def test_leaves_out_sub_tasks(self):
        self.assertNotIn("86 points", run(SPRINT).stdout)

    def test_draws_each_bucket_as_its_share_of_the_bar(self):
        found = widths(run(SPRINT).stdout)
        self.assertAlmostEqual(found["done"], 70.4, places=1)
        self.assertAlmostEqual(found["progress"], 25.9, places=1)
        self.assertAlmostEqual(found["todo"], 3.7, places=1)

    def test_counts_tickets_when_no_ticket_has_points(self):
        html = run([{"points": None, "bucket": "done"}, {"bucket": "todo"}]).stdout
        self.assertIn("1 of 2 tickets", html)
        self.assertIn("50% done", html)

    def test_shows_zero_for_an_empty_sprint(self):
        result = run([])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0% done", result.stdout)

    def test_has_no_inline_style(self):
        self.assertNotIn("style=", run(SPRINT).stdout)


if __name__ == "__main__":
    unittest.main()
