# 0014 One marketplace

**Status:** Accepted, 2026-11-13.

## Context

A second marketplace, `xxkeefer-work`, held the skills for work at an employer, in three domains:
`tools`, `new`, and `old`. It held 15 skills. Its reason to exist was that these skills named the
employer's tracker, its fields, and its products, which this repo's North Star bars.

Two repos meant two places to edit, two version streams, and skills that duplicated the engineering
skills. A review against `engineering` found that 11 of the 15 skills were covered, or were not
worth a port.

## Decision

- Retire `xxkeefer-work`. This repo is the only marketplace.
- Drop 11 skills: `to-jira`, `jira-action-plan`, `generate-branch-names`, `next-subtask`,
  `next-task`, `triage-feedback`, `apply-fix-and-close-thread`, `pr-description-mp`,
  `review-ping`, `posthog-dashboard`, and `remove-feature-flag`.
- Port 4 skills, with no employer detail: `pick-next-task`, `pr-news`, and `qa-screenshots` go to
  `engineering`, and `retro-note` goes to `scribe`.
- A skill names a tool by its role: the tracker, the code host, the browser. The repo's
  `## Agent skills` block names the product for one repo. The `## Tools on this machine` block in
  the user's global instructions names it for one machine, and can point to a notes file on that
  machine with the employer detail. The repo block wins.

## Consequences

- Each machine needs a `## Tools on this machine` block. With no block, a skill asks for the tool.
- Employer detail lives only in machine files outside any repo. The scrub hook still checks every
  commit for employer names.
- The private pattern file of the scrub hook moves out of the retired repo, to a path that
  `git config scrub.patterns` names on each machine.
