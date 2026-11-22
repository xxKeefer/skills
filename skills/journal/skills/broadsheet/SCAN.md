# Scan keys

Step 2 of the broadsheet skill reads these keys from the JSON of `scan_vault.py`.

| Key | Holds |
|---|---|
| `folders` | Each folder two levels deep: note count, subfolders, loose notes, newest and oldest age, edits in the last 7 days |
| `journal.summaries` | The `>` summary line of each daily of the last 7 days |
| `journal.missing_days` | Each of the last 7 days with no daily, not counting today |
| `journal.checklists` | Each chore that `occasions.py` gives as due on a day (the daily list and the due chores), matched to the tasks of that day's daily: times seen, times ticked, and the rate, over the last 7 days |
| `journal.occasions_errors` | Each row of `occasions.md` that `occasions.py` cannot read: `line`, `row`, and `why`. A file in the old layout gives an error for each row and no chores |
| `journal.broken_nav` | Each `up`, `prev`, or `next` in a journal file edited in the last 7 days that names no file |
| `compass` | One row each for 7, 30, 90, and 365 days: `dailies`, `edits`, `chore_rate` (null with no chores), `busiest` (top 3 folders by edits), and `reflections` (a count) |
| `reflections` | Each journal note of the last 365 days with a filled reflect section, newest first: `path`, `level` (daily, weekly, monthly), `date`, and `sections` of `{heading, text}`. A section is a `###` heading, or in a daily a top-level bullet such as `- 🧠 What I learned`. A backtick placeholder is empty. The `## 🗓️ Weekly Reflect` of a Sunday daily is its own `weekly` item, dated to the Monday of its week, as a weekly file is |
| `projects` | Each project with a `MISSION.md`: `project`, `path`, `status` (`active`, `dormant`, `waiting`, or `archived`), `until`, and `changed_days`, the age of its newest note |
| `inbox` | Each inbox note with its age and word count |
| `recent` | Each note outside the journal edited in the last 7 days |
| `stale` | Each note past the stale limit, with its backlinks, and its backlinks from notes edited inside the limit. Notes in a `*knowledge` folder are never on it |
| `archive` | Each archived note with its age and its links from outside the archive. `delete_candidate` is true past the archive limit with no such link |
| `activity` | Edits by folder, by hour, and by weekday (Monday first), and the tags of notes edited in the last 7 days |
| `bulk_commits_skipped` | The count of commits that the scan skipped because they touch more than `--bulk-files` paths (default 50). Ages, edit counts, hours, and weekdays leave them out. 0 with none, or with no git history |
