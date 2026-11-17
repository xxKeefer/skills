---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-15_ship-stack
status: approved
goal: "/ship on a rebased stack layer accepts the old review when the patch-id matches."
spec: .ai/spec_pstack-15.md
---

# Plan: pstack-15 `ship` with gh-stack, and the map layout

## Goal

Replace the `range-diff` rule and the manual rebase in `ship` with one patch-id compare and `gh stack sync`, read the PR back after the merge, and give the map one layout that the map check accepts. Scope: SCOPED, one PR.

## Spec

`.ai/spec_pstack-15.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Run the `ship` Stack check on a layer whose lower branch moved → the fix that it names is `gh stack sync`. Run the Review check on a rebased layer → it compares `git patch-id --stable` of the reviewed diff and of the current diff, both without `.ai/`. Run Step 5 → it reads the PR back with `gh pr view` and watches the run of its `mergeCommit`.
- [ ] **B.** Write a map with `/write-to-file`, or with `/split-ticket` → the map has the template layout, and `map_units.py next` on it exits 0. Run `map_units.py next` on the fixture → it lists unit 15 first.
- [ ] **C.** Read the `ship` Stack and Review checks → they cover gh-stack sync and a rebase with no manual git rebase step.
- [ ] **D.** Run `/ship` on a rebased stack layer whose old review has the same patch-id → the Review check passes. Change one line on that layer → the Review check fails, and its fix is `/review`.

## Context

- Map: `.ai/map_pstack-program.md`, unit 15. Done line: `/ship` on a rebased stack layer accepts the old review when the patch-id matches.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. Each step replaces text. No step adds a script or a new check. The map check stays `map_units.py next`, which the map playbook already runs at step 1, before each batch.
- Found gap: the inline map block in `/split-ticket` has no `## Units` heading, so `map_units.py next` exits 1 on each map that it writes.
- Out of scope: `create-pr` Step 2, which shows the drift as a warning, keeps its `range-diff`.
- Production gate: none. The change is skill text, live at the next session start. A wrong rule shows at the next `/ship`.
- Push-only map: the build machine runs no `gh` command on this repo. The push step runs `git push -u origin pstack-15_ship-stack`.
- Evidence rule: the repo is public. Proof runs happen in `/tmp` repos.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `python3 skills/engineering/skills/work-on/scripts/map_units.spec.py`, `python3 skills/primitives/skills/write-to-file/scripts/check_plan.spec.py`, `python3 skills/primitives/skills/write-to-file/scripts/check_spec.spec.py`, `sh .githooks/pre-commit_test.sh`, and `sh .githooks/commit-msg_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A, C, D | the patch-id rule in the Review check | H | a wrong rule passes a review that no longer describes the head, and the PR merges with no gate |
| A | the Stack fix and the read-back | L | one command each |
| B | the map template and the `split-ticket` pointer | M | a map with no `## Units` stops `/work-on` at step 1 |
| B | the fixture | L | a test data refresh |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | D | after a rebase onto a moved base, and after a commit to `.ai/` only, the two patch-ids are equal | use case | Manual | step 1, a `/tmp` repo |
| C2 | D | after a change to one line of a reviewed file, the two patch-ids differ | equivalence partition | Manual | step 1, a `/tmp` repo |
| C3 | B | a map from the template, with the `split-ticket` unit fields, passes `map_units.py next` | use case | Unit | step 2, `map_units.spec.py` |
| C4 | B | `map_units.py next` on the refreshed fixture lists unit 15 first | use case | Unit | step 2, `map_units.spec.py` |

### Not testing

- `gh stack sync` and `gh pr view` are not run, because the build machine runs no `gh` command on this repo.

## Steps

- [x] **1. Patch-id review, stack sync, and read-back in `ship`.** Kind: docs. Conditions: C1, C2.
  - Replace the Review row rule: a report of an earlier head passes when `git diff <reviewed base> <reviewed head> -- . ':!.ai' | git patch-id --stable` equals the same for `$(git merge-base origin/<base> HEAD)` and `HEAD`. Delete the `range-diff` sentence and the `.ai/` sentence, which the pathspec now covers. Keep the review-fix-step rule.
  - Stack row fix: `gh stack sync`. Delete the manual pull and rebase.
  - Step 5: merge, then `gh pr view <number> --json state,mergeCommit` must show `MERGED`. Watch the run of that `mergeCommit`.
  - Prove C1 and C2 in a `/tmp` repo with the exact commands.
  - Done: ACs A, C, and D hold when you read `ship`, and the C1 and C2 runs are in Progress.
- [x] **2. The map template.** Seam: `map_units.py next`. Conditions: C3, C4.
  - Add `write-to-file/templates/map.md`: the header (`doctype`, `status`, `goal`, optional `branch_prefix`, `batch`, `push_only`), `## Decisions`, and `## Units` with one `### [ ] N. Title` unit and its `- Done:` line. Point the `map` row of `write-to-file` at it.
  - `split-ticket` Step 7: write the map in the template layout. Keep only its unit bullets inline. Delete the rest of its block.
  - Refresh the fixture from the current map header and unit headings. Add a test for C3 with the `split-ticket` unit fields, and change the fixture test for C4.
  - Done: the two tests pass, and `map_units.py next` on the real map exits 0.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. `map_units.spec.py`, `check_plan.spec.py`, `check_spec.spec.py`, `pre-commit_test.sh`, and `commit-msg_test.sh` pass.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-15.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
  - Result: report `.ai/review_pstack-15_ship-stack.html`. Reviewed base `c78ec66` (`pstack-inspired`), head `65cc83c`. Light run: 0 findings, 0 fixed, 0 open.
- [x] **5. Fix two names outside the panel.** Kind: docs.
  - `ship` Review row: `<base>` named the reviewed base SHA and the base branch. The diff now uses `<from> <to>`. The map template named the engineering script `map_units.py`, but a primitive depends on no other domain. It now says "the map check".
  - Done: the two lines read as above, and the gates pass.
- [x] **6. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The five gates pass on `2756e08`.
- [x] **7. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-15.md`. This step changes no code. Do not raise again a row of the step 4 report.
  - Done: the report path and the reviewed base and head SHAs are in this line.
  - Result: report `.ai/review_pstack-15_ship-stack.html`, run 2. Reviewed base `c78ec66` (`pstack-inspired`), head `bfb4067` (panel read `cbd5350`). Light run: 1 finding, 1 fixed, 0 open.
- [ ] **8. Push.** `git push -u origin pstack-15_ship-stack`. Push-only map: open no PR.
  - Done: the branch is on the remote.

## Suggested skills

- `/build @.ai/plan_pstack-15.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-15.md`: one step per session, from the worktree.
- `/tdd`: step 2.
- `/engineering:mob-review`: the review step.
- `/create-pr`: not used, because the map is push-only.

## Progress

- 2026-11-17: plan written for `pstack-15_ship-stack`.
- Decision log: decisions_pstack-15.tsv
- 2026-11-17: step 1 done. `ship` Review row ends 2 characters shorter. Stack fix is `gh stack sync`. Step 5 reads back `gh pr view --json state,mergeCommit`.
  - C1 and C2 proof in `/tmp/p15`: base commit; `feat` with 2 commits; record `RB=$(git merge-base main feat)` and `RH=$(git rev-parse HEAD)`; new commit `other.txt` on `main`; `git rebase main` on `feat`; commit `.ai/x.md` only. Command: `git diff <base> <head> -- . ':!.ai' | git patch-id --stable`.
  - C1: reviewed pair `95af7a89...` equals rebased pair `95af7a89...` (equal).
  - C2: after one line changed in `a.txt` and committed, the ID is `25eed666...` (differs).
- 2026-11-17: step 2 done, commit `6735290`. `write-to-file/templates/map.md` holds the header, `## Decisions`, and `## Units`. Optional header keys are comment lines, because a placeholder `batch` fails `map_units.py next`. The `map` row of `write-to-file` points at the template. `split-ticket` Step 7 has the unit bullets only. The fixture has the current unit headings, each with `Done: x.`.
  - C3: a template map with the `split-ticket` unit fields passes `map_units.py next`. C4: the fixture lists unit 15 first. `map_units.spec.py` runs 19 tests, all pass. `map_units.py next` on the real map exits 0.
  - Mutation check: the template with `## Units` renamed turns C3 red.
- 2026-11-17: step 4 done. Light run of `correctness` and `test-quality` found nothing. No fix commit. Report: `.ai/review_pstack-15_ship-stack.html`, base `c78ec66`, head `65cc83c`.
- 2026-11-17: step 7 done. Light run of `correctness` and `test-quality` found one nit: the fixture test checked only the first unit ID. Fixed in `bfb4067`, which asserts the full list. Report: `.ai/review_pstack-15_ship-stack.html`, base `c78ec66`, head `bfb4067`.
- 2026-11-17: `/blast-radius` verdict `clear`. Safety fact: the patch-id of the branch diff without `.ai/` stays the same after a rebase, a clean merge of the base, or a commit to `.ai/` only, and changes when a reviewed line changes. Rung 4: the script below exits 0 (`sh <file>`, with `PROOF OK`).
  - Cleared: an edit on the base near a reviewed hunk changes the context lines, so the IDs differ (C4). The check then fails and asks for `/review`. This fails safe, and the old `range-diff` rule failed in the same case. A reviewed SHA that is not in the local repo makes `git diff` exit non-zero, so no ID matches (C5). This fails safe.
  - Cleared: no other skill reads the `ship` Review rule. `create-pr` Step 2 keeps its own `range-diff`. `map_units.py` reads only the `batch:` header line, so the `#` comment lines of the template change nothing. `start-ticket` finds the map by file name, not by layout.
  - Confirmed risks: none.

```sh
set -e
pid() { git diff "$1" "$2" -- . ':!.ai' | git patch-id --stable | cut -c1-12; }
d=$(mktemp -d); cd "$d"; git init -q -b main; git config user.email t@t; git config user.name t
seq 1 30 > a.txt; echo x > b.txt; git add .; git commit -qm base
git switch -qc feat; perl -pi -e 's/^15$/fifteen/' a.txt; git commit -qam f1; echo y >> b.txt; git commit -qam f2
RB=$(git merge-base main feat); RH=$(git rev-parse HEAD); R=$(pid $RB $RH)
git switch -q main; echo o > other.txt; git add .; git commit -qm m1; git switch -q feat
git rebase -q main; mkdir .ai; echo n > .ai/x.md; git add .; git commit -qm ai
C1=$(pid $(git merge-base main HEAD) HEAD); echo "C1 rebase+.ai: $R vs $C1"; [ "$R" = "$C1" ]
git switch -q main; echo p > other2.txt; git add .; git commit -qm m2; git switch -q feat; git merge -q --no-edit main
C3=$(pid $(git merge-base main HEAD) HEAD); echo "C3 clean merge of base: $R vs $C3"; [ "$R" = "$C3" ]
perl -pi -e 's/^3$/three/' a.txt; git commit -qam change
C2=$(pid $(git merge-base main HEAD) HEAD); echo "C2 one changed line: $R vs $C2"; [ "$R" != "$C2" ]
git switch -q main; perl -pi -e 's/^17$/seventeen/' a.txt; git commit -qam near; git switch -q feat; git reset -q --hard HEAD~1; git rebase -q main
C4=$(pid $(git merge-base main HEAD) HEAD); echo "C4 base edit 2 lines from a reviewed hunk: $R vs $C4"; [ "$R" != "$C4" ]
git diff nosuchsha HEAD >/dev/null 2>&1 && exit 1 || echo "C5 reviewed SHA missing: git diff exits non-zero"
echo PROOF OK
```
