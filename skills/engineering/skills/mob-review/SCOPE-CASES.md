# Diff scope: special cases

Step 1 reads this file before it computes the diff when a case below is true. A case changes how
the commands of [`SCOPE.md`](SCOPE.md) compute the diff.

## Uncommitted work

If the branch has no commits ahead of `$BASE` but the working tree is dirty, the change hasn't been committed yet. Review the working tree instead: drop `HEAD` from the three `git diff` commands (`git diff --merge-base "$BASE"` includes staged and unstaged changes), and suffix `SCRATCH` with `-wt`. `/engineering:apply-review` then leaves its fixes in the working tree.

## Branch behind its base

A merge-base diff still carries commits that already landed on the base by squash merge (a sibling ticket's PR, or an earlier slice of a stack), so the panel would review code that is not this PR's change. When `git rev-list --count HEAD..$BASE` is non-zero, compare `git diff --stat --merge-base "$BASE" HEAD` against the diff a merge would leave: `git diff --stat "$BASE" $(git merge-tree --write-tree "$BASE" HEAD | head -1)`. If the second is clearly smaller, stop and offer to merge `$BASE` first (own code) or tell the author (someone else's), then recompute the scope. Conflicts reported by `merge-tree` are part of the offer.
