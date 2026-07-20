# mattpocock

Verbatim vendored copy of [Matt Pocock's skills](https://github.com/mattpocock/skills), tag
`v1.1.0`, MIT licensed (see [LICENSE](LICENSE)). Nothing here is edited — updates come from
re-vendoring a newer tag, never from patching in place. Adapt via wrapper skills in other
domains, not by forking these files.

## Main flow

idea → `/to-spec` → `/to-tickets` → `/implement`, with `/wayfinder` as the large-effort on-ramp
and `/code-review` at the end.

## Skills

| Skill | Role |
|---|---|
| `wayfinder` | Decision-mapping for large-scale work (fog-of-war, HITL/AFK tickets) |
| `to-spec` | Turn an idea/conversation into a spec |
| `to-tickets` | Break a spec into tracer-bullet vertical-slice tickets |
| `implement` | Execute a ticket (TDD-backed) |
| `code-review` | Review with a Fowler smell baseline |
| `setup-matt-pocock-skills` | Per-repo config — writes `docs/agents/issue-tracker.md` + triage labels |

## Dependencies (vendored because the above compose them)

`grilling`, `research`, `triage`, `tdd`

(`grill-with-docs`, `domain-modeling`, `codebase-design`, `improve-codebase-architecture`, and
`prototype` migrated to the `developer` domain, 2026-07; skills here still invoke them by name,
so `developer` must be enabled.)

## Tracker coupling and per-repo setup

The flow skills never hardcode a tool — each reads the repo's `docs/agents/issue-tracker.md`,
written once by `/setup-matt-pocock-skills`. `skills/` is the verbatim vendored tree;
`adapters/` is xxkeefer-authored and safe to edit:

- `adapters/issue-tracker-ai-local.md` — personal repos; scratch root `.ai/`, aligned with
  `/write-to-file`
- `adapters/issue-tracker-jira.md` — work repos; Atlassian MCP, triage roles mapped to Jira
  statuses/labels, wayfinder maps as epics

Per repo: run `/setup-matt-pocock-skills`, and when it asks for the tracker, hand it the
fitting adapter file as the answer.
