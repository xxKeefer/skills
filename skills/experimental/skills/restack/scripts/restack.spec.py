#!/usr/bin/env python3
"""Run: python3 restack.spec.py"""
import os
import subprocess
import sys
import tempfile
import unittest

import restack as rs

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "restack.py")

FAKE_GH = """#!/usr/bin/env python3
import os, sys
args = sys.argv[1:]
head = args[args.index("--head") + 1]
merged = os.environ.get("FAKE_GH_MERGED", "").split(",")
print(1 if head in merged else 0)
"""


class Repo(unittest.TestCase):
    """A clone of a bare origin, with git and gh isolated from the user's setup."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = self._tmp.name
        self.origin = os.path.join(tmp, "origin.git")
        self.root = os.path.join(tmp, "work")
        bin_dir = os.path.join(tmp, "bin")
        os.makedirs(bin_dir)
        gh = os.path.join(bin_dir, "gh")
        with open(gh, "w") as f:
            f.write(FAKE_GH)
        os.chmod(gh, 0o755)
        config = os.path.join(tmp, "gitconfig")
        with open(config, "w") as f:
            f.write("[user]\n\tname = t\n\temail = t@t\n[init]\n\tdefaultBranch = main\n")
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": config,
            "GIT_CONFIG_NOSYSTEM": "1",
            "PATH": bin_dir + os.pathsep + os.environ["PATH"],
            "FAKE_GH_MERGED": "",
        }
        subprocess.run(["git", "init", "-q", "--bare", self.origin], check=True, env=self.env)
        subprocess.run(["git", "clone", "-q", self.origin, self.root], check=True, env=self.env)
        self.commit("base.txt", "base\n", "base")
        self.git("push", "-q", "-u", "origin", "main")
        self.git("remote", "set-head", "origin", "main")

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args, cwd=None):
        out = subprocess.run(
            ["git", *args], cwd=cwd or self.root, env=self.env, capture_output=True, text=True
        )
        if out.returncode:
            raise AssertionError(f"git {' '.join(args)} failed:\n{out.stderr}")
        return out.stdout.strip()

    def commit(self, name, text, message):
        with open(os.path.join(self.root, name), "w") as f:
            f.write(text)
        self.git("add", name)
        self.git("commit", "-q", "-m", message)

    def branch(self, name, *files):
        self.git("switch", "-q", "-c", name)
        for f in files:
            self.commit(f, f"{f}\n", f"add {f}")

    def on_main(self, change):
        """Adds a commit to origin/main from local main, then returns to the branch it started on."""
        current = self.git("branch", "--show-current")
        self.git("switch", "-q", "main")
        change()
        self.git("push", "-q", "origin", "main")
        self.git("switch", "-q", current)

    def squash_merge(self, branch):
        """Squash-merges a branch into origin/main, as GitHub does, and keeps the local branch."""
        def squash():
            self.git("merge", "-q", "--squash", branch)
            self.git("commit", "-q", "-m", f"squash {branch}")
        self.on_main(squash)
        self.env["FAKE_GH_MERGED"] = ",".join(filter(None, [self.env["FAKE_GH_MERGED"], branch]))

    def advance_main(self, name, text=None):
        self.on_main(lambda: self.commit(name, text or f"{name}\n", f"main {name}"))

    def subjects(self, rev_range):
        return self.git("log", "--format=%s", "--reverse", rev_range).splitlines()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *args], cwd=self.root, env=self.env, capture_output=True, text=True
        )

    def build_stack(self):
        """Builds a three-branch stack: a and b are pushed, c is local only. HEAD is c."""
        self.branch("a", "a1.txt", "a2.txt")
        self.git("push", "-q", "-u", "origin", "a")
        self.branch("b", "b1.txt")
        self.git("push", "-q", "-u", "origin", "b")
        self.branch("c", "c1.txt")


class CutPoint(unittest.TestCase):
    def test_returns_none_when_no_branch_is_merged(self):
        self.assertIsNone(rs.cut_point(["a", "b", "c"], set()))

    def test_returns_the_top_merged_branch(self):
        self.assertEqual(rs.cut_point(["a", "b", "c"], {"a", "b"}), "b")

    def test_rejects_a_merged_branch_above_an_unmerged_branch(self):
        with self.assertRaises(rs.StackError):
            rs.cut_point(["a", "b", "c"], {"b"})


class Restack(Repo):
    def test_moves_every_branch_onto_the_new_main_when_nothing_is_merged(self):
        self.build_stack()
        self.advance_main("m.txt")

        out = self.run_cli()

        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(self.subjects("origin/main..c"), ["add a1.txt", "add a2.txt", "add b1.txt", "add c1.txt"])
        self.assertEqual(self.git("merge-base", "origin/main", "a"), self.git("rev-parse", "origin/main"))
        self.assertEqual(self.git("rev-parse", "origin/b"), self.git("rev-parse", "b"))

    def test_drops_the_commits_of_a_squash_merged_bottom_branch(self):
        self.build_stack()
        self.squash_merge("a")

        out = self.run_cli()

        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(self.subjects("origin/main..c"), ["add b1.txt", "add c1.txt"])
        self.assertEqual(self.git("rev-parse", "origin/b"), self.git("rev-parse", "b"))
        self.assertEqual(self.git("branch", "--list", "a"), "")

    def test_does_not_push_a_branch_that_is_not_on_origin(self):
        self.build_stack()
        self.squash_merge("a")

        self.run_cli()

        self.assertEqual(self.git("ls-remote", "--heads", "origin", "c"), "")

    def test_drops_two_merged_branches_at_once(self):
        self.build_stack()
        self.squash_merge("a")
        self.squash_merge("b")

        out = self.run_cli()

        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(self.subjects("origin/main..c"), ["add c1.txt"])
        self.assertEqual(self.git("branch", "--list", "a", "b"), "")

    def test_stops_when_a_merged_branch_is_above_an_unmerged_branch(self):
        self.build_stack()
        self.env["FAKE_GH_MERGED"] = "b"
        before = self.git("rev-parse", "c")

        out = self.run_cli()

        self.assertNotEqual(out.returncode, 0)
        self.assertIn("b", out.stderr)
        self.assertEqual(self.git("rev-parse", "c"), before)

    def test_stops_when_a_stack_branch_is_checked_out_in_another_worktree(self):
        self.build_stack()
        self.git("worktree", "add", "-q", os.path.join(self._tmp.name, "wt-b"), "b")
        self.advance_main("m.txt")
        before = self.git("rev-parse", "c")

        out = self.run_cli()

        self.assertNotEqual(out.returncode, 0)
        self.assertIn("wt-b", out.stderr)
        self.assertEqual(self.git("rev-parse", "c"), before)

    def test_stops_when_run_from_a_branch_below_the_top(self):
        self.build_stack()
        self.git("switch", "-q", "b")

        out = self.run_cli()

        self.assertNotEqual(out.returncode, 0)
        self.assertIn("c", out.stderr)

    def test_stops_when_the_working_tree_has_changes(self):
        self.build_stack()
        with open(os.path.join(self.root, "c1.txt"), "w") as f:
            f.write("dirty\n")

        out = self.run_cli()

        self.assertNotEqual(out.returncode, 0)
        self.assertIn("Commit or stash", out.stderr)

    def test_finishes_the_push_and_delete_on_a_second_run_after_a_conflict(self):
        self.build_stack()
        self.squash_merge("a")
        self.advance_main("b1.txt", "main version\n")

        first = self.run_cli()

        self.assertNotEqual(first.returncode, 0)
        self.assertIn("run restack again", first.stderr)
        with open(os.path.join(self.root, "b1.txt"), "w") as f:
            f.write("resolved\n")
        self.git("add", "b1.txt")
        subprocess.run(
            ["git", "-c", "core.editor=true", "rebase", "--continue"],
            cwd=self.root, env=self.env, check=True, capture_output=True,
        )

        second = self.run_cli()

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.subjects("origin/main..c"), ["add b1.txt", "add c1.txt"])
        self.assertEqual(self.git("rev-parse", "origin/b"), self.git("rev-parse", "b"))
        self.assertEqual(self.git("branch", "--list", "a"), "")


if __name__ == "__main__":
    unittest.main()
