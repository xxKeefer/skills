#!/usr/bin/env python3
"""Tests for due.py. Run: python3 due.spec.py"""
import json
import os
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "due.py")
TODAY = "2026-12-31"


def run(root, tally, today=TODAY):
    return subprocess.run(
        ["python3", SCRIPT, "--root", root, "--tally", tally, "--today", today],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class Due(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.tally = os.path.join(self.root, "skill-tally.json")

    def skill(self, name, deprecated=None):
        path = os.path.join(self.root, "skills", "deprecated", "skills", name)
        os.makedirs(path)
        lines = ["---", f"name: {name}", "description: x"]
        if deprecated:
            lines.append(f"deprecated: {deprecated}")
        lines += ["---", "", f"# {name}", ""]
        with open(os.path.join(path, "SKILL.md"), "w") as f:
            f.write("\n".join(lines))
        return os.path.join(path, "SKILL.md")

    def write_tally(self, data):
        with open(self.tally, "w") as f:
            f.write(data if isinstance(data, str) else json.dumps(data))

    # C1
    def test_30_days_is_not_due_and_31_days_is_due(self):
        self.skill("thirty", "2026-12-01")
        self.skill("thirtyone", "2026-11-30")
        self.write_tally({})
        r = run(self.root, self.tally)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "thirtyone\t2026-11-30\t31\t0\n")

    def test_due_skills_are_listed_oldest_first(self):
        self.skill("newer", "2026-11-01")
        self.skill("older", "2026-10-01")
        self.write_tally({})
        r = run(self.root, self.tally)
        names = [line.split("\t")[0] for line in r.stdout.splitlines()]
        self.assertEqual(names, ["older", "newer"])

    # C2
    def test_due_skill_shows_its_tally_count_and_unknown_shows_zero(self):
        self.skill("used", "2026-10-01")
        self.skill("unused", "2026-10-02")
        self.write_tally({"used": 7, "other": 3})
        r = run(self.root, self.tally)
        self.assertEqual(
            r.stdout,
            "used\t2026-10-01\t91\t7\nunused\t2026-10-02\t90\t0\n",
        )

    # C3
    def test_skill_with_no_deprecated_key_is_an_error_line(self):
        path = self.skill("undated")
        self.skill("dated", "2026-10-01")
        self.write_tally({})
        r = run(self.root, self.tally)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(
            r.stderr,
            f"error: {path}: no deprecated: key. Fix: add deprecated: YYYY-MM-DD to the frontmatter.\n",
        )
        self.assertEqual(r.stdout, "dated\t2026-10-01\t91\t0\n")

    # C4
    def test_missing_tally_file_gives_zero_counts(self):
        self.skill("gone", "2026-10-01")
        r = run(self.root, self.tally)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "gone\t2026-10-01\t91\t0\n")

    def test_broken_tally_file_gives_zero_counts(self):
        self.skill("gone", "2026-10-01")
        self.write_tally("}}garbage")
        r = run(self.root, self.tally)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "gone\t2026-10-01\t91\t0\n")

    def test_tally_that_is_not_an_object_gives_zero_counts(self):
        self.skill("gone", "2026-10-01")
        self.write_tally([1, 2])
        r = run(self.root, self.tally)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "gone\t2026-10-01\t91\t0\n")

    def test_no_deprecated_skills_lists_nothing(self):
        r = run(self.root, self.tally)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
