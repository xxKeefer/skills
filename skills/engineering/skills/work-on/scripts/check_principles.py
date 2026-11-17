#!/usr/bin/env python3
"""Check the principle skills and the index in work-on. Usage: check_principles.py <repo root>.
Exit 0 when all is well. Exit 1 with one error line for each fault."""
import os
import re
import sys

GROUPS = ["Core", "Architecture", "Verification", "Delegation", "Meta"]
EXPECTED = """
principle-attack-the-premise principle-boundary-discipline principle-build-the-lever
principle-encode-lessons-in-structure principle-exhaust-the-design-space
principle-experience-first principle-explain-the-number principle-fix-root-causes
principle-foundational-thinking principle-guard-the-context-window
principle-laziness-protocol principle-make-operations-idempotent
principle-migrate-callers-then-delete-legacy-apis principle-minimize-reader-load
principle-model-the-domain principle-never-block-on-the-human
principle-outcome-oriented-execution principle-prove-it-works
principle-redesign-from-first-principles
principle-separate-before-serializing-shared-state principle-sequence-verifiable-units
principle-subtract-before-you-add principle-test-behavior-not-implementation
principle-type-system-discipline
""".split()


def frontmatter(path):
    with open(path) as f:
        text = f.read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fields = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fields[k.strip()] = v.strip()
    return fields


def main(root):
    skills = os.path.join(root, "skills", "engineering", "skills")
    errors = []
    folders = sorted(
        d for d in os.listdir(skills)
        if d.startswith("principle-") and os.path.isdir(os.path.join(skills, d))
    )
    for name in EXPECTED:
        if name not in folders:
            errors.append(f"missing {name}")
    for name in folders:
        if name not in EXPECTED:
            errors.append(f"extra {name}")
            continue
        path = os.path.join(skills, name, "SKILL.md")
        if not os.path.isfile(path):
            errors.append(f"{name}: no SKILL.md")
            continue
        fields = frontmatter(path)
        if fields.get("name") != name:
            errors.append(f"{name}: name must equal the folder name")
        if fields.get("disable-model-invocation") != "true":
            errors.append(f"{name}: disable-model-invocation must be true")

    with open(os.path.join(skills, "work-on", "SKILL.md")) as f:
        text = f.read()
    for group in GROUPS:
        if not re.search(rf"^\*\*{group}\*\*\s*$", text, re.M):
            errors.append(f"work-on: no group heading {group}")
    entries = re.findall(r"^- `(principle-[a-z-]+)`", text, re.M)
    for name in entries:
        if name not in folders:
            errors.append(f"work-on: index entry {name} has no folder")
    for name in folders:
        if name not in entries:
            errors.append(f"work-on: no index entry {name}")

    for line in errors:
        print(line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
