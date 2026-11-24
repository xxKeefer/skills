---
doctype: spec
ticket: none
status: confirmed
goal: Add /journal:bulletin, a daily page that grows over the ISO week, one dated entry at a time, so the reader and the next agent run see how the goals change.
---

# Spec: Bulletin

## Intent

- Outcome: one HTML file for each ISO week, `{YYYY}-wk{ww}-bulletin.html`, in the journal folder. Each run adds one entry with its own masthead, newest on top, so the file reads Sunday to Monday from top to bottom.
- User: the vault owner, who wants to see what changes over the week, above all how the week's goals progress, with last week for contrast and a look at next week. The yearly and monthly goals live in their own files and stay out of the page.
- Why now: the broadsheet comes once a week and looks back. It cannot show a goal moving from day to day.
- Success: by Sunday the file holds one entry for each day that the user ran it, and each entry says what changed since the entry below it.
- Constraint: tests cover only the scripts. Skills get no tests. The skill reuses the broadsheet scan and weather scripts and the journal `occasions.py`, and copies none.
- Out of scope: vault suggestions, choice controls, and prompts. The broadsheet owns them.

## Decisions

- A new skill `bulletin` in the journal domain, user-invoked like every journal skill (ADR 0007).
- Each run reads the current bulletin file and the vault, and writes one new entry. The earlier entries are input: the agent compares against the latest one, so the entry says what is new, what changed, and what stayed.
- The entry order is newest first, because the user listed the days from Sunday down to Monday. The new entry goes above the older ones, and the older entries are never edited. A script does the insert, so it is testable.
- One entry for each day. A second run on the same day writes nothing and gives the path, as the broadsheet does for a week.
- A missed day is not an error: there is no entry for it, and the next entry says how many days it covers.
- The scan window runs from Monday of last week to today, through `scan_vault.py --window`. `bulletin.py state` gives `last_week_start` and `window_days`, so the agent does no date sums. The first entry of a week has no earlier entry, and says so.
- The entry has a main column and a side column. The side column holds today's weather, the events from `occasions.md`, and the chore ticks. It sits on the right, and drops under the main column on a narrow screen.
- The main column has four parts in this order: This week (the week's goals as served, not served, or carried, and the change since the last entry), Last week (how last week's goals ended, and a chart that sets last week against this week), Next week (what carries over, the events due next week by day, and ideas for the week, marked as a projection), and Reflect.
- Reflect is a masonry of four cards: Learning, Ideas, Friction, and What's next. Each card holds the items of this week and of last week, each marked with its week and linked to its note. A card with no item says so.
- Charts are inline SVG, drawn in the form that `/show-me` gives for a visual: the smallest one that makes the point. Each chart has a `role="img"` and an `aria-label`, and the page has no script. A chart appears only when the scan holds its numbers.
- Weather comes from `weather.py` of the broadsheet, for the places in `~/.claude/broadsheet.md`, as the broadsheet does it. Each entry shows the forecast of its own day.
- Events come from `occasions.py` of the journal domain, run for today and for each later day of the week, so the entry shows what is due now and what comes. No bulletin script reads the `When` rules.
- No suggestion rows, no choice controls, no prompt builders. The page has no script.
- The page uses the broadsheet look: the same fonts and accent, so the two papers match. The masthead of an entry names the paper, the day, and the entry's number in the week.
- Each story has a `data-id` of the form `<section>:<short kebab-case name>`, so the next run can tell new, changed, and unchanged stories. An unchanged story gets one line.
- Reuse: `scan_vault.py` and `weather.py` of the broadsheet are called by path from `$SKILL_DIR/../broadsheet/scripts/`.
- The paper name and the accent come from `~/.claude/broadsheet.md`, with the bulletin name "The {paper name} Bulletin" by default.

## Acceptance criteria

- [ ] **A.** Run `/bulletin` when this week has no bulletin → it writes `{YYYY}-wk{ww}-bulletin.html` in the journal folder, with the ISO week of today, holding one entry with a masthead.
- [ ] **B.** Run it when the file exists and has no entry for today → the new entry goes above every older entry, and the older entries are byte-for-byte unchanged.
- [ ] **C.** Run it when the file has an entry for today → it writes nothing, scans nothing, and gives the path.
- [ ] **D.** A day passes with no run → the file has no entry for it, nothing fails, and the next entry says how many days it covers.
- [x] **E.** An entry is written → the scan covers Monday of last week to today, and the entry names no note older than that window except in a goal's context.
- [x] **F.** An entry is written → it gives each goal of the week as served, not served, or carried, and says what changed since the latest earlier entry, or that it is the first of the week. It names no yearly or monthly goal table.
- [ ] **G.** Earlier entries exist → each story is marked new, changed, or unchanged by its `data-id` against the latest earlier entry, and an unchanged story gets one line.
- [ ] **H.** The page is checked → the check fails on a suggestion row, a choice control, a prompt box, a script, an entry with no masthead, two entries for one day, entries out of newest-first order, an entry outside the file's ISO week, or a placeholder left over.
- [ ] **I.** The file name is built → `bulletin.py` gives the same week number as the broadsheet for every date, including the 2027-01-01 case in ISO year 2026 week 53.
- [ ] **J.** An entry is written and a place is set → it holds today's forecast from `weather.py` (conditions, high and low, chance of rain), or a line that says the forecast is not available, or a line that says to set a place.
- [ ] **K.** An entry is written → it lists the items that `occasions.py` gives as due today, and the items due on each later day of the week, by day, and says so when `occasions.md` has rows it cannot read.
- [ ] **L.** The skill is installed → the journal README lists `/bulletin`, the journal `CLAUDE.md` data flow names it, and the journal plugin version moves up one minor.
- [x] **M.** An entry is written → it has a main column with This week, Last week, Next week, and Reflect, and a side column with the weather, the events, and the chores.
- [x] **N.** An entry is written → Reflect holds four cards: Learning, Ideas, Friction, and What's next, each with items of this week and of last week, or a line that says it has none.
- [x] **O.** An entry is written → it holds at least one chart as inline SVG, each with `role="img"` and an `aria-label`, and the page check fails on an `<svg>` with neither.
- [ ] **P.** The state is read → it gives `last_week_start` and `window_days`, so that the scan covers Monday of last week to today for every weekday.
- [ ] **Q.** The page is checked → the check fails on an entry with no Reflect card for one of the four names, and passes an entry with all four.

## Out of scope

- Reading the bulletin from the broadsheet. It adds coupling, and the user chose to leave it.
- Any vault suggestion. The broadsheet owns them.
- Moving a finished bulletin to `chronicles/{YYYY}/`. The user moves past weeks by hand.
