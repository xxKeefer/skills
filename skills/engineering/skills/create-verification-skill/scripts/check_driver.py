#!/usr/bin/env python3
"""Check the layout of a verification driver.

A driver folder holds `SKILL.md` with the frontmatter keys `name` and
`app-paths`, and the H2 sections Launch, Doctor, Drive, Evidence, Cleanup, and
Helpers. It also holds `features/README.md`, which links each other file in
`features/`. Each feature file has the H2 sections `Sub-features`,
`How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`.

Prints `ok` and exits 0, or prints one error per line to stderr and exits 1.
Each error names the file, the missing item, and the fix.

Usage: check_driver.py <driver dir>
"""
import os
import re
import sys

SECTIONS = ["Launch", "Doctor", "Drive", "Evidence", "Cleanup", "Helpers"]
FEATURE_H2S = ["Sub-features", "How to get to it (user POV)", "Driving it with", "Gotchas"]


def read(path):
    with open(path) as f:
        return f.read()


def h2_titles(text):
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", text, re.M)]


def frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    block = []
    for line in lines[1:]:
        if line.strip() == "---":
            return block
        block.append(line)
    return None


def check_skill(root, errors):
    path = os.path.join(root, "SKILL.md")
    if not os.path.isfile(path):
        errors.append("SKILL.md: file is missing. Fix: add SKILL.md to the driver folder.")
        return
    text = read(path)
    block = frontmatter(text)
    if block is None:
        errors.append("SKILL.md: frontmatter is missing. Fix: start the file with a --- block.")
        block = []
    if not any(re.match(r"^name:\s*\S", l) for l in block):
        errors.append("SKILL.md: frontmatter key `name` is missing. Fix: add `name: verify-<repo>-<app>`.")
    start = next((i for i, l in enumerate(block) if re.match(r"^app-paths:\s*$", l)), None)
    items = []
    if start is not None:
        for l in block[start + 1:]:
            if re.match(r"^\s+-\s+\S", l):
                items.append(l)
            elif re.match(r"^\S", l):
                break
    if not items:
        errors.append("SKILL.md: frontmatter key `app-paths` is missing or empty. Fix: list the app globs from the repo root under `app-paths:`.")
    titles = h2_titles(text)
    for section in SECTIONS:
        if section not in titles:
            errors.append("SKILL.md: section `## %s` is missing. Fix: add the section." % section)


def check_features(root, errors):
    folder = os.path.join(root, "features")
    index = os.path.join(folder, "README.md")
    if not os.path.isfile(index):
        errors.append("features/README.md: file is missing. Fix: add an index that links each feature file.")
        return
    index_text = read(index)
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md") or name == "README.md":
            continue
        if name not in index_text:
            errors.append("features/README.md: feature file `%s` is not in the index. Fix: add a link to it." % name)
        titles = h2_titles(read(os.path.join(folder, name)))
        for h2 in FEATURE_H2S:
            if not any(t == h2 or (h2 == "Driving it with" and t.startswith("Driving it with ")) for t in titles):
                shown = "Driving it with <harness>" if h2 == "Driving it with" else h2
                errors.append("features/%s: section `## %s` is missing. Fix: add the section." % (name, shown))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("usage: check_driver.py <driver dir>\n")
        sys.exit(2)
    root = sys.argv[1]
    errors = []
    check_skill(root, errors)
    check_features(root, errors)
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
