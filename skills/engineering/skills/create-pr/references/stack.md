# Stacks and merge order

Read this file only when the branch is in a gh stack (`gh stack view` succeeds), or when the plan
header has a `merge` key.

## The stack skill

For stack work, compose the stack skill of the code host. On GitHub, that skill is `/gh-stack`,
which ships with the `gh stack` extension. Run each `gh stack` command as that skill says.

If this session does not list `gh-stack`, stop and ask the user to install it with
`gh skill install github/gh-stack`. Do not install it yourself.

## Step 1: the base and the merge PRs

1. In a gh stack, the base is the branch below this one in `gh stack view`.
2. If the `merge` key names sub-task keys, find the PR of each key:
   - Find `plan_<SUBKEY>.md` in the folder that item 3 of [`read.md`](read.md) searches, and its subfolders. Read
     the `branch` key of its YAML header.
   - Run `gh pr list --head <its branch> --state all --json number`.
   - With no plan, no `branch` key, or no PR, use the key.

## Step 5: the merge line

Make the merge line the first line of the body:

- `merge: alone` gives `Merges alone.`
- `merge: after <SUBKEY list>` gives `Merge after <list>.` Name each PR from Step 1, else its
  sub-task key, such as `Merge after #12 and <SUBKEY>.`
- In a gh stack with a base other than the default branch, add: `Merge after #<base PR>. After it
  merges, run gh stack sync, then merge this PR.` A squash merge of the lower PR leaves its old
  commits in this branch, and the sync drops them.

## Step 7: push and open

1. Push with `gh stack push`, through the `gh-stack` skill. It force-pushes each branch with a
   lease, which a rebased stack needs. ADR 0011 allows this push.
2. With no open PR, open it with `gh stack submit --auto`. This opens drafts and links the stack
   on GitHub. Then set the title and the body with `gh pr edit`, and request the bot review with
   the `gh api` call in Step 7 of `SKILL.md`.
