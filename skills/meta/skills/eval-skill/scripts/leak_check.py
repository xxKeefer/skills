#!/usr/bin/env python3
import re
import sys
from pathlib import Path

WORDS = ["eval", "test", "judge", "experiment", "rubric", "score", "compare", "benchmark", "candidate", "arena"]
PATTERN = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(WORDS) + r")s?(?![A-Za-z0-9])", re.IGNORECASE)


def main(folder, prompt_file):
    hits = []
    for path in sorted(Path(folder).rglob("*")):
        rel = path.relative_to(folder).as_posix()
        if rel.startswith(".claude/skills/"):
            continue
        for w in dict.fromkeys(m.lower() for m in PATTERN.findall(rel)):
            hits.append(f"{rel}: {w}")
    with open(prompt_file) as f:
        for w in dict.fromkeys(m.lower() for m in PATTERN.findall(f.read())):
            hits.append(f"prompt: {w}")
    if hits:
        print("\n".join(hits))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
