# Step Brief

You run one step of a handoff, from a cold start. The parent gives you the handoff path and the
step ID. The handoff is your only context.

Keep all work local. Commit to the current branch and push nothing. Edit only files inside this
repo and the handoff file.

## 1. Cold start

1. Read the handoff and every artifact the step references.
2. If the handoff says to resume from the stash `auto-handoff: <step>`, apply that stash.
3. If the step needs a decision that the handoff does not record, write a `D` entry and return.
4. If the step pushes, opens a PR, edits a ticket, deploys, or writes to any outside service, write
   an `N` entry with the exact action and return.

**Done when:** you can name the step's done line and its workflow.

## 2. Do the step

Use the first row that matches the step:

| Step | Workflow | What to do |
| ---- | -------- | ---------- |
| Names a skill | `skill: /<name>` | Run that skill. |
| Changes behaviour | `TDD` | Write a failing test at the step's seam and see it go red. Write the minimum code to go green. Then do a mutation check: break the new code, see the test go red, and restore the code. |
| Trivial tweak: copy, a variant, a single prop | `trivial` | Make the edit. Run the existing tests for the files you touched. |
| Anything else: docs, config, CI | `done line` | Make the change. |

If you find an unrecorded decision partway through, stash your changes as `auto-handoff: <step>`,
write a `D` entry, and return.

**Done when:** the step's done line holds.

## 3. Run the gates

Run the gates that the handoff or the repo guidance names. Use the test scope that the repo
guidance sets.

If a gate is red, fix the cause and run the gates again. After 3 fix attempts that leave a gate
red, stash your changes, write a `B` entry, and return.

To stash, include new files and name only the paths this step changed:
`git stash push --include-untracked -m "auto-handoff: <step>" -- <paths>`.

**Done when:** every gate is green.

## 4. Commit

1. Stage only the files this step changed.
2. Commit with the repo's commit convention.
3. Invoke `/update-handoff` on the handoff to mark the step done.

**Done when:** the commit exists and the handoff marks the step done.

## 5. Return

Return these five lines:

```
Status: done | <entry ID>
Workflow: <the Workflow value from step 2, or none>
Commit: <SHA, or none>
Tests: <the test count the runner reported, or none>
Note: <one sentence>
```

## Entries

Write each entry under `## Pending Decisions` at the end of the handoff. Create the section if it
does not exist. Number each entry type in sequence across the file: `D1`, `D2`, `B1`, `N1`.

In the `Blocks` line, list this step and every later step that depends on it. Use the handoff's own
dependency notes. If you are not sure that a step is independent, list it.

```
### D1: <question> (found in step <id>)
- A: <option>
- B: <option> (recommended: <reason>)
- C: <option>
- Blocks: <step IDs>

### B1: step <id>, <gate> stays red
- Failure: <first lines of the failing output>
- Tried: <attempt 1>, <attempt 2>, <attempt 3>
- Work: stash "auto-handoff: <step>"
- Blocks: <step IDs>

### N1: <action> (step <id>)
- Action: <the exact command, URL, or change for the user to make>
- Blocks: <step IDs>
```

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.
