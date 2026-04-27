---
name: chronicle
description: >
  Generate monthly or yearly progress arc from sprint data. Coach drafts a narrative covering
  north star progress, velocity trends, accomplishments, and friction themes. Use when user says
  "chronicle", "monthly review", "yearly review", "how's the month going", "progress report",
  or at the end of a month/year.
---

# Chronicle

Progress arc — the long view. Coach generates a narrative draft from sprint data. The user
reviews and adjusts. Be honest about the arc — celebrate real progress, call out drift.

## Step 1: Parse Input

`<user-input>` may contain:
- A **month** (e.g., "chronicle march", "chronicle 2026-03") — monthly chronicle
- A **year** (e.g., "chronicle 2026") — yearly chronicle
- **Nothing** — default to the current month

Determine the period and file name:
- Monthly: `YYYY-MM-chronicle.md`
- Yearly: `YYYY-chronicle.md`

Locate the sanctum directory per the journal domain's discovery convention.

Check if the file already exists. If so:
> Chronicle for {period} already exists. Update it, or start fresh?

## Step 2: Gather Data

### For monthly chronicles
Read all files from the month:
- Sprint plans (`YYYY-wkNN-sprint.md` for weeks in this month)
- Ponder files (`YYYY-wkNN-ponder.md` for weeks in this month)
- North stars (`north-stars.md` in the sanctum directory)
- Quest files (`quest-*.md` in the sanctum directory) for active quests
- `kaizen.md` -- filter Standards by Adopted date in the period; filter Improvement Log by date;
  filter Active Calibrations by Trial Sprint week falling in the period

### For yearly chronicles
Read all monthly chronicles from the year. If monthly chronicles don't exist, read ponder files
directly. Also read `kaizen.md` and aggregate Standards / Improvement Log / Calibrations across
the full year.

## Step 3: Compile North Star Progress

For each active north star during the period:
- What milestone progress was made (from quest files and ponder data)
- Were any north stars achieved? (celebrate!)
- Were any shelved? (note why)
- Any new north stars set?

Build the progress table:

| Domain | Goal | Progress | Trend |
|---|---|---|---|
| #domain/AREA | goal | progress summary | 📈 📉 ➡️ |

## Step 4: Compile Velocity Trends

Aggregate velocity data from ponders:

### Monthly
| Week | Tasks | Habits | Knowledge |
|---|---|---|---|
| wkNN | N/N (%) | per-habit summary | [[artifacts]] |

### Yearly
| Month | Avg Tasks | Avg Habits | Knowledge Count |
|---|---|---|---|
| Month | N% | N% | N artifacts |

Note trends: improving, stable, declining. Be direct about what the numbers show.

## Step 5: Compile Accomplishments

Pull from ponder "What worked" sections and completed tasks. List the highlights — things
worth remembering. Connect to north stars and quests where relevant.

## Step 6: Compile Friction Themes

Aggregate friction from ponders. Look for:
- **Recurring friction** that persisted across the period
- **Resolved friction** that experiments addressed
- **New friction** that emerged

This is where the coaching shines — connect dots the user might not see:
> "You flagged time pressure on philosophy 3 out of 4 weeks. The Tue/Thu experiment helped
> week 3 but you dropped it week 4. Is the schedule the issue, or the commitment level?"

## Step 6.5: Compile Kaizen Metrics

From `kaizen.md`, count for the period:
- **Standards adopted:** N (list each with adoption date and source ponder)
- **Improvements logged:** N (one-line summary of the most notable, or full list if monthly)
- **Calibrations applied:** N shrinks + N re-grows (list each with original target and trial
  sprint)

If any count is zero, say so explicitly -- the section must not be omitted. An empty improvement
log over a month is itself a signal worth surfacing.

## Step 7: Write Coach Notes

This is the narrative heart of the chronicle. Draft a 3–5 sentence narrative covering:
- The overall arc of the period (what defined it)
- Key growth or regression
- Emerging direction — where is the user trending?
- Suggestion for next period's focus

Also draft a separate **Kaizen Arc** paragraph (2-3 sentences) describing the trajectory of small
wins: which standards stuck, what calibrations revealed about the user's real capacity, whether
the improvement log shows compounding momentum or a flatline.

For yearly chronicles, this should be more reflective:
- What domains defined the year
- Biggest growth areas
- What surprised you (the user)
- Direction for the coming year

## Step 8: Present for Review

Show the full draft:

> **Chronicle — {period}**
> {full content}
>
> Does this capture the month/year accurately? Anything to add or correct?

Iterate until the user is satisfied.

## Step 9: Write Chronicle File

Create the file in the sanctum directory:

### Monthly (`YYYY-MM-chronicle.md`)
```markdown
---
type: sanctum/chronicle
tags:
  - sanctum
  - sanctum/chronicle
date: YYYY-MM-01
up: "[[YYYY-chronicle]]"
prev: "[[YYYY-PP-chronicle]]"
next: "[[YYYY-NN-chronicle]]"
---

# Chronicle — Month YYYY

## North Star Progress
{table from Step 3}

## Velocity Trend
{table from Step 4}

## Accomplishments
{list from Step 5}

## Friction Themes
{from Step 6}

## Kaizen
- **Standards adopted ({N}):** {list with adopted date + source ponder, or "none this month"}
- **Improvements logged ({N}):** {full list or "none this month"}
- **Calibrations ({N}):** {list with original + trial sprint, or "none this month"}

## Coach Notes
{narrative from Step 7}

### Kaizen Arc
{2-3 sentence paragraph from Step 7 -- trajectory of compounding improvements}
```

### Yearly (`YYYY-chronicle.md`)
```markdown
---
type: sanctum/chronicle
tags:
  - sanctum
  - sanctum/chronicle
date: YYYY-01-01
prev: "[[PPPP-chronicle]]"
next: "[[NNNN-chronicle]]"
---

# Chronicle — YYYY

## North Star Progress
{table}

## Velocity Trend (Monthly)
{table}

## Accomplishments
{highlights}

## Domains Explored
{all domains active during the year with timeline}

## Friction Themes
{year-level patterns}

## Kaizen
- **Standards adopted ({N}):** {list, or "none this year"}
- **Improvements logged ({N}):** {monthly counts summary, or "none this year"}
- **Calibrations ({N}):** {list of shrinks and re-grows, or "none this year"}

## Coach Notes
{reflective narrative}

### Kaizen Arc
{2-3 sentence paragraph -- the year's compounding trajectory}
```

## Step 10: Close

> **Chronicle written.**
> {One-line summary of the period's arc}
>
> Use this as context for your next `/weekly` or `/smart-goal` session.
