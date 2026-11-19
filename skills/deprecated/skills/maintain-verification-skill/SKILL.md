---
name: maintain-verification-skill
description: "Merged into the maintain mode of create-verification-skill."
disable-model-invocation: true
deprecated: 2026-11-19
argument-hint: "[<driver name>]"
---

# Maintain a verification skill

A feature map goes stale when the app changes. This skill is the upkeep loop for a driver that
`/create-verification-skill` wrote. Cover each feature file from the source, and drive each feature
live. Do not prove each sentence.

Principle: **principle-prove-it-works**, a skill of the engineering plugin. Read it before you apply it, and name it in the reply when it shaped a choice.

`$SKILL_DIR` is this skill's base directory.

Run each source reader at the `explorer` role of the `models` block in `~/.claude/AGENTS.md`. Do
the live pass yourself at the `verifier` role. With no `models` block, use the session model.

```
locate → index hygiene → source wave → reconcile → live pass → triage → ship or stop
```

## Outcomes

Pick one, and say which:

- **clean**: each feature had source and live coverage, and nothing needs a fix. No commit.
- **changed**: proven fixes to the driver are shipped (Step 7).
- **blocked**: coverage could not finish, or a proven fix could not ship safely. Say what blocked
  it.

## Edit scope

Edit only the driver's own folder: its `SKILL.md`, `features/`, and the scripts that it ships.
Never edit product code. When the map describes a behaviour that the app no longer has, decide
which it is. Doc drift: fix the map. A product regression: report it to the user in the reply, and
do not hide it in the docs.

## Step 1: Locate the driver

1. Find each driver for this repo by the name `verify-<repo>-*` and the frontmatter key
   `repo: <repo>`. `<repo>` is the last part of `git remote get-url origin`, with no `.git`. Skip a
   driver whose `repo` value differs. Search `<repo root>/.claude/skills/` and
   `~/.claude/skills/`. These are the places that `/verify` searches.
2. The argument can name the driver. With several matches and no argument, ask the user which one.
3. With no match, stop. Point the user at `/create-verification-skill`. Do not invent a target.

**Done when:** you have one driver folder, or you have stopped with that pointer.

## Step 2: Index hygiene

1. Read `<driver>/features/README.md`, and list the files in `features/`.
2. Fix each missing, extra, duplicate, or dead entry in the index.
3. Find the `check_driver.py` of the engineering plugin, and run it. The first path is a repo
   checkout, and the second is the newest engineering version in the plugin cache:

   ```bash
   CHECK="$SKILL_DIR/../../../engineering/skills/create-verification-skill/scripts/check_driver.py"
   [ -f "$CHECK" ] || CHECK="$(ls -d "$SKILL_DIR"/../../../../engineering/*/ | sort -V | tail -1)skills/create-verification-skill/scripts/check_driver.py"
   python3 "$CHECK" <driver dir>
   ```

   Fix each error that it names, and run it again.

**Done when:** the index matches the files, and the script prints `ok`.

## Step 3: Source wave

1. Start one read-only subagent for each feature file, all in parallel, at the `explorer` role.
2. Each subagent explains from the source how its feature works for a user. It flags likely doc
   drift with a citation (file and line), and returns one live recipe.
3. A subagent never drives the app and never edits a file.
4. Each subagent returns four parts: feature summary, source entry points, likely drift or
   `none`, and one recipe.

**Done when:** each feature file has a returned summary.

## Step 4: Reconcile

1. Merge recipes that overlap into as few app states as you can.
2. Spot-check each cited drift against the source. Do not re-prove a claim that has no flag.
3. Look at recent changes (`git log` on the app paths) for a user-facing surface that the map does
   not hold. Call a surface missing only when you can name its source path.

**Done when:** you have a list of confirmed drift, a list of missing surfaces, and the merged
recipes.

## Step 5: Live pass

Do this step even when the source looks clean. Follow the Launch section of the driver. It decides
the model: one long-lived instance that you drive in series, or a fresh session for each drive.

1. Drive each feature at least once.
2. Keep three rules for the whole pass:
   - Never drive an instance that you did not check since it last did something odd. Run Doctor
     before the first drive, on each fresh session, and after each failed drive. When Doctor cannot
     see the fault (a stuck screen on a healthy process), reset to a known state or start again.
   - Evidence that you kept survives each cleanup. Check it at the place that the driver names.
   - Nothing that a drive started outlives the drive. Clean the residue of a failed try, also when
     the session is stuck, exited, or shared. For a shared instance, clean the residue and keep the
     instance.
3. A Doctor failure that the driver's own drift caused is drift. Fix it within the edit scope, and
   try once more. Restart only what the fix broke. Then call the pass `blocked` if it still fails.
4. A feature that you cannot reach is `verified-unreachable`, and only with the prerequisite (sign
   in, entitlement, OS, outside state) and the route that you tried. When the map omits that
   prerequisite, that is drift.
5. Drive each harness fix again live before it ships.
6. Tear down after the last drive of the run, the re-proofs included. The evidence stays.

**Done when:** each feature has a live result (`pass`, `fail`, or `verified-unreachable`), and no
instance that the run started is still up.

## Step 6: Triage

| Finding | Class | Action |
|---|---|---|
| The user-POV text is wrong or missing | Doc drift | Fix it in the driver |
| The app works, and the harness cannot drive it | Harness gap | Fix the harness. A script stays executable, and the Helpers section shows its call |
| The app behaviour is broken | Product regression | Record it for the user. Keep it out of the commit |

Run the layout check again after the fixes.

**Done when:** each finding has a class, and the check prints `ok`.

## Step 7: Ship or stop

- **clean** and **blocked**: make no commit. Report the outcome and the coverage as it was.
- **changed**: re-read each changed file first. Then ship by the place of the driver:
  - A driver in the repo (`.claude/skills/`): make one commit of the proven fixes on the agent's own
    branch, and open a draft PR with `/create-pr`. Both need no stop on the pause list.
  - A driver in `~/.claude/skills/`: the edit in place is the whole ship. Open no PR.

Write short run notes in a scratch file with `/write-to-file`, doctype `scratch`: the features
covered, each unreachable prerequisite, the confirmed drift, and the outcome. Never commit the
notes.

**Done when:** the reply names the outcome, the coverage, each product regression for the user, and
the commit or PR when there is one.
