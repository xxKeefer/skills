---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills/.claude/worktrees/scan-ignore-bulk-commits
branch: worktree-scan-ignore-bulk-commits
status: approved
goal: Make scan_vault.py skip any commit that touches more than 50 paths, so a bulk commit stops corrupting note ages and edit counts.
spec: .ai/spec_scan-ignore-bulk-commits.md
---

# Plan: Scan ignores bulk commits

## Goal

Make `scan_vault.py` skip any commit that touches more than 50 paths, and report the count as `bulk_commits_skipped`. Scope: SCOPED, one PR, two build steps.

## Spec

`.ai/spec_scan-ignore-bulk-commits.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Scan a vault whose history holds one commit of 51 or more paths → that commit adds nothing to note ages, `edits_by_folder`, `compass` edits, `hours` or `weekdays`.
- [x] **B.** Scan a vault with a commit of exactly 50 paths → the commit counts as before.
- [x] **C.** A note edited only by a skipped commit, and earlier by a normal commit → its age comes from the normal commit.
- [x] **D.** A note edited only by a skipped commit → its age comes from its mtime.
- [x] **E.** A commit of 51 pure renames → it is skipped.
- [x] **F.** Scan with `--bulk-files 10` and a commit of 11 paths → the commit is skipped.
- [x] **G.** Scan any vault in git → the output holds `bulk_commits_skipped` with the number of skipped commits, and 0 when none.
- [x] **H.** Scan a vault with no git history → the output holds `bulk_commits_skipped` as 0, and the scan runs as before.
- [ ] **I.** Read the broadsheet `SKILL.md` with `bulk_commits_skipped` above 0 → it tells the editor to say that bulk commits were ignored.

## Context

Approval: the user approved this plan at the plan gate on 2026-11-22.

Intent: `scan_vault.py` skips any commit that touches more than 50 paths, and reports how many it skipped as `bulk_commits_skipped`. The reader is the broadsheet reader. The last tidy made six of seven inbox notes read as one day old, and the 7, 30 and 90 day windows all showed 546 edits.

Decisions:

- Skip, do not flag. A flag alone leaves ages and counts wrong.
- Count every path in the commit, renames included. A tidy that moves 300 files is bulk.
- Filter in `git_history`. It feeds note age, edit counts, hours and weekdays.
- The limit is `--bulk-files`, default 50. A commit over the limit is skipped. A commit at the limit stays.
- A skipped commit still feeds the rename alias in `git_history`, so older history follows a bulk move.

Out of scope: a flag-only mode, any change to the page layout, and any other script.

Production gate: none. This is a local script. The default drops only commits above 50 paths.

Gates: `python3 skills/journal/skills/broadsheet/scripts/scan_vault.spec.py` and `sh .githooks/pre-commit_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | skip a commit over the limit | M | wrong ages and edit counts reach the page. `scan_vault.py` has 3 fix commits, so likelihood is up one step |
| B | keep a commit at the limit | M | an off-by-one drops real edits |
| C | age falls back to an earlier commit | M | a skipped bulk move must pass old history on |
| D | age falls back to mtime | M | same path, no earlier commit |
| E | pure renames count | M | renames are not in the `files` list today |
| F | `--bulk-files` | L | one option, same code path as A |
| G | `bulk_commits_skipped` | L | one number in the JSON |
| H | no git | L | the number is 0 |
| I | `SKILL.md` line | L | docs, read in review |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | a 51-path commit adds nothing to ages, `edits_by_folder`, `compass`, `hours`, `weekdays` | BVA | Integration | `scan_vault.spec.py` |
| C2 | B | a 50-path commit counts as before | BVA | Integration | `scan_vault.spec.py` |
| C3 | C | a note in a skipped commit keeps the age of its earlier commit | EP | Integration | `scan_vault.spec.py` |
| C4 | C | a note that a skipped commit moved keeps the age of its earlier commit under the old name | state transition | Integration | `scan_vault.spec.py` |
| C5 | D | a note touched only by a skipped commit takes its mtime | EP | Integration | `scan_vault.spec.py` |
| C6 | E | 51 pure renames are skipped | BVA | Integration | `scan_vault.spec.py` |
| C7 | F | `--bulk-files 10` skips an 11-path commit | EP | Integration | `scan_vault.spec.py` |
| C8 | G, H | `bulk_commits_skipped` is the count, 0 with none, and 0 with no git | EP | Integration | `scan_vault.spec.py` |

### Not testing

- The wording of `SKILL.md` (AC I): L, a reviewer reads it.

## Steps

- [x] **1. Skip bulk commits.** Seam: `git_history` and `scan` in `skills/journal/skills/broadsheet/scripts/scan_vault.py`. Conditions: C1, C2, C3, C4, C5, C6, C7, C8.
  - Done: eight tests, written first and seen to fail, then green in `scan_vault.spec.py`. They prove AC A to H, and the whole spec file passes.
- [ ] **2. Docs.** Kind: docs.
  - Done: `SCAN.md` names `bulk_commits_skipped`, the `SKILL.md` Step 2 text names `--bulk-files`, and `SKILL.md` Step 6 tells the editor to say that bulk commits were ignored when the count is above 0. This proves AC I.
- [ ] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_scan-ignore-bulk-commits.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **5. Push.** Push the branch and open a draft PR with `/create-pr @.ai/plan_scan-ignore-bulk-commits.md`.
  - Done: the draft PR URL is in this line.

## Suggested skills

- `/build @.ai/plan_scan-ignore-bulk-commits.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_scan-ignore-bulk-commits.md`: one step per session, from the worktree.
- `/tdd`: step 1.
- `/engineering:mob-review`: the review step.
- `/create-pr`: the push step.

## Progress

- 2026-11-22: plan written on `worktree-scan-ignore-bulk-commits`.
- 2026-11-22: step 1 done. Eight tests in `scan_vault.spec.py`, seen red, then green. 54 tests pass.
