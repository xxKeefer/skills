---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills.feat-broadsheet-feedback
branch: feat/broadsheet-feedback
status: approved
goal: Make the broadsheet a page the user can act on, and make the journal record what the user did.
spec: .ai/spec_broadsheet-feedback.md
---

# Plan: Broadsheet feedback

## Goal

Two phases on one branch. Phase 1 changes the broadsheet. Phase 2 changes the journal and projects skills from the insights of the first edition. Scope: SCOPED, one PR. Estimate: large.

## Spec

`.ai/spec_broadsheet-feedback.md`, all of it.

## Acceptance criteria

- [x] **A.** The weather box shows today's forecast for the configured place → it gives the conditions, the high and low, and the chance of rain, or a line that says the forecast is not available.
- [x] **B.** The Chores box shows each chore's tick rate from the journal → it uses no weather icons.
- [x] **C.** The page has no Carried over section and no Link health section → the check fails a page that has one.
- [x] **D.** The broadsheet and the gazette use no Shantell Sans → each lead headline uses the heading font.
- [ ] **E.** The page has a compass section after the lead → it compares dailies written, edits, chore rates, and the busiest folders across the last 7, 30, 90, and 365 days.
- [x] **F.** The skill takes no time-period argument → the lead covers the last 7 days.
- [ ] **G.** Each row in the ledger, letters, stale shelf, morgue, floor plan, board, and editorial has a choice control and a comment → the page builds one prompt from the chosen rows, and gives a button that copies it.
- [x] **H.** `/journal:act-on-broadsheet` reads the prompt → it applies each chosen row to the vault, asks before it deletes a note, writes each veto and snooze to `broadsheet-memory.md` so `/broadsheet` leaves that row out (a snooze until its end date), and reports each change.
- [x] **I.** Each letter, stale pick, and morgue item gives the reason for its suggestion and what the action does → no item is a bare folder name.
- [x] **J.** A note in the knowledge folder (`*knowledge`) is never an archive suggestion for its age → the scanner leaves it off the stale list.
- [x] **K.** The board reads each project's `status` → it leaves out `dormant` projects, gives a `waiting` project one line only when it changed in the last 7 days, and names the next card of each `active` project.
- [x] **L.** Back pages give the story and outcome of each item → an item with no story is left out, and a want list gets suggestions.
- [x] **M.** `/daily` asks once which of yesterday's open items the user did → it ticks those items in yesterday's file before it carries anything forward, and asks nothing when nothing is open.
- [x] **N.** `/daily` backs up the vault → when the vault is a git repo with a remote, it commits every change and pushes, and a failure gives one line and does not stop the daily.
- [x] **O.** `/new-project` documents the four `status` values and `until` → a new MISSION file says which values exist.
- [x] **P.** The Sunday daily holds the weekly reflect prompts → the user can write the weekly reflect where they already write on Sunday.
- [x] **Q.** The daily template puts free sections, such as a shopping list, above Reflect → a skill that reads Reflect reads only the reflect.
- [x] **R.** The skill writes the page to the journal folder as `{YYYY}-wk{ww}-broadsheet.html`, with the ISO week of today → no page goes to the inbox.
- [x] **S.** The user asks for a broadsheet when this week's page exists → the skill writes no page, scans nothing, and gives the path of this week's page.
- [x] **T.** Last week's page exists → the skill marks each story and row as new or repeat, gives a repeat less space unless it changed, and the lead and compass name the trends across the two weeks.
- [x] **U.** A skill needs the vault's knowledge folder → it finds it with `*knowledge`, and no skill names `*research`, `*reference`, or a numbered vault folder.
- [x] **V.** `occasions.md` has one fixed layout → a daily list of nested chores, then one table layout, `| Item | When | Section |`, under each of `## Weekly`, `## Yearly`, `## Maintenance`, and `## One-off`.
- [x] **W.** `occasions.py` reads `occasions.md` for a date → it prints the items due that day by section, the rows that it cannot read, and the one-off rows that are past.
- [x] **X.** `/daily`, `/weekly`, `/monthly`, `/yearly`, and `/broadsheet` get due items from `occasions.py` → no journal skill reads the `When` rules itself.
- [x] **Y.** `/update-occasions-config` writes only the new layout → given a file in the old layout, it migrates it after one yes, and lists each row it could not convert.
- [ ] **Z.** The compass quotes each reflection that the user filled in within its window (daily, weekly, monthly reflect sections), with a link to its note → a filled reflection gets more space than the counts, and an empty one is not named.

## Context

- Decisions: see the spec's Decisions section.
- Tests cover only the scripts: `scan_vault.py`, `check_broadsheet.py`, and the new `weather.py`, `edition.py`, and `occasions.py`. The user said not to test the skills. Each skill-only AC is checked by one real run in step 22.
- Production gate: none. Each skill runs only when the user calls it. The page and the vault are the user's own.
- The vault layout changes are not in this branch. They have their own plan outside this repo.
- Commits: conventional, scope `journal` or `projects`. No attribution line.
- Gates: `python3 -m pytest` or each `*.spec.py` as the repo runs it, and `sh .githooks/pre-commit_test.sh`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | forecast from Open-Meteo | M | network call; a failure must not stop the page |
| B | chore rates | L | same data, new layout |
| C | removed sections | L | check list change |
| D | font | L | two templates only |
| E | compass windows | M | new date math across four windows |
| F | no time argument | L | skill text |
| G | choice controls and prompt | M | a script in the page; the check must accept it |
| H | act-on skill | H | edits and moves vault notes |
| I | reasons on rows | L | skill text |
| J | knowledge folder off stale list | M | wrong match hides or shows notes |
| K | project status | M | a parse error shows a quiet project |
| L | back pages | L | skill text |
| M | backfill | M | edits yesterday's file |
| N | git backup | M | pushes the vault |
| O | status docs | L | docs |
| P | Sunday reflect | L | skill text |
| Q | template order | L | template |
| R | page path | M | a wrong week number at a year end splits or loses an edition |
| S | one page per week | M | a miss writes over or duplicates the week's page |
| T | new or repeat | M | a wrong match hides fresh news |
| U | knowledge glob | L | docs; a missed copy fails to find the folder |
| V | occasions layout | L | template |
| W | occasions parser | H | a wrong rule puts the wrong chores on every daily |
| X | skills use the parser | M | skill text; a skill that still reads rules itself drifts |
| Z | filled reflections | M | a missed reflection hides the highest-value signal |
| H | veto and snooze memory | M | a lost veto brings back a suggestion the user already refused |
| Y | migration | M | edits the user's file; a lost row loses a birthday |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | a good response gives conditions, high, low, rain chance | EP | Unit | `weather.spec.py` |
| C2 | A | a network error or bad JSON gives `available: false` and exit 0 | error guessing | Unit | `weather.spec.py` |
| C3 | C | a page with `carried-over` or `link-health` fails the check | EP | Unit | `check_broadsheet.spec.py` |
| C4 | E | the scan gives a compass row for 7, 30, 90, and 365 days | EP | Unit | `scan_vault.spec.py` |
| C5 | E | a daily on day 7 and day 8 falls in the right windows | BVA | Unit | `scan_vault.spec.py` |
| C6 | G | an action row with no `data-id` fails the check | EP | Unit | `check_broadsheet.spec.py` |
| C7 | G | the page script is allowed, and an inline style still fails | EP | Unit | `check_broadsheet.spec.py` |
| C8 | J | a note in `02-knowledge` past the limit is not stale; one in `03-work` is | EP | Unit | `scan_vault.spec.py` |
| C9 | K | the scan gives each project's `status` and `until`, and `active` for a MISSION with none | EP | Unit | `scan_vault.spec.py` |
| C11 | R | the path for Sun 2026-11-22 is wk47 and Mon 2026-11-23 is wk48; 2027-01-01 is `2026-wk53` | BVA | Unit | `edition.spec.py` |
| C12 | S | `exists` is true when this week's page is in the journal folder, false when not | EP | Unit | `edition.spec.py` |
| C13 | T | last week's `data-id` values are listed; a page with no ids, or no page, gives an empty list | EP | Unit | `edition.spec.py` |
| C14 | W | weekdays, `Wed even` and `Wed odd` on ISO weeks 47 and 48, `Jan 5`, `2nd Sun May`, `1st Sun` | EP | Unit | `occasions.spec.py` |
| C15 | W | `easter`, `easter+1`, `easter-2` in 2026 and 2027 | EP | Unit | `occasions.spec.py` |
| C16 | W | `every 3 months from Feb 15` is due on Feb 15, May 15, and Nov 15, and not on Mar 15 | BVA | Unit | `occasions.spec.py` |
| C17 | W | a one-off is due on its date, is listed as past the day after, and an empty `Section` gives `chores` | BVA | Unit | `occasions.spec.py` |
| C18 | W | a row with an unknown `When`, such as `Aug (varies)`, goes to `errors`, and the other rows still print | error guessing | Unit | `occasions.spec.py` |
| C19 | B | the scan counts chores from the items that `occasions.py` gives, not from a text match | EP | Unit | `scan_vault.spec.py` |
| C20 | Z | a reflect section with only its sub-headings gives nothing; one with text under a sub-heading gives that text | EP | Unit | `scan_vault.spec.py` |
| C21 | Z | a `## Shopping` heading under Reflect ends the reflection, so the list is not quoted; reflections outside a window are not in it | EP | Unit | `scan_vault.spec.py` |
| C22 | H | `edition.py` lists vetoed ids, and a snoozed id until its end date but not on the day after | BVA | Unit | `edition.spec.py` |
| C23 | H | no memory file, or a line it cannot read, gives no muted ids and no failure | error guessing | Unit | `edition.spec.py` |
| C24 | Z | a Sunday daily's `Weekly Reflect` section is a weekly reflection, not a daily one | EP | Unit | `scan_vault.spec.py` |
| C25 | T | last week's page in `chronicles/<ISO year>/` is found when it is not in the journal root, and the root copy wins when both exist | EP | Unit | `edition.spec.py` |
| C10 | H, M, N, P, S, T, Y, Z | one real run of each skill against a copy of the vault | exploratory | Manual | step 22 |

### Not testing

- B, D, F, I, L, O, Q, U, V, X: skill text or template only. The user asked for no skill tests.
- The prompt-building script in the browser: checked by hand in step 22.

## Steps

### Phase 1: Broadsheet

- [x] **1. Groom `.ai/`.** Kind: mechanical. Delete the files of each pstack unit whose PR is merged, as `.ai/CLAUDE.md` says.
  - Done: `.ai/` holds only open units and this spec and plan.
- [x] **2. Weather script.** Seam: `scripts/weather.py <lat> <lon>`, with the fetch passed in for tests. Conditions: C1, C2.
  - Done: `weather.spec.py` passes. Proves A.
- [x] **3. Edition script.** Seam: `scripts/edition.py <journal folder> [--date YYYY-MM-DD]`, which prints this week's path, `exists`, last week's path, and last week's row ids. Conditions: C11, C12, C13.
  - Done: `edition.spec.py` passes. Proves R, S, T (data).
- [x] **4. Scanner: compass, knowledge folders, project status.** Seam: `scan()` in `scan_vault.py`. Conditions: C4, C5, C8, C9.
  - Done: the scan JSON has `compass`, `projects`, and a stale list without knowledge folders. Proves E, J, K (data).
- [x] **5. Check: new section list and action rows.** Seam: `check_broadsheet.py`. Conditions: C3, C6, C7.
  - Done: the check wants `compass` and `chores`, rejects `carried-over` and `link-health`, and checks each action row. Proves C.
- [x] **6. Scanner: filled reflections.** Seam: `scan()` in `scan_vault.py`. Conditions: C20, C21.
  - Done: the scan JSON has `reflections`: each reflect section with real text, with its note, level (daily, weekly, monthly), date, and text. Proves Z (data).
- [x] **7. Template.** Kind: config. Drop Shantell Sans from the broadsheet and gazette templates. Add the compass, chores, and weather boxes. Remove carried over and link health. Add the choice control, the comment, and the copy-prompt bar, with one small script.
  - Done: the template passes the check after a fill with sample data, and no template in the repo names Shantell Sans. Proves D, G (page).
- [x] **8. Broadsheet SKILL.md and config.** Kind: docs. Remove the time argument. Add the location line. The default paper name is "The Obsidian Oracle" (user request, 2026-11-21). Step 1 runs `edition.py` and stops with the path when this week's page exists. Write the page to the journal folder. Read last week's page, and mark new and repeat rows. Rewrite steps for weather, chores, the compass (lead with the filled reflections from `reflections`), reasons on each row, the board by status, and back pages with stories.
  - Done: the skill and `config.example.md` match the template and the scan. Proves B, F, I, K, L, R, S, T.
- [x] **9. `/journal:act-on-broadsheet`.** Kind: docs. A new skill: parse the prompt, apply each row (move, archive, set project status, tick a goal, edit a template), ask before a delete, report each change.
  - Done: the skill exists in the journal domain and the domain README lists it. Proves H.

### Phase 2: Journal and projects

- [x] **10. `/daily` backfill.** Kind: docs. One question before carry-forward, with `all`, `none`, numbers, or skip. No question when nothing is open.
  - Done: the daily skill has the step. Proves M.
- [x] **11. `/daily` git backup.** Kind: docs. Commit and push the vault when it is a git repo with a remote. One line on failure.
  - Done: the daily skill has the step. Proves N.
- [x] **12. Daily template and Sunday reflect.** Kind: docs. Add a free section above Reflect. On Sunday, the daily holds the weekly reflect prompts.
  - Done: the template and the daily skill match. Proves P, Q.
- [x] **13. Project status.** Kind: docs. `/new-project` documents `active`, `dormant`, `waiting`, `archived`, and `until`.
  - Done: the skill and its MISSION template list the values. Proves O.
- [x] **14. Veto and snooze memory.** Seam: `edition.py`, which also prints `muted`: the ids to leave out on the date. Conditions: C22, C23. `/journal:act-on-broadsheet` appends `<data-id> | veto` or `<data-id> | snooze until <YYYY-MM-DD>` to `broadsheet-memory.md` in the journal folder. `/broadsheet` leaves out each row whose id is in `muted`. A snooze with no date in the comment lasts 4 weeks.
  - Done: `edition.spec.py` passes, and both skills name the file. Proves H (memory).
- [x] **15. Sunday weekly reflect: scan and Templater copy.** Seam: `scan()` in `scan_vault.py`. Conditions: C24. Give the `Weekly Reflect` section of a Sunday daily the level `weekly`. Add the Notes section and the Sunday Weekly Reflect section to `scripts/obsidian/templates/template-journal_daily.md`, so it matches `skills/journal/templates/daily.md`.
  - Done: `scan_vault.spec.py` passes, and the two daily templates have the same sections. Proves Z (data).

### Phase 3: Knowledge folder and occasions

- [x] **16. Knowledge folder.** Kind: docs. Change `/add-procedure`, the scribe `CLAUDE.md`, and the `/discover-vault-directory` example from `*reference` and `*research` to `*knowledge`. The vault renumbers every top folder except `98-archive` and `99-meta`: `04-work` to `03-work`, `05-projects` to `04-projects`, `06-lessons` to `05-lessons`, `07-omen` to `06-omen`. Skills find folders by glob, so they need no change for this. Change the hard paths in `docs/agents/issue-tracker.md` (`05-projects`) and the example in `CONTEXT.md` (`05-projects/`). Leave the ADRs, which record past decisions.
  - Done: a search of the repo outside `docs/adr/` and `.ai/` for `*research`, `*reference`, `02-research`, `03-reference`, `04-work`, `05-projects`, `06-lessons`, and `07-omen` finds nothing. Proves U.
- [x] **17. Journal chronicles.** Seam: `edition.py`. Conditions: C25. The vault keeps live journal files in the journal root, and the user moves past weeks by hand into `chronicles/{YYYY}/`. `edition.py` also looks for last week's page there. In `/broadsheet`, the floor plan treats `chronicles/{YYYY}/` as the expected place for past journal files, not as news.
  - Done: `edition.spec.py` passes, and the floor plan rule names `chronicles/`. Proves T (data).
- [x] **18. Occasions parser.** Seam: `skills/journal/scripts/occasions.py <occasions.md> [--date YYYY-MM-DD]`, which prints JSON. Conditions: C14, C15, C16, C17, C18.
  - Done: `occasions.spec.py` passes. Proves W.
- [x] **19. Scanner uses the parser.** Seam: the chore count in `scan_vault.py`. Conditions: C19.
  - Done: `scan_vault.spec.py` passes with a fixture in the new layout. Proves B (data).
- [x] **20. Occasions template and skills.** Kind: docs. Rewrite `templates/occasions.md` in the new layout. Change `CHECKLIST_RULES.md`, `/daily`, `/weekly`, `/monthly`, and `/yearly` to run `occasions.py` for due items.
  - Done: no journal skill describes a `When` rule. Proves V, X.
- [x] **21. Occasions config skill.** Kind: docs. `/update-occasions-config` writes only the new layout. It finds an old-layout file, shows the migrated file, writes it after one yes, and lists each row it could not convert.
  - Done: the skill has the migrate step. Proves Y.

### Phase 4: Check and ship

- [ ] **22. Live run.** Seam: the skills, run by hand. Conditions: C10. Delete this week's page if it exists. Run `/broadsheet` on the real vault, then run it again to see it point to the same page. Tick rows, and run `/journal:act-on-broadsheet` on a copy of the vault. Run `/update-occasions-config` on the copy to migrate `occasions.md`. Run `/daily` on the copy for backfill, Sunday, and backup to a scratch remote.
  - Done: the page check prints `ok`, and each skill run did what its AC says. Proves H, M, N, P, S, T, Y, Z.
- [ ] **23. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **24. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_broadsheet-feedback.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **25. Push.** Push the branch and open a draft PR with `/create-pr @.ai/plan_broadsheet-feedback.md`.
  - Done: the draft PR URL is in this line.

## Suggested skills

- `/build @.ai/plan_broadsheet-feedback.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_broadsheet-feedback.md`: one step per session, from the worktree.
- `/tdd`: each step with a `Seam:` line that names a script.
- `/engineering:mob-review`: the review step.
- `/create-pr`: the push step.

## Progress

- 2026-11-21: plan written on `feat/broadsheet-feedback`.
- 2026-11-21: step 1 done. Deleted the files of pstack units 20 to 33 (all PRs merged) and the `reports.js` index.

- 2026-11-21: step 2 done. `weather.py <lat> <lon>` prints `{available, date, conditions, high, low, rain_chance, unit}`, or `{available: false}` on any failure, and exits 0. It asks Open-Meteo for 1 day with `timezone=auto`, so `date` is the local day of the place. An unknown WMO code gives `Unknown`. 7 tests. One live run for Sydney gave a good forecast.
- 2026-11-21: step 3 done. `edition.py <journal folder> [--date YYYY-MM-DD]` prints `{path, exists, last_path, last_ids}`. `last_path` is null and `last_ids` is empty when last week's page is not there. `last_ids` keeps page order and drops repeats. Last week is the ISO week of the date minus 7 days, so 2027-wk01 reads 2026-wk53. 10 tests.
- 2026-11-21: step 4 done. The scan JSON has `compass` (one row each for 7, 30, 90, 365 days: `dailies`, `edits`, `chore_rate`, `busiest`), `projects` (`project`, `path`, `status` with `active` as default, `until`, `changed_days`), and a stale list with no notes from a `*knowledge` top folder. Fixtures moved to `02-knowledge` and `03-work`. `--window` stays until step 8. 28 tests.
- 2026-11-21: step 5 done. The check wants `compass` and `chores`, and fails a page with `carried-over` or `link-health`. Action row shape for steps 7 and 9: `<li class="action" data-id="<unique id>">` (any tag with class `action`) that holds `<select class="choice">` and one `<input class="comment">` or `<textarea class="comment">`, such as `<details><summary>Comment</summary><textarea class="comment"></textarea></details>`. A row with no or a repeated `data-id`, no choice, or no comment fails. The page can have 1 `<script>` block; 2 or more fail. An inline `style` still fails. The spec now tests a page that it builds; the current template fails the check until step 7. 17 tests.
- Decision log: decisions_broadsheet-feedback.tsv
- 2026-11-21: user asked to surface filled reflections in the compass. Added AC Z and step 6. Later steps moved up by one.
- 2026-11-21: step 6 done. The scan JSON has a top-level `reflections` list, newest first: `{path, level, date, sections: [{heading, text}]}`, for each journal note of the last 365 days with a filled reflect section. Each compass row has a `reflections` count, so step 8 groups the list by `date` for each window. A section holds the lines under a `##` heading with the word `Reflect`, to the next `#` or `##` heading. Blank lines and empty list markers are dropped. `heading` is null for text above the first `###`. The level and the date come from frontmatter `type` and `date`, else from the file name (`YYYY-wkNN-day`, `YYYY-wkNN-week` gives the Monday, `YYYY-MM-mon` gives the 1st). 33 tests.
- 2026-11-21: step 7 done. Both templates drop Shantell Sans; each lead `h2` uses `--heading`. The broadsheet template: lead and compass (`{{compass_body}}`) in the main column, then weather, chores (`{{chores_body}}`), and gaps in the aside. Carried over and link health are gone. The skill writes each action row with an empty `<select class="choice" aria-label="...">`, and the page script adds the options `-`, do, veto, snooze, done. The comment goes in `<details><summary>Comment</summary><textarea class="comment" aria-label="..."></textarea></details>`. A sticky prompt bar at the foot gives the row count, a Copy prompt button, and a Show prompt textarea, which opens when the copy fails. Prompt format for step 9: line 1 `/journal:act-on-broadsheet`, line 2 `Edition: <page title>`, line 3 a header, then one line per row with a choice or a comment: `- <data-id> | <choice, or comment> | <section id> | <row text> | comment: <text>` (the comment part only when there is one). A chosen row gets an accent left rule. `check_broadsheet.spec.py` fills the template with sample data and checks it. The script ran in no browser: no browser is on this machine, so step 22 checks it by hand. 18 tests.
- 2026-11-21: step 8 done. `SKILL.md` runs `edition.py` first and stops with the path when this week's page exists, then scans with no `--window` (the scanner keeps the flag at its default of 7 for its tests), runs `weather.py` when the config has a `location: <lat> <lon>` line, reads last week's page for new and repeat rows, and writes to the journal folder. Default name: The Obsidian Oracle. Row shape for step 9: each suggestion row holds `<strong>Why:</strong>` and `<strong>Do:</strong>`. Its `data-id` is `<section id>:<target>`: the note path with `.md` (letters, stale-shelf, the-morgue), the folder path (floor-plan), the project folder name (the-board), `<want list path>:<item slug>` (back-pages), `<journal file name>:<goal slug>` (the-ledger), or `<change slug>` (editorial). An id holds no space and no `|`, and the row text never holds ` | comment: `. Want-list suggestions in the back pages are action rows too. README and domain CLAUDE.md updated. 68 tests.
- 2026-11-21: step 9 done. `skills/journal/skills/act-on-broadsheet/SKILL.md` parses each row line by its first three ` | ` fields and the first ` | comment: ` after them, reads the full `Do:` text from the page by `data-id`, asks one `all`/`none`/numbers question before any delete, applies the rest with no stop, fixes path links after a move, and reports one line per row. `do` applies the action, `comment` applies the comment, `done` ticks an open goal or card, `veto` and `snooze` change nothing. It commits nothing in the vault. Listed in the journal README and the domain CLAUDE.md data flow; journal plugin 2.9.0 to 2.10.0. 68 tests.
- 2026-11-21: step 10 done. `/daily` Step 4 has a Backfill Yesterday part before Carry Forward. It lists each open child item of yesterday's `## 📋 Today`, numbered, and asks one question. `all` or numbers tick those items in yesterday's file, and a group line when all its children are ticked. `none`, `skip`, or no answer tick nothing. No question when yesterday has no file or no open item. Carry-forward then takes the items still open. Journal plugin stays at 2.10.0, the bump of this branch.
- 2026-11-21: step 11 done. `/daily` Step 7, Back Up the Vault, runs after Done. It goes on only when `git rev-parse --show-toplevel` from the journal folder gives a folder with `.obsidian/` and `git remote` prints a name. It runs `add -A`, commits `vault: daily <YYYY-MM-DD>` with the daily's date (no commit when nothing changed), and pushes with no force. A failure gives `Backup failed: {first line}` and nothing more. The journal `CLAUDE.md` data flow says so.
- 2026-11-21: step 12 done. The daily template has `## 📝 Notes` above `## 🤔 Reflect`, and a `## 🗓️ Weekly Reflect (Sundays only)` section after it with the three `###` headings of the weekly template's reflect. `/daily` adds that section only on a Sunday and keeps free sections above Reflect. `/weekly` and `/reflect week` copy the Sunday text into the weekly file's empty `## 🤔 Reflect`, so `/monthly` still reads weekly files. `/reflect` on a Sunday daily fills both sections. The scanner reads `## 🗓️ Weekly Reflect` as its own reflect section, with level daily. The Templater daily in `scripts/obsidian/templates/` is not changed; it has no Notes or Sunday section. 68 tests.
- 2026-11-21: step 13 done. `MISSION-FORMAT.md` has a table of `active`, `dormant`, `waiting`, and `archived`, with what each means on `/broadsheet`, and an optional `until: YYYY-MM-DD` for a `waiting` or `dormant` project. `archived` replaces the old `done` value. The template has a `%% status: active | dormant | waiting | archived. Optional: until: YYYY-MM-DD %%` line under the frontmatter, so a new MISSION file lists the values; a comment inside the frontmatter would break the scanner's parser. `/new-project` Step 4 lists the values. Projects plugin 0.12.0 to 0.13.0.
- 2026-11-22: D1 closed. The user chose A: a `broadsheet-memory.md` file in the journal folder. Folded it into AC H and added step 14. Step 15 fixes two gaps from step 12: the scan read the Sunday weekly reflect as a daily, and the Templater daily copy missed the new sections. Later steps moved up by two.
- 2026-11-22: step 14 done. `edition.py` prints `muted` too: each id in `<journal folder>/broadsheet-memory.md` with a `<id> | veto` line, or a `<id> | snooze until <YYYY-MM-DD>` line whose date is today or later. File order, no repeats. No file gives `[]`. A line that is not exactly two `|` fields, has another rule, or has a bad date is skipped. `/journal:act-on-broadsheet` Step 5 appends one such line per veto or snooze row (no date in the comment: 4 weeks from today), and its report says `muted`. `/broadsheet` Step 7 leaves out each row whose id is in `muted`. The journal `CLAUDE.md` data flow names the file. 16 edition tests. Pre-existing reds not from this branch: `triage_dir.spec.py` (no `file` command) and `skill-tally.spec.py` (expects `primitives:grill-it`).
- 2026-11-22: step 15 done. The scan gives the `## 🗓️ Weekly Reflect` section of a daily as its own `reflections` item with level `weekly`, the daily's path, and the date of the Monday of its ISO week, as `YYYY-wkNN-week` files and the weekly frontmatter `date` are. The `## 🤔 Reflect` of the same daily stays a `daily` item. An empty weekly section gives no item. The Templater daily has `## 📝 Notes` above `## 🤔 Reflect`, and adds `## 🗓️ Weekly Reflect` with the three weekly `###` headings only when `m.isoWeekday() === 7`. The `/broadsheet` scan table says so. 35 scan tests.
- 2026-11-22: step 16 done. `/add-procedure`, the scribe `CLAUDE.md`, `/triage-notes`, and the `/discover-vault-directory` example use `*knowledge` in place of `*reference` and `*research`. `05-projects` is `04-projects` in `CONTEXT.md`, `docs/agents/issue-tracker.md`, the projects README, and the utility issue-tracker template. The `scan_vault.spec.py` and `check_broadsheet.spec.py` fixtures use `06-omen`, `05-lessons`, and `02-knowledge`. Scribe 1.28.0, primitives 2.27.0, utility 1.29.0. The only search hits left are the bold word `**reference**` in `writing-great-skills`, which names no folder. 35 scan and 18 check tests.
- 2026-11-22: the vault plan put past journal files in `chronicles/{YYYY}/`. Added step 17 so `edition.py` finds last week's page there and the floor plan does not flag the folder. Later steps moved up by one.
- 2026-11-22: step 17 done. `edition.py` looks for last week's page in the journal root first, then in `chronicles/{YYYY}/` with the ISO year of last week, so 2027-wk01 reads `chronicles/2026/2026-wk53-broadsheet.html`. The root copy wins when both exist. The `/broadsheet` floor plan treats `chronicles/{YYYY}/` as the place for past journal files, not as news. The journal `CLAUDE.md` flat rule names the same exception. `/daily` is not changed. 18 edition tests.
- 2026-11-22: step 18 done. `skills/journal/scripts/occasions.py <occasions.md> [--date YYYY-MM-DD]` prints `{date, daily, due: {chores, work, tasks}, errors: [{line, row, why}], past: [{line, item, when, section}]}`. `daily` is each non-blank line under `## Daily`, as written. Every other `##` heading holds `| Item | When | Section |` rows; a table header row (the row above a `---` row) is skipped, and cells split on `|` but not on `\|`, so a wikilink alias stays whole. A day past the month end, such as `Feb 29` in 2027 or `every 1 months from Jan 31` in April, falls on the month's last day. `every N months` takes N from 1 to 12 and gives the same months each year. ISO weeks 53 and 1 are both odd. Exit 2 only when the file is missing or unreadable. The real vault file, in the old layout, gives 80 errors and no due items until step 21 migrates it. 32 occasions tests.
- 2026-11-22: step 19 done. `scan_vault.py` loads `skills/journal/scripts/occasions.py` by a path from `__file__`. For each daily, the chores are the leaf tasks of the `daily` list and the `due.chores` items for that day's date (bold removed, spaces collapsed), matched to the ticked and open leaf tasks of the daily. `work` and `tasks` items are not chores. `journal.checklists` and the compass `chore_rate` use this count. `journal.occasions_errors` gives the parser `errors` for today. A file in the old layout gives an error for each row and no chores, and the scan does not fail: the real vault gives 80 errors. No file gives no errors. The `/broadsheet` key table names `journal.occasions_errors`, and the Chores box gives the error count with a pointer to `/update-occasions-config`. The fixture is in the new layout. 38 scan tests.
- 2026-11-22: step 20 done. `templates/occasions.md` has `## Daily` (a nested list), then `| Item | When | Section |` tables under `## Weekly`, `## Yearly`, `## Maintenance`, and `## One-off`, with generic examples and one `%%` comment above the first heading that lists the `When` forms. `/daily`, `/weekly`, `/monthly`, and `/yearly` say what `$SKILL_DIR` is and run `python3 $SKILL_DIR/../../scripts/occasions.py <journal directory>/occasions.md --date <date>`; the range skills run it once per date. `CHECKLIST_RULES.md` maps `daily` and `due.*` to the groups. `/daily` names an old-layout file (no `## Daily`, or every table row in `errors`) and `/update-occasions-config`, gives one line per error row, lists `past` one-offs to prune, deletes nothing, and goes on. The range skills take events only from the `## Yearly`, `## Maintenance`, and `## One-off` tables (yearly: `## Yearly` and `## One-off`). The journal `CLAUDE.md` state file line says only the script reads `When`. Only `/update-occasions-config` still describes `When` rules, for step 21. 113 tests.
- 2026-11-22: step 21 done. `/update-occasions-config` Step 2 runs `occasions.py` and finds an old-layout file (no `## Daily`, or every table row in `errors`). Step 3 converts each row by a table (Day-Specific to `## Weekly`, `Wednesday (even weeks)` to `Wed even`, `Easter calc` by the holiday name to `easter-2`/`easter-1`/`easter`/`easter+1`, Recurring to `## Yearly`, `Quarterly`/`Biannual`/`Annual` with the anchor to `every 3/6/12 months from ...`, `Monthly (1st Sun)` to `1st Sun`, `Weekly (Sun)` to `Sun`, one-offs to ISO dates with the heading year, `<br>` cells to one row each, `Type` and `Anchor Date` dropped). An old one-off with an empty Section gets `tasks`, its old default. A row it cannot convert stays in its table with its When as written, so `errors` lists it and no row is lost. It shows the whole file and the rows it could not convert, writes after one `yes` with a `.bak` copy (dated when a `.bak` exists), then shows `errors` of the new file. Steps 4 and 5 build `vault_occasions.js` from the rows not in `errors`, with one moment test per `When` form that gives the same days as the parser; the public-holiday weekend carry-over is gone. The JS Easter helper matches `occasions.easter` for 1900 to 2199. README row updated. Journal plugin stays at 2.10.0. 113 tests.
