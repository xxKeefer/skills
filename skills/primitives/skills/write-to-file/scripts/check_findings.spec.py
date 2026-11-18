#!/usr/bin/env python3
"""Tests for check_findings.py. Run: python3 check_findings.spec.py"""
import os
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_findings.py")

HEADER_KEYS = ["doctype", "ticket", "status"]


def run(path):
    return subprocess.run(
        ["python3", SCRIPT, path],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class CheckFindings(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "findings_x.md")
        self.header = {"doctype": "findings", "ticket": "none", "status": "answered"}
        self.sections = {
            "Question": ["Why does x fail?"],
            "Answer": ["The cache is stale."],
            "Evidence": ["- The run prints y."],
            "Open points": ["- Check z.", "- Check w."],
        }

    def write(self):
        lines = ["---"] + [f"{k}: {v}" for k, v in self.header.items()] + ["---", "", "# Findings: x", ""]
        for name, body in self.sections.items():
            lines += [f"## {name}", ""] + body + [""]
        with open(self.path, "w") as f:
            f.write("\n".join(lines))
        return run(self.path)

    def line_of(self, text):
        with open(self.path) as f:
            for i, line in enumerate(f, 1):
                if text in line:
                    return i
        raise AssertionError(f"{text!r} not in file")

    def test_template_layout_passes(self):
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout, "open points: 2\n")

    def test_header_errors(self):
        for key in HEADER_KEYS:
            with self.subTest(key=key):
                self.setUp()
                del self.header[key]
                r = self.write()
                self.assertEqual(r.returncode, 1)
                self.assertIn(f"{self.path}:1: header has no `{key}`. Fix: add `{key}:` to the YAML header.", r.stdout)
        self.setUp()
        self.header["doctype"] = "spec"
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('doctype:')}: doctype `spec` is not `findings`. Fix: set `doctype: findings`.", r.stdout)
        for status in ["open", "answered", "consumed"]:
            self.setUp()
            self.header["status"] = status
            self.assertEqual(self.write().returncode, 0, status)
        self.setUp()
        self.header["status"] = "active"
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('status:')}: status `active` is not valid. Fix: set it to one of open, answered, consumed.", r.stdout)

    def test_section_errors(self):
        del self.sections["Evidence"]
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn("no `## Evidence` section. Fix: add `## Evidence`.", r.stdout)

        self.setUp()
        self.sections = {k: self.sections[k] for k in ["Question", "Evidence", "Answer", "Open points"]}
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('## Answer')}: `## Answer` is out of order.", r.stdout)

        self.setUp()
        self.sections["Answer"] = []
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:{self.line_of('## Answer')}: `## Answer` has no body. Fix: write text, or `none`.", r.stdout)

    def test_added_section_and_none(self):
        self.sections["Open points"] = ["none"]
        self.sections["Ruled out"] = ["- a."]
        self.sections["Fix direction"] = ["- b."]
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(r.stdout, "open points: 0\n")

    def test_unfilled_template_fails(self):
        template = os.path.join(os.path.dirname(SCRIPT), "..", "templates", "findings.md")
        r = run(template)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("has no body", r.stdout)


if __name__ == "__main__":
    unittest.main()
