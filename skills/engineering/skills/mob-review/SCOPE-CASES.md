# Diff scope

Step 1 reads this file on each run. Run the commands of the first two sections. A special case
changes how they compute the diff.

## Compute the scope

Compute the changed-file list and the diff **once, to disk**, and hand every persona those paths instead of a command each one re-runs:

```bash
SCRATCH="${TMPDIR:-/tmp}/mob-$(git rev-parse --abbrev-ref HEAD | tr / -)-$(git rev-parse --short HEAD)"
mkdir -p "$SCRATCH"
git diff --name-only --merge-base "$BASE" HEAD > "$SCRATCH/files.txt"
git diff        --merge-base "$BASE" HEAD > "$SCRATCH/diff.patch"
git diff --stat --merge-base "$BASE" HEAD | tail -1
cat "$SCRATCH/files.txt"
```

The path holds the branch and the SHA, so a run after a fix commit never reads a stale patch.

## Record the SHAs and the owner

Record the two SHAs the panel reads. Step 5 prints them, so a later push step can compare the branch with what the panel read:

```bash
git rev-parse --short "$(git merge-base "$BASE" HEAD)"   # base
git rev-parse --short HEAD                                   # head
```

Record whose code this is, for the ownership rule of Step 1:

```bash
git config user.email                                          # you
git log --format='%ae' $(git merge-base "$BASE" HEAD)..HEAD | sort -u   # branch authors
```

## Special cases

### Uncommitted work

If the branch has no commits ahead of `$BASE` but the working tree is dirty, the change hasn't been committed yet. Review the working tree instead: drop `HEAD` from the three `git diff` commands (`git diff --merge-base "$BASE"` includes staged and unstaged changes), and suffix `SCRATCH` with `-wt`. `/engineering:apply-review` then leaves its fixes in the working tree.

### Branch behind its base

A merge-base diff still carries commits that already landed on the base by squash merge (a sibling ticket's PR, or an earlier slice of a stack), so the panel would review code that is not this PR's change. When `git rev-list --count HEAD..$BASE` is non-zero, compare `git diff --stat --merge-base "$BASE" HEAD` against the diff a merge would leave: `git diff --stat "$BASE" $(git merge-tree --write-tree "$BASE" HEAD | head -1)`. If the second is clearly smaller, stop and offer to merge `$BASE` first (own code) or tell the author (someone else's), then recompute the scope. Conflicts reported by `merge-tree` are part of the offer.
