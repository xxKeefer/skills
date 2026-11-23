---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills.feat-bulletin
branch: feat/bulletin
status: approved
goal: Add /journal:bulletin, a daily page that grows over the ISO week, one dated entry at a time, so the reader and the next agent run see how the goals change.
spec: .ai/spec_bulletin.md
---

# Plan: Bulletin

## Goal

Add the `bulletin` skill to the journal domain. It writes `{YYYY}-wk{ww}-bulletin.html` and adds one entry for each day, newest on top. Scope: SCOPED, one PR, eight steps.

## Spec

`.ai/spec_bulletin.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Run `/bulletin` when this week has no bulletin → it writes `{YYYY}-wk{ww}-bulletin.html` in the journal folder, with the ISO week of today, holding one entry with a masthead.
- [x] **B.** Run it when the file exists and has no entry for today → the new entry goes above every older entry, and the older entries are byte-for-byte unchanged.
- [x] **C.** Run it when the file has an entry for today → it writes nothing, scans nothing, and gives the path.
- [x] **D.** A day passes with no run → the file has no entry for it, nothing fails, and the next entry says how many days it covers.
- [x] **E.** An entry is written → the scan covers Monday to today only, and the entry names no note older than that window except in a goal's context.
- [x] **F.** An entry is written → it gives each goal of the year, month, and week as served, not served, or carried, and says what changed since the latest earlier entry, or that it is the first of the week.
- [x] **G.** Earlier entries exist → each story is marked new, changed, or unchanged by its `data-id` against the latest earlier entry, and an unchanged story gets one line.
- [x] **H.** The page is checked → the check fails on a suggestion row, a choice control, a prompt box, a script, an entry with no masthead, two entries for one day, entries out of newest-first order, an entry outside the file's ISO week, or a placeholder left over.
- [x] **I.** The file name is built → `bulletin.py` gives the same week number as the broadsheet for every date, including the 2027-01-01 case in ISO year 2026 week 53.
- [x] **J.** An entry is written and a place is set → it holds today's forecast from `weather.py` (conditions, high and low, chance of rain), or a line that says the forecast is not available, or a line that says to set a place.
- [x] **K.** An entry is written → it lists the items that `occasions.py` gives as due today, and the items due on each later day of the week, by day, and says so when `occasions.md` has rows it cannot read.
- [x] **L.** The skill is installed → the journal README lists `/bulletin`, the journal `CLAUDE.md` data flow names it, and the journal plugin version moves up one minor.

## Context

Approval: the user approved this plan at the plan gate on 2026-11-24.

Intent: one file for each ISO week. Each run adds one entry with its own masthead, newest on top. The entry leads with how the goals moved since the entry below it, then gives the weather and the events. Earlier entries are input to the next run.

Decisions:

- Newest entry first: the user listed the days from Sunday down to Monday.
- One entry for each day. A same-day re-run writes nothing. The user said to append a new day each time, so no entry is edited.
- A script does the file work: the name, the state, and the insert. The agent writes only the entry's HTML.
- The skill calls `scan_vault.py` and `weather.py` of the broadsheet by `$SKILL_DIR/../broadsheet/scripts/`, with `--window` set to the days since Monday. It copies no scanner code.
- Weather: `weather.py` runs for the places of `~/.claude/broadsheet.md`. Each entry shows the forecast of its own day.
- Events: the skill runs `$SKILL_DIR/../../scripts/occasions.py` for today and for each later day of the week, and lists the due items by day. No bulletin script reads the `When` rules.
- No suggestion rows, no choice controls, no prompts, no script on the page.
- The entry's `data-id` is `<section>:<short kebab-case name>`, as in the broadsheet.

Out of scope: the broadsheet reading the bulletin, vault suggestions, and moving past weeks to `chronicles/`.

Production gate: none. The skill is user-invoked, and it writes one file.

Gates: `python3 skills/journal/skills/bulletin/scripts/bulletin.spec.py`, `python3 skills/journal/skills/bulletin/scripts/check_bulletin.spec.py`, and `sh .githooks/pre-commit_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | name and first write | M | a wrong week breaks every later run |
| B | insert above, older bytes kept | H | the file is the input of the next run, so a bad insert loses history |
| C | same-day re-run writes nothing | M | a second entry for one day breaks the order |
| D | gap days | M | a gap must not fail the run |
| E | scan window | L | one argument to an existing script |
| F | goal status and change | L | the agent writes it, and a reviewer reads it |
| G | new, changed, unchanged | L | the agent compares ids, and the state script lists them |
| H | the page check | M | the check is the only guard on the page shape |
| I | ISO week | M | the year edge gives the wrong file name |
| J | weather | L | `weather.py` has its own tests, and the skill only calls it |
| K | events | L | `occasions.py` has its own tests, and the skill only calls it |
| L | docs and version | L | docs |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A, I | 2026-11-22 is week 47, 2026-11-23 is week 48, 2027-01-01 is 2026 week 53, and the name ends in `-bulletin.html` | BVA | Unit | `bulletin.spec.py` |
| C2 | A | `state` on a folder with no file gives `exists: false` and no days | EP | Unit | `bulletin.spec.py` |
| C3 | A | `add` on a missing file creates it from the template with one entry | state transition | Integration | `bulletin.spec.py` |
| C4 | B | `add` puts the new entry above the older ones, and the older entries stay byte-for-byte | state transition | Integration | `bulletin.spec.py` |
| C5 | C | `state` gives `today_present: true` when an entry for today exists, and `add` for that day exits 1 and writes nothing | EP | Integration | `bulletin.spec.py` |
| C6 | D | `state` gives `days_since_last` for a gap of 0, 1, and 3 days, and none for the first entry | BVA | Unit | `bulletin.spec.py` |
| C7 | G | `state` gives the `data-id` list of the latest entry, and an empty list for the first entry | EP | Unit | `bulletin.spec.py` |
| C8 | H | the check passes a good page | EP | Unit | `check_bulletin.spec.py` |
| C9 | H | the check fails on each of: a `class="action"` row, a `<select>`, a `<textarea>`, a `<script>`, an entry with no masthead, two entries for one day, entries oldest first, an entry outside the file's week, a `{{placeholder}}` | decision table | Unit | `check_bulletin.spec.py` |

### Not testing

- AC E, F, G prose: L, the agent writes it from `SKILL.md`, and a reviewer reads it. The id list that G needs is C7.
- AC J and K: L, the skill calls `weather.py` and `occasions.py`, which have their own tests. A reviewer reads the skill text.
- AC L: L, docs, read in review.

## Steps

- [x] **1. Name and state.** Seam: `state` in `skills/journal/skills/bulletin/scripts/bulletin.py`. Conditions: C1, C2, C5, C6, C7.
  - Done: tests in `bulletin.spec.py`, written first and seen to fail, then green. `state <journal folder> --date <date>` prints `{path, exists, today_present, days, days_since_last, last_ids, week_start}`. They prove AC C, D, I, and the state half of A and G.
- [x] **2. Add an entry.** Seam: `add` in `bulletin.py`, and `skills/journal/skills/bulletin/template.html`. Conditions: C3, C4, C5.
  - Done: tests in `bulletin.spec.py`, written first and seen to fail, then green. `add <path> <entry file> --date <date>` creates the file from the template or inserts the entry above the older ones, and exits 1 for a day that has an entry. They prove AC A and B.
- [x] **3. Check the page.** Seam: `skills/journal/skills/bulletin/scripts/check_bulletin.py`. Conditions: C8, C9.
  - Done: tests in `check_bulletin.spec.py`, written first and seen to fail, then green. The check prints `ok` or one line for each fault, and exits 1 on a fault. They prove AC H.
- [x] **4. Skill text.** Kind: docs.
  - Done: `SKILL.md` has the steps: resolve with `state`, stop when today is present, scan with `--window` from `week_start`, run `weather.py` for each place, run `occasions.py` for today and each later day, read the earlier entries, write the entry, `add`, `check`, open, reply. `LAYOUT.md` gives the entry placeholders (goals, weather, events, chores, board, notes) and the `data-id` rules. The frontmatter has `disable-model-invocation: true`, as every journal skill has. This covers AC E, F, G, J, and K.
- [x] **5. Register.** Kind: docs.
  - Done: the journal README has the `/bulletin` row, the journal `CLAUDE.md` data flow has the line, `CONTEXT.md` defines Bulletin, and `skills/journal/.claude-plugin/plugin.json` moves from 2.11.0 to 2.12.0. This proves AC L.
- [ ] **6. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **7. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_bulletin.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **8. Push.** Push the branch and open a draft PR with `/create-pr @.ai/plan_bulletin.md`.
  - Done: the draft PR URL is in this line.

## Suggested skills

- `/build @.ai/plan_bulletin.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_bulletin.md`: one step per session, from the worktree.
- `/tdd`: steps 1 to 3.
- `/engineering:mob-review`: the review step.
- `/create-pr`: the push step.

## Progress

- 2026-11-24: plan written on `feat/bulletin`.
- 2026-11-24: step 1 done. `bulletin.py` has `state` and `add`, `check_bulletin.py` and `template.html` exist, and both specs are green (steps 2 and 3 code landed with it). Commit 4925f0e.
- 2026-11-24: step 2 done. C3, C4, C5 had tests in `bulletin.spec.py`; mutation checks (insert at end, no template fill, no same-day guard, no template) went red and were restored. AC A, B proven.
- 2026-11-24: step 3 done. C8, C9 had tests in `check_bulletin.spec.py`; mutation checks on each fault rule went red and were restored. AC H proven.
- 2026-11-24: step 4 done. `SKILL.md` and `LAYOUT.md` written; the pre-commit gate is green. AC E, F, G, J, K covered.
- 2026-11-24: step 5 done. README row, CLAUDE.md data flow, CONTEXT.md term, and plugin 2.12.0. The marketplace registry lists no versions.
