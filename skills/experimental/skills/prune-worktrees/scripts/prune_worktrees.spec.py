#!/usr/bin/env python3
"""Run: python3 prune_worktrees.spec.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prune_worktrees.py")

FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
head = args[args.index("--head") + 1]
print(json.dumps(json.loads(os.environ.get("FAKE_GH_PRS", "{}")).get(head, [])))
"""

OLD = "2020-01-01T00:00:00Z"


class Repo(unittest.TestCase):
    """A clone of a bare origin with sibling worktrees, and git and gh isolated from the user's setup."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = os.path.realpath(self._tmp.name)
        origin = os.path.join(self.tmp, "origin.git")
        self.root = os.path.join(self.tmp, "repo")
        bin_dir = os.path.join(self.tmp, "bin")
        os.makedirs(bin_dir)
        gh = os.path.join(bin_dir, "gh")
        with open(gh, "w") as f:
            f.write(FAKE_GH)
        os.chmod(gh, 0o755)
        config = os.path.join(self.tmp, "gitconfig")
        with open(config, "w") as f:
            f.write("[user]\n\tname = t\n\temail = t@t\n[init]\n\tdefaultBranch = main\n")
        self.prs = {}
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": config,
            "GIT_CONFIG_NOSYSTEM": "1",
            "PATH": bin_dir + os.pathsep + os.environ["PATH"],
        }
        subprocess.run(["git", "init", "-q", "--bare", origin], check=True, env=self.env)
        subprocess.run(["git", "clone", "-q", origin, self.root], check=True, env=self.env)
        self.commit(self.root, "base.txt", "base")
        self.git("push", "-q", "-u", "origin", "main")
        self.git("remote", "set-head", "origin", "main")

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args, cwd=None, env=None):
        out = subprocess.run(["git", *args], cwd=cwd or self.root, env=env or self.env, capture_output=True, text=True)
        if out.returncode:
            raise AssertionError(f"git {' '.join(args)} failed:\n{out.stderr}")
        return out.stdout.strip()

    def commit(self, cwd, name, message, date=None):
        with open(os.path.join(cwd, name), "w") as f:
            f.write(f"{message}\n")
        env = {**self.env, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date} if date else None
        self.git("add", name, cwd=cwd)
        self.git("commit", "-q", "-m", message, cwd=cwd, env=env)

    def worktree(self, branch, base="main", date=None):
        """Adds a worktree on a new branch with one commit, and returns its path."""
        path = os.path.join(self.tmp, f"repo.{branch}")
        self.git("worktree", "add", "-q", "-b", branch, path, base)
        self.commit(path, f"{branch}.txt", f"add {branch}", date)
        return path

    def pr(self, branch, number, state, head=None):
        self.prs[branch] = [{"number": number, "state": state, "headRefOid": head or self.git("rev-parse", branch)}]

    def plan(self, *args):
        env = {**self.env, "FAKE_GH_PRS": json.dumps(self.prs)}
        out = subprocess.run([sys.executable, SCRIPT, "plan", *args], cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return {os.path.basename(row["path"]): row for row in json.loads(out.stdout)}

    def apply(self, rows):
        plan_file = os.path.join(self.tmp, "plan.json")
        with open(plan_file, "w") as f:
            json.dump(list(rows.values()), f)
        return subprocess.run([sys.executable, SCRIPT, "apply", "--plan", plan_file], cwd=self.root, env=self.env, capture_output=True, text=True)


class Plan(Repo):
    def test_removes_the_worktree_and_branch_of_a_merged_pr(self):
        self.worktree("done")
        self.pr("done", 1, "MERGED")

        row = self.plan()["repo.done"]

        self.assertEqual(row["action"], "remove-branch")
        self.assertIn("#1", row["reason"])

    def test_keeps_a_merged_branch_with_commits_after_the_merge(self):
        path = self.worktree("done")
        self.pr("done", 1, "MERGED")
        self.commit(path, "late.txt", "late fix")

        self.assertEqual(self.plan()["repo.done"]["action"], "keep")

    def test_keeps_a_worktree_with_uncommitted_changes(self):
        path = self.worktree("done")
        self.pr("done", 1, "MERGED")
        with open(os.path.join(path, "new.txt"), "w") as f:
            f.write("x")

        row = self.plan()["repo.done"]

        self.assertEqual(row["action"], "keep")
        self.assertIn("uncommitted", row["reason"])

    def test_removes_only_the_worktree_of_a_branch_that_another_worktree_stacks_on(self):
        self.worktree("lower")
        top = self.worktree("upper", base="lower")
        self.pr("lower", 2, "OPEN")

        row = self.plan()["repo.lower"]

        self.assertEqual(row["action"], "remove-worktree")
        self.assertEqual(row["held_by"], top)

    def test_keeps_the_top_branch_of_a_stack(self):
        self.worktree("lower")
        self.worktree("upper", base="lower")

        self.assertEqual(self.plan()["repo.upper"]["action"], "keep")

    def test_keeps_a_worktree_with_an_open_pr(self):
        self.worktree("review", date=OLD)
        self.pr("review", 3, "OPEN")

        self.assertEqual(self.plan()["repo.review"]["action"], "keep")

    def test_removes_only_the_worktree_of_an_old_branch_with_no_pr(self):
        self.worktree("idle", date=OLD)

        row = self.plan()["repo.idle"]

        self.assertEqual(row["action"], "remove-worktree")
        self.assertIn("no PR", row["reason"])

    def test_keeps_a_recent_branch_with_no_pr(self):
        self.worktree("fresh")

        self.assertEqual(self.plan()["repo.fresh"]["action"], "keep")

    def test_lists_no_row_for_the_main_worktree(self):
        self.worktree("fresh")

        self.assertNotIn("repo", self.plan())


class Apply(Repo):
    def test_removes_each_planned_worktree_and_each_merged_branch(self):
        done = self.worktree("done")
        self.pr("done", 1, "MERGED")
        idle = self.worktree("idle", date=OLD)
        fresh = self.worktree("fresh")

        out = self.apply(self.plan())

        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertFalse(os.path.exists(done))
        self.assertFalse(os.path.exists(idle))
        self.assertTrue(os.path.exists(fresh))
        self.assertEqual(self.git("branch", "--list", "done"), "")
        self.assertNotEqual(self.git("branch", "--list", "idle"), "")

    def test_skips_a_worktree_that_changed_after_the_plan(self):
        done = self.worktree("done")
        self.pr("done", 1, "MERGED")
        rows = self.plan()
        with open(os.path.join(done, "late.txt"), "w") as f:
            f.write("x")

        out = self.apply(rows)

        self.assertNotEqual(out.returncode, 0)
        self.assertTrue(os.path.exists(done))
        self.assertNotEqual(self.git("branch", "--list", "done"), "")


if __name__ == "__main__":
    unittest.main()
