---
name: create-pr
description: >
  Push the branch and open a draft PR, or rewrite the open PR: check the review for drift, fill the
  repo's PR template with an AC table and its gaps, then push without asking. Use when the user
  asks to open or update a PR, or when the push step of a handoff runs.
argument-hint: "[handoff path]"
---

# Create PR

Turn a reviewed branch into a draft PR. The skill pushes without asking: the user's check-in is the
review report before the push step, and the draft PR after it. A run of this skill is the request
to push.

```
read → review check → AC table → title and body → gate → push and write → read back
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
   the base is its head branch.
3. Find the handoff:
   - Use the path in `$ARGUMENTS`.
   - Else take the folder that the user's instructions name for handoffs or plans, with no ticket
     subfolder. With no such folder, take `.ai/` in the root that `/write-to-file` uses.
   - Search that folder and its subfolders for the file whose `Worktree:` line names this branch.
     A sub-task plan is in the folder of its parent ticket, so search each subfolder.
   - Two or more files: ask which one. No file: there is no handoff.
4. From the handoff, read the `## Acceptance criteria` section, the `## Test approach` section, the
   `Merge:` line, the done line of each step, and the two SHAs in the done line of the review
   step: the reviewed base and the reviewed head.
5. If the `Merge:` line names sub-task keys, find the PR of each key:
   - Read the `Worktree:` line of `plan_<SUBKEY>.md` in the folder of the handoff.
   - Run `gh pr list --head <its branch> --state all --json number`.
   - With no stub, no `Worktree:` line, or no PR, use the key.
6. With no handoff, read the ticket whose key is in the branch name with `/look-up`, and take its
   ACs. With no key or no ticket, there are no ACs.
7. List the test files that `git diff --merge-base origin/<base> HEAD --name-only` names, and the
   test names that the diff adds or changes in them.
8. Read the PR conventions: the repo's PR template (`.github/`, `docs/`, or the root, in any case),
   the repo's contribution docs, and each git or GitHub convention skill that this session has.

**Done when:** you have the branch, the base, the open PR or none, the handoff or none, the ACs or
none, the merge order or none, and the test names.

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

**Done when:** you have the result: no review, no change, or the drift.

## Step 3: Build the AC table

With no ACs, write no table and no Gaps line, and go to Step 4.

If the handoff has no Test approach section, derive one from the ACs and the diff. Read
[`../../TEST-APPROACH.md`](../../TEST-APPROACH.md)
and follow its Steps 1 to 3. Step 8 tells the user. The body does not say it.

| AC | Risk | Tested by | Conditions |
| --- | --- | --- | --- |
| **A.** <AC, short> | H | Unit: `<test file>` › <test name> | C1 quantity 1 and 99 · C2 0 and 100 |
| — | <behaviour that no AC covers> | … | … |

- One row for each AC letter. A sub-check gets its own row only when a different test proves it.
  A struck-through AC gets no row.
- One `—` row for each `—` row of the Test approach.
- **Risk** comes from the Risks table.
- **Tested by** is the level, the test file, and the test name, from the step done lines and the
  Step 1 test names. Use `Manual: <why>` only when no test can prove the AC.
- **Conditions** lists the condition IDs that a test in the diff covers, each with a few words.
- **Gaps** lists each planned condition with no test in the diff, and each Not testing item. Each
  gap has a reason or a follow-up. If the handoff gives no reason, write `reason needed`, and the
  gate asks for it. Write `**Gaps:** None` only when that is true.

Put the table in a collapsed block. Keep a blank line after `<summary>` and before `</details>`:

```markdown
**Gaps:** <None | n>
- <condition>: <reason or follow-up>

<details>
<summary>Acceptance criteria: <n>, <n> high risk, <all tested | n not tested (B, C)></summary>

<the table>

</details>
```

**Done when:** each AC letter and each `—` row has a row, and each untested condition is a gap.

## Step 4: Write the title and the body

1. Write the title in the form that the Step 1 conventions give. Else use the form of the branch's
   commit messages.
2. With a PR template, fill it:
   - Replace each instruction and placeholder with content.
   - Keep each checkbox. Tick a box only when the diff shows that it is true. Leave each box about
     the author's own action, such as a self-review, for the user.
   - Remove a section that has nothing to say, such as screenshots when there are none.
   - Put the Step 3 block at the end of the testing or verification section, else at the end.
3. With no template, write one to three bullets on what changes and for whom, then the Step 3
   block.
4. If the handoff has a `Merge:` line, make the merge line the first line of the body:
   - `Merge: alone` gives `Merges alone.`
   - `Merge: after <SUBKEY list>` gives `Merge after <list>.` Name each PR from Step 1, else
     its sub-task key, such as `Merge after #12 and <SUBKEY>.`
5. For an open PR, start from its current body. Keep each part that this skill did not write, such
   as images or links that a person added. Rewrite each part that is out of date.
6. Apply the PR rules:
   - Describe the change, not how you made it. After feedback or a red build, rewrite the affected
     section so it reads as always correct.
   - Cut anything that would not change a reviewer's decision.
   - Name no personal skill, agent, or review tool. Add no AI attribution.
7. Scan the title and the body, and fix each hit:
   - An em dash or an en dash used as a connector. The `—` row marker in the AC table stays.
   - `e.g.`, `i.e.`, `etc.`, `vs.`, or `via`.
   - A prose word spelled outside the locale that the user's instructions name. Identifiers, API
     fields, config keys, and quoted UI strings keep their spelling.
   - A list of three or more items with no Oxford comma.
   - The name of a personal skill, an agent, or a review tool.
   - A placeholder or an instruction from the template, except `reason needed`.

**Done when:** the scan finds nothing.

## Step 5: The gate

Show, in this order:

1. The link to the open PR, if there is one.
2. The base.
3. The Step 2 result. To review again, the user stops here and runs the review.
4. Each file in `git status --porcelain`. The PR holds only commits, so these files are not in it.
5. The title and the body. For an open PR, show the current title and body first, then the new
   ones.
6. Each `reason needed` gap.

Then push. Stop and change nothing only when one of these is true:

- The Step 2 result shows drift since the review.
- A `reason needed` gap remains.

**Done when:** the summary is shown, and you went on to Step 6 or stopped on drift or a gap.

## Step 6: Push and write

1. Run `git push -u origin <branch>`. If the push fails, show the error and stop. Never force the
   push.
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

## Step 7: Read back

Run `gh pr view <number> --json url,isDraft,title,body`. Compare its words with the title and the
body that you sent. Show the user each difference.

**Done when:** the PR holds the words that you sent, or the user has seen each difference.

## Step 8: Return

Give the PR link, whether it is a draft, and the result of the bot review request. If Step 3
derived the Test approach, say that no plan-time test approach existed.

**Done when:** the user has the PR link.
