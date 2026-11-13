# Project rubric

## Step 3: Spawn the rubric

The rubric is a review rubric skill that the repo's `CLAUDE.md` or `AGENTS.md` names. With no such skill, it is the repo's `CODING_STANDARDS.md` or `CONTRIBUTING.md`. If the diff touches code the rubric covers, spawn one more `general-purpose` subagent with `model: "sonnet"`. It reads a written rubric, like a persona:

> Invoke the `<rubric skill name>` skill via the Skill tool, or read `<absolute path to the rubric file>`. If the file states no rule about how to write code, return `{"persona":"<rubric>","inScope":false,"findings":[]}`. Apply the rubric as a **review only** of the diff at `<SCRATCH>/diff.patch` (changed files in `<SCRATCH>/files.txt`): no edits, no PR comments. Only report problems on changed lines, verified against the code. Read `<PERSONAS>/../PERSONA-CONTRACT.md`, and follow its Findings and Code references sections. Return raw JSON only (no prose, no code fences), in the form that its "When a caller asks for JSON" section gives, with `"persona"` set to the skill name or the file name, and `category` set to the rubric section. Skip a rule that the repo's tooling already enforces. Severity: a defect the rubric calls out as a bug or contract violation → `change-requested`; a standards deviation → `nit`; a larger refactor idea → `future`.

## Step 4: Merge its findings

The project rubric overlaps the personas by design. When one of its findings names the same file, line, and problem as a persona finding, keep the persona's. Its remaining findings stand.
