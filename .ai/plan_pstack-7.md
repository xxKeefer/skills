---
doctype: plan
ticket: none
worktree: ~/studio/code/pstack-inspiration
branch: pstack-7_agents-md
status: approved
goal: A run on a copy of the user's AGENTS.md adds the blocks at the top, keeps the user's text, and a second run changes nothing.
spec: .ai/spec_pstack-7.md
---

# Plan: pstack-7 `install-agents-md` and the models block

## Goal

A run on a copy of the user's AGENTS.md adds the blocks at the top, keeps the user's text, and a
second run changes nothing. Scope: SCOPED, one PR. Estimate: 3 points.

## Spec

`.ai/spec_pstack-7.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** Run `utility/install-agents-md` with its `sections/`, `HYDRATE.md`, and backup → `AGENTS.md.bak` exists, and the managed blocks are written from `sections/`.
- [ ] **B.** Read the written blocks → the file holds the `coding` block (the TDD rule), the `tools` block (the role table), and the `models` block (the model table).
- [ ] **C.** Read `build`, `implement`, `mob-review`, and `/work-on` → each names a role and reads the `models` block, and none names a model.
- [ ] **D.** Run the installer on a copy of the user's AGENTS.md, then run it again → the first run adds the blocks at the top and keeps the user's text, and the second run changes nothing.
- [ ] **E.** Run the installer when a section needs a machine value that is not set → the script writes nothing, exits 1, and names the missing key and its `HYDRATE.md` entry.
- [ ] **F.** Run the installer on a file with an old plain-text section that a block replaces → the script lists the old section, and deletes it only when the caller passes its name.

## Context

- Map: `.ai/map_pstack-program.md`, unit 7. Done line: "a run on a copy of the user's AGENTS.md
  adds the blocks at the top, keeps the user's text, and a second run changes nothing."
- Approval: the agent approved the plan under the approved map (H0). The user waived the H2 stop for map units on 2026-11-17.
- From the spec Intent: the repo holds only generic text. Machine facts are hydrated on the
  machine. Text outside the markers is the user's own.
- From the spec Decisions: markers `<!-- managed: <name> -->` and `<!-- end managed -->`. The
  first run puts the blocks at the top. A later run replaces only the text inside the markers.
  Each run first copies the file to `AGENTS.md.bak`. The first run shows the old plain-text
  sections beside the new blocks, and the user confirms the deletion of the old text. The
  installer lists edits for the user's own text, such as the system map line `<repo>.<KEY>/`, and
  does not apply them. Deterministic work goes to a script (r1.4).
- Model roles, from the map's Models table: judgement, worker, mechanical worker, reviewer,
  mechanical reviewer, verifier, prover, panel, explorer. The escalation rules go into the
  `models` block as text. Unit 20 builds the escalation behaviour.
- Out of scope: the worktrunk template step (unit 14), the notifier role (unit 16), the
  no-comments text in the `coding` block (unit 19), and a `plugin.json` version bump (unit 33).
- Design: `scripts/install_agents_md.py` does every file change. Each `sections/<name>.md` holds
  generic text, with `{{key}}` placeholders for machine facts, and an optional `replaces:` line
  that names the old heading it replaces. The machine values live in
  `~/.claude/agents-md.values.json`, outside the repo. `HYDRATE.md` tells the agent how to fill
  each key and to confirm each value with the user. The skill keeps
  `disable-model-invocation: true`, as the other installers do.
- Never commit a copy of the user's real AGENTS.md. It holds work facts. Test fixtures are
  synthetic, and the proof run uses a temp copy.
- Production gate: none. The skill runs only when the user types it, and it backs up the file
  before each write.
- Gates: `python3 skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`,
  and `sh .githooks/pre-commit_test.sh`.
- Commits: conventional commits, no AI attribution.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | backup, then write blocks from `sections/` | H | one-way change to the user's own global file |
| B | the three blocks and their text | L | copy |
| C | four skills name a role | L | docs |
| D | blocks at the top, user text kept, second run a no-op | H | data loss in a file read by every session |
| E | missing machine value stops the write | M | a half-hydrated block leaks `{{key}}` into every session |
| F | old section listed, deleted only by name | H | deletes the user's own text |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | each run writes `AGENTS.md.bak` with the old bytes before it writes | state | Unit | `install_agents_md.spec.py` |
| C2 | D | a file with no markers gets every block at the top, in `sections/` order, and the old text below, byte for byte | EP | Unit | `install_agents_md.spec.py` |
| C3 | D | a second run gives the same bytes | state | Unit | `install_agents_md.spec.py` |
| C4 | D | a file with old markers gets only the inside of the markers replaced, and text between and after the blocks stays | EP | Unit | `install_agents_md.spec.py` |
| C5 | E | a missing value key: exit 1, the key named, no write, no backup | error guessing | Unit | `install_agents_md.spec.py` |
| C6 | — | a missing target file: the script creates it with the blocks | EP | Unit | `install_agents_md.spec.py` |
| C7 | F | an old heading that a section `replaces`: listed, and kept without the flag | decision table | Unit | `install_agents_md.spec.py` |
| C8 | F | the same heading with `--drop <name>`: its section, up to the next heading of the same or a higher level, is deleted | BVA | Unit | `install_agents_md.spec.py` |
| C9 | — | an unmatched start marker, or a marker for an unknown block: exit 1, no write | error guessing | Unit | `install_agents_md.spec.py` |
| C10 | D | the proof run on a temp copy of the real file, twice | — | Manual | Progress entry |

### Not testing

- B and C: text only. The review step reads them.

## Steps

- [x] **1. Install the blocks into AGENTS.md, with backup and hydration.** Seam: the CLI `install_agents_md.py --target <file> --values <json>`. Conditions: C1, C2, C3, C4, C5, C6, C9.
  - Add `skills/utility/skills/install-agents-md/` with `SKILL.md`, `HYDRATE.md`, `README.md`, `sections/coding.md` (the TDD rule from the map's TDD decision), `sections/tools.md` (the role table, with `{{key}}` values), `sections/models.md` (the model table and the escalation rules), and `scripts/install_agents_md.py` with `scripts/install_agents_md.spec.py`.
  - Add the skill row to `skills/utility/README.md`.
  - Done: the spec file covers C1 to C6 and C9, and passes. A user can run `/install-agents-md` on a file and see the three blocks at the top.
- [x] **2. List and drop the old plain-text sections.** Seam: the same CLI, with `--drop <name>`. Conditions: C7, C8.
  - `sections/tools.md` replaces `## Tools on this machine`. `sections/coding.md` names no old heading, because the user's `# Coding Preferences` holds more than the TDD rule: the script lists the TDD lines as an edit for the user and does not apply it.
  - `SKILL.md` shows each old section beside its block and asks once before `--drop`.
  - Done: the spec file covers C7 and C8, and passes. A user sees the old section and drops it with one yes.
- [x] **3. Name roles in four skills.** Kind: docs.
  - `build`, `implement`, `mob-review` (with `PANEL.md` and `RUBRIC.md`), and `work-on` name a role from the `models` block and name no model. Each says: with no `models` block, use the session model.
  - Done: `grep -n -iE "opus|sonnet|haiku" ` on the four skill folders finds no model name outside a `PANEL.md` lane override line.
- [x] **4. Prove the done line on a copy.** Kind: config.
  - Copy `~/.claude/AGENTS.md` to a temp folder. Fill a temp values file. Run the script twice on the copy. Compare the user text and the second-run bytes. Write the result into Progress. Commit no copy.
  - Done: Progress holds the two runs and their result (C10).
- [x] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-7.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
- [ ] **7. Push.** Push the branch with `git push -u origin pstack-7_agents-md`. Run no `gh` command on this machine. The home machine opens the PR.
  - Done: the pushed branch and its head SHA are in this line.

## Suggested skills

- `/build @.ai/plan_pstack-7.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-7.md`: one step per session, from the worktree.
- `/tdd`: steps 1 and 2.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-inspired`. Playbook: map (`/work-on @.ai/map_pstack-program.md`, batch of one). Stop: H2, the user approves this plan. Next: step 4 of the map playbook, make `pstack-7_agents-md` from `pstack-inspired`, then `/build`.
- 2026-11-17: steps 1 to 3 done on `pstack-7_agents-md`. Commits: step 1 `9d3d5d6` (the script and spec already hold the `--drop` code of step 2), step 2 `de35126` (SKILL.md drop flow), step 3 `56b4cc0`. Spec: 20 tests, green, mutation checks went red (no backup, wrong heading end). Grep for model names in the four skill folders: none.
- 2026-11-17: step 4, C10 proof run on a temp copy of the real `~/.claude/AGENTS.md`, with a temp values file. Run 1: `updated`, three blocks at the top, the last N bytes equal the original file (user text kept byte for byte), `AGENTS.md.bak` equals the original, `OLD tools` and `EDIT coding` lines listed. Run 2: `unchanged`, bytes equal to run 1. A run with `--drop tools` removed only the 11-line old tools section. No copy committed, temp folder deleted.
- 2026-11-17: step 5, gates green: `install_agents_md.spec.py` (20 tests OK), `pre-commit_test.sh` (all ok).
