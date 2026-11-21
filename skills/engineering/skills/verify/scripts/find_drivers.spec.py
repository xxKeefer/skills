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


def driver(root, name, paths, repo="demo"):
    head = "---\nname: %s\n" % name
    if repo is not None:
        head += "repo: %s\n" % repo
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
        write(os.path.join(self.repo, rel), "change " + rel + "\n")
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
        driver(self.home, "verify-other-cli", ["src/**"], repo="other")
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

    def test_driver_of_a_longer_repo_name_is_not_matched(self):
        a = driver(self.repo_skills, "verify-demo-x", ["src/**"])
        driver(self.repo_skills, "verify-demo-web-x", ["src/**"], repo="demo-web")
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), a)

    def test_driver_with_no_repo_key_is_named_and_not_matched(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["src/**"], repo=None)
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")
        self.assertIn("no repo: " + path, r.stderr)

    def test_driver_with_another_repo_value_is_named_and_not_matched(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["src/**"], repo="other")
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")
        self.assertIn("no repo: " + path, r.stderr)

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

    def test_base_that_moved_after_the_fork_is_ignored(self):
        git(self.repo, "checkout", "-q", "main")
        self.change("src/x.py")
        git(self.repo, "checkout", "-q", "work")
        driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        self.change("docs/a.md")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")

    def test_leading_double_star_matches_a_root_file(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["**/*.py"])
        self.change("a.py")
        self.assertEqual(self.run_script().stdout.strip(), path)

    def test_leading_double_star_matches_a_deep_file(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["**/*.py"])
        self.change("src/deep/a.py")
        self.assertEqual(self.run_script().stdout.strip(), path)

    def test_middle_double_star_matches_zero_depth(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["app/**/x.py"])
        self.change("app/x.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), path)

    def test_dot_in_glob_is_literal(self):
        driver(self.repo_skills, "verify-demo-cli", ["src/*.py"])
        self.change("src/apy")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")

    def test_question_mark_matches_one_character(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["src/?.py"])
        self.change("src/a.py")
        self.assertEqual(self.run_script().stdout.strip(), path)

    def test_question_mark_does_not_match_two_characters(self):
        driver(self.repo_skills, "verify-demo-cli", ["src/?.py"])
        self.change("src/ab.py")
        self.assertEqual(self.run_script().stdout.strip(), "no driver")

    def test_quoted_app_paths_match(self):
        a = driver(self.repo_skills, "verify-demo-cli", ['"src/**"'])
        b = driver(self.repo_skills, "verify-demo-web", ["'docs/*.md'"])
        self.change("src/a.py")
        self.change("docs/a.md")
        r = self.run_script()
        self.assertEqual(sorted(r.stdout.split()), sorted([a, b]))

    def test_one_driver_from_repo_and_home_prints_once(self):
        path = driver(self.repo_skills, "verify-demo-cli", ["src/**"])
        os.symlink(os.path.dirname(path), os.path.join(self.home, "verify-demo-cli"))
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(len(r.stdout.split()), 1)

    def test_unindented_dashes_in_app_paths_match(self):
        path = os.path.join(self.repo_skills, "verify-demo-cli", "SKILL.md")
        write(path, "---\nname: verify-demo-cli\nrepo: demo\napp-paths:\n- src/**\n---\n")
        self.change("src/a.py")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), path)

    def test_untracked_path_is_relative_to_the_repo_root(self):
        path = driver(self.home, "verify-demo-cli", ["src/**"])
        write(os.path.join(self.repo, "src", "new.py"), "untracked\n")
        r = subprocess.run(
            ["python3", SCRIPT, "--repo", os.path.join(self.repo, "src"), "--base", "main", "--home", self.home],
            capture_output=True, text=True,
        )
        self.assertEqual(r.stdout.strip(), path)

    def test_items_of_a_later_key_are_not_app_paths(self):
        path = os.path.join(self.repo_skills, "verify-demo-cli", "SKILL.md")
        write(path, "---\nname: verify-demo-cli\nrepo: demo\napp-paths:\n  - src/**\ntags:\n  - docs/**\n---\n")
        self.change("docs/a.md")
        r = self.run_script()
        self.assertEqual(r.stdout.strip(), "no driver")


if __name__ == "__main__":
    unittest.main()
