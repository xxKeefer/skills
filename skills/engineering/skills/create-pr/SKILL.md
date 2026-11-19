---
name: create-pr
description: >
  Push the branch and open a draft PR, or rewrite the body of the open PR. Use when the user asks
  to open or update a PR, or when the push step of a plan runs.
argument-hint: "[plan path]"
---

# Create PR

Turn a reviewed branch into a draft PR. The skill pushes without asking: the user's check-in is the
review report before the push step, and the draft PR after it. A run of this skill is the request
to push.

```
read → review check → AC table → top sections → title and body → gate → push and write → read back
```

## Step 1: Read the work

1. Run `git fetch origin`. Then run these in parallel:
   - `git branch --show-current`
   - `git status --porcelain`
   - `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`
   - `gh pr view --json number,url,state,title,body`: an `OPEN` state is the open PR. If it
     exists, give its link now.
   - `gh pr list --state open --json headRefName`
2. Find the base. It is the default branch. If the head branch of another open PR is an ancestor
   of `HEAD` (`git merge-base --is-ancestor origin/<head> HEAD`), the branch stacks on that PR, and
   the base is its head branch. If `gh stack view` succeeds, the branch is in a **gh stack**.
3. Read [`references/read.md`](references/read.md), and do its items 3 to 8: the plan, the ACs,
   the stack, the test names, and the PR conventions.

**Done when:** you have the branch, the base, the open PR or none, the plan or none, the goal or
none, the Intent or none, the ACs or none, the merge order or none, and the test names.

## Step 2: Check the review

Compare the branch with what the review read. The result is a warning for the gate. It never
blocks.

1. Take the reviewed base and the reviewed head from the review step. Else take them from the
   last `Reviewed: base <sha>, head <sha>` line in this session. With neither, the result is
   "No review is recorded."
2. If `HEAD` is the reviewed head, the result is "No change since the review at `<sha>`."
3. Else show the drift:

   ```bash
   git range-diff <reviewed base>..<reviewed head> "$(git merge-base origin/<base> HEAD)"..HEAD
   ```

   The command skips merge commits. For each merge in
   `git rev-list --merges <reviewed head>..HEAD`, run `git show --remerge-diff --format= <sha>`.
   No output means a clean merge. Output is a conflict that a person resolved, so show it.
4. If each line of the range-diff is `=` and no merge shows a conflict, the branch only moved to a
   new base. The result is "Each reviewed commit is unchanged (`=`) after a rebase onto
   `<base>`." This result is not drift.

**Done when:** you have the result: no review, no change, a rebase only, or the drift.

## Step 3: Build the AC table

With no ACs, write no table and no Gaps line, and go to Step 4.

If the plan has no Test approach section, derive one from the ACs and the diff. Read
[`../../TEST-APPROACH.md`](../../TEST-APPROACH.md)
and follow its Steps 1 to 3. Step 9 tells the user. The body does not say it.

Fill the AC block of [`templates/body.md`](templates/body.md), as its rules say.

**Done when:** each AC letter and each `—` row has a row, and each untested condition is a gap.

## Step 4: Write the top sections

These sections lead the body, so a reviewer sees what changes and how much care the review needs
before reading the diff. Keep prose brief. Use the terms in the repo's `CONTEXT.md` glossary, if
it has one.

Use the top sections of [`templates/body.md`](templates/body.md).

1. **Why.** Write the reason for the change from the plan's `goal`. With a spec, add the
   Intent's `User` and `Why now` lines when the spec has them, in the reader's words. With no plan, take the reason from
   the ticket. With no goal and no ticket, remove the section. Do not invent a reason.
2. **Summary.** Run `/show-me` on the diff from `git diff --merge-base origin/<base> HEAD`. Use
   a text view or Mermaid. Take no HTML file. One view is usual; use two only when one hides the
   point.
3. **Evidence.** Show that the change works, before and after:
   - A screenshot is best, when the change is visual and the environment can take one.
   - Else name the test that failed before the change and passes after it, as pseudocode or as
     the test name, or show the command output.
   - With no evidence, remove the section. Do not invent output.
4. **Merge danger.** Name the door and the blast radius, as the rules in the template say.
5. **Follow-ups.** List each entry of the plan's `Follow-ups` section. With none, remove the
   section.

**Done when:** the Why gives the goal or is removed, the Summary has a visual, the Evidence shows
proof or is removed, the Merge danger names a door and a blast radius, and the Follow-ups list the
plan's entries or are removed.

## Step 5: Write the title and the body

1. Write the title in the form that the Step 1 conventions give. Else use the form of the branch's
   commit messages.
2. With a PR template, fill it:
   - Replace each instruction and placeholder with content.
   - Keep each checkbox. Tick a box only when the diff shows that it is true. Leave each box about
     the author's own action, such as a self-review, for the user.
   - Remove a section that has nothing to say, such as screenshots when there are none.
   - Put the Step 3 block at the end of the testing or verification section, else at the end.
   - Drop a template section that repeats a Step 4 section, such as a summary.
3. With no template, write one to three bullets on what changes and for whom, then the Step 3
   block.
4. Put the Step 4 sections above the template content.
5. With a `merge` key or in a gh stack, write the merge line as `references/stack.md` says.
6. For an open PR, start from its current body. Keep each part that this skill did not write, such
   as images or links that a person added. Rewrite each part that is out of date.
7. Apply the PR rules:
   - Describe the change, not how you made it. After feedback or a red build, rewrite the affected
     section so it reads as always correct.
   - Cut anything that would not change a reviewer's decision.
   - Add no AI attribution.
8. Scan the title and the body as [`DRAFT-SCAN.md`](../../DRAFT-SCAN.md) says. The `—` row
   marker in the AC table stays.
   - A placeholder or an instruction from the template, except `reason needed`.

**Done when:** the scan finds nothing.

## Step 6: The gate

Show, in this order:

1. The link to the open PR, if there is one.
2. The base.
3. The Step 2 result. To review again, the user stops here and runs the review.
4. Each file in `git status --porcelain`. The PR holds only commits, so these files are not in it.
5. The title and the body. For an open PR, show the current title and body first, then the new
   ones.
6. Each `reason needed` gap.
7. The door. Mark a one-way door in bold, so the user reads it before the PR goes out.

Then push. Stop and change nothing only when one of these is true:

- The Step 2 result shows drift since the review.
- A `reason needed` gap remains.

**Done when:** the summary is shown, and you went on to Step 7 or stopped on drift or a gap.

## Step 7: Push and write

In a gh stack, push and open the PR as `references/stack.md` says.

1. Run `git push -u origin <branch>`. If the push fails, show the error and stop. Never force a
   push with `git push --force`.
2. Write the body to a file from `mktemp`.
3. With no open PR, open the draft, then request the bot review:

   ```bash
   gh pr create --draft --base <base> --head <branch> --title "<title>" --body-file <file>
   gh api -X POST "repos/{owner}/{repo}/pulls/<number>/requested_reviewers" \
     -f 'reviewers[]=copilot-pull-request-reviewer[bot]'
   ```

   The `--reviewer` flag rejects a bot, so the request goes through the API. If GitHub rejects
   the request, the repo has no bot review. Say so in one line, and continue.
4. With an open PR, run `gh pr edit <number> --title "<title>" --body-file <file>`. Request no
   review.

**Done when:** the branch is on the remote, and the PR has the title and the body.

## Step 8: Read back

Run `gh pr view <number> --json url,isDraft,title,body`. Compare its words with the title and the
body that you sent. Show the user each difference.

**Done when:** the PR holds the words that you sent, or the user has seen each difference.

## Step 9: Return

Give the PR link, whether it is a draft, and the result of the bot review request. If Step 3
derived the Test approach, say that no plan-time test approach existed.

**Done when:** the user has the PR link.
