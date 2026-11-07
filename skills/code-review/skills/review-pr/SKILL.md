---
name: review-pr
description: >
  Review an open PR from its number, URL, branch, or ticket key: resolve the PR, claim its
  worktree, sync it by fast-forward only, then run /code-review:mob-review there, which writes an HTML
  report. On someone else's code, give the report path, so the user ticks the rows to post and
  pastes the prompt that the report builds. Use when the user asks to review a PR from its number,
  URL, branch, or ticket key.
argument-hint: "<PR number or URL | branch | ticket key>"
---

# Review PR

Put an open PR in its own worktree and run the review panel on it. The user's current folder and
branch do not change. This skill posts nothing. The user ticks rows in the report, and the prompt
that the report builds runs `/code-review:post-review-comments` on those rows only.

```
resolve → show → /claim → sync → /code-review:mob-review → point to the report → return
```

## Step 1: Resolve the PR

1. Read the handle from `$ARGUMENTS`. If it is not there, ask for it. Run `gh` from the current
   folder, so that it reads this repo.
2. Find the open PR by the kind of handle:

   | Handle | Do |
   |---|---|
   | A PR URL | Take `<n>` from `github.com/<owner>/<repo>/pull/<n>`. If `<owner>/<repo>` is not this repo, stop, and say to run `review-pr` from a clone of that repo. |
   | A PR number, or `#<n>` | Take `<n>`. |
   | Only a ticket key, such as `PROJ-123` | `gh pr list --state open --search "<key>" --json number,headRefName,title,url` |
   | Anything else | It is a branch: `gh pr list --state open --head "<branch>" --json number,headRefName,title,url` |

3. Use the result of a search:
   - One PR: continue with it.
   - Two or more: list them, and continue with the one that the user picks.
   - None: stop. Say that the handle has no open PR.
4. Run `gh pr view <n> --json number,title,url,state,isDraft,author,headRefName,headRefOid,baseRefName`.
5. If `state` is not `OPEN`, stop and give the state.

The branch is the `headRefName` of the PR. Never guess the branch from a ticket key.

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

Make the worktree hold the PR head with no lost commit. Run each git command in the worktree, with
`git -C <path>`. Never run `reset --hard`.

1. Run `git status --porcelain`. If it prints a line, stop. Show the files, and change nothing.
2. If `git cat-file -e <headRefOid>` fails, get the PR head with `git fetch origin pull/<n>/head`.
3. Compare `HEAD` with `<headRefOid>`:
   - The same commit: continue.
   - `HEAD` is an ancestor of `<headRefOid>` (`git merge-base --is-ancestor HEAD <headRefOid>`):
     run `git merge --ff-only <headRefOid>`. Then check that `git rev-parse HEAD` prints
     `<headRefOid>`.
   - Else: stop. Show `git log --oneline <headRefOid>..HEAD`, the local commits that the PR does
     not have. Say that the panel would review commits that are not in the PR. Change nothing.

**Done when:** the worktree holds the PR head, or you stopped and changed nothing.

## Step 5: Run the panel

If this session does not have `/code-review:mob-review`, stop here, and give the worktree path.

Run `/code-review:mob-review` with no target, and name the worktree as its repo folder. Every command
of the panel runs in the worktree. Do not give it the PR number, because its PR path runs
`gh pr checkout`.

`mob-review` finds the PR from the branch, decides whose code it is, writes the report, and
prints the report path. On the user's own code, its Step 6 points to the `/code-review:apply-review`
prompt that the report builds.

**Done when:** the panel wrote its report and printed the report path.

## Step 6: Point to the report

Skip this step on the user's own code, and when the report has no finding.

On someone else's code, give the report path. Tell the user to tick the rows to post in the
report, then paste the prompt that the report builds. The prompt runs
`/code-review:post-review-comments`, which shows each draft before it posts. Do not offer a post, and
do not run `/code-review:post-review-comments` from this skill.

**Done when:** the user has the report path and knows to tick the rows and paste the prompt.

## Step 7: Return

Give:

1. The PR link and the worktree path.
2. The result: the panel found nothing, or the report path and the count of findings in each
   tier.
3. The worktree stays. When the review is done, the user removes it with `wt remove <branch>`.

**Done when:** the user has the PR link, the worktree path, and the result.
