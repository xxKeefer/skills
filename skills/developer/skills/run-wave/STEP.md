# Step Brief

You run one step of a handoff, from a cold start. The parent gives you the handoff path and the
step ID. The handoff is your only context.

The parent can give a list of review fix step IDs in place of one ID. Do each step in order
through sections 1 to 4, with one commit for each step. Stop at the first step that writes an
entry. Return the five lines once for each step.

Commit to the current branch. Push only in the push step, through `/create-pr`. Edit only files
inside this repo, the handoff file, and the step's patch file (see Save the work).

## 1. Cold start

1. Read the handoff and every artifact the step references.
2. If the handoff says to resume from a patch file, run `git apply <patch>`. Then delete the patch
   file.
3. If the step needs a decision that the handoff does not record, write a `D` entry and return.
   A step that changes behaviour and names no seam needs one: ask for the seam. Never pick a seam
   yourself. A review fix step needs no seam: the report row is its spec.
4. The push step is the one step that pushes. Step 2 runs `/create-pr @<handoff path>` for it,
   which pushes the branch and opens a draft PR. Never mark the PR ready for review. If
   `/create-pr` stops on drift or a gap, write a `D` entry with its reason and return.
5. If the step edits a ticket, deploys, or writes to any other outside service, write an `N` entry
   and return.

**Done when:** you can name the step's done line and its workflow.

## 2. Do the step

Use the first row that matches the step:

| Step | Workflow | What to do |
| ---- | -------- | ---------- |
| Names a skill | `skill: /<name>` | Run that skill. |
| Review fix | `review fix` | Read the row in the report that the step names. Find the code by its content, not by the line number in the row, because earlier fixes can move the code. Make the change that the done line names. If the row names a missing test, write it first and see it go red. If the new test covers code that already works, it cannot go red first. Break the code under test, see the test go red, and restore the code. Keep every other test green. |
| Changes behaviour | `TDD` | Write a failing test at the step's seam and see it go red. Write the minimum code to go green. Then do a mutation check: break the new code, see the test go red, and restore the code. |
| Trivial tweak: copy, a variant, a single prop | `trivial` | Make the edit. Run the existing tests for the files you touched. |
| Anything else: docs, config, CI | `done line` | Make the change. |

If you find an unrecorded decision partway through, save the work, write a `D` entry, and return.

**Done when:** the step's done line holds.

## 3. Run the gates

Run the gates that the handoff or the repo guidance names. Use the test scope that the repo
guidance sets.

Run the gates in every step. Run them also in a step that changes no file, such as a review step.
In the push step, run them before you push.

If a gate is red, fix the cause and run the gates again. After 3 fix attempts that leave a gate
red, save the work, write a `B` entry, and return.

**Done when:** every gate is green.

## 4. Commit

1. Stage only the files this step changed.
2. Commit with the repo's commit convention.
3. Invoke `/update-handoff` on the handoff to mark the step done.

If the step changed no file except the handoff, make no commit. A review step that only records its
report is an example. Return `Commit: none`.

**Done when:** the handoff marks the step done, and the commit exists or the step changed no file
except the handoff.

## 5. Return

Return these five lines, once for each step of a batch:

```
Status: done | <entry ID>
Workflow: <the Workflow value from step 2, or none>
Commit: <SHA, or none>
Tests: <the test count the runner reported, or none>
Note: <one sentence>
```

## Save the work

Save the step's changes as a patch file in the handoff's folder, then clean the tree. Name only
the paths this step changed, new files too. The patch name is `<handoff name>.step-<id>.patch`,
such as `plan_auth.step-4.patch`.

1. `git add -- <paths>`
2. `git diff --cached --binary -- <paths> > <patch>`
3. `git restore --source=HEAD --staged --worktree -- <paths>`

Write the patch path on the `Work` line of the entry.

During a merge or a rebase, save no patch. Run `git merge --abort` or `git rebase --abort`. In the
entry, record each conflicting hunk: the file, both sides, and the evidence for each side. The next
run merges again and uses the answer.

## Entries

Write each entry under `## Pending Decisions` at the end of the handoff. Create the section if it
does not exist. Number each entry type in sequence across the file: `D1`, `D2`, `B1`, `N1`.

In the `Blocks` line, list this step and every later step that depends on it. Use the handoff's own
dependency notes. If you are not sure that a step is independent, list it.

In an `N` entry, when the outside action is the whole step, the Action line is
`/do-next @<handoff path>`. The user then runs the step with its skills, not a bare command.

```
### D1: <question> (found in step <id>)
- A: <option>
- B: <option> (recommended: <reason>)
- C: <option>
- Work: <patch path, or none>
- Blocks: <step IDs>

### B1: step <id>, <gate> stays red
- Failure: <first lines of the failing output>
- Tried: <attempt 1>, <attempt 2>, <attempt 3>
- Work: <patch path>
- Blocks: <step IDs>

### N1: <action> (step <id>)
- Action: <the /do-next line, or the exact command, URL, or change for the user to make>
- Blocks: <step IDs>
```

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.
