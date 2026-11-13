---
name: pickup
description: >
  Pick up an open PR from its number, URL, branch, or ticket key: confirm the PR, claim its
  worktree, sync the branch by fast-forward only, then assess its open review threads into a review
  report, whose ticks build the /engineering:apply-review prompt. Use when the user asks to pick up a PR
  or a branch.
argument-hint: "<PR number or URL | branch | ticket key>"
---

# Pickup

Get onto an open PR with no lost work, and assess its open review threads into a review report.
The user ticks the rows to act on, and the prompt of the report runs `/engineering:apply-review`. This
skill ends at the report. It never pushes, never posts, and never discards a change.

```
resolve → confirm → /claim → sync → assess the threads → return
```

## Step 1: Resolve the PR

1. Follow "Resolve the PR" in [`PR-HANDLE.md`](../../PR-HANDLE.md). When no PR matches, the next
   step is `/start-ticket` for a ticket key, or `/claim <branch>` for a branch.
2. Read the PR and its checks, in parallel:
   - `gh pr view <n> --json number,title,url,state,isDraft,headRefName,headRefOid,baseRefName,mergeable,reviewDecision`
   - `gh pr checks <n> --json bucket`: count the checks in each bucket.
3. If `state` is not `OPEN`, stop and give the state.

**Done when:** you have one open PR with its branch, its head SHA, and its checks, or you stopped
and said why.

## Step 2: Confirm the PR

Show the PR before any change:

```
PR #<n>: <title>
<url>
Branch: <headRefName> → <baseRefName>. Head: <short headRefOid>.
Draft: <yes | no>. Merge state: <mergeable>. Review: <reviewDecision>.
Checks: <n> pass, <n> fail, <n> pending.
```

Ask whether to pick up this PR. Change nothing before the yes.

**Done when:** the user confirmed the PR, or you stopped.

## Step 3: Claim the worktree

Run `/claim` with the PR number. It returns the worktree path, the branch, and a handoff path or
`none`. If `/claim` stops to ask a question, put the question to the user, and continue with the
answer.

If `/claim` returns a handoff, the work can have a plan. Show the path. The threads still go to the
report in Step 5, so the handoff and the report do not compete.

**Done when:** you have the worktree path, and the handoff path or `none`.

## Step 4: Sync the branch

Follow "Sync the worktree" in [`PR-HANDLE.md`](../../PR-HANDLE.md). With local commits, ask
whether to keep them, because the next push sends them. Continue after a yes.

**Done when:** the worktree holds the PR head and no commit is lost, or you stopped and changed
nothing.

## Step 5: Assess the threads

Read [`resolve-feedback`](../resolve-feedback/SKILL.md), and follow its Steps 1 to 3 for PR `<n>`.
The repo folder is the worktree. Read the code and run each git command there, not in the current
folder.

- Step 1 lists the open threads of the PR with the shared query. With no open thread, it writes
  no report.
- Step 2 gives each thread one row: a verdict, a recommendation, a draft reply, and the `thread`
  URL, with the ticks `fix`, `reply`, and `resolve`.
- Step 3 adds a `Threads at <short head>` run to `review_<KEY>.html`. A panel run of
  `/engineering:mob-review` on the same branch uses the same key, so both runs go to one file.

Do not follow its Step 4. Step 6 below returns.

**Done when:** the report holds the threads run, or Step 1 found no open thread.

## Step 6: Return

Give:

1. The PR link, the branch, and the worktree path.
2. The sync result: the branch matched, the fast-forward took `<n>` commits, or the user kept `<n>`
   local commits.
3. The count of each verdict and the report path, or that the PR has no open thread.
4. The next action. Tick the rows in the report, then paste its prompt. The prompt runs
   `/engineering:apply-review`, which fixes test-first, commits once, and pushes once. Then it replies
   on and resolves the ticked threads.
5. To add a panel run to the same report, run `/engineering:mob-review` in the worktree. For the
   essential lanes only, run `/engineering:light-review`.
6. When `/claim` returned a handoff, its path. The user continues it with
   `/do-next @<handoff path>` in a session in the worktree.

Neither this skill nor `/engineering:apply-review` merges the base or watches CI.

**Done when:** the user has the worktree path, and the report path or the reason for no report.
