---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-8_principles-tdd-skip
status: approved
goal: /work-on on a task names the principle that shaped a choice, and the principle's file was read in that session.
spec: .ai/spec_pstack-8.md
---

# Plan: pstack-8 principles and the TDD skip rule

## Goal

/work-on on a task names the principle that shaped a choice, and the principle's file was read in
that session. Scope: SCOPED, one PR. Estimate: 3 points. Most of the diff is 24 short skill files.

## Spec

`.ai/spec_pstack-8.md`. This plan builds all of it.

## Acceptance criteria

- [ ] **A.** List the `principle-*` skills in `engineering` → 24 skills with pstack's names, each with `disable-model-invocation: true`, and the two adapted principles point at the pause list, and at subagents and `/checkpoint`.
- [ ] **B.** Read `/work-on` → an inline index in the five groups, one "when it applies" line per principle, the reply rule, and the "read it first" rule.
- [ ] **C.** Read `engineering/tdd` → the skip rule: the three skip reasons, the closest real check, and a skipped step that stays in the plan with its reason.
- [ ] **D.** Type `/principle-fix-root-causes` → the skill runs, and no rule file holds the principles.
- [ ] **E.** Run `/work-on` on a task → the reply names the principle that shaped a choice, and the principle's file was read in that session.

## Context

- Map: `.ai/map_pstack-program.md`, unit 8. Done line: `/work-on` on a task names the principle that shaped a choice, and the principle's file was read in that session.
- Approval: the map (H0).
- Push-only map: the build machine runs no `gh` command. The push step runs `git push -u origin pstack-8_principles-tdd-skip`. The home machine opens the PR into `pstack-inspired`.
- Spec Intent: the 24 pstack `principle-*` skills live in `engineering`, `/work-on` indexes them, and `engineering/tdd` has the skip rule. The principles stay skills with `disable-model-invocation: true`, not a rule file (r1.2 user note). Out of scope: `/verify` and its drivers (unit 11), `/checkpoint` (unit 13), `/sitrep` (unit 12). The text names them as they will be.
- Spec Decisions:
  - Take all 24 pstack `principle-*` skills, with pstack's names, into `engineering`. Each keeps `disable-model-invocation: true`.
  - `/work-on` holds an inline index in pstack's five groups (Core, Architecture, Verification, Delegation, Meta), with one "when it applies" line each.
  - The agent reads a principle's `SKILL.md` by path when it applies it. A skill that runs without the router names its principles in bold, with a sibling path such as `../principle-fix-root-causes/SKILL.md`.
  - The reply names each principle that shaped a decision, and cites only a principle it read in this session.
  - Adapt two: `principle-never-block-on-the-human` points at the pause list, and `principle-guard-the-context-window` points at subagents and `/checkpoint`.
  - TDD by default. Skip a test only when it would be expensive, integration-heavy, or unclear, and use the closest real check instead (`/verify` when the repo has a driver). A skip is never silent: the plan step stays, marked skipped with its reason, and `/sitrep` shows it.
- Source: pstack, `https://github.com/cursor/plugins/tree/main/pstack/skills`, MIT licence. Copy the licence notice into the repo with the skills.
- Write each principle body in the repo voice (STE-flavoured, Australian English) and keep the pstack meaning. A pstack link to a skill this repo does not have points at the repo's own skill or rule, or goes.
- Production gate: none. Each principle has `disable-model-invocation: true`, so it adds no context load and runs only when the user types it or an agent reads it by path.
- Commit convention: conventional commits with the domain as scope, such as `feat(engineering): ...`.
- Gates: `python3 skills/engineering/skills/work-on/scripts/check_principles.spec.py`, `python3 skills/engineering/skills/work-on/scripts/map_units.spec.py`, and `.githooks/pre-commit`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | 24 principle skills, user-only, two adapted | M | a missing flag adds context load to every session |
| B | the index in `/work-on` matches the skills | M | a drifted index sends the agent to a missing file |
| C | the TDD skip rule | L | prose only |
| D | a principle runs when typed | L | the plugin loader proves it |
| E | the reply cites a principle it read | M | the done line of the unit, a model behaviour |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | each `principle-*` folder has `disable-model-invocation: true`, and a `name` equal to the folder name | EP | Unit | `check_principles.spec.py` |
| C2 | A | the set of folders is the 24 pstack names, and a missing or extra folder fails with its name | EP | Unit | `check_principles.spec.py` |
| C3 | B | each index entry in `work-on/SKILL.md` names a folder that exists, each folder has an entry, and the five group headings exist | EP | Unit | `check_principles.spec.py` |
| C4 | A | the two adapted principles name the pause list, and subagents and `/checkpoint` | review | Manual | the review step |
| C5 | E | a `/work-on` run cites only a principle whose file it read in the session | use case | Manual | the user, after the trial |

### Not testing

- C, D: prose and the plugin loader. The review step reads C, and `/reload-plugins` shows D.
- C5 runs on a live session. A subagent build cannot start `/work-on`, so the user checks it in the trial.

## Steps

- [x] **1. The 24 principle skills, the `/work-on` index, and the check.** Seam: `python3 skills/engineering/skills/work-on/scripts/check_principles.py <repo root>`, exit 0 or 1, one error line per fault. Conditions: C1, C2, C3.
  - Write `check_principles.spec.py` first, with fixtures in a temp folder, then `check_principles.py`. Then add `skills/engineering/skills/principle-*/SKILL.md` for the 24 pstack names, each with `disable-model-invocation: true` and a one-line human description. Adapt `principle-never-block-on-the-human` to point at the `pause-list.md` rule, and `principle-guard-the-context-window` to point at subagents and `/checkpoint`. Add a `## Principles` section to `work-on/SKILL.md`: the five groups, one entry per principle with its folder name and one "when it applies" line, the read-it-first rule, and the reply rule. Add the pstack MIT licence notice as `skills/engineering/PSTACK-LICENSE`.
  - Done: `check_principles.spec.py` covers C1 to C3 and passes, `check_principles.py` exits 0 on the repo, and a user can type each `/principle-*` after `/reload-plugins`.
- [x] **2. Skills that run without the router name their principles.** Kind: docs.
  - Name the principles in bold with a sibling path in the skills that apply them alone: `diagnose` and `fix` (fix-root-causes), `tdd` (test-behavior-not-implementation), `code-simplify` (laziness-protocol, minimize-reader-load), `prototype` (exhaust-the-design-space), `build` (prove-it-works, sequence-verifiable-units), `webperf` (explain-the-number).
  - Done: each named skill has one line with the bold principle names and their sibling paths, and each path resolves.
- [x] **3. The TDD skip rule.** Kind: docs.
  - Add a `## When to skip a test` section to `engineering/tdd/SKILL.md`: the three reasons, the closest real check (`/verify` when the repo has a driver), and the skipped plan step `- [-]` with its `Skipped: <reason>` line, which `/sitrep` shows.
  - Done: `tdd/SKILL.md` holds the skip rule, and the plan template's skipped mark matches it.
- [x] **4. The domain docs.** Kind: docs.
  - Add a Principles table to `skills/engineering/README.md`, and a Principles section to `skills/engineering/CLAUDE.md`: the rules for editing a principle, the check script, and the licence file. Add a "Principle" row to `CONTEXT.md`.
  - Done: the README lists 24 principles, `CLAUDE.md` names the check, and `CONTEXT.md` defines a principle.
- [x] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-8.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line. Before the push step, the user ticks the rows to fix in the report and runs its prompt.
- [ ] **7. Push.** Push the branch with `git push -u origin pstack-8_principles-tdd-skip`. Push-only map: open no PR.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-8.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-8.md`: one step per session, from the worktree.
- `/tdd`: step 1.
- `/engineering:mob-review`: the review step.
- `/create-pr`: not in a push-only map.

## Progress

- 2026-11-17: plan written on `pstack-8_principles-tdd-skip`.
- 2026-11-17: judgement calls that the unit does not decide:
  - The scope verdict came from the planner, with no `/scope-ticket` run. The unit is one PR of short skill files.
  - A check script (`check_principles.py`) guards the index against drift from the skill folders (principle-encode-lessons-in-structure).
  - The principle bodies are rewritten in the repo voice. Five pstack bodies are only one or two lines, so their body comes from their description.
  - The pstack MIT notice goes in `skills/engineering/PSTACK-LICENSE`.
  - Step 2 picks seven skills that apply a principle alone. The map names none.
  - The push step pushes and opens no PR, because the map is push-only.
