#!/usr/bin/env python3
"""Tests for log_decision.py. Run: python3 log_decision.spec.py"""
import os
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_decision.py")
HEADER = "decision\treason\tevidence\tresult"


def run(plan, decision="d", reason="r", evidence="e", result="x"):
    return subprocess.run(
        ["python3", SCRIPT, plan, "--decision", decision, "--reason", reason,
         "--evidence", evidence, "--result", result],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class LogDecision(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.plan = os.path.join(self.dir, "plan_demo-1.md")
        self.log = os.path.join(self.dir, "decisions_demo-1.tsv")

    def read(self):
        with open(self.log) as f:
            return f.read().split("\n")

    def test_makes_log_with_header_and_row(self):
        r = run(self.plan, "pick A", "faster", "step 2", "kept")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), self.log)
        self.assertEqual(self.read(), [HEADER, "pick A\tfaster\tstep 2\tkept", ""])

    def test_second_call_appends_and_keeps_one_header(self):
        run(self.plan, "one")
        run(self.plan, "two")
        lines = self.read()
        self.assertEqual(lines.count(HEADER), 1)
        self.assertEqual([l.split("\t")[0] for l in lines[1:3]], ["one", "two"])

    def test_tab_and_newline_become_spaces(self):
        run(self.plan, "a\tb\nc", "r\r\nq")
        row = self.read()[1].split("\t")
        self.assertEqual(len(row), 4)
        self.assertEqual(row[0], "a b c")
        self.assertEqual(len(self.read()), 3)

    def test_empty_field_exits_1(self):
        r = run(self.plan, reason="  ")
        self.assertEqual(r.returncode, 1)
        self.assertIn("reason", r.stderr)
        self.assertFalse(os.path.exists(self.log))

    def test_plan_name_without_prefix_exits_1(self):
        r = run(os.path.join(self.dir, "notes_x.md"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("plan_", r.stderr)


if __name__ == "__main__":
    unittest.main()
