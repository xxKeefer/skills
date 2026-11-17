---
doctype: spec
ticket: none
status: confirmed
goal: "/ship on a rebased stack layer accepts the old review when the patch-id matches."
---

# Spec: `ship` with gh-stack, and the map layout

## Intent

- Outcome: `/ship` proves that a review still describes the head after a gh-stack rebase, and every map that a skill writes passes the map check.
- User: the user who runs `/work-on` on a map, and ships stacked layers.
- Why now: map unit 15 (r1.11). The workflow uses gh-stack, so a rebase must not void a review.
- Success: a rebased layer with the same patch-id passes the Review check of `/ship`. A map from `/split-ticket` passes `map_units.py next`.
- Constraint: subtract before you add. Replace the old rule with the new one, and write no second check that does the work of an existing one.
- Out of scope: `create-pr` Step 2 (the drift warning), `babysit` (unit 16).

## Decisions

- Subtract first: `ship` already has a Stack check (`gh stack rebase --upstack`), a `range-diff` rule in its Review check, and `gh stack sync` in Step 5. Change these rows. Add no new section.
- One patch-id replaces the `range-diff` rule and the `.ai/` exception: compare `git patch-id --stable` of the reviewed diff and the current diff, both with the pathspec `':!.ai'`. Equal means the review describes the head. A rebase, a clean merge of the base, and a commit to `.ai/` only all keep the patch-id. A changed line does not.
- The Stack check fix becomes `gh stack sync`: it fetches, rebases with the tool, and pushes in one command. Remove the manual pull and rebase.
- Read the PR back after the merge: `gh pr view <number> --json state,mergeCommit` shows `MERGED`, and its `mergeCommit` names the commit whose run Step 5 watches. Replace the vague "find the run" line.
- The map check is `map_units.py next`. It already checks the `## Units` section, each heading, each `Done:` line, and `batch`. Write no `check_map.py`. The map playbook already runs it at step 1, before each batch.
- The map layout is a template: `write-to-file/templates/map.md`. `/split-ticket` points at it and drops its inline copy. Reason: the inline copy has no `## Units` heading, so `map_units.py next` rejects each map that `/split-ticket` writes.
- The fixture is a copy of this map (`work-on/scripts/fixtures/map_program.md`), because `.ai/` files go when the program ends. Refresh the copy from the current header and unit headings.

## Acceptance criteria

- [ ] **A.** Run the `ship` Stack check on a layer whose lower branch moved → the fix that it names is `gh stack sync`. Run the Review check on a rebased layer → it compares `git patch-id --stable` of the reviewed diff and of the current diff, both without `.ai/`. Run Step 5 → it reads the PR back with `gh pr view` and watches the run of its `mergeCommit`.
- [ ] **B.** Write a map with `/write-to-file`, or with `/split-ticket` → the map has the template layout, and `map_units.py next` on it exits 0. Run `map_units.py next` on the fixture → it lists unit 15 first.
- [ ] **C.** Read the `ship` Stack and Review checks → they cover gh-stack sync and a rebase with no manual git rebase step.
- [ ] **D.** Run `/ship` on a rebased stack layer whose old review has the same patch-id → the Review check passes. Change one line on that layer → the Review check fails, and its fix is `/review`.
