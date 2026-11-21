---
doctype: spec
ticket: none
status: confirmed
goal: Make the broadsheet a page the user can act on, and make the journal record what the user did.
---

# Spec: Broadsheet feedback

## Intent

- Outcome: once a week, the broadsheet shows true data, gives context for each suggestion, and lets the user tick a choice and a comment on each suggestion, which a skill then applies.
- User: the vault owner, who reads the broadsheet and maintains the vault alone.
- Why now: the first edition showed that the chore counts are wrong, that most sections cannot be acted on, and that the editorial and the floor plan find real problems.
- Success: the next edition has no section that the user calls low value, and each suggestion on it can be applied or vetoed from the page.
- Constraint: tests cover only the scripts. Skills get no tests.
- Out of scope: the vault layout changes themselves. They have their own plan outside this repo.

## Decisions

- Actions are ticks and comments on the page: the page builds a prompt, and `/journal:act-on-broadsheet` applies it. The user said the tick UX of `/write-report` is weak, so each row gets one compact choice control and a comment that opens on demand.
- Habit accuracy comes from a morning backfill in `/daily`: one question that lists yesterday's open items. The user expects it can get annoying, so it is one question, it accepts `all`, `none`, or numbers, and it does not show when nothing is open.
- The vault git backup is a step in `/daily`. This replaces the rule that agents never commit in the vault.
- Project state lives in the `status` line of `MISSION.md`: `active`, `dormant`, `waiting`, or `archived`, with an optional `until`. The file already has `status: active`.
- The weather box shows the real forecast for today, from Open-Meteo, which needs no API key. The location is a config line. The chore table moves to its own box, named Chores, with plain rates and no weather icons.
- The time-period argument goes. The lead covers the last 7 days. A compass section after the lead compares the last week, month, 3 months, and year.
- Carried over and link health go. Gaps stays, and is the next section to cut.
- Shantell Sans goes from the broadsheet and the gazette. Each lead headline uses the heading font.
- Notes in the knowledge folder are never archive suggestions for age. The user keeps dormant knowledge.
- Knowledge notes live in one `02-knowledge` folder, found by `*knowledge`. The vault agent made the merge, and this branch updates the skills.
- `occasions.md` gets one layout and a small `When` grammar, read by one script. The old file mixes four table layouts, free-text rules such as "Easter calc" and "Aug (varies)", empty cells, and two items in one cell. Each journal skill reads it its own way. One script makes the due items the same in each skill, and testable.
- The `When` grammar: a weekday or weekdays (`Sun`, `Mon Wed`), a week parity (`Wed even`, by ISO week), a yearly date (`Jan 5`), an nth weekday (`2nd Sun May`, or `1st Sun` for each month), a repeat (`every 3 months from Feb 15`), Easter offsets (`easter`, `easter+1`, `easter-2`), and a one-off ISO date (`2026-11-03`). The `Type` column goes, because no skill reads it. `Section` stays: `chores`, `work`, or `tasks`, with `chores` as the default.
- Back pages give the story and the outcome of each item, and suggestions for want lists. An item with no story is left out.
- One edition per ISO week, in the journal folder, as `{YYYY}-wk{ww}-broadsheet.html`, the same week numbers as the dailies. A second call in the same week points to the page that exists.
- Last week's page is the baseline. Each action row has a stable `data-id`, so a script can tell new rows from repeats. A page with no ids, such as the first edition, gives no repeats.

## Acceptance criteria

- [ ] **A.** The weather box shows today's forecast for the configured place → it gives the conditions, the high and low, and the chance of rain, or a line that says the forecast is not available.
- [ ] **B.** The Chores box shows each chore's tick rate from the journal → it uses no weather icons.
- [ ] **C.** The page has no Carried over section and no Link health section → the check fails a page that has one.
- [ ] **D.** The broadsheet and the gazette use no Shantell Sans → each lead headline uses the heading font.
- [ ] **E.** The page has a compass section after the lead → it compares dailies written, edits, chore rates, and the busiest folders across the last 7, 30, 90, and 365 days.
- [ ] **F.** The skill takes no time-period argument → the lead covers the last 7 days.
- [ ] **G.** Each row in the ledger, letters, stale shelf, morgue, floor plan, board, and editorial has a choice control and a comment → the page builds one prompt from the chosen rows, and gives a button that copies it.
- [ ] **H.** `/journal:act-on-broadsheet` reads the prompt → it applies each chosen row to the vault, asks before it deletes a note, and reports each change.
- [ ] **I.** Each letter, stale pick, and morgue item gives the reason for its suggestion and what the action does → no item is a bare folder name.
- [ ] **J.** A note in the knowledge folder (`*knowledge`) is never an archive suggestion for its age → the scanner leaves it off the stale list.
- [ ] **K.** The board reads each project's `status` → it leaves out `dormant` projects, gives a `waiting` project one line only when it changed in the last 7 days, and names the next card of each `active` project.
- [ ] **L.** Back pages give the story and outcome of each item → an item with no story is left out, and a want list gets suggestions.
- [ ] **M.** `/daily` asks once which of yesterday's open items the user did → it ticks those items in yesterday's file before it carries anything forward, and asks nothing when nothing is open.
- [ ] **N.** `/daily` backs up the vault → when the vault is a git repo with a remote, it commits every change and pushes, and a failure gives one line and does not stop the daily.
- [ ] **O.** `/new-project` documents the four `status` values and `until` → a new MISSION file says which values exist.
- [ ] **P.** The Sunday daily holds the weekly reflect prompts → the user can write the weekly reflect where they already write on Sunday.
- [ ] **Q.** The daily template puts free sections, such as a shopping list, above Reflect → a skill that reads Reflect reads only the reflect.
- [ ] **R.** The skill writes the page to the journal folder as `{YYYY}-wk{ww}-broadsheet.html`, with the ISO week of today → no page goes to the inbox.
- [ ] **S.** The user asks for a broadsheet when this week's page exists → the skill writes no page, scans nothing, and gives the path of this week's page.
- [ ] **T.** Last week's page exists → the skill marks each story and row as new or repeat, gives a repeat less space unless it changed, and the lead and compass name the trends across the two weeks.
- [ ] **U.** A skill needs the vault's knowledge folder → it finds it with `*knowledge`, and no skill names `*research`, `*reference`, or a numbered vault folder.
- [ ] **V.** `occasions.md` has one fixed layout → a daily list of nested chores, then one table layout, `| Item | When | Section |`, under each of `## Weekly`, `## Yearly`, `## Maintenance`, and `## One-off`.
- [ ] **W.** `occasions.py` reads `occasions.md` for a date → it prints the items due that day by section, the rows that it cannot read, and the one-off rows that are past.
- [ ] **X.** `/daily`, `/weekly`, `/monthly`, `/yearly`, and `/broadsheet` get due items from `occasions.py` → no journal skill reads the `When` rules itself.
- [ ] **Y.** `/update-occasions-config` writes only the new layout → given a file in the old layout, it migrates it after one yes, and lists each row it could not convert.
