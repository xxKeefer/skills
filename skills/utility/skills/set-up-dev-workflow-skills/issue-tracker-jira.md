# Issue tracker: Jira (Atlassian MCP)

Issues for this repo live in Jira. All operations go through the Atlassian MCP tools — never
tell the agent to open a browser or shell out to a CLI. Specs and long-form docs live in
Confluence, linked from their Jira issues.

## Conventions

- **Project key**: per the repo's CLAUDE.md or the `jira-conventions` skill — never guess one
- **Issue creation**: `createJiraIssue`; epics hold features, stories hold tracer-bullet slices,
  subtasks hold progress-tracking steps
- **Fetch**: `getJiraIssue` by key (e.g. `ENG-1234`); search with `searchJiraIssuesUsingJql`
- **Comments**: `addCommentToJiraIssue` — the equivalent of "comment on the issue"
- **Specs/PRDs**: a Confluence page (`createConfluencePage`, space per `confluence-conventions`),
  linked from the epic; the Jira description carries the summary and the link, not the full spec

## Triage state

Jira expresses triage as status transitions plus labels, not bare labels alone:

| Canonical role | Jira expression |
|---|---|
| `needs-triage` | status `Open` + label `needs-triage` |
| `needs-info` | label `needs-info`, comment @-mentioning the reporter |
| `ready-for-agent` | status `To Do` + label `ready-for-agent` |
| `ready-for-human` | status `To Do` + label `ready-for-human` |
| `wontfix` | transition to `Closed`/`Won't Do` via `transitionJiraIssue` |

## When a skill says "publish to the issue tracker"

Create the issue(s) with `createJiraIssue` in dependency order (blockers first), then wire
blocking edges with `createIssueLink` (`Blocks` link type — check `getIssueLinkTypes` once per
session).

## Wayfinding operations

Used by `/wayfinder`. The **map** is an epic; tickets are its child issues.

- **Map**: an epic labelled `wayfinder-map`; its description holds Notes / Decisions-so-far / Fog
- **Child ticket**: an issue in the epic, question in the description; ticket type recorded as a
  label (`wf-research`/`wf-prototype`/`wf-grilling`/`wf-task`)
- **Blocking**: native `Blocks` issue links — Jira renders the frontier visually
- **Frontier**: JQL — `parentEpic = <MAP-KEY> AND statusCategory != Done AND assignee IS EMPTY`,
  filtered to issues whose blocking links are all resolved
- **Claim**: assign the issue to yourself and transition to `In Progress`
- **Resolve**: comment the answer, transition to `Done`, then edit the epic description to append
  the gist + issue link under Decisions-so-far

## Concurrency

Other sessions may be working sibling tickets — re-fetch before editing the map epic, and never
cache frontier queries across steps.
