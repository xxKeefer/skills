---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-28_unslop
status: approved
goal: "`proof-read` flags a tell by its ID."
spec: .ai/spec_pstack-28.md
builds_on: pstack-27
---

# Plan: pstack-28 `UNSLOP.md`

## Goal

`skills/scribe/UNSLOP.md` is a numbered catalogue of AI tells, each with a stable ID. `proof-read` cites the catalogue, and names each tell that it flags by its ID. Scope: SCOPED, one PR: one new reference file and its pointers.

## Spec

`.ai/spec_pstack-28.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `scribe/UNSLOP.md` → it is a numbered catalogue of AI tells, each with a stable ID, and `proof-read` cites it.
- [x] **B.** Run `proof-read` on a text that holds a catalogued tell → the finding names the tell by its ID.

## Context

- Map: `.ai/map_pstack-program.md`, unit 28. Done line: `proof-read` flags a tell by its ID.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-27_design-it-twice`, because the unit 20 to 27 PRs are not merged. The home machine sets the unit 28 PR base to that branch. Keep the unit 20 to 27 `.ai/` files.
- Intent: see the spec. Source: pstack `skills/unslop` (research row r1.20). The scribe skills have plain-word rules, but no list of AI vocabulary and tells. Credit pstack `unslop` in one line of prose in `UNSLOP.md`.
- Decisions: the map names none for this unit.
- Out of scope: `grices-maxims`, `asd-ste100`, `orwells-six`, and the output style.
- Where it lands: `UNSLOP.md` sits at the scribe domain root, beside `HARD-RULES.md`, because it is shared reference, not a skill. `proof-read` hunts the tells in Pass 4 (Orwell), because a tell is a word-level or phrase-level fault, and Pass 4 hunts the delta that the earlier lenses leave.
- ID rule: an ID has a group prefix and a number, such as `V3`. An ID never changes and is never reused. A retired tell keeps its row, marked retired.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A skill edit loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-28_unslop`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the catalogue has stable IDs, and `proof-read` cites it | L | skill text |
| B | a `proof-read` finding names a tell by its ID | M | behaviour that an agent must follow. A text read cannot prove it. |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | B | a fresh agent follows `proof-read` Pass 4 on a short text that holds at least three catalogued tells. Each finding for a tell names its ID from `UNSLOP.md` | EP | Manual | the live run in step 2 |

### Not testing

- A: skill text. The review step reads it against its AC.

## Steps

- [x] **1. The catalogue and its cite.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` first. Write `skills/scribe/UNSLOP.md`: a short intro, the ID rule from Context, and tells in groups, each group with a letter prefix (such as vocabulary, stock phrases, structure, and hedging). Each tell has an ID, the tell, one example, and the plain fix. Credit pstack `unslop` in one line of prose. In `skills/scribe/skills/proof-read/SKILL.md`, Pass 4: hunt each tell in `UNSLOP.md`, and name each tell finding by its ID. Add one line to `skills/scribe/CLAUDE.md` under Editing that names `UNSLOP.md`.
  - Seam: `skills/scribe/UNSLOP.md` and `proof-read` Pass 4.
  - Done: AC A holds on a read, and the pre-commit test passes.
- [x] **2. Live run.** Kind: config. Conditions: C1. Give a fresh agent the new `proof-read/SKILL.md`, `HARD-RULES.md`, and `UNSLOP.md`, and a short text that holds at least three catalogued tells. Tell it to run Pass 4 only and return its findings, with no gate. Copy the result in short form into this Done line.
  - Seam: the `proof-read` Pass 4 text, as an agent follows it.
  - Done: AC B holds. A fresh agent ran Pass 4 on a four-sentence text with ten planted tells. It returned ten findings, each with its ID: P2, V6, P1, V2, V4, V7, H5, H1, P4, S2. It asked for the author's fact in place of an invented one (V6, V4, V7), kept "may" by Rule 6, and listed the IDs with no hit.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-28.md`. This step changes no code. Name `/engineering:light-review`.
  - Done: report `.ai/review_pstack-28_unslop.html`, reviewed base 9224398, head 19f88e7 (panel read 04914f6). One open row: the `/orwells-six` standalone lens has no Tells rule. Its fix edits `orwells-six`, which is out of scope. One nit fixed in 19f88e7.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-28_unslop`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-28.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-28.md`: one step per session, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-27_design-it-twice`, for the branch `pstack-28_unslop`.
- Decision log: decisions_pstack-28.tsv
- 2026-11-18: playbook `map`, step 3: four choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done (85bd015): `UNSLOP.md` holds 32 tells in four groups (V, P, S, H); `proof-read` Pass 4 hunts them and names each by ID.
- 2026-11-18: step 2 done: the live run proves AC B. See the step 2 Done line.
- 2026-11-18: step 3 done: the gates each exit 0.
- 2026-11-18: step 4 done: light review ran the `persona-skills` lane. One nit fixed (19f88e7), one row open.
