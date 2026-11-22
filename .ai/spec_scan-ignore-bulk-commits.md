---
doctype: spec
ticket: none
status: confirmed
goal: Make scan_vault.py skip any commit that touches more than 50 paths, so a bulk commit stops corrupting note ages and edit counts.
---

# Spec: Scan ignores bulk commits

## Intent

- Outcome: `scan_vault.py` skips any commit that touches more than 50 paths, and reports how many it skipped as `bulk_commits_skipped`.
- User: the broadsheet reader, whose inbox ages and edit counts are wrong after a tidy.
- Why now: the last tidy made six of seven inbox notes read as one day old, and the 7, 30 and 90 day windows all showed 546 edits.
- Success: a vault with one 1000-file commit gives the same note ages, edit counts, hours and weekdays as the vault without it.
- Constraint: the count includes every path, pure renames too. The limit is `--bulk-files`, default 50, and a commit with more than the limit is skipped. A skipped commit's files take their age from an earlier commit, or from mtime.
- Out of scope: flag-only mode, any change to the broadsheet page layout, and any other script.

## Decisions

- Skip, do not flag: a flag alone leaves ages and counts wrong, which is the bug.
- Report the skipped count as `bulk_commits_skipped` in the JSON: the broadsheet can then say that it ignored bulk commits.
- Count every path in the commit, renames included: a tidy that moves 300 files is bulk even when git reads them as pure renames.
- Filter in `git_history`: it feeds note age, edit counts, hours and weekdays, so one filter fixes all four.
- The limit is the `--bulk-files` option, default 50: the user judged 50 reasonable, and a tuned vault can change it.
- Over the limit skips, at the limit stays: "more than a set number" is the user's wording.

## Acceptance criteria

- [ ] **A.** Scan a vault whose history holds one commit of 51 or more paths → that commit adds nothing to note ages, `edits_by_folder`, `compass` edits, `hours` or `weekdays`.
- [ ] **B.** Scan a vault with a commit of exactly 50 paths → the commit counts as before.
- [ ] **C.** A note edited only by a skipped commit, and earlier by a normal commit → its age comes from the normal commit.
- [ ] **D.** A note edited only by a skipped commit → its age comes from its mtime.
- [ ] **E.** A commit of 51 pure renames → it is skipped.
- [ ] **F.** Scan with `--bulk-files 10` and a commit of 11 paths → the commit is skipped.
- [ ] **G.** Scan any vault in git → the output holds `bulk_commits_skipped` with the number of skipped commits, and 0 when none.
- [ ] **H.** Scan a vault with no git history → the output holds `bulk_commits_skipped` as 0, and the scan runs as before.
- [ ] **I.** Read the broadsheet `SKILL.md` with `bulk_commits_skipped` above 0 → it tells the editor to say that bulk commits were ignored.

## Out of scope

- A mode that flags a bulk commit and keeps it: the bug stays.
- Page layout changes: the page needs only the one line from AC I.
