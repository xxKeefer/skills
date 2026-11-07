---
name: apply-review
description: >
  Apply the rows that you tick in a review report of your own branch. Fix test-first, commit once,
  push once, then reply on and resolve the ticked threads.
disable-model-invocation: true
argument-hint: "@<report path> <row IDs>"
---

# Apply review

Act on the rows that the user ticked in a review report of their own branch. The ticks are the
approval, so this skill asks no question by default.

```
read → check the branch → fix → gates and commit → push → reply and resolve → record
```

## Step 1: Read the report

`$ARGUMENTS` holds the prompt that the report builds:

```text
/code-review:apply-review @<report path> r2.1 r3.2:fix+reply+resolve
Notes:
- r2.1: <note>
```

1. Read the report path, the row IDs, and the notes. An ID with no colon means the one tick that
   its row has. With no report path or no ID, stop. Say to tick the rows in a review report and
   paste its prompt. Never review again here.
2. Parse the JSON in the `<script type="application/json" id="runs">` block of the report. A row
   ID `r<run>.<n>` names its run. Find each row in its run.
3. Stop and name the ID when one of these is true:
   - The ID has no row, or a tick that the `ticks` of its row does not list.
   - A row with a `reply` or a `resolve` tick has no `thread` cell.
   - A row with a `reply` tick has no `draft` cell and no `fix` tick, so the reply has no text.
4. From each ticked row, read `where` (`<path>:<line>`), `issue`, `recommendation`, and the
   `draft` and `thread` cells when the row has them. `thread` is the URL of the first comment of
   the thread: `https://github.com/<owner>/<repo>/pull/<n>#discussion_r<id>`.
5. From each run that holds a ticked row, read `head` and these `meta` keys: `Base` (the base
   branch, then the base SHA), `Folder` (the repo folder that the panel ran in), and `PR` (the PR
   URL, when the branch had a PR).
6. Run each git command in `Folder`, with `git -C <path>`. Give each `gh` command
   `-R <owner>/<repo>`.

**Done when:** each ticked ID has its row, its ticks, its note, and the head of its run.

## Step 2: Check the branch

1. Compare the branch authors with you:

   ```bash
   git config user.email
   git log --format='%ae' "$(git merge-base origin/<base> HEAD)..HEAD" | sort -u
   ```

   If one author is not you, stop. Say that the branch is someone else's, and name
   `/code-review:post-review-comments`.
2. A run whose `head` ends in `+ working tree` reviewed uncommitted work. Else, if
   `git status --porcelain` shows a change, stop. A fix commit would take in that change.
3. If HEAD is not the head of the run, find the code of each row with a `fix` tick at HEAD, and
   take its new line. Drop each row whose code is gone or changed, and say which.

**Done when:** the branch is yours, the working tree is clean or the run reviewed it, and each row
with a `fix` tick has its code at HEAD.

## Step 3: Apply the fixes

Do each row with a `fix` tick, in ID order. With no `fix` tick, go to Step 5.

1. Apply the note of the row. A note can change the fix or narrow it. If the row and its note
   leave a choice between two fixes, ask the user which, and wait.
2. Sort the fix. A **behaviour** fix changes what the code does. A **mechanical** fix leaves the
   code doing the same thing, such as a rename or a deleted duplicate.
3. For a behaviour fix, write the failing test first, from the counterexample in `issue`. Run it,
   and see it go red. Then fix the code, and see the test go green.
4. For a mechanical fix, make the change. The existing specs stay green.
5. For each added test, break the code that it targets, see the test go red, and restore the code.
   A test that passes either way covers nothing.

**Done when:** each row with a `fix` tick is applied, each behaviour fix has a test that went red
and then green, and each added test went red under its break.

## Step 4: Run the gates and commit

1. Run the typecheck, the lint, the format check, and the affected tests that the repo's
   `CLAUDE.md` or `AGENTS.md` names, at the smallest scope that proves the change. A failure
   returns to Step 3.
2. For a working-tree run, leave the fixes in the working tree, and go to Step 7.
3. Make one commit in the repo's commit convention. The body lists each change and why.

**Done when:** each gate passes, and the commit exists or the run is a working-tree run.

## Step 5: Push

1. Push nothing, and go to Step 7, when one of these is true:
   - The branch has no open PR. Check with `gh pr view --json state -q .state`.
   - A handoff step runs this skill. The push step of the handoff pushes.
2. If a note or the user's message asks to check first, show `git show --stat HEAD` when Step 4
   made a commit, and the text of each reply. Ask once: push and reply, or stop.
3. When Step 4 made no commit, go to Step 6.
4. Run `git push`. Never force.
5. If the push fails, post no reply, because the hash is not on the remote. Say why the push
   failed, and go to Step 7.

**Done when:** the remote branch holds the commit, or the run has no commit to push, or Step 7
names why the push did not happen.

## Step 6: Reply and resolve

Do this step for the rows with a `reply` or a `resolve` tick. Read
[`references/threads.md`](references/threads.md) before the first call.

1. List the threads of the PR. Match each row to its thread by the comment id in its `thread`
   URL. When no thread matches, skip the row and say which.
2. For each `reply` tick, apply the note of the row to its `draft`. When the row also has a `fix`
   tick, end the reply with `Fixed in <short hash>.` With no draft, the reply is that line alone.
   Post the reply on the thread.
3. For each `resolve` tick, resolve the thread after its reply.

**Done when:** each `reply` tick has a posted reply, and each `resolve` tick has a resolved thread.

## Step 7: Record the results

Add a result run to the report with `/write-report`:

- `kind`: `review`. `key`: the `<KEY>` from the file name `review_<KEY>.html`. If `/write-report`
  returns another path, write to the report path.
- `title`: the `title` of the report. `skill`: `/code-review:apply-review`.
- The run:
  - `title`: `Applied at <short hash>`, else `Applied in the working tree`, else `Not applied`.
  - `head`: HEAD after the commit.
  - `meta`: `Commit` (when Step 4 made one), `PR` (when the branch has one), and `Folder`.
  - `answer`: the count of fixes, replies, and resolved threads, and each tick not done.
  - `columns`: `row` (the ticked ID), `where` (set `mono`), and `result`.
  - `rows`: one row for each ticked ID, with no ticks. `result` lists `applied`, `replied`, and
    `resolved`, as done. A tick not done gets `not done: <why>`, such as `no open PR` or
    `code changed after the review`.

Then give the user the commit hash, the result of each ID, and the report path. Say that no panel
read the fix commit, so the head of the last panel run is the last reviewed head.

**Done when:** the report holds the result run, and the user has the results.
