---
name: principle-build-the-lever
description: "Apply to any non-trivial work: edits, migrations, analyses, checks. Build the tool that does the work or proves it, so that a reviewer can run it again."
disable-model-invocation: true
---

# Build the Lever

When the work is not trivial, build the tool that does it. A tool can be a codemod, a script, a generator, or a check that you can run again. Do not do the work by hand. The bar is triviality, not repetition. Skip the tool only for a couple of obvious edits.

- Do the first unit by hand. Then build the tool, and prove it by running it on that unit. Make it safe to run again.
- A deterministic tool beats a fan-out of subagents. When you do fan out, write the recipe, the check, and the limits as one skill that the subagents read and cannot edit.
- This principle produces a file. If the diff has no script, codemod, generator, or skill for subagents, you did not apply it. Commit the file when the work outlives the session.
- Build the smallest script that does or proves the job. Do not build a framework.
