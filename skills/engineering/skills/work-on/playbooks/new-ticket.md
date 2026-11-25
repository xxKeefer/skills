# Playbook: New Ticket

Take one ticket key or one idea to a draft PR. Each step calls one ★ command. The stops are the
stops in [`SKILL.md`](../SKILL.md).

| # | Step | Stop after the step |
| --- | --- | --- |
| 1 | `/spec <ticket key>` or `/spec <idea>`. Skip it when the ticket already has lettered ACs and a plain summary, or when the user gives a spec. | H1: the user says yes to the spec. `/refine-ticket` writes the ticket back, so that write is also an H4 stop. |
| 2 | `/plan <ticket key>` or `/plan @<spec path>`. | H2: the user approves the plan. |
| 3 | `/build @<plan path>`. | H3, only when the plan has an open `D` entry at the end of the build. |
| 4 | Run `/blast-radius @<plan path>`. When the verdict is `risk` and each confirmed risk has a clear fix, add one fix step for each to the plan, and run `/build @<plan path>`, so that the review covers the fix. Run `/interrogate @<plan path>`, which runs its adversaries at the `panel` models, only when a confirmed risk has no clear fix. | H3, only when the report keeps a finding and the plan has no fix step for it. |
| 5 | `/ship @<plan path>`. It opens a draft PR with no stop. | H4, only before an action on the pause list, such as mark the PR ready or merge. |
| 6 | Offer `/retro` on the session. The user runs it, or says no. | H5, when the user runs `/retro`: the user picks the skill edits. |

When `/plan` splits the ticket, stop at H2, and give the wave 1 commands that `/plan` returns.
Each sub-task is a new `/work-on` run.

**Done when:** the ticket has a draft PR, and the user has the `/retro` offer.
