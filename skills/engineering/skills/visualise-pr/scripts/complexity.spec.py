#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "complexity.py")

BASE = """def keep(a):
    return a


def grow(a):
    return a


def gone(a):
    return a
"""

HEAD = """def keep(a):
    return a


def grow(a):
    if a:
        return 1
    if a > 2:
        return 2
    return a


def fresh(a):
    return a
"""


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout.strip()


def run(repo, *args, env=None):
    return subprocess.run([sys.executable, SCRIPT, *args], cwd=repo, capture_output=True, text=True, env=env)


class ComplexityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        os.makedirs(os.path.join(self.repo, "src"))
        self.write("src/a.py", BASE)
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "base")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self.write("src/a.py", HEAD)
        self.write("src/b.py", "def new(a):\n    return a\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "head")
        self.head = git(self.repo, "rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, text):
        with open(os.path.join(self.repo, path), "w") as f:
            f.write(text)

    def test_lists_only_changed_functions_with_base_and_head(self):
        result = run(self.repo, self.base, self.head, "src/a.py", "src/b.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.strip().split("\n")
        self.assertEqual(lines[0], "file\tfunction\tline\tbase_ccn\thead_ccn\tbase_nloc\thead_nloc")
        rows = {tuple(line.split("\t")[:2]): line.split("\t") for line in lines[1:]}
        self.assertNotIn(("src/a.py", "keep"), rows)
        self.assertEqual(rows[("src/a.py", "grow")], ["src/a.py", "grow", "5", "1", "3", "2", "6"])
        self.assertEqual(rows[("src/a.py", "fresh")], ["src/a.py", "fresh", "13", "-", "1", "-", "2"])
        self.assertEqual(rows[("src/a.py", "gone")], ["src/a.py", "gone", "-", "1", "-", "2", "-"])
        self.assertEqual(rows[("src/b.py", "new")], ["src/b.py", "new", "1", "-", "1", "-", "2"])

    def test_reads_refs_not_the_working_tree(self):
        self.write("src/a.py", BASE)
        result = run(self.repo, self.base, self.head, "src/a.py")
        self.assertIn("grow", result.stdout)

    def test_missing_lizard_exits_2_with_install_command(self):
        env = dict(os.environ, PATH=os.path.dirname(subprocess.run(["which", "git"], capture_output=True, text=True).stdout.strip()))
        result = run(self.repo, self.base, self.head, "src/a.py", env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pipx install lizard", result.stderr)


if __name__ == "__main__":
    unittest.main()
