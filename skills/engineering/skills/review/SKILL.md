---
name: review
description: >
  ★ Review: review a branch or a PR. The current branch gets /mob-review light, or /mob-review when you
  say full. A PR number, URL, or ticket key goes to /review-pr. Use when the user says "review", or
  asks to review a branch, a PR, or a ticket key.
argument-hint: "[full] [<PR number | URL | ticket key>]"
---

# Review

Review code before it merges. The review skills do the work. This command picks one.

## Step 1: Route

| `$ARGUMENTS` | Run |
|---|---|
| A PR number, a PR URL, a branch name, or a ticket key | `/review-pr` with it. |
| `full` and nothing else | `/mob-review` on the current branch. |
| Empty | `/mob-review light` on the current branch. |

Pass the plan path to the review skill when one exists, for the AC and test-design checks.
Find it as `/implement` Step 1 does.

**Done when:** one review skill ran and wrote its report.

## Step 2: Hand on

Give the next command:

- Open rows on your own branch: the prompt that the report builds.
- Open rows on someone else's PR: tick the rows, then paste the prompt that the report builds.
- No open rows on your own branch: `/ship`.

**Done when:** the user has the next command.
