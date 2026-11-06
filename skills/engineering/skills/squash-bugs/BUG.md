# Bug Brief

You fix one QA bug ticket from a cold start, inside one worktree. The parent gives you the ticket
ID, the worktree path, and the path to this brief. On a rerun, it also gives you the ticket's hunt
doc.

Run every command from the worktree. Edit only files inside the worktree, plus the hunt doc. Commit
to the worktree's branch. Push nothing, and write nothing to the tracker.

## 1. Cold start

1. Read the ticket with `/look-up`, and every resource it links.
2. If the parent gave a hunt doc, read it. Its `## Decisions` section holds the user's answers, and
   they override the verdict in it.
3. Read the repo guidance from the worktree: the commit convention, the gates, and the test scope.

**Done when:** you can state the symptom, the expected behaviour, and the gates.

## 2. Reproduce

Find the code that produces the symptom. Then use the first row that matches:

| Case | Verdict | What to do |
| ---- | ------- | ---------- |
| The fix is a cosmetic one-line change: copy, a variant, a single prop | `trivial` | Make the edit. Go to step 4, and use the existing specs for the files you touched. |
| The behaviour matches the documented design, and the design is the same in every provider, variant, and flow that shares it | `not a bug` | Go to step 6. |
| Anything else | | Write a spec at the seam where the user sees the bug. If the design differs between providers, variants, or flows, write the spec to show the difference. Run it. |

If the spec goes red, go to step 3. If it stays green, the verdict is `cannot reproduce`. Go to
step 6.

**Done when:** you have a verdict, or a spec that is red for the reason the ticket gives.

## 3. Fix

Trace the red spec to the root cause. Fix the cause at the most general layer that owns it: the
shared provider, not each component that shows the symptom.

If the fix needs a choice that the ticket and the hunt doc do not settle, the verdict is
`decision`. Leave the red spec uncommitted, and go to step 6.

**Done when:** the spec is green.

## 4. Run the gates

Run the gates and the test scope that the repo guidance names.

If a spec outside your change goes red, look first for state that leaks between tests: a toast, a
global store, a timer, or a mock that a test does not reset.

If a gate is red, fix the cause and run the gates again. After 3 fix attempts that leave a gate
red, the verdict is `blocked`. Leave the work uncommitted, and go to step 6.

When every gate is green, the verdict is `fixed`, unless it is already `trivial`.

**Done when:** every gate is green, or the verdict is `blocked`.

## 5. Mutation check

Skip this step for `trivial`.

1. Revert the fix, and keep the spec.
2. Run the spec and see it go red.
3. Restore the fix and see it go green.

If the spec stays green without the fix, it does not test the bug. Rewrite the spec, then do this
step again.

**Done when:** the spec is red without the fix and green with it.

## 6. Write the hunt doc

Write `hunt_<ticket>.md` with `/write-to-file`. On a rerun, update the hunt doc that the parent gave
you.

```markdown
# Hunt: <ticket> <symptom>

**Verdict:** fixed | trivial | not a bug | cannot reproduce | decision | blocked

## Symptom

What the ticket reports, and what the spec shows.

## Root cause

The location, what happens, and why. For `not a bug` and `cannot reproduce`, the evidence.

## Fix

What changed, and at which layer. For `decision`, options A, B, and C, with the one you recommend
and the reason. For `blocked`, the red gate, the first lines of its output, and the 3 attempts.

## Risk

What else the fix touches: other providers, flows, and callers of the changed code.

## Decisions

The user's answers. The parent writes this section.
```

Write in **Simplified Technical English**. Read [`STE.md`](../../STE.md) before you write, and
follow every rule in it.

**Done when:** the hunt doc exists, and each section holds its content or "none".

## 7. Commit

Do this step only for `fixed` and `trivial`.

1. Stage only the spec and the fix.
2. Commit with the repo's commit convention.

**Done when:** the commit exists, and the worktree has no modified or staged files.

## 8. Return

Return these lines:

```
Verdict: fixed | trivial | not a bug | cannot reproduce | decision | blocked
Commit: <SHA, or none>
Root cause: <one sentence, or none>
Files changed: <paths, or none>
Tests: <the test count the runner reported, or none>
Hunt doc: <absolute path>
```
