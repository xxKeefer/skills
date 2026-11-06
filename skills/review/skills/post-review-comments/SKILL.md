---
name: post-review-comments
description: >
  Post the review findings that the user picks to the PR: tick the findings, show each draft, then
  post the approved ones as one comment review and read them back. Five or more picks go to a
  handoff instead. Use when the user asks to post the review findings to the PR, or when the step
  of a review comment handoff runs.
argument-hint: "[handoff path]"
---

# Post review comments

Turn the review findings that the user picks into inline comments on the PR. A post publishes text
to the PR's author and reviewers, so the user sees each draft first. Nothing posts by default.

```
read → head check → pick → draft → gate (or handoff) → post → read back → return
```

## Step 1: Read the review

1. With a handoff path in `$ARGUMENTS`, this is a handoff run. Read the PR, the repo, the
   reviewed head, and the base from the handoff, and each draft under `## Drafts`.
2. Else find the last `mob-review` report in this session. Read its
   `Reviewed: base <sha>, head <sha>` line, its Spec findings, and its findings table. With no
   report, stop and say to run `/review:review-pr` first. Never review again here.
3. Run each git command in the folder that the review ran in, with `git -C <path>`.
   `/review:review-pr` names its worktree. Give each `gh` command `-R <owner>/<repo>`.
4. Number the findings in the report's order: the Spec findings first, then the table.

**Done when:** you have the PR, the reviewed head, and the numbered findings or the drafts.

## Step 2: Check the PR head

Run `gh pr view <n> -R <owner>/<repo> --json state,headRefOid,baseRefName`.

- If `state` is not `OPEN`, stop and give the state.
- If `headRefOid` starts with the reviewed head, continue.
- Else the author pushed after the review. Ask: map the findings to the new head, or review again
  with `/review:review-pr`.

To map, run `git fetch origin pull/<n>/head`. Read each file at the new head with
`git show "<new head>:<path>"`, find the code of each finding or draft, and take its new line.
Drop each one whose code is gone or changed, and say which. Never post a reviewed line number against a
new head. From here on, the new head is the head.

**Done when:** the PR is open, and each finding has a line at the head.

## Step 3: Pick the findings

Skip this step in a handoff run.

Print the numbered list once, one line for each finding: `#<n> <Tier> <file>:<line>: <summary>`.

Then ask a multi-select question, with one option for each finding and no option ticked. If the
question tool caps the number of options, split the findings across several questions. A free-text
answer, such as "1, 3, 4" or "all the change requests", overrides the ticks.

With no pick, stop and post nothing.

**Done when:** you have the picked findings, or the user picked none.

## Step 4: Draft each comment

Skip this step in a handoff run.

Write one comment for each pick, in this layout, with a blank line between the blocks:

````markdown
**:robot: AI Review (<Tier>):**

**Problem:** <what is wrong on this line, one or two short sentences>

**Risk:** <the failure if it ships>

**Proposed Solution:** <the fix, one sentence>

```suggestion
<the new text of the anchored line>
```
````

- `<Tier>` is `Change Requested`, `Nit`, or `Future`. Every comment starts with this prefix line,
  word for word.
- Problem comes from the summary, Risk from the detail, and Proposed Solution from the suggestion.
  Keep each one short. Do not restate the code. The reader can see the line.
- Add the `suggestion` block only when the fix replaces the anchored line. Copy that line from the
  head with `git show "<head>:<path>" | sed -n '<line>p'`, and keep its indentation. Else describe
  the fix in Proposed Solution, and leave out the block.
- Write for the PR author. Name no persona, and use no panel term such as `inScope`.
- Keep each markdown link to `main` from the finding.
- If the user changed a tier or the words of a finding during the review, use the user's version.

Find the anchor. A comment can sit only on a line inside a hunk of the PR diff, on the new side.
List the hunks with `git diff --merge-base origin/<base> <head> -- <path> | grep '^@@'`. A hunk
`+<start>,<count>` holds the lines `<start>` to `<start> + <count> - 1`. A finding outside every
hunk, or on line 0, goes in the review body, as `` `<path>:<line>` `` and then its comment.

Scan each draft, and fix each hit:

- An em dash or an en dash used as a connector.
- `e.g.`, `i.e.`, `etc.`, `vs.`, or `via`.
- A prose word spelled outside the locale that the user's instructions name. Identifiers, API
  fields, config keys, and quoted UI strings keep their spelling.
- A list of three or more items with no Oxford comma.
- The name of a personal skill, an agent, or a review tool. The prefix line stays.

Write each draft to `c<n>.md` in a folder from `mktemp -d`. Use a quoted heredoc (`<<'EOF'`), so
that backticks and `$` stay as written.

**Done when:** each pick has a draft with an anchor, and the scan finds nothing.

## Step 5: The gate

Use the row that fits:

| Case | Do |
|---|---|
| 1 to 4 picks | Show each draft in turn, with its anchor. Ask: post, revise, or skip. To revise, change the draft, scan it again, and show it again. After the last draft, go to Step 6 with the approved drafts. With none approved, stop. |
| 5 or more picks | Write the handoff below with `/write-to-file`, as `handoff_pr-<n>-review.md`. Post nothing. Give the path and `/do-next @<path>`, then stop. |
| A handoff run | Write each draft to `c<n>.md` as Step 4 does, and scan it again, because the user can edit the file. Show the drafts. Ask once: post them all, or stop. |

The handoff:

````markdown
# Review comments for PR #<n>

PR: <url>. Repo: <owner>/<repo>. Reviewed head: <full sha>. Base: <baseRefName>.

Edit or delete any draft. Keep the `Anchor:` line of each draft that stays.

## Steps

- [ ] **1. Post the drafts.** Run `/review:post-review-comments @<this file>`. Done when the review
  is on the PR, and its read-back matches the drafts.

## Drafts

### <n>. <path>:<line>

Anchor: `<path>:<line>`, or `review body`.

<the comment>
````

A draft runs from its `Anchor:` line to the next `### ` heading.

**Done when:** the user approved the drafts to post, or the handoff exists, or the user stopped.

## Step 6: Post as one review

Post every approved comment in one review, so that the author gets one notification:

```bash
jq -n --arg sha "<full head sha>" --arg body "<the review body, or empty>" \
  --rawfile c1 "$DIR/c1.md" --rawfile c2 "$DIR/c2.md" \
  '{commit_id:$sha, event:"COMMENT", body:$body, comments:[
    {path:"<path>", line:<line>, side:"RIGHT", body:$c1},
    {path:"<path>", line:<line>, side:"RIGHT", body:$c2}]}' > "$DIR/review.json"
gh api repos/<owner>/<repo>/pulls/<n>/reviews --input "$DIR/review.json" --jq '{id, html_url}'
```

- The event is always `COMMENT`. Use `REQUEST_CHANGES` or `APPROVE` only when the user asks,
  because that verdict is the user's.
- An error 422 that says the user can have only one pending review: the user has a draft review
  on this PR. Never submit, edit, or delete it. Show it with
  `gh api repos/<owner>/<repo>/pulls/<n>/reviews --jq '.[] | select(.state=="PENDING") | {id, body}'`.
  Ask the user to submit or discard it in GitHub and then post again, or to hold.
- Another error 422 usually means an anchor outside the diff. Move that comment to the review
  body, and post again once.

**Done when:** GitHub returned the review's `id` and `html_url`.

## Step 7: Read back

The comment list of a review gives `line: null`, so check the bodies from the list and each anchor
from its own comment:

```bash
gh api repos/<owner>/<repo>/pulls/<n>/reviews/<id>/comments --jq '[.[].body]' > "$DIR/landed.json"
jq '[.comments[].body]' "$DIR/review.json" > "$DIR/sent.json"
diff <(jq -S . "$DIR/sent.json") <(jq -S . "$DIR/landed.json") && echo MATCH
gh api repos/<owner>/<repo>/pulls/<n>/reviews/<id>/comments --jq '.[] | "\(.id) \(.html_url)"'
gh api repos/<owner>/<repo>/pulls/comments/<comment id> --jq '{path, line, side}'
```

**Done when:** each body and each anchor matches what you sent, or the user has seen each
difference.

## Step 8: Return

Give a table with one row for each posted comment: the number, the tier, `<path>:<line>`, and the
comment link. Then give the review link. Say each body that differs from what you sent, and each
anchor on the wrong line.

**Done when:** the user has the review link and the table.
