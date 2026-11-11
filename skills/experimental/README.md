# Experimental

Personal skills on probation. Promote once usage justifies it; demote to `deprecated` if it doesn't.

## Skills

| Skill | Purpose |
|---|---|
| `/lobotomize` | Table the agent's memories by age and purpose, then purge the ones the user multi-selects |
| `/prune-worktrees` | Remove the worktree and branch of each merged PR, and the worktree of each old branch with no PR, after one yes |
| `/restack` | Rebase a stack of branches with `gh stack`, across the `wt` worktrees that hold them, and push. Leaves the bottom branch alone while its PR is open, and removes the merged branches. Needs `gh stack`, `wt`, and the official `gh-stack` skill at user level |
| `/retro` | Read a session, find what in the skills, hooks, rules, and steering slowed or misled the agent, then apply and commit the fixes the user picks |
| `/roleplay` | Play a narrative scene in character from `🎬 ACTION! 🥸` to `OK_STOP`, then debrief what the play surfaced |
| `/simulate` | Stand in for a technical system from `⚙️ RUNNING! 🧪` to `OK_STOP`, then debrief where the render cheated |

## Installation

```json
{
  "enabledPlugins": {
    "experimental@xxkeefer-skills": true
  }
}
```
