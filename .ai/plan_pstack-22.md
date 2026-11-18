---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-22_loop-until
status: approved
goal: "A loop on a small metric stops at the predicate, with one log row per try."
spec: .ai/spec_pstack-22.md
builds_on: pstack-21
---

# Plan: pstack-22 `loop-until`

## Goal

A new `engineering/loop-until` improves one measured number to a stated predicate: one change, one measure, keep or revert, with one decision log row per try. Scope: SCOPED, one PR: one new skill with no script, and a row in the engineering `README.md`.

## Spec

`.ai/spec_pstack-22.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `engineering/loop-until` → before any change, it names a repro case, one metric, the direction that is better, and a predicate with a target and a floor on tries.
- [x] **B.** Read `engineering/loop-until` → it proves that the harness separates a contrast case from the target case, records the baseline and a green gate, then freezes the harness.
- [x] **C.** Read `engineering/loop-until` → each try makes one change and measures it with the frozen harness. It keeps the change as one commit only past noise with the gate green, else reverts in full. Each try logs one row either way.
- [x] **D.** Read `engineering/loop-until` → a run of rejected tries makes it change approach, it stops only on the predicate or a surfaced dead end, and it never relaxes the predicate.
- [x] **E.** Run `loop-until` on a small metric → it stops at the predicate, with one log row per try.

## Context

- Map: `.ai/map_pstack-program.md`, unit 22. Done line: a loop on a small metric stops at the predicate, with one log row per try.
- Approval: the map (H0).
- Stack: this branch starts from `pstack-21_eval-skill`, because the unit 20 and unit 21 PRs are not merged. The home machine sets the unit 22 PR base to that branch. Keep the unit 20 and unit 21 `.ai/` files.
- Intent and Decisions: see the spec. Source: pstack `skills/poteto-mode/playbooks/hillclimb.md` and `autonomous-run.md`. Credit them in one line of prose in the skill.
- The decision log is the existing one. The skill gives each try to `/update-plan` as a choice: `decision` is the try number and the change, `reason` is the mechanism that the hypothesis names, `evidence` is the metric before and after and the gate result, and `result` is `kept <sha>` or `reverted`. It names no script path, so it needs no `$SKILL_DIR`.
- Not `/webperf`: `/webperf` fixes one page bottleneck with the user's yes on each fix. `loop-until` runs many tries to a predicate with no stop between tries. Name the difference in one line of the skill.
- Each try runs in a fresh subagent at the `worker` role. The main thread measures, and keeps or reverts.
- Principles to cite in the skill, by sibling path: `principle-prove-it-works`, `principle-build-the-lever`, `principle-sequence-verifiable-units`, `principle-explain-the-number`.
- Model: each build subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. A new skill loads at the next session start.
- Push-only map: the push step runs `git push -u origin pstack-22_loop-until`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the skill frames the metric and predicate first | L | skill text |
| B | the skill proves the harness before it freezes it | M | skill text; a harness that cannot fail makes every kept try a false win |
| C | each try is one change, kept or reverted, with one log row | M | skill text that commits and reverts code in the user's tree |
| D | a plateau changes approach, and the predicate never moves | L | skill text |
| E | the end-to-end loop stops at the predicate | M | joins A to D with live agents and git |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | E | a live loop on a scratch git repo with a slow function stops when the predicate holds, with one log row per try | EP | Manual | the live run in step 2 |
| C2 | B | in the live run, the harness gives a different number for the contrast case and the target case | EP | Manual | the live run in step 2 |

### Not testing

- A, C, and D: skill text. The review step reads each against its AC. The live run in step 2 also exercises C.

## Steps

- [x] **1. The `loop-until` skill.** Kind: docs. Read `skills/meta/skills/writing-great-skills/SKILL.md` and `skills/meta/skills/write-a-skill/SKILL.md` first. Write `skills/engineering/skills/loop-until/SKILL.md`, model-invoked, with no ★. Steps, each with a done line: 1. Frame: the repro case, one metric, the better direction, the predicate (a target and a floor on tries), and the regression gate. With no plan, write one with `/write-to-file`, doctype `plan`, and put the frame in its Context. 2. Prove and freeze the harness: one command that prints the metric as the median of N runs; show that it separates a contrast case from the target case; record the baseline and a green gate; then change the harness no more. 3. Loop, one hypothesis per try: name the mechanism; one fresh subagent at the `worker` role makes the change; measure with the frozen harness and run the gate; keep only past noise with the gate green, as one commit that stages only the changed files; else revert in full; give the try to `/update-plan` as a choice either way. 4. Plateau: after three rejected tries in a row, change the kind of change. 5. Stop: when the predicate holds; or report a dead end as a `D` entry. Never relax the predicate. 6. Report: the metric and predicate, baseline to final, the tries kept and reverted, each kept commit, and the next idea. Credit pstack in one line. Add a row to `skills/engineering/README.md`.
  - Done: AC A, B, C, and D hold on a read, and the pre-commit test passes.
- [x] **2. Live run.** Kind: config. Conditions: C1, C2. Make a scratch git repo in a temp folder with one slow function, a test file as the gate, and a harness that prints the median runtime of five runs. Run `/loop-until` on it from this thread, with a predicate such as "at most half the baseline, after at least three tries". The scratch repo takes the plan and the decision log of the loop, so this plan's log gets no try rows. Copy the loop's log rows and the final numbers into this Done line. Delete the scratch repo.
  - Done: AC E holds. The loop on `count_primes(4000)` stopped at the predicate (at most 16.7 ms, at least three tries) after three tries, with three log rows: try 1, isqrt bound, 33.5 to 1.8 ms, kept; try 2, a counter in place of a list, 1.8 to 1.8 ms inside the noise, kept as a simplification; try 3, a plain loop in place of `all()`, 1.8 to 1.0 ms, kept. Final: 1.0 ms, 97% faster than the baseline. The contrast case gave 0.3 ms against 33.1 ms (C2). No try was reverted, so the revert path did not run. The scratch repo is deleted.
- [x] **2a. Live-run fix: noise and the plan check.** Kind: docs. In `loop-until/SKILL.md`, Step 3: after each kept try, measure the noise again at the new level, and judge the next try against it. Step 1: the loop step of a new plan names `Seam:` (the code under the metric) and `Conditions:` (an ID for the gate), so that the plan check passes.
  - Done: both lines are in the skill, and the pre-commit test passes.
- [x] **3. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green. The pre-commit test, the commit-msg test, and `check_principles.py` each exit 0.
- [x] **4. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-22.md`. This step changes no code.
  - Done: the report path and the reviewed base and head SHAs are in this line. Report: `.ai/review_pstack-22_loop-until.html`, base 51455c7, reviewed head cf0adc2 (panel read 73a54a7). One nit fixed in cf0adc2, none open.
- [ ] **5. Push.** Push-only map: run `git push -u origin pstack-22_loop-until`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-22.md`: every step, then the test and review loop, from the worktree.
- `/engineering:light-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-22_loop-until`.
- 2026-11-18: playbook `map`, step 3: five choices logged. Next: step 4, branch and `/build`.
- 2026-11-18: step 1 done: `loop-until` skill and README row written (e801432).
- 2026-11-18: step 4 done: light review, one nit fixed (cf0adc2), none open.
- Decision log: decisions_pstack-22.tsv
- 2026-11-18: step 2 done: live run of `/loop-until` in a scratch repo, driven from this thread, with each try in a `sonnet` subagent. Two gaps found in the skill text: the noise is recorded once, but after a big kept try it must be measured again at the new level; and the loop plan fails the plan check until its step names `Seam:` and `Conditions:`. Step 2a fixes both.
- 2026-11-18: step 2a done: `loop-until` re-measures the noise after each kept try, and the loop step names `Seam:` and `Conditions:`.
- 2026-11-18: `/blast-radius`: verdict `clear`. Safety fact: outside `.ai/` and the new skill folder, the branch adds one line (`skills/engineering/README.md:62`) and deletes none; `loop-until` is the only skill of that name; each relative link in the skill resolves. Rung 4. No confirmed risk. Cleared: no script parses the engineering `README.md`; `plugin.json` lists no skills; no other skill calls `loop-until`. Not proven: the revert path of Step 3, because no live try was reverted. Proof, from the repo root on this branch:
  ```
  python3 - <<'PY'
  import os, re, subprocess, sys
  num = subprocess.run(["git","diff","--numstat","51455c7","HEAD","--",".",":!.ai",":!skills/engineering/skills/loop-until"],capture_output=True,text=True).stdout.split("\n")
  bad = [l for l in num if l and l.split("\t")[1] != "0"]
  names = [n for d in os.listdir("skills") if os.path.isdir(f"skills/{d}/skills") for n in os.listdir(f"skills/{d}/skills")]
  s = "skills/engineering/skills/loop-until/SKILL.md"
  bad += [l for l in re.findall(r"\]\((\.\./[^)#]+)", open(s).read()) if not os.path.exists(os.path.join(os.path.dirname(s), l))]
  bad += [] if names.count("loop-until") == 1 else ["name clash"]
  print(bad or "ok"); sys.exit(1 if bad else 0)
  PY
  ```
