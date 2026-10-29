---
name: discover-vault-directory
description: >
  Find a folder in the user's Obsidian vault from a glob relative to the vault root, plus optional
  marker files the folder must hold, and return its absolute path. Use when another skill needs a
  vault folder, such as `*projects` or the folder that holds `occasions.md`.
---

# Discover Vault Directory

Find one folder in the user's Obsidian vault. Scan on every run, and store nothing.

The caller gives a glob relative to the vault root, then optional marker files after `holding`.
The glob sets the scan depth.

```
/discover-vault-directory *reference
/discover-vault-directory * holding occasions.md
/discover-vault-directory *omen/* holding log.md lore/_cannon.md
```

## Step 1: Find the Vault Root

The vault root is a folder that holds `.obsidian/`. Use the first of these that exists:

1. `~/studio/notes`.
2. The current folder, or the nearest parent folder, that holds `.obsidian/`.
3. A search of the home folder for `.obsidian/`. On one match, use it. On many, ask the user which
   vault. On zero, ask the user where the vault is.

**Done when:** you have the absolute path of a folder that holds `.obsidian/`.

## Step 2: Match the Folder

Expand the glob from the vault root. Keep only the folders that hold every marker file.

- **One match** -- use it.
- **Many matches** -- list them, and ask the user which one.
- **Zero matches** -- ask the user where the folder is.

**Done when:** you have reported the absolute path of one folder.
