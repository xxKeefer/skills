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
| `grill-with-docs` | Grill-led requirements gathering, doc-anchored |
| `wayfinder` | Decision-mapping for large-scale work (fog-of-war, HITL/AFK tickets) |
| `to-spec` | Turn an idea/conversation into a spec |
| `to-tickets` | Break a spec into tracer-bullet vertical-slice tickets |
| `implement` | Execute a ticket (TDD-backed) |
| `code-review` | Review with a Fowler smell baseline |
| `improve-codebase-architecture` | Scan for deepening opportunities, HTML report, grill through picks |
| `setup-matt-pocock-skills` | Per-repo config — writes `docs/agents/issue-tracker.md` + triage labels |
| `writing-great-skills` | Reference on skill-authoring principles |
| `codebase-design` | Deep-module vocabulary the architecture skills compose |

## Dependencies (vendored because the above compose them)

`grilling`, `domain-modeling`, `prototype`, `research`, `triage`, `tdd`

## Tracker coupling

Matt's flow assumes GitHub (`gh` CLI, issues, PRs). This repo's flows are tracker-agnostic —
local `.ai/` markdown at home, Jira/Confluence at work. Do not edit these skills to fix that;
front them with adapter skills that resolve "the tracker" from the project's CLAUDE.md.
