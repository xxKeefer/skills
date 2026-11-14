# Solo or team

Checkpoints protect other people. When no other person sees the work before it ships, a
checkpoint only slows the user down.

The work is **solo** when one of these is true:

- The user's instructions say that the repo or the work is solo.
- The repo has no human author other than the user in the last 90 days
  (`git shortlog -sne --since=90.days HEAD`, minus bots), and no open PR has a human reviewer
  other than the user.

Else the work is **team**. When you cannot tell, treat it as team.

In solo mode:

- Push the work branch, open the PR, and run CI on it without asking.
- Check each result that a command can show yourself. Ask the user only for a real decision, or
  for a result that needs eyes on a screen.
- Mark the PR ready and merge it after `/ship` gives go. The user reviews after the fact.

In team mode, keep every checkpoint that the skill gives. Never push the default branch in either
mode.
