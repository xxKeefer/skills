# Experimental

Personal skills on probation. Promote once usage justifies it; demote to `deprecated` if it doesn't.

## Skills

| Skill | Purpose |
|---|---|
| `/append-to-note` | Append something from the conversation to a named note, in that note's style |
| `/lobotomize` | Table the agent's memories by age and purpose, then purge the ones the user multi-selects |
| `/post-review-comments` | Post the review findings you tick to the PR: show each draft, then post the approved ones as one comment review. Five or more picks go to a handoff |
| `/repro` | Give the numbered steps to reproduce an issue, from a cold start to the trigger |
| `/review-pr` | Resolve a PR from its number, URL, branch, or ticket key, claim its worktree, sync it, run `/mob-review` there, then offer `/post-review-comments` |
| `/roleplay` | Play a narrative scene in character from `🎬 ACTION! 🥸` to `OK_STOP`, then debrief what the play surfaced |
| `/simulate` | Stand in for a technical system from `⚙️ RUNNING! 🧪` to `OK_STOP`, then debrief where the render cheated |
| `/squash-bugs` | Fix a batch of QA bug tickets in parallel, one worktree and one subagent per ticket, then report every fix and every open decision |
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
