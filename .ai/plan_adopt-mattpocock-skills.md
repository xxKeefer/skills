# Plan: Adopt Matt Pocock's skills (v1.1.0) as the `mattpocock` domain

**Spike:** none — driven by three tabular analyses in-session (2026-07-09).
**Source:** https://github.com/mattpocock/skills @ v1.1.0, MIT. Clone cached at scratchpad
`mattpocock-skills/` (re-clone `--branch v1.1.0` if gone).

## Decisions already made

- Vendor verbatim, never patch in place; MIT LICENSE travels with the copy.
- Adopt wholesale wherever nothing in my chain depends on an equivalent (domain-modeling,
  prototype, triage, codebase-design, writing-great-skills, set-up-dev-workflow-skills,
  improve-codebase-architecture).
- Where my chain has dependents (grill-it ×7, tdd ×3, handoff ×3): keep my skill name as the
  stable identity, align its body to Matt's design. Duplicate triggers with the vendored twins
  are then benign — both resolve to the same behaviour.
- No cross-plugin delegation from `primitives` to `mattpocock` — primitives is the always-required
  base and must not depend on an optional domain. Sync bodies, don't delegate.
- Tracker adapters: Matt's skills read a per-repo `docs/agents/issue-tracker.md` written by
  `/set-up-dev-workflow-skills`. We ship two ready-made variants (local `.ai/`, Jira/Confluence)
  as xxkeefer-authored files beside the vendored skills — never inside them.

## Already in the working tree (uncommitted)

- `skills/mattpocock/` — 12 skills (grill-with-docs, wayfinder, to-spec, to-tickets, implement,
  code-review, grilling, domain-modeling, prototype, research, triage, tdd), LICENSE, README,
  plugin.json v1.1.0.
- `.claude-plugin/marketplace.json` — mattpocock entry added.

### Step 1: Complete and commit the vendored domain

**What:** Vendor the 4 remaining adopt-wholesale skills from the clone
(`set-up-dev-workflow-skills`, `codebase-design`, `improve-codebase-architecture` from
engineering/, `writing-great-skills` from productivity/). Update the domain README skill table,
add a `mattpocock` row to the root CLAUDE.md domains table.
**Files:** `skills/mattpocock/skills/{set-up-dev-workflow-skills,codebase-design,improve-codebase-architecture,writing-great-skills}/`, `skills/mattpocock/README.md`, `CLAUDE.md`
**Done when:** 16 skills vendored byte-identical to the v1.1.0 clone, registry and docs
consistent, one commit.

### Step 2: Ship tracker adapter docs

**What:** Create `skills/mattpocock/adapters/issue-tracker-ai-local.md` (derived from his
`issue-tracker-local.md` template, but scratch root `.ai/` and `/write-to-file` conventions) and
`skills/mattpocock/adapters/issue-tracker-jira.md` (Atlassian MCP, Megaport project keys per
`jira-conventions`, native blocking = Jira issue links, triage labels mapped to status
transitions/labels, wayfinding operations section). README gains a "per-repo setup" section:
run `/set-up-dev-workflow-skills`, hand it the fitting adapter.
**Files:** `skills/mattpocock/adapters/*.md`, `skills/mattpocock/README.md`
**Done when:** both adapters exist, README marks `skills/` as verbatim and `adapters/` as ours,
one commit.

### Step 3: Align primitives — grill-it and handoff

**What:** `grill-it` body is Matt's pre-v1.1.0 grilling verbatim; update it to his v1.1.0 body
(one question at a time, recommended answers, facts-vs-decisions split, confirmation gate),
keeping my name/description/triggers. Diff `primitives:handoff` against his
`productivity/handoff` and fold in anything his has that mine lacks, preserving my temp-dir
convention and argument-hint (do-next/update-handoff depend on them). Bump primitives → 1.8.0.
**Files:** `skills/primitives/skills/grill-it/SKILL.md`, `skills/primitives/skills/handoff/SKILL.md`, `skills/primitives/.claude-plugin/plugin.json`
**Done when:** grill-it matches v1.1.0 grilling behaviour; the 7 grill-it callers and 3 handoff
dependents need no edits; one commit.

### Step 4: Align developer:tdd to his reference-only design

**What:** Replace the 153-line `developer:tdd` SKILL.md body with his 36-line reference-format
tdd, keeping the `developer:tdd` identity (do-it, hunt-it, plan-it keep resolving). Copy his
sibling reference files (`tests.md`, `mocking.md`) alongside. Bump developer → 3.4.0.
**Files:** `skills/developer/skills/tdd/{SKILL.md,tests.md,mocking.md}`, `skills/developer/.claude-plugin/plugin.json`
**Done when:** developer:tdd is his design under my name, his `implement` and my `do-it` both
resolve `/tdd` to identical behaviour; one commit.

### Step 5: Drop the `*-it` convention — repo-wide rename

**What:** Rename every `*-it` skill to a straight descriptive kebab-case verb name (Matt's
style: `implement`, `to-spec`). The HITL-vs-AFK distinction the suffix carried moves to Matt's
mechanism: `disable-model-invocation: true` frontmatter on HITL skills. Mechanics per skill:
rename the directory, update `name:` in frontmatter, update every cross-reference in other
skills' SKILL.md bodies (grill-it has 7 dependents; sweep with grep, not memory). Major-bump
every touched domain. **Gate: present the proposed mapping table for approval before renaming
anything** — collisions with vendored twins (research, to-tickets) are benign post-alignment,
but collisions with different-behaviour skills (e.g. explain-it vs primitives:explain) need
distinct names.

Proposed mapping (to be approved at execution):

| old | new | note |
|---|---|---|
| grill-it | grill | body already aligned to his grilling (step 3) |
| plan-it | to-plan | his transform-into-X naming |
| do-it | implement | converges with his implement's role |
| spike-it | spike | |
| task-it | to-tickets | benign twin of vendored to-tickets |
| research-it | research | benign twin |
| hunt-it | diagnose | matches his diagnosing-bugs vocabulary |
| fix-it | fix | |
| tweak-it | tweak | |
| resolve-it | resolve-feedback | avoid clash with resolve-conflicts |
| document-it | sync-docs | |
| explain-it | explain-reasoning | primitives:explain already exists |

**Files:** every `skills/*/skills/*-it/` directory, all SKILL.md cross-references, domain
plugin.json versions, hooks/skill-tally continuity note.
**Done when:** zero `*-it` names remain, `grep -r '\-it\b' skills/` shows no dangling skill
references, HITL skills carry `disable-model-invocation: true`, one commit.

### Step 6: Documentation pass

**What:** Sweep every documentation surface for the new names and the adopted conventions:
root README, CLAUDE.md, CONTEXT.md (rewrite the HITL definition — suffix convention →
`disable-model-invocation` frontmatter), each touched domain's README/CLAUDE.md, memory
pointers, and the mattpocock README cross-links. Root README gains an attribution section pointing at
https://github.com/mattpocock/skills (MIT, vendored at v1.1.0) covering both the vendored domain
and the aligned skill bodies. Verify no doc references a dead skill name.
**Files:** `README.md`, `CLAUDE.md`, `CONTEXT.md`, `skills/*/README.md`, `skills/*/CLAUDE.md`
**Done when:** grep for every old name across `*.md` returns only git history/changelog-style
mentions, one commit.

## Out of repo scope (manual follow-ups)

- Point `~/.claude/AGENTS.md`'s deep-module reference at the vendored `codebase-design` skill
  (one source of truth).
- Run `/set-up-dev-workflow-skills` in real work repos with the Jira adapter; in personal repos
  with the `.ai/` adapter.
- Later: watch his in-progress writing pipeline (fragments/beats/shape) and `wizard` for a
  future re-vendor; tally will decide whether my duplicated grilling/tdd twins get retired.
