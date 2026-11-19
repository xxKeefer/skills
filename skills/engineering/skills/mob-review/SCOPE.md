# Diff scope

Step 1 reads this file on each run, and runs its commands.

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
