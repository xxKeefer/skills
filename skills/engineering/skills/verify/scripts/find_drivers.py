#!/usr/bin/env python3
"""Find the verification drivers that match a diff.

A driver is `verify-<repo>-<app>/SKILL.md` in `<repo root>/.claude/skills/` or in
the home skills folder. Its frontmatter key `app-paths:` is a list of globs from
the repo root. `*` matches within one folder. `**` matches across folders.

Its frontmatter key `repo:` names the repo. Prints one driver path per line, or
`no driver`. A driver with no `app-paths` key is not matched, and a
`no app-paths: <path>` line goes to stderr. A driver whose `repo:` key is
missing or differs from the repo name is not matched, and a `no repo: <path>`
line goes to stderr.

Usage: find_drivers.py --repo <root> --base <ref> [--home ~/.claude/skills]
"""
import argparse
import glob
import os
import re
import subprocess
import sys


def git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write("git %s failed: %s\n" % (" ".join(args), r.stderr.strip()))
        sys.exit(1)
    return r.stdout


def repo_name(repo):
    url = git(repo, "remote", "get-url", "origin").strip()
    last = re.split(r"[/:]", url.rstrip("/"))[-1]
    return last[:-4] if last.endswith(".git") else last


def diff_paths(repo, base):
    merge_base = git(repo, "merge-base", base, "HEAD").strip()
    changed = git(repo, "diff", "--name-only", merge_base).splitlines()
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "--full-name").splitlines()
    return sorted(set(changed + untracked))


def glob_regex(pattern):
    out = ""
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            out += ".*"
            i += 2
        elif pattern[i] == "*":
            out += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(pattern[i])
            i += 1
    return re.compile("^" + out + "$")


def app_paths(skill_md):
    with open(skill_md) as f:
        lines = f.read().split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    paths = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if re.match(r"^app-paths:\s*$", line):
            paths = []
        elif paths is not None and re.match(r"^\s*-\s+", line):
            paths.append(re.sub(r"^\s*-\s+", "", line).strip().strip("\"'"))
        elif re.match(r"^\S", line):
            if paths is not None:
                break
    return paths


def repo_key(skill_md):
    with open(skill_md) as f:
        lines = f.read().split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^repo:\s*(\S.*?)\s*$", line)
        if m:
            return m.group(1).strip("\"'")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--home", default=os.path.expanduser("~/.claude/skills"))
    args = ap.parse_args()

    name = repo_name(args.repo)
    paths = diff_paths(args.repo, args.base)
    folders = [os.path.join(args.repo, ".claude", "skills"), args.home]

    found = []
    seen = set()
    for folder in folders:
        pattern = os.path.join(glob.escape(folder), "verify-%s-*" % glob.escape(name), "SKILL.md")
        for skill_md in sorted(glob.glob(pattern)):
            real = os.path.realpath(skill_md)
            if real in seen:
                continue
            seen.add(real)
            if repo_key(skill_md) != name:
                sys.stderr.write("no repo: %s\n" % skill_md)
                continue
            globs = app_paths(skill_md)
            if not globs:
                sys.stderr.write("no app-paths: %s\n" % skill_md)
                continue
            regexes = [glob_regex(g) for g in globs]
            if any(rx.match(p) for rx in regexes for p in paths):
                found.append(skill_md)

    print("\n".join(found) if found else "no driver")


if __name__ == "__main__":
    main()
