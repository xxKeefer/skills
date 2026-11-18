---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-33_retire-versions
status: approved
goal: "Each changed domain has one new version, and only this unit changed a plugin.json."
spec: .ai/spec_pstack-33.md
builds_on: pstack-32
---

# Plan: pstack-33 Retire list and version bumps

## Goal

List `/do-next` as the skill to retire after the trial, in a place that outlives the map, and give each domain that the program changed one new version over `main`. Scope: SCOPED, one PR: three `plugin.json` edits, one version line, and one vault task note.

## Spec

`.ai/spec_pstack-33.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Read the retire list → it names `/do-next` as the skill to retire after the trial, and `/do-next` is still in `primitives`.
- [ ] **B.** Compare each domain's `plugin.json` version with `main` → `engineering` is 3.0.0, and each other domain with a change since `main` is one minor version over `main`.
- [ ] **C.** Compare each `plugin.json` with `main` → each changed domain has one new version, and a domain with no change keeps its `main` version.

## Context

- Map: `.ai/map_pstack-program.md`, unit 33. Done line: each changed domain has one new version, and only this unit changed a `plugin.json`.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-32_script-audit`, because the unit 20 to 32 PRs are not merged. The home machine sets the unit 33 PR base to that branch. Keep the unit 20 to 32 `.ai/` files.
- Decisions: Domains and lifecycle (map). The candidate to retire after the trial is `/do-next`. Do not move it.
- Decisions: Rules (map). Only the top unit (33) changes a `plugin.json` version.
- Versions on `main`, then on this branch before the unit: `engineering` 2.4.1 then 2.5.0, `primitives` 2.25.0 then 2.26.0, `meta` 1.20.0 then 1.21.0, `deprecated` 2.21.0 then 2.22.0, `projects` 0.11.0, `scribe` 1.26.0, `utility` 1.25.0. Unit 2 bumped the first four in 519effb, when it removed `experimental`. `journal` and `nix-manager` have no change since `main`. `experimental` is gone.
- Version targets: `engineering` 3.0.0. `projects` 0.12.0, `scribe` 1.27.0, `utility` 1.26.0. `primitives`, `meta`, and `deprecated` keep their unit 2 version, which is already one minor over `main`. `journal` and `nix-manager` keep theirs.
- Retire list home: the map is deleted in this unit's PR, by the `.ai/CLAUDE.md` rule, so the list moves out of `.ai/`. It goes into a vault task note `Trial the pstack program`, with a `Backlog` card that links to it on the repo's tracker board (`docs/agents/issue-tracker.md`). The note also takes the map's Trial steps, which the user needs after the last unit. The vault is private, so the pause list does not hold the note.
- Map clean-up: after the push, tick unit 33. Every unit then has a tick, so delete the map in a new commit and push again.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A version is a record, because the marketplace loads each domain in place (ADR 0001).
- Push-only map: the push step runs `git push -u origin pstack-33_retire-versions`. Run no `gh` command.
- Commit convention: conventional commits with the domain as scope, `chore(skills)` for the version bumps, `docs(ai)` for `.ai/`. No Claude attribution line.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`, and the version compare in condition C2.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the retire list names `/do-next`, and no skill moves | L | one note, and `git diff` shows no skill move |
| B, C | each changed domain has exactly one new version over `main` | M | a missed domain or a double bump drifts with no error |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | the task note names `/do-next`, and `skills/primitives/skills/do-next/SKILL.md` exists on the branch | EP | Manual | read the note and list the folder |
| C2 | B, C | for each domain folder, a change since `main` gives exactly one version step over `main`, and no change gives the `main` version | EP | Integration | a shell loop over `skills/*/` that compares `git diff main...HEAD` with each `plugin.json` version |

### Not testing

- The choice of minor over major for `primitives`, `meta`, and `deprecated`. The map names only `engineering` as a major bump.

## Steps

- [ ] **1. Version bumps.** Kind: config. Conditions: C2. Set the versions in Context. Run the C2 loop.
  - Done: the C2 loop prints one line for each domain, and each line passes. B and C hold.
- [ ] **2. Retire list.** Kind: docs. Conditions: C1. Write the vault task note and its `Backlog` card, as Context says.
  - Done: the note names `/do-next` and holds the Trial steps. The card links to the note. `/do-next` is still in `primitives`. A holds.
- [ ] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-33.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-33_retire-versions`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Progress

## Pending Decisions

## Follow-ups
