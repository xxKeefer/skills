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
- [x] **E.** An entry is written → the scan covers Monday of last week to today, and the entry names no note older than that window except in a goal's context.
- [x] **F.** An entry is written → it gives each goal of the week as served, not served, or carried, and says what changed since the latest earlier entry, or that it is the first of the week. It names no yearly or monthly goal table.
- [x] **G.** Earlier entries exist → each story is marked new, changed, or unchanged by its `data-id` against the latest earlier entry, and an unchanged story gets one line.
- [x] **H.** The page is checked → the check fails on a suggestion row, a choice control, a prompt box, a script, an entry with no masthead, two entries for one day, entries out of newest-first order, an entry outside the file's ISO week, or a placeholder left over.
- [x] **I.** The file name is built → `bulletin.py` gives the same week number as the broadsheet for every date, including the 2027-01-01 case in ISO year 2026 week 53.
- [x] **J.** An entry is written and a place is set → it holds today's forecast from `weather.py` (conditions, high and low, chance of rain), or a line that says the forecast is not available, or a line that says to set a place.
- [x] **K.** An entry is written → it lists the items that `occasions.py` gives as due today, and the items due on each later day of the week, by day, and says so when `occasions.md` has rows it cannot read.
- [x] **L.** The skill is installed → the journal README lists `/bulletin`, the journal `CLAUDE.md` data flow names it, and the journal plugin version moves up one minor.
- [x] **M.** An entry is written → it has a main column with This week, Last week, Next week, and Reflect, and a side column with the weather, the events, and the chores.
- [x] **N.** An entry is written → Reflect holds four cards: Learning, Ideas, Friction, and What's next, each with items of this week and of last week, or a line that says it has none.
- [x] **O.** An entry is written → it holds at least one chart as inline SVG, each with `role="img"` and an `aria-label`, and the page check fails on an `<svg>` with neither.
- [x] **P.** The state is read → it gives `last_week_start` and `window_days`, so that the scan covers Monday of last week to today for every weekday.
- [x] **Q.** The page is checked → the check fails on an entry with no Reflect card for one of the four names, and passes an entry with all four.

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

Revision 2026-11-24: the user asked for a tighter focus on this week, last week, and next week, the weather and events in a side column, more charts through `/show-me`, and a masonry of reflect cards. Steps 12 to 19 do it. The year and month goal tables leave the entry. Charts are inline SVG, because the page has no script.

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
| M, N | layout and reflect cards | L | the agent writes it from `SKILL.md`, and a reviewer reads it. The page check holds the card names |
| O | chart labels | M | an unlabelled chart is invisible to a screen reader, and the check is the only guard |
| P | window arithmetic | H | the first build got the window wrong by one day, and every weekday has its own value |
| Q | reflect cards in the check | M | the check is the only guard on the page shape |

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

| C10 | P | `state` gives `window_days` and `last_week_start` for each weekday Monday to Sunday, and for the 2027-01-01 case | BVA | Unit | `bulletin.spec.py` |
| C11 | O | the check fails on an `<svg>` with no `role="img"`, and on one with no `aria-label`, and passes a labelled one | decision table | Unit | `check_bulletin.spec.py` |
| C12 | Q | the check fails on an entry that lacks one of the four reflect cards, and passes an entry with all four | decision table | Unit | `check_bulletin.spec.py` |

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
- [x] **6. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [x] **7. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_bulletin.md`. This step changes no code.
  - Done: report `.ai/review_feat-bulletin.html`, base 0472310, reviewed head 4461b04 (panel read 33ce948). The panel fixed 9 of 9 findings, and no row stays open.
- [x] **8. Test.** Run the project's test suite, and add a test for each changed behaviour that no test covers. This step changes no behaviour.
  - Done: the suite passes, and each behaviour that the branch changes has a test.
- [x] **9. Review.** Review the branch with this plan: `.ai/plan_bulletin.md`. This step changes no code. Name `/engineering:mob-review`. Run the lanes that raised a finding in run 1 (a11y, code-quality, comments, skills, test-design, test-quality), and correctness, because `bulletin.py` and `check_bulletin.py` changed after the reviewed head. No row stays open from run 1, so tell the panel to raise no repeat of the run 1 rows.
  - Done: report `.ai/review_feat-bulletin.html` run 2, base 0472310, reviewed head 036dfe7 (panel read 03139c9). The panel fixed 4 of 5 findings. One future row stays open.
- [x] **10. Test.** Run the project's test suite, and add a test for each changed behaviour that no test covers. This step changes no behaviour.
  - Done: the suite passes, and each behaviour that the branch changes has a test.
- [x] **11. Review.** Review the branch with this plan: `.ai/plan_bulletin.md`. This step changes no code. Name `/engineering:mob-review`. Run correctness and test-design, which raised a finding in run 2, and code-quality and test-quality, whose files changed after the run 2 read of 03139c9. Do not raise the open run 2 row again (the future row on `check_bulletin.py:74`), and do not raise any row that only repeats it. This is the third review step, so the loop stops after it.
  - Done: report `.ai/review_feat-bulletin.html` run 3, base 0472310, reviewed head b632088 (panel read 67b884a). The panel fixed 3 of 3 findings. The loop stopped at the third review step.
- [x] **12. State gives the window.** Seam: `state` in `skills/journal/skills/bulletin/scripts/bulletin.py`. Conditions: C10.
  - Done: tests in `bulletin.spec.py`, written first and seen to fail, then green. `state` also prints `last_week_start` and `window_days`, where `window_days` is the days from Monday of last week to today. They prove AC P.
- [x] **13. Check the new page shape.** Seam: `skills/journal/skills/bulletin/scripts/check_bulletin.py`. Conditions: C11, C12. The existing check tests must keep passing, so edit the `entry()` helper of the spec to hold the four cards.
  - Done: tests in `check_bulletin.spec.py`, written first and seen to fail, then green (23 tests). The check fails on an `<svg>` with no `role="img"` or no `aria-label`, and on an entry with no card for one of Learning, Ideas, Friction, and What's next. A card is `<article class="card" data-card="learning|ideas|friction|next">`. They prove AC O and Q.
- [x] **14. Template.** Kind: docs.
  - Done: `template.html` has a two-column `.layout` with a `.side` column that drops under the main column below 700px, a `.masonry` of `.card` items made with CSS columns, and the chart classes for SVG (`.chart`, `.fill-accent`, `.fill-muted`, `.axis`, `.label`). It has no inline style and no script. A sample entry in `/tmp` is added with `bulletin.py add`, and `check_bulletin.py` prints `ok` on it. The sample is rendered with the `agent-browser` tool at 1200px and at 480px wide, and each screenshot is read: the side column sits right and then below, the cards pack in columns, and the charts show. Delete the sample after.
- [x] **15. Skill text.** Kind: docs.
  - Done: `SKILL.md` scans with `--window <window_days>`, reads last week and this week from the scan, runs `occasions.py` for each day of next week as well as today and the rest of this week, and draws charts with the rule of `/show-me`: inline SVG only. `LAYOUT.md` gives the new entry frame (main and side columns, the four main parts, the four reflect cards with their `data-card` values), the chart rule (`role="img"`, `aria-label`, a `<figcaption>`, classes only), the `data-id` sections (`week`, `last`, `next`, `reflect`, `weather`, `events`, `chores`, `board`, `notes`), and the rule that the entry holds no yearly or monthly goal table. It covers AC E, F, M, N, and O.
- [ ] **16. Register.** Kind: docs.
  - Done: the `/bulletin` row of the journal README, the journal `CLAUDE.md` data-flow line, and the Bulletin term of `CONTEXT.md` match the new entry. The plugin version stays 2.12.0, because no push has shipped it. This proves AC L still holds.
- [ ] **17. Test.** Run the project's test suite, and add a test for each changed behaviour that no test covers. This step changes no behaviour.
  - Done: the suite passes, and each behaviour that the branch changes has a test.
- [ ] **18. Review.** Review the branch with this plan: `.ai/plan_bulletin.md`. This step changes no code. Name `/engineering:mob-review`. The run 2 future row on `check_bulletin.py:74` stays open: do not raise it again.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **19. Push.** Push the branch and open a draft PR with `/create-pr @.ai/plan_bulletin.md`.
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
- 2026-11-24: step 6 done. Both specs and `pre-commit_test.sh` are green: 15 tests, 12 tests, 19 ok lines.
- 2026-11-24: step 7 done. The panel read 33ce948 and found 9 issues (4 change requested, 5 nits). Fix commit 4461b04 fixed all 9. The fix changed `bulletin.py`, `check_bulletin.py`, and the `--window` rule of `SKILL.md`, so the run adds steps 8 and 9 as a second test and review round. Report: `.ai/review_feat-bulletin.html`.
- 2026-11-24: step 8 done. Both bulletin specs (16 and 13 tests), both hook tests, and the journal and broadsheet specs are green.
- 2026-11-24: step 9 done. Run 2 found 5 issues (1 change requested, 3 nits, 1 future). Fix commit 036dfe7 fixed 4: `add` keeps entries newest-first on a backfill, refuses an entry dated for another day, and exits 1 on a missing folder, and the check has a test for a placeholder in an attribute. The future row on `check_bulletin.py:74` stays open, because the persona marked it future and the impact is low. `add` changed, so the run adds steps 10 and 11 as the third and last round.
- 2026-11-24: step 10 done. Both bulletin specs (20 and 15 tests) and both hook tests are green.
- 2026-11-24: step 11 done. Run 3 found 3 nits. Fix commit b632088 fixed all 3: `insert` is now a pure function, the page keeps CRLF bytes, and an entry file with no final newline has a test. The third review step stops the loop, even though the fix changed `add`.
- 2026-11-24: decision. The run 2 future row on `check_bulletin.py:74` stays open. Reason: the persona marked it future, the impact is low, and the file is local. To fix it, tick the row in `.ai/review_feat-bulletin.html` run 2, and run `/build` on the prompt.
- 2026-11-24: the user asked for a redesign of the entry. The spec and the plan have new ACs M to Q and steps 12 to 19. The first build ends at step 11.
- 2026-11-24: step 12 done. `state` prints `last_week_start` and `window_days`; C10 tests cover Monday to Sunday and 2027-01-01 (11 days from 2026-12-21). Mutation (+6 for +7) went red and was restored. AC P proven.
- 2026-11-24: step 14 done. `template.html` holds the layout CSS (sheet max-width 1080px, grid 2fr/1fr, 700px stack, CSS-column masonry, chart classes); no script, no inline style. A sample was added with `add`, `check_bulletin.py` printed ok, and screenshots at 1200px and 480px were read: at 1200px the side column sits right of the main column with a rule, the cards pack in two columns (learning and ideas left, friction and next right), and the bars show in accent and muted; at 480px everything stacks, side parts follow the main parts, the cards are one column, and the charts show. Sample deleted. Commit 308ce59. Class names: `.layout`, `.main`, `.side`, `.masonry`, `.card`, `.chart`, `.fill-accent`, `.fill-muted`, `.axis`, `.label`, `.forecast`, `.masthead`, `.dateline`, `.standfirst`, `.tag`, `.tag.unchanged`; plain `figure`, `figcaption`, `h3` (part heading), `h4` (card title), `table`. Chart rules: `svg.chart` with `viewBox`, `role="img"`, `aria-label`; children `line.axis` (the baseline), `text.label` (category name left of the axis), `rect.fill-accent` (the focus bar), `rect.fill-muted` (other bars); no `style` attribute. Skeleton:
  - `article.entry[data-date]`
    - `header.masthead` > `div.dateline`, `h2`
    - `p.standfirst`
    - `div.layout`
      - `div.main`
        - `section` (This week) > `h3`, `table` (goal rows with `data-id`), `figure` > `svg.chart[role=img][aria-label]`, `figcaption`
        - `section` (Last week) > `h3`, `p`, `figure` > `svg.chart`, `figcaption`
        - `section` (Next week) > `h3`, `ul` > `li`
        - `section` (Reflect) > `h3`, `div.masonry` > 4 x `article.card[data-card=learning|ideas|friction|next]` > `h4`, `p` or `ul`
      - `aside.side`
        - `h3` (Weather), `p.forecast` > `strong`, `p`
        - `h3` (Events), `p` for each day
        - `h3` (Chores), `table`, `figure` > `svg.chart`, `figcaption`
  - The sections are plain `<section>` with no class. The `<h3>` is the part heading of each.
- 2026-11-24: step 15 done. `SKILL.md` (9.5 KB) scans with `--window <window_days>`, runs `occasions.py` through next Sunday, and sends charts to `/show-me` in inline SVG form. `LAYOUT.md` has the main and side frame, the four cards, the chart rule, and the story sections. Choice: the nine section names are the `data-id` prefixes of stories, and the plain `<section>` containers carry no `data-id`. Gates green. Commit d336e84.
