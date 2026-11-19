#!/usr/bin/env python3
"""Check the principle skills and the index in work-on. Usage: check_principles.py <repo root>.
Exit 0 when all is well. Exit 1 with one error line for each fault."""
import re
import sys
from pathlib import Path

GROUPS = ["Core", "Architecture", "Verification", "Delegation", "Meta"]
EXPECTED = """
principle-build-the-lever principle-encode-lessons-in-structure principle-experience-first
principle-fix-root-causes principle-guard-the-context-window principle-make-operations-idempotent
principle-minimize-reader-load principle-model-the-domain principle-prove-it-works
principle-redesign-from-first-principles principle-separate-before-serializing-shared-state
principle-sequence-verifiable-units principle-subtract-before-you-add
principle-type-system-discipline
""".split()


def frontmatter(path):
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    fields = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fields[k.strip()] = v.strip()
    return fields


def check_folders(folders):
    errors = [f"missing {n}" for n in EXPECTED if n not in folders]
    errors += [f"extra {n}" for n in folders if n not in EXPECTED]
    return errors


def check_frontmatter(skills, folders):
    errors = []
    for name in folders:
        if name not in EXPECTED:
            continue
        path = skills / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"{name}: no SKILL.md")
            continue
        fields = frontmatter(path)
        if fields.get("name") != name:
            errors.append(f"{name}: name must equal the folder name")
        if fields.get("disable-model-invocation") != "true":
            errors.append(f"{name}: disable-model-invocation must be true")
    return errors


def check_index(text, folders):
    errors = []
    for group in GROUPS:
        if not re.search(rf"^\*\*{group}\*\*\s*$", text, re.M):
            errors.append(f"work-on: no group heading {group}")
    entries = re.findall(r"^- `(principle-[a-z-]+)`", text, re.M)
    errors += [f"work-on: index entry {n} has no folder" for n in entries if n not in folders]
    errors += [f"work-on: no index entry {n}" for n in folders if n not in entries]
    return errors


def main(root):
    skills = Path(root) / "skills" / "engineering" / "skills"
    folders = sorted(
        d.name for d in skills.iterdir() if d.name.startswith("principle-") and d.is_dir()
    )
    index = (skills / "work-on" / "SKILL.md").read_text()
    errors = check_folders(folders) + check_frontmatter(skills, folders) + check_index(index, folders)
    for line in errors:
        print(line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
