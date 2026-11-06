---
name: update-personas
description: Refresh the persona-* reviewer skills so they stay accurate. Re-check persona-best-practice against the versions actually installed in the target repo (and what has since shipped upstream), and run the shared structural lint over any other persona. Use when the user says "update personas", "refresh the personas", "the personas are stale", "check the best-practice versions", or after a big dependency bump.
---

# update-personas: keep the review panel accurate

Personas rot in two ways: **version rot** (`persona-best-practice` recommends an API that is now legacy, or flags one that is now the default) and **structural drift**: a broken output contract, a lane that overlaps another, a guard that no longer matches the panel table.

Edit the personas in the marketplace checkout, under `skills/review/skills/`. When the domain loads from a directory source, `${CLAUDE_SKILL_DIR}/..` is that folder. If `${CLAUDE_SKILL_DIR}` sits under `~/.claude/plugins/cache`, it is an installed copy that an update overwrites: ask for the checkout path. Stop and ask if the checkout has uncommitted work. Below, `$SKILL_DIR/..` means that folder, and the panel that spawns the personas is `$SKILL_DIR/../mob-review/SKILL.md`.

## Modes

Read the argument:

- *(none)* or `all`: run **Part A** (best-practice), then **Part C** (structural lint) over every persona.
- `best-practice`: Part A only.
- `persona-<name>`: Part C for that persona only.
- `backlog`: Part C item 7 for every approved entry, then items 1 to 6 for each persona that item 7
  changed, then item 8. `/review:self-improve` runs this mode.

## Rules that apply to every edit

- **Never copy the persona contract into a persona.** The shared Scope, findings, and output rules live in `$SKILL_DIR/../../PERSONA-CONTRACT.md`, and `mob-review` parses its JSON. Do not change that JSON unless you change `mob-review` Steps 4 and 5 in the same pass.
- Keep the frontmatter fields (`name`, `description`, `disable-model-invocation: true` on every `persona-*`) and the section order: Guard → Scope → What you review → Out of lane → Severity → Output.
- **Adding** a rule is routine. **Removing** a rule, dropping a lane, or deleting a persona needs the user's OK first. State what you'd remove and why.
- Every rule must be checkable against a changed line in a diff. If you can't say what the reviewer greps for, don't add it.
- When a persona's `description`, guard, or existence changes, update the matching row (and the description list) in `mob-review/SKILL.md` in the same pass.

## Part A: `persona-best-practice` version refresh

The persona's whole premise is "you're on a modern version, use the modern API." That premise needs both numbers: what's **installed** and what's **current**.

### A1. Read the installed versions

Ask for the path of the target repo the personas review.

```bash
cd <target repo checkout>
rg -N '"(vue|typescript|pinia|vue-router|@tanstack/vue-query|reka-ui|zod)":' package.json apps/*/package.json libs/*/package.json
cat .nvmrc
```

Prefer the resolved version over the range: `pnpm why vue` or `rg -A2 "^  vue@" pnpm-lock.yaml` when a range is ambiguous. Note any package where apps disagree; that mismatch is itself worth telling the user about (syncpack should catch it).

### A2. Read the current upstream versions

```bash
npm view vue version; npm view typescript version; npm view pinia version
npm view vue-router version; npm view @tanstack/vue-query version; npm view reka-ui version
```

For what *changed* between installed and latest, use the library's release notes / changelog (`npm view <pkg> repository.url` finds them), or the `context7` MCP if you have it installed. Do not answer from memory: the personas exist precisely because memory goes stale.

### A3. Reconcile each `references/*.md`

Files: the version references in `persona-best-practice/references/`, whose title says "written against" a version (currently `vue.md`, `vue-router.md`, `typescript.md`, `pinia.md`, `tanstack-query.md`, `node.md`). The other files in that folder hold rules moved out of `SKILL.md`, and A4 checks them. For each version reference, compare its header version against A1 and fix these classes of drift:

| Drift | Fix |
|---|---|
| Header says an older version than installed | Update the header **and** re-read the rules under it: a rule justified by "stable since 3.4" may now be the plain default |
| An API the file calls "new/opt-in" is now the documented default | Promote it: raise the severity, reword from "prefer" to "use" |
| An API the file recommends is now deprecated or superseded | Replace it; move the old form to the flag-list |
| Installed version gained a stable API the file doesn't mention | Add a section: recommended form, legacy form to flag, severity |
| A rule guards against something the installed version made impossible | Propose removal (needs user OK) |
| Latest upstream is a major ahead of installed | Do **not** write the new major's API in as a rule. Add it under a `## Not yet — installed is vN` note so the next bump has a checklist |

### A4. Sync `SKILL.md` to the references

The persona's opening line lists installed versions inline (`Vue 3.5.17, TS 6.0.2, …`): update it. Then check every bullet under "What you review", and in each rule file that it links, still has a backing section in a version reference, and that severities match. The SKILL.md is the index; the references are the detail. They must not disagree.

### A5. Report

Show a table: package | installed | latest | reference updated? | rules added/changed/removed.

## Part C: structural lint (any persona)

For each persona in scope, verify and fix:

1. **Frontmatter**: `name` matches the directory; `disable-model-invocation: true` present; `description` names the lane, the trigger phrasings, and what it explicitly does *not* cover.
2. **Guard matches the panel.** The guard sentence in the persona and the Guard column in `mob-review/SKILL.md` must describe the same condition.
3. **Contract pointer intact.** The first line under the frontmatter is the pointer, word for word: "Read [`PERSONA-CONTRACT.md`](../../PERSONA-CONTRACT.md) before you start, and follow every rule in it." The Output section names the `category` slug. The persona holds no copy of contract text: no git fallback block, no Code references paragraph, no JSON line.
4. **No lane overlap.** For each rule, check no other persona claims it. If two do, the narrower one keeps it and the other gains an "Out of lane" line pointing at it.
5. **Severity list covers every rule**: each rule appears in exactly one tier.
6. **Dead references**: a `references/` file nothing links to, or a link to a file that doesn't exist.
7. **Calibration backlog.** `mob-review` Step 7 records edits from real runs in `${XDG_STATE_HOME:-$HOME/.local/state}/self-improve/improve-personas.md`. Apply each entry with `Status: approved`, then delete that entry from the backlog. Leave `open` and `rejected` entries as they are.
8. **Scrub check clean.** Stage the persona changes, then run `.githooks/pre-commit` from the root of the marketplace checkout. It must print nothing.

## Finish

Print one table (persona | changed? | what changed) and list anything you deliberately left for the user to decide (removals, version majors not yet installed). Don't commit unasked: leave the changes in the marketplace checkout and offer to commit.
