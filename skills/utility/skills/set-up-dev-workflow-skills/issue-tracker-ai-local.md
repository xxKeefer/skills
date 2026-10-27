# Issue tracker: Local Markdown (`.ai/`)

Issues and specs for this repo live as markdown files in `.ai/` at the repo root — the
same scratch root the xxkeefer `/write-to-file` primitive uses, so both skill ecosystems write
to one place.

## Conventions

- One feature per directory: `.ai/<feature-slug>/`
- The spec/PRD is `.ai/<feature-slug>/PRD.md`
- Implementation issues are `.ai/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Comments and conversation history append under a `## Comments` heading at the bottom
- Standalone artifacts that predate this convention (`.ai/plan_*.md`, `.ai/spike_*.md`,
  `.ai/hunt_*.md`) stay flat — don't migrate them

## When a skill says "publish to the issue tracker"

Create a new file under `.ai/<feature-slug>/`, creating the directory if needed.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user normally passes the path or issue number directly.
