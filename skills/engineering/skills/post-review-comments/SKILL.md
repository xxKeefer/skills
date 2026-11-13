---
name: post-review-comments
description: >
  Post the rows ticked in a review report to the PR as one review. Use when the user pastes the
  prompt that a review report builds, or asks to post the ticked findings.
argument-hint: "@<report path> <row IDs>"
---

# Post review comments

Turn the rows that the user ticked in a review report into inline comments on the PR. A post
publishes text to the PR's author and reviewers, so the user sees each draft first. Nothing posts
by default.

```
read → head check → prepare → gate → post → read back → return
```

## Step 1: Read the report

`$ARGUMENTS` holds the prompt that the report builds:

```text
/engineering:post-review-comments @<report path> <ID> <ID>
Notes:
- <ID>: <note>
```

1. Read the report path and the row IDs from the first line. Read each note from the `Notes:`
   list. With no report path or no ID, stop. Say to tick the rows in a review report and paste its
   prompt. Never review again here.
2. Parse the JSON in the `<script type="application/json" id="runs">` block of the report. A row
   ID `r<run>.<n>` names its run. Find each row in its run. If an ID has no row, or its row has no
   `draft` cell, stop and name the ID.
3. From each ticked row, read `where` (`<path>:<line>`), `tier`, and `draft`.
4. From each run that holds a ticked row, read `head` and these `meta` keys:
   - `PR`: the PR URL, `https://github.com/<owner>/<repo>/pull/<n>`. Take `<owner>/<repo>` and
     `<n>` from it.
   - `Base`: the base branch, then the base SHA.
   - `Folder`: the repo folder that the panel ran in.
5. If a run has no `PR`, stop. Say that the branch had no PR when the panel ran, so the review
   has no PR to post to.
6. Run each git command in `Folder`, with `git -C <path>`. Give each `gh` command
   `-R <owner>/<repo>`.

**Done when:** you have the PR, and each ticked row with its draft, its note, and the head of its
run.

## Step 2: Check the PR head

Run `gh pr view <n> -R <owner>/<repo> --json state,headRefOid,baseRefName`.

- If `state` is not `OPEN`, stop and give the state.
- If `headRefOid` starts with the head of each run that holds a ticked row, continue.
- Else the author pushed after the review, or a ticked row comes from an older run. Ask once:
  map the rows to the PR head, or review again with `/engineering:review-pr`.

To map, run `git fetch origin pull/<n>/head`. Read each file at the PR head with
`git show "<PR head>:<path>"`, find the code of each row, and take its new line. Drop each row
whose code is gone or changed, and say which. Never post a reviewed line number against a new
head. From here on, the PR head is the head.

**Done when:** the PR is open, and each ticked row has a line at the head.

## Step 3: Prepare each draft

1. Apply the note of each row to its draft. A note can change the tier, the words, or the fix.
2. Check each draft against [the comment layout](#the-comment-layout) and its rules. Fix each
   break.
3. Find the anchor. A comment can sit only on a line inside a hunk of the PR diff, on the new
   side. List the hunks with
   `git diff --merge-base origin/<base> <head> -- <path> | grep '^@@'`. A hunk `+<start>,<count>`
   holds the lines `<start>` to `<start> + <count> - 1`. A row outside every hunk, or on line 0,
   goes in the review body, as `` `<path>:<line>` `` and then its comment.
4. Scan each draft as [`DRAFT-SCAN.md`](../../DRAFT-SCAN.md) says. The prefix line stays.
5. Write each draft to `c<n>.md` in a folder from `mktemp -d`, with `<n>` from 1 in the order of
   the IDs. Use a quoted heredoc (`<<'EOF'`), so that backticks and `$` stay as written.

**Done when:** each ticked row has a draft with an anchor, and the scan finds nothing.

## Step 4: The gate

Show each draft with its row ID and its anchor. Ask once: post them all, or stop. With a stop,
post nothing. If the user asks for a change instead, make it, scan the draft again, and ask
again.

**Done when:** the user approved the post, or the user stopped.

## Step 5: Post as one review

Post every comment in one review, so that the author gets one notification:

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

## Step 6: Read back

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

## Step 7: Return

Give a table with one row for each posted comment: the row ID, the tier, `<path>:<line>`, and the
comment link. Then give the review link. Say each body that differs from what you sent, and each
anchor on the wrong line.

**Done when:** the user has the review link and the table.

## The comment layout

`/engineering:mob-review` writes each draft in this layout, with a blank line between the blocks:

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
