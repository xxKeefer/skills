---
name: review
description: "★ Review: review a branch or a PR. The current branch gets /light-review, or /mob-review when you say full. A PR number, URL, or ticket key goes to /review-pr."
argument-hint: "[full] [<PR number | URL | ticket key>]"
disable-model-invocation: true
---

# Review

Review code before it merges. The review skills do the work. This command picks one.

## Step 1: Route

| `$ARGUMENTS` | Run |
|---|---|
| A PR number, a PR URL, a branch name, or a ticket key | `/review-pr` with it. |
| `full` and nothing else | `/mob-review` on the current branch. |
| Empty | `/light-review` on the current branch. |

Pass the plan handoff path to the review skill when one exists, for the AC and test-design checks.
Find it as `/build` Step 1 does.

**Done when:** one review skill ran and wrote its report.

## Step 2: Hand on

Give the next command:

- Open rows on your own branch: the prompt that the report builds.
- Open rows on someone else's PR: tick the rows, then paste the prompt that the report builds.
- No open rows on your own branch: `/ship`.

**Done when:** the user has the next command.
