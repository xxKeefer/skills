# PR handle

`review-pr` and `pickup` both start from a PR handle. This file holds the two steps they share.

## Resolve the PR

1. Read the handle from `$ARGUMENTS`. If it is not there, ask for it. Run `gh` from the current
   folder, so that it reads this repo.
2. Find the open PR by the kind of handle:

   | Handle | Do |
   |---|---|
   | A PR URL | Take `<n>` from `github.com/<owner>/<repo>/pull/<n>`. If `<owner>/<repo>` is not this repo, stop, and say to run the skill from a clone of that repo. |
   | A PR number, or `#<n>` | Take `<n>`. |
   | Only a ticket key, such as `PROJ-123` | `gh pr list --state open --search "<key>" --json number,headRefName,title,url` |
   | Anything else | It is a branch: `gh pr list --state open --head "<branch>" --json number,headRefName,title,url` |

3. Use the result of a search:
   - One PR: continue with it.
   - Two or more: list them, and continue with the one that the user picks.
   - None: stop. Say that the handle has no open PR, and give the next step that the calling skill
     names.

The branch is the `headRefName` of the PR. Never guess the branch from a ticket key.

## Sync the worktree

Make the worktree hold the PR head with no lost commit. Run each git command in the worktree, with
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
   | 0 | 1 or more | Show the local commits with `git log --oneline <headRefOid>..HEAD`. Do what the calling skill says for local commits. |
   | 1 or more | 1 or more | Stop. Show both lists of commits. Say that the branch and the PR diverged, so a fast-forward cannot sync them. Change nothing. |

**Done when:** the worktree holds the PR head and no commit is lost, or you stopped and changed
nothing.
