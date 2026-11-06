---
name: pickup
description: >
  Pick up an open PR from its number, URL, branch, or ticket key: confirm the PR, claim its
  worktree, sync the branch by fast-forward only, then triage its open review threads into the
  handoff that /do-next runs. Use when the user asks to pick up a PR or a branch.
argument-hint: "<PR number or URL | branch | ticket key>"
---

# Pickup

Get onto an open PR with no lost work, and turn its review threads into a handoff. The next session
works the handoff with `/do-next`, so this skill ends at the handoff. It never pushes, and it never
discards a change.

```
resolve → confirm → /claim → sync → /triage-feedback → return
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

If `/claim` returns a handoff, the work can have a plan or earlier feedback tasks. Show the path.
Ask whether to continue that handoff or to triage the threads into a new handoff.

**Done when:** you have the worktree path, and you know whether to triage.

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
   | 0 | 1 or more | Stop. Show the local commits with `git log --oneline <headRefOid>..HEAD`. Ask whether to keep them. The push task of the handoff sends them. Continue after a yes. |
   | 1 or more | 1 or more | Stop. Show both lists of commits. Say that the branch and the PR diverged, so a fast-forward cannot sync them. Change nothing. |

**Done when:** the worktree holds the PR head and no commit is lost, or you stopped and changed
nothing.

## Step 5: Triage the threads

Skip this step when the user chose to continue the `/claim` handoff in Step 3.

Run `/triage-feedback <n>` if this session has it. Give it two inputs:

- Read the code that each thread names in the worktree, not in the current folder.
- Propose the handoff as `handoff_pr-<n>.md` in the folder that `/write-to-file` picks, because
  `/claim` finds handoffs there.

When the handoff exists, write `Worktree: <path>. Branch: <branch>.` on the line after its title.
`/do-next` reads this line to check the branch.

With no open thread, `/triage-feedback` writes no handoff. Without `/triage-feedback` in this
session, write no handoff. Say which case applies in Step 6.

**Done when:** the handoff has its `Worktree:` line, or you know why no handoff exists.

## Step 6: Return

Give:

1. The PR link, the branch, and the worktree path.
2. The sync result: the branch matched, the fast-forward took `<n>` commits, or the user kept `<n>`
   local commits.
3. The handoff path, or why no handoff exists.
4. The next command. The user starts a new session in the worktree, and runs
   `/do-next @<handoff path>`.

The handoff merges a stale base in its first task and watches CI in its last task, so this skill
does neither.

**Done when:** the user has the worktree path, and the next command or the reason for no handoff.
