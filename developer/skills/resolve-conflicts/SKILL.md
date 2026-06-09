---
name: resolve-conflicts
description: >
  Resolve git merge/rebase conflicts in a file using its history and the in-progress operation as
  context. Simple conflicts resolve automatically; complex ones (both sides added, or a
  migration/refactor collided with edits) pause for the user with evidence and a justified
  recommendation. Then follows links to conflicted test siblings and refactor parents/children.
  Usage: resolve-conflicts <filepath>. Use when the user says "resolve conflicts", "fix the merge",
  "resolve this conflict", or hands you a conflicted file.
argument-hint: "<filepath>"
---

# Resolve Conflicts

Resolve conflicts the way a careful engineer would: understand what each side was trying to do
*before* touching a marker, auto-resolve only what's unambiguous, and bring the user in with
evidence when intent actually clashes. Then keep the resolution consistent across the file's
test sibling and any refactor relatives that are also conflicted.

## Step 1: Establish the merge context

Before reading the file, understand the operation in progress — it sets the meaning of "ours" and
"theirs" (they **invert** between merge and rebase, and cherry-pick/revert behave like rebase):

- Detect the operation: merge (`MERGE_HEAD`), rebase (`rebase-merge`/`rebase-apply`),
  cherry-pick (`CHERRY_PICK_HEAD`), or revert.
- Identify both sides in human terms — branch names and the commit subjects each side carries —
  not just "ours/theirs". State which real branch/change each side maps to.
- Confirm `<filepath>` actually contains conflict markers. If git reports it conflicted but there
  are none, it's a delete/rename conflict — handle that as a complex case (Step 4).

**Done when:** you can name what each side represents and how they relate to this file.

## Step 2: Gather evidence per conflict hunk

For the conflicted file, collect the three versions and the intent behind each side:

- **base / ours / theirs** content (the common ancestor and each side's version of the region).
- **What each side did and why** — the commits on each side that touched this region since the
  merge base, with their messages and diffs. The commit messages are the intent; the diffs are
  the evidence.

Delegate to `/look-up` if you need to pull in related files to understand a side's change.

**Done when:** every conflict hunk has base/ours/theirs and a one-line statement of each side's intent.

## Step 3: Classify each hunk — simple or complex

**Simple (resolve automatically in Step 4):** intent is unambiguous and the sides don't fight:

- Identical change on both sides.
- Pure addition on one side in a region the other only reformatted or left alone.
- One side reformatted / reordered imports / changed whitespace; the other made the real change.
- One side deleted or moved a block the other never semantically touched.

**Complex (escalate to the user in Step 5):** intent clashes or both sides changed meaning:

- **Both sides added new code** in the same place — two new functions, cases, fields, routes.
  The default is *integrate both*, but order/interaction needs a human eye.
- **Migration/refactor vs edit** — one side renamed/moved/changed a signature or migrated an API
  while the other edited the same region against the old shape.
- Both sides changed the same logic in different directions.
- Delete/rename conflict (one side deleted or moved the file, the other edited it).

When unsure, treat it as complex. Auto-resolution is only for cases with one defensible answer.

**Done when:** each hunk is tagged simple or complex.

## Step 4: Auto-resolve the simple hunks

Apply the obvious resolution for each simple hunk. For "both sides added, no interaction" keep
both. Record what you did and why in one line each — this goes in the Step 7 summary.

**Done when:** no simple hunks remain in the file.

## Step 5: Escalate complex hunks — evidence, then a recommendation (checkpoint)

This is the mandatory pause. For each complex hunk, present to the user:

1. **The three versions** — base, ours, theirs, labelled with the real branch/change each maps to.
2. **Each side's intent** — drawn from the commit messages and diffs gathered in Step 2.
3. **Recommended resolution + justification** — the concrete merged result you propose and *why*
   it honours both intents (or why one must yield). Ground it in the evidence, not a guess.
4. **Alternatives** — other defensible resolutions and their trade-offs.

Wait for the user's decision before writing the hunk. Never apply a complex resolution unprompted.

**Done when:** the user has chosen a path for every complex hunk and it's applied.

## Step 6: Verify and stage the file

- Re-read the file: no conflict markers remain and the result is internally coherent (imports,
  references, and the symbols touched all line up).
- Stage the file so git records it resolved (`git add <filepath>`).
- Do **not** run `git rebase --continue` / `git commit` to complete the operation — that's the
  user's call. Note it as outstanding in the summary.

**Done when:** the file is marker-free, coherent, and staged.

## Step 7: Follow the links

A resolution in one file usually implies resolutions in related files. For each link below, act
**only on files git currently reports as conflicted** — never edit clean files (out of scope).
Pull each linked file in with `/look-up`, then run it through Steps 2–6, keeping the resolution
**consistent** with the decision already made here.

- **Test sibling** — if `<filepath>` has a corresponding test file (or is one, find its subject),
  resolve that file next so tests match the resolved behaviour.
- **Refactor parent/child** — if the resolution involved a rename, move, signature change, or
  migration, find the files that depend on or are depended on by the changed symbols and resolve
  any that are conflicted, consistent with the new shape.

Recurse: a linked file may surface its own test sibling or refactor relatives. Track what you've
visited so you don't loop.

**Done when:** the conflicted set reachable from `<filepath>` via test and refactor links is resolved.

## Step 8: Summarise

Report: every file touched, each conflict and how it was resolved (auto vs user-decided), files
followed via links, and what's still outstanding (e.g. "rebase still in progress — run
`git rebase --continue` when ready"). Do not commit on the user's behalf.
