---
name: pickup
description: >
  Pick up an open PR from its number, URL, branch, or ticket key: confirm the PR, claim its
  worktree, sync the branch by fast-forward only, then assess its open review threads into a review
  report, whose ticks build the /code-review:apply-review prompt. Use when the user asks to pick up a PR
  or a branch.
argument-hint: "<PR number or URL | branch | ticket key>"
---

# Pickup

Get onto an open PR with no lost work, and assess its open review threads into a review report.
The user ticks the rows to act on, and the prompt of the report runs `/code-review:apply-review`. This
skill ends at the report. It never pushes, never posts, and never discards a change.

```
resolve → confirm → /claim → sync → assess the threads → return
```

## Step 1: Resolve the PR

1. Read the handle from `$ARGUMENTS`. If it is not there, ask for it. Run `gh` from the current
   folder, so that it reads this repo.
2. Find the open PR by the kind of handle:

   | Handle | Do |
   |---|---|
   | A PR URL | Take `<n>` from `github.com/<owner>/<repo>/pull/<n>`. If `<owner>/<repo>` is not this repo, stop, and say to run `pickup` from a clone of that repo. |
   | A PR number, or `#<n>` | Take `<n>`. |
   | Only a ticket key, such as `PROJ-123` | `gh pr list --state open --search "<key>" --json number,headRefName,title,url` |
   | Anything else | It is a branch: `gh pr list --state open --head "<branch>" --json number,headRefName,title,url` |

3. Use the result of a search:
   - One PR: continue with it.
   - Two or more: list them, and continue with the one that the user picks.
   - None for a ticket key: stop. Say that the ticket has no open PR, and that `/start-ticket`
     starts work on it.
   - None for a branch: stop. Say that the branch has no open PR, and that `/claim <branch>` gives
     its worktree.
4. Read the PR and its checks, in parallel:
   - `gh pr view <n> --json number,title,url,state,isDraft,headRefName,headRefOid,baseRefName,mergeable,reviewDecision`
   - `gh pr checks <n> --json bucket`: count the checks in each bucket.
5. If `state` is not `OPEN`, stop and give the state.

The branch is the `headRefName` of the PR. Never guess the branch from a ticket key.

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

Make the worktree match the PR head with no lost commit. Run each git command in the worktree, with
`git -C <path>`. Never run `reset --hard`.

1. Run `git status --porcelain`. If it prints a line, stop. Show the files, and say that the user
   must commit or move them before the next run. Change nothing.
2. If `git cat-file -e <headRefOid>` fails, get the PR head with `git fetch origin pull/<n>/head`.
3. Run `git rev-list --left-right --count <headRefOid>...HEAD`. It prints `<behind> <ahead>`.
   Use the row that fits:

   | Behind | Ahead | Do |
   |---|---|---|
   | 0 | 0 | The branch matches the PR. Continue. |
   | 1 or more | 0 | Run `git merge --ff-only <headRefOid>`. Then check that `git rev-parse HEAD` prints `<headRefOid>`. |
   | 0 | 1 or more | Stop. Show the local commits with `git log --oneline <headRefOid>..HEAD`. Ask whether to keep them. The next push sends them. Continue after a yes. |
   | 1 or more | 1 or more | Stop. Show both lists of commits. Say that the branch and the PR diverged, so a fast-forward cannot sync them. Change nothing. |

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
  `/code-review:mob-review` on the same branch uses the same key, so both runs go to one file.

Do not follow its Step 4. Step 6 below returns.

**Done when:** the report holds the threads run, or Step 1 found no open thread.

## Step 6: Return

Give:

1. The PR link, the branch, and the worktree path.
2. The sync result: the branch matched, the fast-forward took `<n>` commits, or the user kept `<n>`
   local commits.
3. The count of each verdict and the report path, or that the PR has no open thread.
4. The next action. Tick the rows in the report, then paste its prompt. The prompt runs
   `/code-review:apply-review`, which fixes test-first, commits once, and pushes once. Then it replies
   on and resolves the ticked threads.
5. To add a panel run to the same report, run `/code-review:mob-review` in the worktree. For the
   essential lanes only, run `/code-review:light-review`.
6. When `/claim` returned a handoff, its path. The user continues it with
   `/do-next @<handoff path>` in a session in the worktree.

Neither this skill nor `/code-review:apply-review` merges the base or watches CI.

**Done when:** the user has the worktree path, and the report path or the reason for no report.
