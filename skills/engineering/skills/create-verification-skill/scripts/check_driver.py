#!/usr/bin/env python3
"""Check the layout of a verification driver.

A driver folder holds `SKILL.md` with the frontmatter keys `name`,
`repo`, and `app-paths`, and the H2 sections Launch, Doctor, Drive, Evidence, Cleanup, and
Helpers. It also holds `features/README.md`, which links each other file in
`features/`. Each feature file has the H2 sections `Sub-features`,
`How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`.

Prints `ok` and exits 0, or prints one error per line to stderr and exits 1.
Each error names the file, the missing item, and the fix.

Usage: check_driver.py <driver dir>
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent / "../../verify/scripts"))
from find_drivers import app_paths

SECTIONS = ["Launch", "Doctor", "Drive", "Evidence", "Cleanup", "Helpers"]
FEATURE_H2S = ["Sub-features", "How to get to it (user POV)", "Driving it with", "Gotchas"]


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


def check_skill(root):
    errors = []
    path = root / "SKILL.md"
    if not path.is_file():
        return ["SKILL.md: file is missing. Fix: add SKILL.md to the driver folder."]
    text = path.read_text()
    block = frontmatter(text)
    if block is None:
        errors.append("SKILL.md: frontmatter is missing. Fix: start the file with a --- block.")
        block = []
    if not any(re.match(r"^name:\s*\S", l) for l in block):
        errors.append("SKILL.md: frontmatter key `name` is missing. Fix: add `name: verify-<repo>-<app>`.")
    if not any(re.match(r"^repo:\s*\S", l) for l in block):
        errors.append("SKILL.md: frontmatter key `repo` is missing. Fix: add `repo: <repo>`, the last part of `git remote get-url origin` with no `.git`.")
    if not app_paths(path):
        errors.append("SKILL.md: frontmatter key `app-paths` is missing or empty. Fix: list the app globs from the repo root under `app-paths:`.")
    titles = h2_titles(text)
    for section in SECTIONS:
        if section not in titles:
            errors.append("SKILL.md: section `## %s` is missing. Fix: add the section." % section)
    return errors


def check_features(root):
    errors = []
    folder = root / "features"
    index = folder / "README.md"
    if not index.is_file():
        return ["features/README.md: file is missing. Fix: add an index that links each feature file."]
    index_text = index.read_text()
    for file in sorted(folder.glob("*.md")):
        name = file.name
        if name == "README.md":
            continue
        if not re.search(r"\((?:[^)\s]*/)?" + re.escape(name) + r"(?:[#\s][^)]*)?\)", index_text):
            errors.append("features/README.md: feature file `%s` is not in the index. Fix: add a link to it." % name)
        titles = h2_titles(file.read_text())
        for h2 in FEATURE_H2S:
            if not any(t == h2 or (h2 == "Driving it with" and t.startswith("Driving it with ")) for t in titles):
                shown = "Driving it with <harness>" if h2 == "Driving it with" else h2
                errors.append("features/%s: section `## %s` is missing. Fix: add the section." % (name, shown))
    return errors


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("usage: check_driver.py <driver dir>\n")
        sys.exit(2)
    root = Path(sys.argv[1])
    errors = check_skill(root) + check_features(root)
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
