---
doctype: spec
ticket: none
status: confirmed
goal: "Each changed domain has one new version, and only this unit changed a plugin.json."
---

# Spec: Retire list and version bumps

## Intent

- Outcome: the skills to retire after the trial are listed in a place that outlives the program map: `/do-next`. No skill moves.
- Outcome: each domain that the program changed has one new version over `main`. `engineering` goes to 3.0.0, because callable skills and the rename break existing prompts.
- User: the repo owner, who runs the trial and then decides each retirement with `/retire-a-skill`.
- Why now: map unit 33, the last unit.
- Success: each changed domain has one new version, and only this unit changed a `plugin.json`.
- Constraint: move no skill, and change no skill text.

## Decisions

- Domains and lifecycle (map): the candidate to retire after the trial is `/do-next`. Do not move it during the program.
- Rules (map): only the top unit (33) changes a `plugin.json` version.

## Acceptance criteria

- [ ] **A.** Read the retire list → it names `/do-next` as the skill to retire after the trial, and `/do-next` is still in `primitives`.
- [ ] **B.** Compare each domain's `plugin.json` version with `main` → `engineering` is 3.0.0, and each other domain with a change since `main` is one minor version over `main`.
- [ ] **C.** Compare each `plugin.json` with `main` → each changed domain has one new version, and a domain with no change keeps its `main` version.
