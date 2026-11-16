#!/usr/bin/env python3
"""Tests for migrate_plan.py. Run: python3 migrate_plan.spec.py"""
import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
MIGRATE = os.path.join(HERE, "migrate_plan.py")
CHECK = os.path.join(HERE, "check_plan.py")
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def run(script, *paths):
    return subprocess.run(["python3", script, *paths], capture_output=True, text=True, env=ENV)


def old_plan(worktree):
    return f"""# Plan: X-1 Make x work
Worktree: {worktree}. Branch: x-1_make-x.

Ticket: X-1. Spec: unit 4 of `/tmp/map_x.md`. Goal: make x work: fast. Scope: SCOPED. Estimate: 3.
Builds on: X-0.
Merge: after X-0
Approval: the user approved the plan.

## Acceptance criteria

- [ ] **A.** run x → it works

## Steps

- [x] **1. Add x.** Seam: the CLI `x`. Conditions: C1.
  - Done: x passes.
- [ ] **2. Review.** Depends on every earlier step. This step changes no code.
  - Done: the report path is in this line.
- [ ] **3. Push.** Push the branch and open a draft PR with `/create-pr @plan_X-1.md`.

## Progress

- 2026-11-16: step 1 done.
"""


class MigratePlan(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "plan_X-1.md")

    def write(self, text):
        with open(self.path, "w") as f:
            f.write(text)

    def read(self):
        with open(self.path) as f:
            return f.read()

    # C7
    def test_old_plan_migrates_and_passes_the_check(self):
        self.write(old_plan(self.dir))
        r = run(MIGRATE, self.path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        c = run(CHECK, self.path)
        self.assertEqual(c.returncode, 0, c.stdout + self.read())

    def test_header_holds_the_old_lines(self):
        self.write(old_plan(self.dir))
        run(MIGRATE, self.path)
        text = self.read()
        header = text.split("---\n")[1]
        self.assertEqual(
            header,
            "doctype: plan\n"
            "ticket: X-1\n"
            f"worktree: {self.dir}\n"
            "branch: x-1_make-x\n"
            "status: building\n"
            'goal: "make x work: fast"\n'
            "spec: unit 4 of `/tmp/map_x.md`\n"
            "builds_on: X-0\n"
            "merge: after X-0\n",
        )

    def test_old_lines_leave_the_body(self):
        self.write(old_plan(self.dir))
        run(MIGRATE, self.path)
        body = self.read().split("---\n", 2)[2]
        for old in ("Worktree:", "Ticket:", "Builds on:", "Merge:"):
            self.assertNotIn(old, body)
        self.assertIn("# Plan: X-1 Make x work\n", body)
        self.assertIn("## Goal\n\nmake x work: fast. Scope: SCOPED. Estimate: 3.\n", body)
        self.assertIn("Approval: the user approved the plan.\n", body)

    def test_push_step_gets_a_done_line(self):
        self.write(old_plan(self.dir))
        run(MIGRATE, self.path)
        self.assertIn(
            "with `/create-pr @plan_X-1.md`.\n  - Done: the draft PR URL is in this line.\n",
            self.read(),
        )

    def test_second_run_changes_nothing(self):
        self.write(old_plan(self.dir))
        run(MIGRATE, self.path)
        first = self.read()
        r = run(MIGRATE, self.path)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(self.read(), first)
        self.assertIn("no change", r.stdout)

    def test_sub_task_ticket_and_none_builds_on(self):
        text = old_plan(self.dir)
        text = text.replace("Ticket: X-1.", "Ticket: X-1, a sub-task of X.")
        text = text.replace("Builds on: X-0.", "Builds on: none.")
        self.write(text)
        run(MIGRATE, self.path)
        header = self.read().split("---\n")[1]
        self.assertIn("ticket: X-1\n", header)
        self.assertNotIn("builds_on", header)

    def test_value_that_starts_with_a_backtick_is_quoted(self):
        self.write(old_plan(self.dir).replace("Spec: unit 4 of `/tmp/map_x.md`.", "Spec: `/tmp/map_x.md`."))
        run(MIGRATE, self.path)
        header = self.read().split("---\n")[1]
        self.assertIn('spec: "`/tmp/map_x.md`"\n', header)

    def test_ticket_line_with_no_goal(self):
        self.write(old_plan(self.dir).replace(" Goal: make x work: fast.", ""))
        r = run(MIGRATE, self.path)
        self.assertEqual(r.returncode, 0, r.stderr)
        text = self.read()
        self.assertNotIn("goal:", text.split("---\n")[1])
        self.assertIn("## Goal\n\nScope: SCOPED. Estimate: 3.\n", text)

    def test_status_from_the_steps(self):
        cases = [
            ("- [x] **1.", "- [ ] **1.", "approved"),
            ("- [ ] **2.", "- [x] **2.", "building"),
        ]
        for old, new, status in cases:
            with self.subTest(status=status):
                self.write(old_plan(self.dir).replace(old, new))
                run(MIGRATE, self.path)
                self.assertIn(f"status: {status}\n", self.read())
        text = old_plan(self.dir).replace("- [ ] **2.", "- [x] **2.").replace("- [ ] **3.", "- [x] **3.")
        self.write(text)
        run(MIGRATE, self.path)
        self.assertIn("status: done\n", self.read())

    def test_no_approval_line_gives_approved(self):
        text = old_plan(self.dir).replace("- [x] **1.", "- [ ] **1.")
        text = text.replace("Approval: the user approved the plan.\n", "")
        self.write(text)
        run(MIGRATE, self.path)
        self.assertIn("status: approved\n", self.read())

    def test_waived_approval_line_gives_draft(self):
        text = old_plan(self.dir).replace("- [x] **1.", "- [ ] **1.")
        text = text.replace("Approval: the user approved the plan.", "Approval: none, the user waived questions.")
        self.write(text)
        run(MIGRATE, self.path)
        self.assertIn("status: draft\n", self.read())

    def test_step_that_only_begins_with_push_gets_no_pr_done_line(self):
        for title in ("Pushes events.", "Push notifications on login."):
            with self.subTest(title=title):
                self.write(old_plan(self.dir).replace("**3. Push.**", f"**3. {title}**"))
                run(MIGRATE, self.path)
                self.assertNotIn("draft PR URL", self.read())

    def test_many_files(self):
        other = os.path.join(self.dir, "plan_X-2.md")
        self.write(old_plan(self.dir))
        with open(other, "w") as f:
            f.write(old_plan(self.dir))
        r = run(MIGRATE, self.path, other)
        self.assertEqual(r.returncode, 0)
        for p in (self.path, other):
            self.assertEqual(run(CHECK, p).returncode, 0)

    def test_no_args_is_usage(self):
        self.assertEqual(run(MIGRATE).returncode, 2)


if __name__ == "__main__":
    unittest.main()
