---
name: patch-doctor
description: >
  Diagnose and fix drift between a skill's current output contract and the artifacts it already
  produced. Call it when a skill misbehaves or its generated files look stale after a plugin update --
  point it at the skill and/or domain and it reconciles live vault artifacts and repo example files,
  dry-run first. Use when the user says "patch-doctor", "this skill is acting weird", "fix the drift",
  or "the generated file is out of sync".
---

# Patch Doctor

A reactive drift-reconciler. After you update plugins and start using skills, you sometimes notice a
discrepancy -- a skill fails, a generated file looks stale, output is subtly wrong. You point
patch-doctor at the offending skill (and/or its domain) and it works out what drifted and fixes it,
showing you the changes before writing anything.

> The intended workflow: **1.** update plugins -> **2.** use skills -> **3.** notice weirdness ->
> **4.** `/patch-doctor <skill> <domain>` -> **5.** patch-doctor resolves it contextually.

> **Never commit in the vault.** The user manages vault git separately. Repo commits are a separate
> deliberate step too -- write files, then stop.

## Step 1: Scope the Complaint

Parse `$ARGUMENTS` for a skill name, a domain, and/or a free-text description of the weirdness
("dates not showing", "occasions missing", "board won't render"). At least one of skill/domain is
expected; if neither is given, ask:

> What's acting up? Give me the skill name, the domain, or describe the weirdness.

If only a domain is given, list its skills and ask which one(s) -- or take "all of them" and sweep.

## Step 2: Learn the Contract

For each suspect skill, read its `SKILL.md` and any `*-FORMAT.md` it references to learn:

- **What it produces** -- the artifacts it writes and where (live vault files, repo example/template
  files).
- **The current shape** of those artifacts (object shape, required sections, frontmatter, columns).

Then check git for *why* it might have drifted: `git log`/`git diff` on the skill's path (default
window: this branch vs its merge-base with `main`). A recent contract change is the usual culprit and
tells you exactly what to look for.

## Step 3: Find the Drift

Compare reality to the current contract. Two artifact kinds, two methods:

- **Generator artifacts** (a skill writes a derived file from a source -- e.g.
  `update-occasions-config` writes `vault_occasions.js` from `occasions.md`): **invoke the generator
  skill itself** against current inputs and diff its result against the on-disk file. Do not
  reimplement its logic -- composing the live skill means patch-doctor always uses the current
  behaviour.
- **Spec-defined artifacts** (files that must match a `*-FORMAT.md` or template -- boards, mission
  files, the `occasions.md` template, journal templates): structurally compare each live file to the
  current contract and list what's missing or mismatched (a table missing a new column, an absent
  section, wrong frontmatter).

Check **both** the live vault artifact and the repo's example/template copy -- they drift apart too.

## Step 4: Dry-Run Preview

Present every proposed change before touching anything:

> **patch-doctor: {skill}** -- {N} files with drift
>
> `path/to/file` -- {one-line what's wrong}
> ```diff
> {the proposed change}
> ```
>
> Apply? (per-file or all)

If nothing drifted, say so plainly -- "in sync, no changes". That's a valid and useful result: proof
the skill is healthy.

## Step 5: Apply on Confirm

Write only approved changes, file by file. Rules:

- **Preserve user-authored content.** Source-of-truth files (e.g. `occasions.md` with real
  birthdays, personal one-offs) are authoritative -- only add or fix *structure*, never delete user
  rows.
- **Regenerate after patching a source.** If you patched a generator's input, re-run the generator so
  the derived file is rebuilt cleanly.
- **Don't guess.** If a skill's targets can't be determined from its docs, or a fix is ambiguous,
  flag it for the human instead of inventing one.
- **No commits** -- vault or repo.

## Step 6: Report

> Checked **{skill(s)}**:
> - Fixed: {files} ({what})
> - In sync: {files}
> - Flagged for you: {anything ambiguous or undeterminable}
>
> Re-run the skill to confirm the weirdness is gone. (Reload Obsidian if a vault file changed.)
