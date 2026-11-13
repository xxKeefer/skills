---
name: pr-news
description: >
  Summarise what happened on your open PRs and your review requests over a time period, one table
  per repo. Use when the user says "pr news" or "catch me up on my reviews", or is back from
  leave.
argument-hint: "[time-period, default last 24 hours]"
---

# PR News

The code host is GitHub, through `gh`. If the code host named in the user's instructions is not
GitHub, stop and say that this skill needs GitHub.

Turn a window of PR activity into one table per repo that the user can scan in a minute. One row
per PR, not one per event. The sibling of `/codebase-news`, which covers a repo's default branch.

## Step 1: Resolve the window

- Take `<time-period>` in any form that `date` or `git log --since` reads: `2 weeks`,
  `2026-10-07`, `last monday`. A range such as `2026-10-01..2026-10-14` also sets the end.
- No argument: use the last 24 hours.
- Turn the start and the end into ISO 8601 UTC timestamps, so you can compare them with the
  timestamps from `gh`.

**Done when:** you have a start timestamp and an end timestamp.

## Step 2: Find the PRs

Run the two searches. Both cover every repo that the user can see.

```sh
gh search prs --author=@me --state=open --limit 100 \
  --json repository,number,title,url,isDraft,updatedAt
gh search prs "user-review-requested:@me" --state=open --limit 100 \
  --json repository,number,title,url,isDraft,updatedAt
```

- `user-review-requested` matches only requests to the user, not requests to a team that the user
  is in.
- A PR in both lists is the user's own PR. Keep it in the first list only.
- Drop each PR whose `updatedAt` is before the start. Keep its number for the quiet list in Step 6.

**Done when:** you have two lists of PRs, each PR tagged with its `nameWithOwner`.

## Step 3: Read each PR

For each PR that Step 2 kept, run:

```sh
gh pr view <number> -R <nameWithOwner> --json \
  title,url,isDraft,state,headRefName,baseRefName,mergeable,reviewDecision,\
  commits,reviews,latestReviews,comments,statusCheckRollup,reviewRequests
```

Keep only the events inside the window:

| Source | What to keep |
| --- | --- |
| `commits` | Commits whose `committedDate` is in the window. Count them and read their headlines |
| `reviews` | Reviews whose `submittedAt` is in the window: the author, the state, and the body |
| `comments` | Comments whose `createdAt` is in the window: the author and the gist |
| `statusCheckRollup` | The current result. Name each check that failed |
| `mergeable` | `CONFLICTING` means the branch needs a rebase or a merge |
| `reviewDecision` | `APPROVED`, `CHANGES_REQUESTED`, or `REVIEW_REQUIRED` |

Review comments on code lines are not in `comments`. To count the unresolved threads, run:

```sh
gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){pullRequest(number:$n){reviewThreads(first:100){nodes{isResolved comments(last:1){nodes{author{login} createdAt}}}}}}}' \
  -F o=<owner> -F r=<repo> -F n=<number>
```

Count the unresolved threads, and the threads whose last comment is in the window.

For a review request, also find the user's last review in `reviews`. If commits landed after it,
the PR needs a re-review.

Leave out events by the user, and comments by bots that only post a status, such as coverage or
deploy previews. Keep a bot comment that asks for a change.

**Done when:** each PR has its in-window events and its current state.

## Step 4: Write each row

One row per PR. Write the news in short phrases, the most important first:

- **Your PR:** changes requested and by whom, new unresolved threads, failed checks, merge
  conflicts, approvals, then new commits by someone else.
- **Review request:** new request, new commits since your last review, replies to your threads,
  failed checks, then approvals by other reviewers.

End the row with what the user does next, if anything: "address 3 threads", "rebase", "re-review",
"ready to merge". Write `—` if there is nothing to do.

**Done when:** each PR has its news and its next action.

## Step 5: Build the tables

One section per repo, headed by the repo name. Order the repos by the number of PRs in them, most
first. In each section, list the user's own PRs, then the review requests.

```markdown
### owner/repo

| # | PR | role | state | news | next |
| --- | --- | --- | --- | --- | --- |
```

- `#`: the row number. Count from 1 across all tables, so the user can refer to "row 7".
- `PR`: `[#<number>](<url>) <title>`, with the ticket key kept. Add `(draft)` for a draft.
- `role`: `author` or `reviewer`.
- `state`: the review decision, the check result and the merge state, such as
  `changes requested, checks fail, conflicts`.
- `news`: the in-window events from Step 4.
- `next`: the next action from Step 4.
- An empty cell gets `—`, never a guess.

**Done when:** each PR with news is in one row.

## Step 6: Present

1. Above the tables, write at most three sentences. Give the window, the number of PRs with news,
   and the most urgent item, such as a change request on the user's PR.
2. Show the tables.
3. Below the tables, list the quiet PRs in one line per role, as `repo#number`.

If the user asks to keep the tables, delegate to `/write-to-file`.

## Principles

- **PRs, not events.** Ten comments on one PR make one row.
- **Your PRs first.** Your own work is blocked on feedback. A review request waits on you, but it
  blocks someone else.
- **Evidence only.** Every cell traces to a commit, a review, a comment, or a check from `gh`.
- **Read the remote.** Use `gh`, not a local checkout. The user may not have each repo cloned.
