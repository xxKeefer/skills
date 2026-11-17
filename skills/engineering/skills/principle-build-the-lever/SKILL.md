---
name: principle-build-the-lever
description: "Apply to non-trivial work: edits, migrations, analyses, checks. Build a tool only when it saves time or tokens, or when the result must be deterministic."
disable-model-invocation: true
---

# Build the Lever

A tool earns its place when it does one of these:

- It saves time or tokens, such as a codemod that makes fifty edits that you would otherwise make by hand.
- It gives a deterministic result that a reviewer can run again, such as a check that exits non-zero on the bug.

A judgement that a model already makes well, such as whether a line is a comment, is not a lever. A script for it adds code and misses, and no value. Read the input, and decide.

- Do the first unit by hand. Then build the tool, and prove it by running it on that unit. Make it safe to run again.
- A deterministic tool beats a fan-out of subagents. When you do fan out, write the recipe, the check, and the limits as one skill that the subagents read and cannot edit.
- Build the smallest script that does or proves the job. Do not build a framework.
- Commit the tool when the work outlives the session.

Test question: does this tool save time or tokens, or make a result deterministic? If neither, do the work without it.
