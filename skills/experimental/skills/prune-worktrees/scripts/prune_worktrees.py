#!/usr/bin/env python3
"""Finds stale git worktrees, and removes them after the user approves the plan.

  prune_worktrees.py plan [--stale-days 7]   prints the plan as JSON
  prune_worktrees.py apply --plan FILE       removes the rows whose action is not keep
"""
import argparse
import json
import os
import subprocess
import sys
import time


def git(*args, cwd=None, check=True):
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and out.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{out.stderr.strip()}")
    return out


def ok(*args, cwd=None):
    return git(*args, cwd=cwd, check=False).returncode == 0


def worktrees():
    """Returns [{path, branch}] for each worktree, the main worktree first. branch is None when HEAD is detached."""
    rows = []
    for line in git("worktree", "list", "--porcelain").stdout.splitlines():
        if line.startswith("worktree "):
            rows.append({"path": line[len("worktree "):], "branch": None})
        elif line.startswith("branch refs/heads/"):
            rows[-1]["branch"] = line[len("branch refs/heads/"):]
    return rows


def dirty(path):
    return bool(git("status", "--porcelain", cwd=path).stdout.strip())


def pull_requests(branch):
    out = subprocess.run(
        ["gh", "pr", "list", "--head", branch, "--state", "all", "--json", "number,state,headRefOid"],
        capture_output=True, text=True,
    )
    if out.returncode:
        raise RuntimeError(f"gh pr list failed for {branch}:\n{out.stderr.strip()}")
    return json.loads(out.stdout or "[]")


def in_merged_pr(branch, pr):
    """Returns True when every commit on the branch is in the head that the PR merged."""
    head = pr["headRefOid"]
    if not ok("cat-file", "-e", f"{head}^{{commit}}"):
        git("fetch", "-q", "origin", f"pull/{pr['number']}/head", check=False)
    return ok("merge-base", "--is-ancestor", branch, head)


def default_base():
    out = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", check=False)
    return out.stdout.strip() if out.returncode == 0 else None


def classify(tree, others, base, stale_days):
    """Returns the action and reason for one worktree, and the path of the worktree that holds its stack."""
    branch, path = tree["branch"], tree["path"]
    if branch is None:
        return "keep", "HEAD is detached", None
    if dirty(path):
        return "keep", "uncommitted changes", None

    prs = pull_requests(branch)
    merged = next((p for p in prs if p["state"] == "MERGED"), None)
    if merged:
        if in_merged_pr(branch, merged):
            return "remove-branch", f"PR #{merged['number']} is merged", None
        return "keep", f"PR #{merged['number']} is merged, but the branch has later commits", None

    on_base = base is not None and ok("merge-base", "--is-ancestor", branch, base)
    if not on_base:
        for other in others:
            if other["branch"] and other["branch"] != branch and ok("merge-base", "--is-ancestor", branch, other["branch"]):
                return "remove-worktree", f"the stack in {other['path']} holds this branch", other["path"]

    open_pr = next((p for p in prs if p["state"] == "OPEN"), None)
    if open_pr:
        return "keep", f"PR #{open_pr['number']} is open", None

    last = int(git("log", "-1", "--format=%ct", branch).stdout.strip())
    days = int((time.time() - last) // 86400)
    if days >= stale_days:
        return "remove-worktree", f"no PR, and no commit for {days} days", None
    return "keep", f"no PR, last commit {days} days ago", None


def plan(stale_days):
    trees = worktrees()
    here = os.path.realpath(git("rev-parse", "--show-toplevel").stdout.strip())
    base = default_base()
    rows = []
    for tree in trees[1:]:
        if os.path.realpath(tree["path"]) == here:
            continue
        others = [t for t in trees[1:] if t is not tree]
        action, reason, held_by = classify(tree, others, base, stale_days)
        rows.append({**tree, "action": action, "reason": reason, "held_by": held_by})
    return rows


def apply(rows):
    """Removes each planned worktree, and the branch of each merged PR. Returns the failures."""
    failures = []
    for row in rows:
        if row["action"] == "keep":
            continue
        path, branch = row["path"], row["branch"]
        if os.path.exists(path) and dirty(path):
            failures.append(f"{path}: changed after the plan, skipped")
            continue
        removed = git("worktree", "remove", path, check=False)
        if removed.returncode:
            failures.append(f"{path}: {removed.stderr.strip()}")
            continue
        print(f"removed worktree: {path}")
        if row["action"] == "remove-branch":
            git("branch", "-D", branch)
            print(f"deleted branch: {branch}")
    git("worktree", "prune")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("--stale-days", type=int, default=7)
    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--plan", required=True)
    args = parser.parse_args()
    try:
        if args.command == "plan":
            git("fetch", "-q", "--prune", "origin", check=False)
            print(json.dumps(plan(args.stale_days), indent=2))
            return
        with open(args.plan) as f:
            failures = apply(json.load(f))
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    for failure in failures:
        print(failure, file=sys.stderr)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
