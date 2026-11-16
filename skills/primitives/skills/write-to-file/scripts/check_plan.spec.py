#!/usr/bin/env python3
"""Tests for check_plan.py. Run: python3 check_plan.spec.py"""
import os
import re
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_plan.py")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "plan.md")

HEADER_KEYS = ["doctype", "ticket", "worktree", "branch", "status", "goal"]


def run(path, **env):
    return subprocess.run(
        ["python3", SCRIPT, path],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", **env},
    )


class CheckPlan(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "plan_x.md")
        self.header = {
            "doctype": "plan",
            "ticket": "none",
            "worktree": self.dir,
            "branch": "x_branch",
            "status": "approved",
            "goal": "make x work",
        }
        self.steps = [
            "- [ ] **1. Add x.** Seam: the CLI `x`. Conditions: C1.",
            "  - Done: x passes.",
            "- [ ] **2. Test.** Run the gates.",
            "  - Done: the gates are green.",
        ]
        self.decisions = None

    def write(self, **env):
        lines = ["---"]
        lines += [f"{k}: {v}" for k, v in self.header.items()]
        lines += ["---", "", "# Plan: x", "", "## Goal", "", "Make x work.", "", "## Steps", ""]
        lines += self.steps
        lines += ["", "## Progress", "", "- 2026-11-16: written."]
        if self.decisions is not None:
            lines += ["", "## Pending Decisions", ""] + self.decisions
        with open(self.path, "w") as f:
            f.write("\n".join(lines) + "\n")
        return run(self.path, **env)

    def line_of(self, text):
        with open(self.path) as f:
            for i, line in enumerate(f, 1):
                if text in line:
                    return i
        raise AssertionError(f"{text!r} not in plan")

    # C1
    def test_plan_with_every_key_passes(self):
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout, "open decisions: 0\n")

    def test_each_missing_key_fails_with_its_line_and_fix(self):
        for key in HEADER_KEYS:
            with self.subTest(key=key):
                self.setUp()
                del self.header[key]
                r = self.write()
                self.assertEqual(r.returncode, 1)
                self.assertIn(f"{self.path}:1: header has no `{key}`. Fix: add `{key}:`", r.stdout)

    def test_each_empty_key_fails_with_one_error(self):
        for key in HEADER_KEYS:
            with self.subTest(key=key):
                self.setUp()
                self.header[key] = ""
                r = self.write()
                self.assertEqual(r.returncode, 1)
                self.assertIn(f"{self.path}:1: header has no `{key}`. Fix: add `{key}:`", r.stdout)
                self.assertEqual(len(r.stdout.splitlines()), 2, r.stdout)

    def test_no_steps_section_fails_with_its_fix(self):
        with open(self.path, "w") as f:
            f.write("---\n" + "".join(f"{k}: {v}\n" for k, v in self.header.items()) + "---\n\n## Goal\n\nx.\n")
        r = run(self.path)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stderr, "")
        self.assertIn("no `## Steps` section. Fix: add `## Steps`", r.stdout)

    def test_no_frontmatter_fails_on_line_1(self):
        with open(self.path, "w") as f:
            f.write("# Plan: x\n\n## Steps\n")
        r = run(self.path)
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:1: no YAML header", r.stdout)

    def test_header_with_no_closing_fence_fails_on_line_1(self):
        lines = ["---"] + [f"{k}: {v}" for k, v in self.header.items()]
        lines += ["", "# Plan: x", "", "## Steps", ""] + self.steps
        with open(self.path, "w") as f:
            f.write("\n".join(lines) + "\n")
        r = run(self.path)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stderr, "")
        self.assertIn(f"{self.path}:1: no YAML header", r.stdout)

    def test_each_valid_status_passes(self):
        for status in ["draft", "approved", "building", "done"]:
            with self.subTest(status=status):
                self.header["status"] = status
                r = self.write()
                self.assertEqual(r.returncode, 0, r.stdout)

    def test_bad_status_fails_on_its_line(self):
        self.header["status"] = "wip"
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:6: status `wip` is not valid. Fix:", r.stdout)

    def test_bad_doctype_fails_on_its_line(self):
        self.header["doctype"] = "handoff"
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:2: doctype `handoff` is not `plan`. Fix:", r.stdout)

    # C2
    def test_worktree_that_does_not_exist_fails(self):
        self.header["worktree"] = os.path.join(self.dir, "gone")
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:4: worktree `{self.header['worktree']}` does not exist. Fix:", r.stdout)

    def test_worktree_with_a_tilde_passes(self):
        self.header["worktree"] = "~"
        r = self.write(HOME=self.dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    # C3
    def test_step_with_no_done_line_fails_naming_its_line(self):
        del self.steps[1]
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("**1. Add x.**")
        self.assertIn(f"{self.path}:{line}: step 1 has no done line. Fix: add `  - Done: <line>`", r.stdout)
        self.assertEqual(r.stdout.count("no done line"), 1)

    # C4
    def test_behaviour_step_with_no_seam_fails(self):
        self.steps[0] = "- [ ] **1. Add x.** Conditions: C1."
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('**1. Add x.**')}: step 1 changes behaviour and names no seam. Fix:", r.stdout)

    def test_behaviour_step_with_no_conditions_fails(self):
        self.steps[0] = "- [ ] **1. Add x.** Seam: the CLI."
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('**1. Add x.**')}: step 1 changes behaviour and names no tests. Fix:", r.stdout)

    def test_non_behaviour_steps_pass_without_seam_or_conditions(self):
        titles = ["Write docs.** Kind: docs.", "Set x.** Kind: config.", "Rename x.** Kind: mechanical.",
                  "Test.**", "Test the edges.**", "Review.**", "Push.**"]
        self.steps = []
        for i, t in enumerate(titles, 1):
            self.steps += [f"- [ ] **{i}. {t}", "  - Done: it holds."]
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_title_that_only_begins_with_a_non_behaviour_word_needs_a_seam(self):
        for title in ("Testable export.", "Reviewer assignment.", "Pushes events."):
            with self.subTest(title=title):
                self.steps[0] = f"- [ ] **1. {title}**"
                r = self.write()
                self.assertEqual(r.returncode, 1)
                self.assertIn("step 1 changes behaviour and names no seam", r.stdout)

    def test_kind_on_a_sub_line_counts(self):
        self.steps[0] = "- [ ] **1. Write docs.**"
        self.steps.insert(1, "  - Kind: docs.")
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_step_line_not_in_the_layout_fails(self):
        for done in (True, False):
            with self.subTest(done=done):
                self.steps[:2] = ["- [ ] 1. Add x. Seam: s. Conditions: C1."] + (["  - Done: x passes."] if done else [])
                r = self.write()
                self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
                self.assertEqual(r.stderr, "")
                line = self.line_of("- [ ] 1. Add x.")
                self.assertIn(f"{self.path}:{line}: step line is not in the step layout. Fix:", r.stdout)

    def test_steps_section_with_no_step_fails(self):
        self.steps = []
        r = self.write()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(f"{self.path}:{self.line_of('## Steps')}: `## Steps` has no step. Fix:", r.stdout)

    # C5
    def test_skipped_step_with_no_reason_fails(self):
        self.steps[0] = self.steps[0].replace("[ ]", "[-]")
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('**1. Add x.**')}: step 1 is skipped with no reason. Fix: add `  - Skipped: <reason>`", r.stdout)

    def test_skipped_step_with_a_reason_passes(self):
        self.steps[0] = self.steps[0].replace("[ ]", "[-]")
        self.steps.insert(1, "  - Skipped: the user dropped it.")
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_done_step_passes(self):
        self.steps[0] = self.steps[0].replace("[ ]", "[x]")
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_unknown_mark_fails(self):
        self.steps[0] = self.steps[0].replace("[ ]", "[?]")
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('**1. Add x.**')}: step mark `[?]` is not valid. Fix:", r.stdout)

    # C6
    def test_no_pending_decisions_section_prints_zero(self):
        r = self.write()
        self.assertEqual(r.stdout.splitlines()[-1], "open decisions: 0")

    def test_counts_open_d_b_n_entries(self):
        self.decisions = ["### D1: which x? (found in step 1)", "- A: y", "",
                          "### B1: step 2, tests stay red", "- Failure: z", "",
                          "### N1: deploy (step 2)", "- Action: go"]
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(r.stdout.splitlines()[-1], "open decisions: 3")

    def test_empty_pending_decisions_section_prints_zero(self):
        self.decisions = []
        r = self.write()
        self.assertEqual(r.stdout.splitlines()[-1], "open decisions: 0")

    def test_count_prints_after_errors(self):
        del self.header["goal"]
        self.decisions = ["### D1: which x? (found in step 1)"]
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.splitlines()[-1], "open decisions: 1")


class Template(unittest.TestCase):
    # C8
    def test_template_filled_with_example_values_passes(self):
        with open(TEMPLATE) as f:
            text = f.read()
        tmp = tempfile.mkdtemp()
        text = re.sub(r"(?m)^worktree: .*$", f"worktree: {tmp}", text, count=1)
        path = os.path.join(tmp, "plan_x.md")
        with open(path, "w") as f:
            f.write(text)
        r = run(path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout, "open decisions: 0\n")

    def test_template_has_every_section(self):
        with open(TEMPLATE) as f:
            headings = re.findall(r"(?m)^## (.+)$", f.read())
        self.assertEqual(headings, [
            "Goal", "Spec", "Acceptance criteria", "Context", "Test approach",
            "Steps", "Progress", "Pending Decisions", "Follow-ups",
        ])


if __name__ == "__main__":
    unittest.main()
