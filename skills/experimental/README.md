# Experimental

Personal skills on probation. Promote once usage justifies it; demote to `deprecated` if it doesn't.

## Skills

| Skill | Purpose |
|---|---|
| `/lobotomize` | Table the agent's memories by age and purpose, then purge the ones the user multi-selects |
| `/prune-worktrees` | Remove the worktree and branch of each merged PR, the worktree of each branch that a stack in another worktree holds, and the worktree of each old branch with no PR, after one yes |
| `/restack` | Move a stack of branches onto the latest default branch in one rebase, drop each squash-merged branch, push the open branches, and delete the merged ones |
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
