#!/usr/bin/env python3
"""Tests for check_driver.py. Run: python3 check_driver.spec.py"""
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_driver.py")
EXAMPLE = os.path.join(HERE, "..", "references", "feature-map-example")
SECTIONS = ["Launch", "Doctor", "Drive", "Evidence", "Cleanup", "Helpers"]
H2S = ["Sub-features", "How to get to it (user POV)", "Driving it with demo-harness", "Gotchas"]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def skill_md(sections=SECTIONS, frontmatter="name: verify-demo-cli\napp-paths:\n  - src/**\n"):
    body = "".join("## %s\n\nText.\n\n" % s for s in sections)
    return "---\n%sdescription: Drives the demo CLI.\n---\n\n# Driver\n\n%s" % (frontmatter, body)


def feature(h2s=H2S):
    return "# Greet\n\nA user greets.\n\n" + "".join("## %s\n\nText.\n\n" % h for h in h2s)


class CheckDriver(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)
        write(os.path.join(self.dir, "SKILL.md"), skill_md())
        write(os.path.join(self.dir, "features", "README.md"), "# Map\n\n- [Greet](./greet.md)\n")
        write(os.path.join(self.dir, "features", "greet.md"), feature())

    def run_script(self, target=None):
        return subprocess.run(
            ["python3", SCRIPT, target or self.dir],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_complete_driver_passes(self):
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_each_missing_section_exits_1_and_names_it(self):
        for missing in SECTIONS:
            with self.subTest(section=missing):
                write(os.path.join(self.dir, "SKILL.md"), skill_md([s for s in SECTIONS if s != missing]))
                r = self.run_script()
                self.assertEqual(r.returncode, 1)
                self.assertIn(missing, r.stderr)
                self.assertIn("SKILL.md", r.stderr)

    def test_missing_index_exits_1(self):
        os.remove(os.path.join(self.dir, "features", "README.md"))
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("features/README.md", r.stderr)

    def test_feature_file_not_in_index_exits_1(self):
        write(os.path.join(self.dir, "features", "extra.md"), feature())
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("extra.md", r.stderr)

    def test_each_missing_feature_h2_exits_1_and_names_it(self):
        for missing in ["Sub-features", "How to get to it (user POV)", "Gotchas"]:
            with self.subTest(h2=missing):
                write(os.path.join(self.dir, "features", "greet.md"), feature([h for h in H2S if h != missing]))
                r = self.run_script()
                self.assertEqual(r.returncode, 1)
                self.assertIn(missing, r.stderr)
                self.assertIn("greet.md", r.stderr)

    def test_missing_driving_h2_exits_1(self):
        write(os.path.join(self.dir, "features", "greet.md"), feature(H2S[:2] + H2S[3:]))
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("Driving it with", r.stderr)

    def test_any_harness_name_is_accepted(self):
        write(os.path.join(self.dir, "features", "greet.md"), feature(H2S[:2] + ["Driving it with a PTY"] + H2S[3:]))
        self.assertEqual(self.run_script().returncode, 0)

    def test_missing_name_key_exits_1(self):
        write(os.path.join(self.dir, "SKILL.md"), skill_md(frontmatter="app-paths:\n  - src/**\n"))
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("name", r.stderr)

    def test_missing_app_paths_key_exits_1(self):
        write(os.path.join(self.dir, "SKILL.md"), skill_md(frontmatter="name: verify-demo-cli\n"))
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("app-paths", r.stderr)

    def test_empty_app_paths_exits_1(self):
        write(os.path.join(self.dir, "SKILL.md"), skill_md(frontmatter="name: verify-demo-cli\napp-paths:\n"))
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("app-paths", r.stderr)

    def test_missing_skill_md_exits_1(self):
        os.remove(os.path.join(self.dir, "SKILL.md"))
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("SKILL.md", r.stderr)

    def test_example_feature_map_passes_the_feature_checks(self):
        write(os.path.join(self.dir, "SKILL.md"), skill_md())
        shutil.rmtree(os.path.join(self.dir, "features"))
        shutil.copytree(EXAMPLE, os.path.join(self.dir, "features"))
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_feature_name_that_is_a_tail_of_another_link_exits_1(self):
        write(os.path.join(self.dir, "features", "README.md"), "# Map\n\n- [Greet](./greet.md)\n- [R](./research.md)\n")
        write(os.path.join(self.dir, "features", "research.md"), feature())
        write(os.path.join(self.dir, "features", "search.md"), feature())
        r = self.run_script()
        self.assertEqual(r.returncode, 1)
        self.assertIn("search.md", r.stderr)

    def test_unindented_app_paths_dashes_pass(self):
        write(os.path.join(self.dir, "SKILL.md"), skill_md(frontmatter="name: verify-demo-cli\napp-paths:\n- src/**\n"))
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
