# Issue tracker: Local Markdown (`.ai/`)

Issues, specs, and maps for this repo live as markdown files in `.ai/` at the repo root — the
same scratch root the xxkeefer `/write-to-file` primitive uses, so both skill ecosystems write
to one place.

## Conventions

- One feature per directory: `.ai/<feature-slug>/`
- The spec/PRD is `.ai/<feature-slug>/PRD.md`
- Implementation issues are `.ai/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is a `Status:` line near the top of each issue file (role strings per
  `triage-labels.md`)
- Comments and conversation history append under a `## Comments` heading at the bottom
- Standalone artifacts that predate this convention (`.ai/plan_*.md`, `.ai/spike_*.md`,
  `.ai/hunt_*.md`) stay flat — don't migrate them

## When a skill says "publish to the issue tracker"

Create a new file under `.ai/<feature-slug>/`, creating the directory if needed.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user normally passes the path or issue number directly.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.ai/<effort>/map.md` — the Notes / Decisions-so-far / Fog body
- **Child ticket**: `.ai/<effort>/issues/NN-<slug>.md`, numbered from `01`, question in the body.
  A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:`
  line records `claimed`/`resolved`
- **Blocking**: a `Blocked by: NN, NN` line near the top; unblocked when every listed file is
  `resolved`
- **Frontier**: scan `.ai/<effort>/issues/` for open, unblocked, unclaimed files; lowest number
  wins
- **Claim**: set `Status: claimed` and save before any work
- **Resolve**: append the answer under `## Answer`, set `Status: resolved`, then append a context
  pointer (gist + link) to the map's Decisions-so-far
