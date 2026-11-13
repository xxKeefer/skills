# Diff scope: the special cases

Step 1 reads this file when one of these cases applies. Each case changes how Step 1 computes the
diff.

## Stacked PR

When the PR's base (`gh pr view --json baseRefName`) is not `main`, review vs `origin/<baseRefName>` instead, in every git command of Step 1 and in what the personas are told. The base branch's commits are its own PR's to review.

## Uncommitted work

If the branch has no commits ahead of `origin/main` but the working tree is dirty, the change hasn't been committed yet. Review the working tree instead: drop `HEAD` from the three `git diff` commands (`git diff --merge-base origin/main` includes staged and unstaged changes), and suffix `SCRATCH` with `-wt`. `/engineering:apply-review` then leaves its fixes in the working tree.

## Branch behind `main`

A merge-base diff still carries commits that already landed on `main` by squash merge (a sibling ticket's PR, or an earlier slice of a stack), so the panel would review code that is not this PR's change. When `git rev-list --count HEAD..origin/main` is non-zero, compare `git diff --stat --merge-base origin/main HEAD` against the diff a merge would leave: `git diff --stat origin/main $(git merge-tree --write-tree origin/main HEAD | head -1)`. If the second is clearly smaller, stop and offer to merge `origin/main` first (own code) or tell the author (someone else's), then recompute the scope. Conflicts reported by `merge-tree` are part of the offer.
