#!/usr/bin/env python3
"""Tests for check_principles.py. Run: python3 check_principles.spec.py"""
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_principles.py")

GROUPS = {
    "Core": [
        "laziness-protocol", "foundational-thinking", "redesign-from-first-principles",
        "attack-the-premise", "subtract-before-you-add", "minimize-reader-load",
        "outcome-oriented-execution", "experience-first", "exhaust-the-design-space",
        "build-the-lever",
    ],
    "Architecture": [
        "model-the-domain", "boundary-discipline", "type-system-discipline",
        "make-operations-idempotent", "migrate-callers-then-delete-legacy-apis",
        "separate-before-serializing-shared-state",
    ],
    "Verification": [
        "prove-it-works", "fix-root-causes", "sequence-verifiable-units",
        "test-behavior-not-implementation", "explain-the-number",
    ],
    "Delegation": ["guard-the-context-window", "never-block-on-the-human"],
    "Meta": ["encode-lessons-in-structure"],
}
NAMES = [f"principle-{t}" for g in GROUPS.values() for t in g]


def skill_md(name, flag="disable-model-invocation: true\n"):
    return f"---\nname: {name}\ndescription: Apply when a test needs it.\n{flag}---\n\n# T\n"


def index(skip=None, extra=None, groups=GROUPS):
    out = ["# Work On", "", "## Principles", ""]
    for group, titles in groups.items():
        out += [f"**{group}**", ""]
        for t in titles:
            if f"principle-{t}" != skip:
                out.append(f"- `principle-{t}`. When it applies.")
        out.append("")
    if extra:
        out.append(f"- `{extra}`. When it applies.")
    return "\n".join(out) + "\n"


def run(root):
    return subprocess.run(
        ["python3", SCRIPT, root],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


class CheckPrinciples(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        self.skills = os.path.join(self.root, "skills", "engineering", "skills")
        for n in NAMES:
            self.write(f"{n}/SKILL.md", skill_md(n))
        self.write("work-on/SKILL.md", index())

    def write(self, rel, text):
        path = os.path.join(self.skills, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def test_valid_repo_passes(self):
        r = run(self.root)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_flag_fails_with_folder_name(self):
        self.write("principle-fix-root-causes/SKILL.md",
                   skill_md("principle-fix-root-causes", flag=""))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("principle-fix-root-causes", r.stdout)
        self.assertIn("disable-model-invocation", r.stdout)

    def test_flag_false_fails(self):
        self.write("principle-experience-first/SKILL.md",
                   skill_md("principle-experience-first", flag="disable-model-invocation: false\n"))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("principle-experience-first", r.stdout)

    def test_name_not_equal_to_folder_fails(self):
        self.write("principle-prove-it-works/SKILL.md", skill_md("principle-prove-it"))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("principle-prove-it-works", r.stdout)
        self.assertIn("name", r.stdout)

    def test_missing_folder_fails_with_its_name(self):
        shutil.rmtree(os.path.join(self.skills, "principle-build-the-lever"))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing principle-build-the-lever", r.stdout)

    def test_extra_folder_fails_with_its_name(self):
        self.write("principle-extra-one/SKILL.md", skill_md("principle-extra-one"))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("extra principle-extra-one", r.stdout)

    def test_folder_without_index_entry_fails(self):
        self.write("work-on/SKILL.md", index(skip="principle-model-the-domain"))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no index entry principle-model-the-domain", r.stdout)

    def test_index_entry_without_folder_fails(self):
        self.write("work-on/SKILL.md", index(extra="principle-ghost"))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("index entry principle-ghost has no folder", r.stdout)

    def test_missing_group_heading_fails(self):
        groups = {k: v for k, v in GROUPS.items() if k != "Meta"}
        groups["Delegation"] = GROUPS["Delegation"] + GROUPS["Meta"]
        self.write("work-on/SKILL.md", index(groups=groups))
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertIn("group heading Meta", r.stdout)


if __name__ == "__main__":
    unittest.main()
