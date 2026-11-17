#!/usr/bin/env python3
"""Tests for find_drivers.py. Run: python3 find_drivers.spec.py"""
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "find_drivers.py")


def git(cwd, *args):
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def driver(root, name, paths):
    head = "---\nname: %s\n" % name
    if paths is not None:
        head += "app-paths:\n" + "".join("  - %s\n" % p for p in paths)
    write(os.path.join(root, name, "SKILL.md"), head + "---\n\n# Driver\n")
    return os.path.join(root, name, "SKILL.md")


class FindDrivers(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.home = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo)
        self.addCleanup(shutil.rmtree, self.home)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "remote", "add", "origin", "git@github.com:owner/demo.git")
        write(os.path.join(self.repo, "README.md"), "x\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "base")
        git(self.repo, "checkout", "-q", "-b", "work")
        self.repo_skills = os.path.join(self.repo, ".claude", "skills")

    def run_script(self, base="main"):
        return subprocess.run(
            ["python3", SCRIPT, "--repo", self.repo, "--base", base, "--home", self.home],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def change(self, rel):
        write(os.path.join(self.repo, rel), "change\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "change")

    def test_matching_path_returns_driver(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        self.change("src/a/b.py")
        r = self.run_script()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), path)

    def test_no_match_returns_no_driver(self):
        driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        self.change("docs/a.md")
        r = self.run_script()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "no driver")

    def test_no_drivers_at_all(self):
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "no driver")

    def test_repo_and_home_drivers_found_and_other_repo_skipped(self):
        a = driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        b = driver(self.home, "verify-demo-web", ["src/*.py"])
        driver(self.home, "verify-other-cli", ["src/**"])
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(sorted(r.stdout.split()), sorted([a, b]))

    def test_repo_name_from_url_forms(self):
        urls = [
            "git@host:owner/demo.git",
            "git@host:owner/demo",
            "https://host/owner/demo.git",
            "https://host/owner/demo",
        ]
        path = driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        self.change("src/a.py")
        for url in urls:
            git(self.repo, "remote", "set-url", "origin", url)
            r = self.run_script()
            self.assertEqual(r.stdout.strip(), path, url)

    def test_driver_without_app_paths_is_named_and_not_matched(self):
        path = driver(self.repo_skills, "verify-demo-cli", None)
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")
        self.assertIn("no app-paths: " + path, r.stderr)

    def test_working_tree_changes_count(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        write(os.path.join(self.repo, "src", "new.py"), "untracked\n")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), path)

    def test_unstaged_edit_counts(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["README.md"])
        write(os.path.join(self.repo, "README.md"), "edited\n")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), path)

    def test_single_star_does_not_cross_directories(self):
        driver(self.repo_skills, "verify-demo-cli", ["src/*.py"])
        self.change("src/deep/a.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")

    def test_bad_base_exits_1(self):
        r = self.run_script(base="nope")
        self.assertEqual(r.returncode, 1)
        self.assertIn("nope", r.stderr)


if __name__ == "__main__":
    unittest.main()
