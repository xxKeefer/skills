# Experimental

Personal skills on probation. Promote once usage justifies it; demote to `deprecated` if it doesn't.

## Skills

| Skill | Purpose |
|---|---|
| `/append-to-note` | Append something from the conversation to a named note, in that note's style |
| `/auto-handoff` | Run every remaining step of a handoff, one fresh subagent per step, then batch the open decisions for the user |
| `/claim` | Find or create the worktree for a ticket, a PR, or a branch, then record it in the handoff. Needs worktrunk (`wt`) |
| `/create-pr` | Check the review for drift, fill the repo's PR template with an AC table and its gaps, then push and open a draft PR after one yes |
| `/lobotomize` | Table the agent's memories by age and purpose, then purge the ones the user multi-selects |
| `/pickup` | Confirm an open PR, claim its worktree, sync it by fast-forward only, then triage its review threads into a handoff |
| `/post-review-comments` | Post the review findings you tick to the PR: show each draft, then post the approved ones as one comment review. Five or more picks go to a handoff |
| `/repro` | Give the numbered steps to reproduce an issue, from a cold start to the trigger |
| `/review-pr` | Resolve a PR from its number, URL, branch, or ticket key, claim its worktree, sync it, run `/mob-review` there, then offer `/post-review-comments` |
| `/roleplay` | Play a narrative scene in character from `🎬 ACTION! 🥸` to `OK_STOP`, then debrief what the play surfaced |
| `/scope-ticket` | Size a ticket with cheap probes, then give one verdict (SCOPED, SPLIT, or CLARIFY) and offer a points estimate |
| `/simulate` | Stand in for a technical system from `⚙️ RUNNING! 🧪` to `OK_STOP`, then debrief where the render cheated |
| `/squash-bugs` | Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision |
| `/start-ticket` | Scope a ticket, claim its worktree, then write the plan handoff with lettered ACs and a test approach for you to approve |
| `/triage-dir` | Sort a cluttered directory into category folders, then report each folder in `triage.html` with a keep, archive, or delete suggestion |
| `/zsh-insights` | Mine the zsh history for aliases, functions, and scripts, show them in an HTML report, then write the picks to `~/.config/zsh/` |

## Installation

```json
{
  "enabledPlugins": {
    "experimental@xxkeefer-skills": true
  }
}
```
