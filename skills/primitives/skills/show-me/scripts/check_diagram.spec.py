#!/usr/bin/env python3
"""Tests for check_diagram.py. Run: python3 check_diagram.spec.py"""
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_diagram.py")

FLOW = """\
      │
      ▼
 ┌─────────┐
 │   map   │  [H0] you approve the map
 └────┬────┘
      │  the router picks the next unit with no tick
      ▼
 needs its own design? ──yes──► /spec ──► ┌──────┐
      │                                   │ spec │  [H1] you say yes
      │ no                                └──┬───┘
      │◄─────────────────────────────────────┘
      ▼
 /plan reads the unit, plus the spec and any findings
      │
      ▼
 ┌─────────┐
 │  plan   │  [H2] you approve the plan
 └────┬────┘
      │  /build runs each step
      ▼
 ┌──────────────── build loop ─────────────────┐
 │ a step runs, then it:                       │
 │   - writes its Progress entry in the plan   │
 │   - appends a row to decisions.tsv          │
 │   - meets an unknown: /diagnose -> findings │
 │ test + review write a report, then:         │
 │   - a row with a fix: a new fix step        │
 │   - a row with no fix: a D entry   [H3]     │
 └──────────────────────┬──────────────────────┘
                        │
                        ▼
               /ship opens a draft PR
                        │
                        ▼  [H4] you mark it ready and merge
          the unit gets its tick on the map
                        │
                        ▼
      /retro reads decisions.tsv and the reports
                        │
                        ▼  [H5] you pick the skill edits
          back to the map for the next unit
"""

GRAPH = """\
                     ┌──────────┐
                     │ findings │
                     └──┬────┬──┘
               evidence │    │ evidence
                        ▼    │
                     ┌──────┐│
                     │ spec ││
                     └──┬───┘│
             /plan reads│    │
                        ▼    ▼
┌─────┐  unit section  ┌──────────┐  /build writes   ┌────────┐
│     ├───────────────►│          ├─────────────────►│        │
│ map │                │   plan   │                  │ report │
│     │◄───────────────┤          │◄─────────────────┤        │
└─────┘ PR exists:tick └────┬─────┘   ticked rows    └────────┘
                            │
                            │ Progress links
                            ▼
                     ┌───────────────┐
                     │ decisions.tsv │
                     └───────────────┘
"""

GOOD_BOX = "┌───┐\n│ a │\n└───┘\n"


def run(path=None, stdin=None):
    args = [sys.executable, SCRIPT, path if path else "-"]
    return subprocess.run(args, input=stdin, capture_output=True, text=True)


def run_text(text):
    return run(stdin=text)


class CheckDiagramTest(unittest.TestCase):
    def test_map_diagrams_pass(self):
        for text in (FLOW, GRAPH):
            result = run_text(text)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(result.stdout.strip(), "ok")

    def test_wide_character_fails(self):
        for bad in ("\U0001F600", "\u4e2d", "\u0301"):
            result = run_text("┌───┐\n│ a%s│\n└───┘\n" % bad)
            self.assertEqual(result.returncode, 1, bad)
            self.assertIn("line 2", result.stdout)
            self.assertIn("column 4", result.stdout)

    def test_misaligned_corner_fails(self):
        result = run_text("┌───┐\n│ a │\n└────┘\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1", result.stdout)
        self.assertIn("column 1", result.stdout)
        result = run_text("┌───┐\n│ a │\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1", result.stdout)
        self.assertIn("column 1", result.stdout)

    def test_short_bottom_row_fails(self):
        result = run_text("┌───┐\n│ a │\n└──\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1", result.stdout)
        self.assertIn("column 1", result.stdout)
        self.assertIn("no ┘", result.stdout)

    def test_corner_error_names_the_bottom_line(self):
        result = run_text("x\ny\n┌───┐\n│ a │\n│ b │\n└────┘\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 3, column 1", result.stdout)
        self.assertIn("on line 6", result.stdout)

    def test_missing_top_right_corner_fails(self):
        result = run_text("┌───\n│ a │\n└───┘\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1", result.stdout)
        self.assertIn("column 1", result.stdout)
        self.assertIn("no ┐", result.stdout)

    def test_character_set_edges(self):
        self.assertEqual(run_text("▲\u257f\n").returncode, 0)
        for bad, column in (("\u2580", "column 1"), ("\x7f", "column 1")):
            result = run_text(bad + "\n")
            self.assertEqual(result.returncode, 1, repr(bad))
            self.assertIn("line 1", result.stdout)
            self.assertIn(column, result.stdout)

    def test_no_argument_reads_stdin(self):
        result = subprocess.run([sys.executable, SCRIPT], input=GOOD_BOX, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "ok")

    def test_stdin(self):
        path = os.path.join(HERE, "_good_box.tmp")
        with open(path, "w", encoding="utf-8") as f:
            f.write(GOOD_BOX)
        try:
            from_file = run(path=path)
        finally:
            os.remove(path)
        from_stdin = run_text(GOOD_BOX)
        self.assertEqual(from_file.stdout, from_stdin.stdout)
        self.assertEqual(from_file.returncode, from_stdin.returncode)
        self.assertEqual(from_stdin.returncode, 0)


if __name__ == "__main__":
    unittest.main()
