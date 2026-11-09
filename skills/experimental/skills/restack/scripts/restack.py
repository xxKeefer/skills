#!/usr/bin/env python3
"""Moves a stack of branches onto the latest default branch, and drops each squash-merged branch.

Run it from the top branch of the stack:

  restack.py [--base origin/main]
"""
import argparse
import os
import subprocess
import sys


class StackError(Exception):
    pass


def git(*args, check=True):
    out = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and out.returncode:
        raise StackError(f"git {' '.join(args)} failed:\n{out.stderr.strip()}")
    return out


def lines(out):
    return [line for line in out.stdout.splitlines() if line]


def cut_point(stack, merged):
    """Returns the top merged branch of a bottom-first stack, or None when no branch is merged."""
    for lower, upper in zip(stack, stack[1:]):
        if upper in merged and lower not in merged:
            raise StackError(f"{upper} is merged, but {lower} below it is not. Merge the stack from the bottom.")
    return next((b for b in reversed(stack) if b in merged), None)


def default_base():
    out = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", check=False)
    if out.returncode:
        raise StackError("origin/HEAD is not set. Run git remote set-head origin --auto, or pass --base.")
    return out.stdout.strip()


def git_path(name):
    return git("rev-parse", "--git-path", name).stdout.strip()


def rebase_in_progress():
    return os.path.exists(git_path("rebase-merge")) or os.path.exists(git_path("rebase-apply"))


def stack_branches(base):
    """Returns the local branches between base and HEAD, bottom first."""
    branches = lines(git("for-each-ref", "--merged", "HEAD", "--no-merged", base, "--format=%(refname:short)", "refs/heads"))
    return sorted(branches, key=lambda b: int(git("rev-list", "--count", f"{base}..{b}").stdout))


def branches_above(current):
    return [b for b in lines(git("for-each-ref", "--contains", "HEAD", "--format=%(refname:short)", "refs/heads")) if b != current]


def other_worktrees():
    """Returns {branch: path} for each branch checked out in a worktree other than this one."""
    here = os.path.realpath(git("rev-parse", "--show-toplevel").stdout.strip())
    found, path = {}, None
    for line in lines(git("worktree", "list", "--porcelain")):
        if line.startswith("worktree "):
            path = line[len("worktree "):]
        elif line.startswith("branch refs/heads/") and os.path.realpath(path) != here:
            found[line[len("branch refs/heads/"):]] = path
    return found


def is_merged(branch):
    out = subprocess.run(
        ["gh", "pr", "list", "--head", branch, "--state", "merged", "--json", "number", "--jq", "length"],
        capture_output=True, text=True,
    )
    if out.returncode:
        raise StackError(f"gh pr list failed for {branch}:\n{out.stderr.strip()}")
    return int(out.stdout.strip() or 0) > 0


def read_state(path):
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        return {line.strip() for line in f if line.strip()}


def restack(base):
    git("fetch", "-q", "origin")
    if rebase_in_progress():
        raise StackError("A rebase is in progress. Finish it with git rebase --continue, then run restack again.")
    if lines(git("status", "--porcelain", "--untracked-files=no")):
        raise StackError("The working tree has changes. Commit or stash them first.")
    current = git("branch", "--show-current").stdout.strip()
    if not current:
        raise StackError("HEAD is not on a branch.")
    above = branches_above(current)
    if above:
        raise StackError(f"Run restack from the top branch of the stack: {', '.join(above)}.")

    stack = stack_branches(base)
    elsewhere = {b: p for b, p in other_worktrees().items() if b in stack}
    if elsewhere:
        held = ", ".join(f"{b} ({p})" for b, p in elsewhere.items())
        raise StackError(f"Git does not move a branch that another worktree has checked out: {held}. Remove those worktrees first.")

    merged = {b for b in stack if is_merged(b)}
    cut = cut_point(stack, merged)
    if cut == current:
        raise StackError(f"{current} is merged. The stack has no open branch to move.")

    state = git_path("restack-merged")
    to_delete = read_state(state) | merged
    with open(state, "w") as f:
        f.write("".join(f"{b}\n" for b in sorted(to_delete)))

    onto = ["--onto", base, cut] if cut else [base]
    rebased = git("rebase", "--update-refs", *onto, check=False)
    if rebased.returncode:
        if rebase_in_progress():
            raise StackError(
                f"{rebased.stdout.strip()}\nResolve the conflicts, run git rebase --continue, then run restack again."
            )
        raise StackError(f"git rebase failed:\n{rebased.stderr.strip()}")

    open_branches = [b for b in stack if b not in merged]
    pushed = [b for b in open_branches if git("rev-parse", "--verify", "-q", f"refs/remotes/origin/{b}", check=False).returncode == 0]
    if pushed:
        git("push", "-q", "--force-with-lease", "origin", *pushed)

    deleted = [b for b in sorted(to_delete) if git("rev-parse", "--verify", "-q", f"refs/heads/{b}", check=False).returncode == 0]
    for b in deleted:
        git("branch", "-D", b)
    os.remove(state)

    print(f"Moved onto {base}: {', '.join(open_branches)}")
    print(f"Pushed: {', '.join(pushed) or 'none'}")
    print(f"Deleted merged branches: {', '.join(deleted) or 'none'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="the branch to move the stack onto (default: origin/HEAD)")
    args = parser.parse_args()
    try:
        restack(args.base or default_base())
    except StackError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
