---
doctype: spec
ticket: none
status: confirmed
goal: A run on a copy of the user's AGENTS.md adds the blocks at the top, keeps the user's text, and a second run changes nothing.
---

# Spec: `install-agents-md` and the models block (r1.10)

Map unit 7 of `.ai/map_pstack-program.md`. Branch `pstack-7_agents-md`.

## Intent

- Outcome: a `utility/install-agents-md` skill writes managed blocks into `~/.claude/AGENTS.md`, from generic text in the repo, with machine facts hydrated on the machine.
- User: the user, on each machine that loads the marketplace.
- Why now: later units (TDD rule, notifier role, no-comments rule, worktrunk template) need a managed place in `~/.claude/AGENTS.md`, and skills must name a role, not a model.
- Success: a run on a copy of the user's AGENTS.md adds the blocks at the top, keeps the user's text, and a second run changes nothing.
- Constraint: the repo holds only generic text. Text outside the markers is the user's own, and the installer never changes it without a yes.
- Out of scope: the worktrunk template step (unit 14), the notifier role (unit 16), and the no-comments text in the `coding` block (unit 19).

## Decisions

- Managed blocks: each block sits between `<!-- managed: <name> -->` and `<!-- end managed -->`. The first run puts the blocks at the top. A later run replaces only the text inside the markers.
- `HYDRATE.md`: tells the agent how to fill each machine fact, and asks the user to confirm.
- Text outside the markers: the user's own. The installer can list edits for it, such as the system map line `<repo>.<KEY>/`, but does not apply them.
- Backup: each run first copies the file to `AGENTS.md.bak`.
- First run: shows the old plain-text sections beside the new blocks, and the user confirms the deletion of the old text.
- Models: a `models` managed block holds the model table. A skill names a role, not a model.
- Model roles: judgement, worker, mechanical worker, reviewer, mechanical reviewer, verifier, prover, panel, explorer, as in the map's Models table.
- Escalation: after two failed fixes on one premise, the next attempt moves one effort step up, to a ceiling of Opus max. Fable runs only when the user asks. The user can override a mechanical mark at H2. `PANEL.md` stays as an override for one lane.
- Deterministic work goes to scripts (user note r1.4).

## Acceptance criteria

- [ ] **A.** Run `utility/install-agents-md` with its `sections/`, `HYDRATE.md`, and backup → `AGENTS.md.bak` exists, and the managed blocks are written from `sections/`.
- [ ] **B.** Read the written blocks → the file holds the `coding` block (the TDD rule), the `tools` block (the role table), and the `models` block (the model table).
- [ ] **C.** Read `build`, `implement`, `mob-review`, and `/work-on` → each names a role and reads the `models` block, and none names a model.
- [ ] **D.** Run the installer on a copy of the user's AGENTS.md, then run it again → the first run adds the blocks at the top and keeps the user's text, and the second run changes nothing.
