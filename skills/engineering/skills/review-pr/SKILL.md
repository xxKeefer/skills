---
name: review-pr
description: >
  Review an open PR from its number, URL, branch, or ticket key: resolve the PR, claim its
  worktree, sync it by fast-forward only, then run /engineering:mob-review there, which writes an HTML
  report. On someone else's code, give the report path, so the user ticks the rows to post and
  pastes the prompt that the report builds. Use when the user asks to review a PR from its number,
  URL, branch, or ticket key.
argument-hint: "<PR number or URL | branch | ticket key>"
---

# Review PR

Put an open PR in its own worktree and run the review panel on it. The user's current folder and
branch do not change. This skill posts nothing. The user ticks rows in the report, and the prompt
that the report builds runs `/engineering:post-review-comments` on those rows only.

```
resolve → show → /claim → sync → /engineering:mob-review → point to the report → return
```

## Step 1: Resolve the PR

1. Follow "Resolve the PR" in [`PR-HANDLE.md`](../../PR-HANDLE.md).
2. Run `gh pr view <n> --json number,title,url,state,isDraft,author,headRefName,headRefOid,baseRefName`.
3. If `state` is not `OPEN`, stop and give the state.

**Done when:** you have one open PR with its branch and its head SHA, or you stopped and said why.

## Step 2: Show the PR

Show what the panel will review, then continue. This step asks nothing, because the next steps
change no branch that the user works on.

```
PR #<n>: <title>, by <author login>
<url>
Branch: <headRefName> → <baseRefName>. Head: <short headRefOid>. Draft: <yes | no>.
```

**Done when:** the user can see which PR the panel reviews.

## Step 3: Claim the worktree

Run `/claim` with the PR number. It returns the worktree path, the branch, and a handoff path or
`none`. If `/claim` stops to ask a question, put the question to the user, and continue with the
answer.

**Done when:** you have the worktree path.

## Step 4: Sync the worktree

Follow "Sync the worktree" in [`PR-HANDLE.md`](../../PR-HANDLE.md). With local commits, stop. Say
that the panel would review commits that are not in the PR. Change nothing.

**Done when:** the worktree holds the PR head, or you stopped and changed nothing.

## Step 5: Run the panel

If this session does not have `/engineering:mob-review`, stop here, and give the worktree path.

Run `/engineering:mob-review` with no target, and name the worktree as its repo folder. Every command
of the panel runs in the worktree. Do not give it the PR number, because its PR path runs
`gh pr checkout`.

`mob-review` finds the PR from the branch, decides whose code it is, writes the report, and
prints the report path. On the user's own code, its Step 6 points to the `/engineering:apply-review`
prompt that the report builds.

**Done when:** the panel wrote its report and printed the report path.

## Step 6: Point to the report

Skip this step on the user's own code, and when the report has no finding.

On someone else's code, give the report path. Tell the user to tick the rows to post in the
report, then paste the prompt that the report builds. The prompt runs
`/engineering:post-review-comments`, which shows each draft before it posts. Do not offer a post, and
do not run `/engineering:post-review-comments` from this skill.

**Done when:** the user has the report path and knows to tick the rows and paste the prompt.

## Step 7: Return

Give:

1. The PR link and the worktree path.
2. The result: the panel found nothing, or the report path and the count of findings in each
   tier.
3. The worktree stays. When the review is done, the user removes it with `wt remove <branch>`.

**Done when:** the user has the PR link, the worktree path, and the result.
