#!/usr/bin/env python3
"""Tests for check_spec.py. Run: python3 check_spec.spec.py"""
import os
import re
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_spec.py")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "spec.md")

HEADER_KEYS = ["doctype", "ticket", "status", "goal"]
SECTIONS = ["Intent", "Decisions", "Acceptance criteria"]


def run(path):
    return subprocess.run(
        ["python3", SCRIPT, path],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class CheckSpec(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "spec_x.md")
        self.header = {"doctype": "spec", "ticket": "none", "status": "confirmed", "goal": "make x work"}
        self.sections = {
            "Intent": ["- Outcome: x works."],
            "Decisions": ["- Use y."],
            "Acceptance criteria": [
                "- [ ] **A.** Run x → it prints y.",
                "- [ ] **B.** Run x with no input → it exits 1.",
            ],
            "Out of scope": ["- z."],
        }

    def write(self, header=True):
        lines = []
        if header:
            lines += ["---"] + [f"{k}: {v}" for k, v in self.header.items()] + ["---", ""]
        lines += ["# Spec: x", ""]
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
        raise AssertionError(f"{text!r} not in spec")

    # C1
    def test_good_spec_passes(self):
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout, "open questions: 0\n")

    def test_optional_sections_can_be_absent(self):
        del self.sections["Out of scope"]
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_no_header_fails(self):
        r = self.write(header=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{self.path}:1: no YAML header. Fix: add a `---` block with", r.stdout)

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
                self.assertEqual(r.stdout, f"{self.path}:1: header has no `{key}`. Fix: add `{key}:` to the YAML header.\nopen questions: 0\n")

    def test_header_with_no_closing_fence_fails_on_line_1(self):
        lines = ["---"] + [f"{k}: {v}" for k, v in self.header.items()] + ["", "# Spec: x", ""]
        for name, body in self.sections.items():
            lines += [f"## {name}", ""] + body + [""]
        with open(self.path, "w") as f:
            f.write("\n".join(lines))
        r = run(self.path)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stderr, "")
        self.assertEqual(r.stdout.splitlines()[0], f"{self.path}:1: no YAML header. Fix: add a `---` block with `doctype`, `ticket`, `status`, `goal`.")
        self.assertEqual(len(r.stdout.splitlines()), 2, r.stdout)

    def test_wrong_doctype_fails_on_its_line(self):
        self.header["doctype"] = "plan"
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("doctype: plan")
        self.assertIn(f"{self.path}:{line}: doctype `plan` is not `spec`. Fix: set `doctype: spec`.", r.stdout)

    def test_bad_status_fails_on_its_line(self):
        self.header["status"] = "approved"
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("status: approved")
        self.assertIn(f"{self.path}:{line}: status `approved` is not valid. Fix: set it to one of draft, confirmed.", r.stdout)

    def test_draft_status_passes(self):
        self.header["status"] = "draft"
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_each_missing_section_fails_with_its_fix(self):
        for name in SECTIONS:
            with self.subTest(section=name):
                self.setUp()
                del self.sections[name]
                r = self.write()
                self.assertEqual(r.returncode, 1)
                self.assertRegex(r.stdout, rf"{self.path}:\d+: no `## {name}` section\. Fix: add `## {name}`")

    # C2
    def test_no_ac_fails(self):
        self.sections["Acceptance criteria"] = ["None yet."]
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("## Acceptance criteria")
        self.assertIn(f"{self.path}:{line}: `## Acceptance criteria` has no AC. Fix: add", r.stdout)

    def test_bad_ac_form_fails_on_its_line(self):
        for bad in ["- [ ] **A.** Run x, it prints y.", "- [ ] A. Run x → y.", "- [ ] **a.** Run x → y."]:
            with self.subTest(bad=bad):
                self.setUp()
                self.sections["Acceptance criteria"] = [bad]
                r = self.write()
                self.assertEqual(r.returncode, 1)
                line = self.line_of(bad)
                self.assertIn(
                    f"{self.path}:{line}: AC is not in the AC layout. Fix: write it as `- [ ] **A.** <action> → <expected>`.",
                    r.stdout,
                )

    def test_repeated_letter_fails_on_its_line(self):
        self.sections["Acceptance criteria"][1] = "- [ ] **A.** Run x again → it prints y."
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("Run x again")
        self.assertIn(f"{self.path}:{line}: AC letter `A` is used twice. Fix: give each AC its own letter.", r.stdout)

    def test_gap_in_letters_fails_on_its_line(self):
        self.sections["Acceptance criteria"][1] = "- [ ] **C.** Run x with no input → it exits 1."
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("**C.**")
        self.assertIn(f"{self.path}:{line}: AC letter `C` is out of order. Fix: set it to `B`.", r.stdout)

    def test_bad_ac_form_keeps_its_letter_place(self):
        self.sections["Acceptance criteria"][0] = "- [ ] **A.** Run x, it prints y."
        r = self.write()
        self.assertEqual(r.returncode, 1)
        self.assertEqual(len(r.stdout.splitlines()), 2, r.stdout)
        self.assertIn(f"{self.path}:{self.line_of('Run x, it')}: AC is not in the AC layout.", r.stdout)

    def test_more_than_26_acs_fails_once_on_the_heading(self):
        letters = [chr(ord("A") + i) for i in range(26)] + ["A"]
        self.sections["Acceptance criteria"] = [f"- [ ] **{c}.** Run x {i} → it prints y." for i, c in enumerate(letters)]
        r = self.write()
        self.assertEqual(r.returncode, 1)
        line = self.line_of("## Acceptance criteria")
        errors = [l for l in r.stdout.splitlines() if not l.startswith("open questions:")]
        self.assertEqual(errors, [f"{self.path}:{line}: `## Acceptance criteria` has more than 26 ACs. Fix: split the spec."])

    def test_no_open_questions_section_counts_0(self):
        r = self.write()
        self.assertEqual(r.stdout.splitlines()[-1], "open questions: 0")

    def test_each_open_question_item_counts(self):
        self.sections["Open questions"] = ["<!-- Optional. -->", "", "- Who owns y?", "- When does z ship?"]
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(r.stdout.splitlines()[-1], "open questions: 2")

    def test_open_questions_with_only_a_comment_counts_0(self):
        self.sections["Open questions"] = ["<!-- Optional. Remove when no question is open. -->"]
        r = self.write()
        self.assertEqual(r.stdout.splitlines()[-1], "open questions: 0")

    def test_done_ac_passes(self):
        self.sections["Acceptance criteria"][0] = "- [x] **A.** Run x → it prints y."
        r = self.write()
        self.assertEqual(r.returncode, 0, r.stdout)


class NoBytecode(unittest.TestCase):
    def test_run_leaves_no_pycache(self):
        d = tempfile.mkdtemp()
        for name in ("check_spec.py", "layout.py"):
            shutil.copy(os.path.join(os.path.dirname(SCRIPT), name), d)
        path = os.path.join(d, "spec_x.md")
        shutil.copy(TEMPLATE, path)
        env = {k: v for k, v in os.environ.items() if k != "PYTHONDONTWRITEBYTECODE"}
        r = subprocess.run(["python3", os.path.join(d, "check_spec.py"), path], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse(os.path.exists(os.path.join(d, "__pycache__")))


class Template(unittest.TestCase):
    # C3
    def test_template_filled_with_example_values_passes(self):
        path = os.path.join(tempfile.mkdtemp(), "spec_x.md")
        shutil.copy(TEMPLATE, path)
        r = run(path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout, "open questions: 1\n")

    def test_template_has_every_section(self):
        with open(TEMPLATE) as f:
            headings = re.findall(r"(?m)^## (.+)$", f.read())
        self.assertEqual(headings, ["Intent", "Decisions", "Acceptance criteria", "Out of scope", "Open questions"])

    def test_template_status_is_confirmed(self):
        with open(TEMPLATE) as f:
            self.assertRegex(f.read(), r"(?m)^status: confirmed$")


if __name__ == "__main__":
    unittest.main()
