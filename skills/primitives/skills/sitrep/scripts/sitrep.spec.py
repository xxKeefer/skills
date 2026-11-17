#!/usr/bin/env python3
"""Tests for sitrep.py. Run: python3 sitrep.spec.py"""
import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "sitrep.py")
LOG_SCRIPT = os.path.join(HERE, "..", "..", "update-plan", "scripts", "log_decision.py")

PLAN = """---
doctype: plan
ticket: none
worktree: /tmp
branch: demo
status: building
goal: Demo.
---

# Plan: demo

## Steps

- [x] **1. First.**
  - Done: yes.
- [-] **2. Second.**
  - Skipped: the base moved.
  - Done: no.

## Pending Decisions

### D1: Which name? (found in step 3)
- A: alpha
- B: beta (recommended: shorter)
- Work: none
- Blocks: 3, 4

### N1: Edit the ticket (step 5)
- Action: edit it
- Blocks: 5

## Follow-ups

- Rename the helper.
"""

QUIET = PLAN.split("- [-]")[0] + "\n## Follow-ups\n\n"


def sitrep(plan):
    return subprocess.run(
        ["python3", SCRIPT, plan], capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class Sitrep(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.plan = os.path.join(self.dir, "plan_demo-1.md")

    def write(self, text):
        with open(self.plan, "w") as f:
            f.write(text)

    def test_lists_open_entries_with_options_blocks_and_recommendation(self):
        self.write(PLAN)
        out = sitrep(self.plan).stdout
        self.assertIn("D1: Which name?", out)
        self.assertIn("- A: alpha", out)
        self.assertIn("- Blocks: 3, 4", out)
        self.assertIn("Recommended: B", out)
        self.assertIn("N1: Edit the ticket", out)

    def test_lists_each_log_row_with_four_fields(self):
        self.write(PLAN)
        subprocess.run(["python3", LOG_SCRIPT, self.plan, "--decision", "kept A",
                        "--reason", "simpler", "--evidence", "step 1", "--result", "green"],
                       check=True, capture_output=True)
        out = sitrep(self.plan).stdout
        self.assertIn("Choices made alone", out)
        for field in ["kept A", "simpler", "step 1", "green"]:
            self.assertIn(field, out)

    def test_lists_skipped_steps_and_follow_ups(self):
        self.write(PLAN)
        out = sitrep(self.plan).stdout
        self.assertIn("2. Second.", out)
        self.assertIn("the base moved.", out)
        self.assertIn("Rename the helper.", out)

    def test_leaves_out_empty_sections(self):
        self.write(PLAN)
        out = sitrep(self.plan).stdout
        self.assertNotIn("Choices made alone", out)

    def test_nothing_pending_exits_0(self):
        self.write(QUIET)
        r = sitrep(self.plan)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Nothing is pending.", r.stdout)

    def test_plan_name_without_prefix_warns_and_still_prints(self):
        self.plan = os.path.join(self.dir, "notes.md")
        self.write(PLAN)
        r = sitrep(self.plan)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("plan_", r.stderr)
        self.assertIn("Rename the helper.", r.stdout)

    def test_short_log_row_still_lists_the_decision(self):
        self.write(PLAN)
        with open(os.path.join(self.dir, "decisions_demo-1.tsv"), "w") as f:
            f.write("decision\treason\tevidence\tresult\nkept A\tsimpler\n")
        r = sitrep(self.plan)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("kept A", r.stdout)


if __name__ == "__main__":
    unittest.main()
