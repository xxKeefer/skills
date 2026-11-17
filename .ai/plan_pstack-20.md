---
doctype: plan
ticket: none
worktree: /Users/danielkeefer/studio/code/pstack-inspiration
branch: pstack-20_premise-escalation
status: approved
goal: "A third fix attempt starts with a written premise and a higher effort."
spec: .ai/spec_pstack-20.md
---

# Plan: pstack-20 Two failures and model escalation

## Goal

After two failed fixes on one premise, the agent writes the premise down and tests it, and the third attempt runs one effort step up, to a ceiling of `opus` at max effort. Scope: SCOPED, one PR: edits to four skill files and one section file, and one test.

## Spec

`.ai/spec_pstack-20.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Read `diagnose` and `fix` → each cites `principle-attack-the-premise` and `principle-fix-root-causes` by sibling path.
- [x] **B.** Read `build` `STEP.md` and `build` `SKILL.md` → after two failed fixes on one premise, the step writes the premise down, tests it, and returns it, and `build` runs the next attempt one effort step up, to a ceiling of `opus` max, and logs the step through `/update-plan`.
- [x] **C.** Run `install_agents_md.py` against a scratch home → the `models` block holds the effort ladder in rule 1.
- [x] **D.** Fail a fix twice on one premise → the third fix attempt starts with a written premise and a higher effort.

## Context

- Map: `.ai/map_pstack-program.md`, unit 20. Done line: a third fix attempt starts with a written premise and a higher effort.
- Approval: the map (H0).
- Intent and Decisions: see the spec. The ladder lives once, in rule 1 of `skills/utility/skills/install-agents-md/sections/models.md`. Each skill points to "rule 1 of the `models` block in `~/.claude/AGENTS.md`" and does not copy the ladder.
- The ladder: `low`, `medium`, `high`, `xhigh`, `max`. At `max` on a model below `opus`, the next step is `opus` at `max`. The ceiling is `opus` at `max`. With no `models` block, the agent uses the same ladder from the session model and its effort.
- A subagent cannot raise its own effort. `build` raises it when it dispatches the step again. `fix` raises it by a subagent for the third attempt.
- The premise text follows `principle-attack-the-premise`: the one sentence that every failed fix assumed, and the observation that tests it.
- Model: each subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. The change is skill text and one section file. It takes effect when the user reloads the plugin and runs `/install-agents-md`.
- Push-only map: this run uses no `gh` command on this repo. The push step runs `git push -u origin pstack-20_premise-escalation`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | `diagnose` and `fix` cite both principles | L | skill text, one line each |
| B | `build` escalates a step after two failures | M | skill text across two files that must agree; a loop with no ceiling would never stop |
| C | the `models` block holds the ladder | L | section text; the installer has tests |
| D | the end-to-end flow | M | joins B and C |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | C | the real `models` section renders the ladder, `low` to `max`, and the `opus` ceiling into the block | EP | Unit | `install_agents_md.spec.py` |
| C2 | D | a trace of `STEP.md` and `build` `SKILL.md` for a gate that stays red: attempt 1 and 2 at `sonnet` medium, a `B` entry with a premise, attempt 3 at `sonnet` high; and at `opus` max, the `B` entry stands | State transition | Manual | a read trace in step 4 |

### Not testing

- A and B: skill text. The review step reads each against its AC.
- A live `/build` run with a gate that fails twice: expensive, and the failure must be staged. C2 traces the text in its place.

## Steps

- [x] **1. The ladder in the `models` block.** Seam: `install-agents-md/sections/models.md`. Conditions: C1. Add a test to `install_agents_md.spec.py` that renders the real `models` section and finds the ladder, and see it fail. Then rewrite rule 1: after two failed fixes on one premise, write the premise down and test it, then move the next attempt one effort step up. Give the ladder `low`, `medium`, `high`, `xhigh`, `max`; at `max` on a model below `opus`, the next step is `opus` at `max`; the ceiling is `opus` at `max`. Record each step in the decision log.
  - Done: `install_agents_md.spec.py` passes, C1. AC C holds.
- [x] **2. `diagnose` and `fix` cite both principles.** Kind: docs. Change the `Principle:` line of each to a `Principles:` line that names **principle-attack-the-premise** and **principle-fix-root-causes**, each with its sibling path, in the form of `build/SKILL.md`. In `fix` Step 3, add: after two failed fixes on one premise, write the premise down and test it, as `principle-attack-the-premise` says. Then run the third attempt in a subagent one effort step up, by rule 1 of the `models` block, and record the step with `/update-plan` when a plan exists. In `diagnose` Step 3, add: when two hypotheses that share one premise fail, write the premise down and test it before the next.
  - Done: AC A holds on a read, and `check_principles.py` exits 0.
- [x] **3. Escalation in `build`.** Kind: docs. In `build/STEP.md` section 3, replace "After 3 fix attempts" with: after two fix attempts on one premise leave a gate red, write the premise down and test it, as `principle-attack-the-premise` says, then save the work, write a `B` entry, and return. Add `- Premise: <the sentence>, tested by <observation>: <result>` and `- Effort: <model> <effort>` to the `B` format, and change `Tried` to two attempts. In `build/SKILL.md` Step 2, add one item after the check: when a step returns a `B` entry below the ceiling, dispatch the step again one effort step up, by rule 1 of the `models` block, with the `B` entry as its start. Record the step with `/update-plan` as a choice, then delete the `B` entry. At the ceiling, the `B` entry stands. Keep the `D` and `N` formats as they are.
  - Done: AC B holds on a read. `STEP.md` and `SKILL.md` agree on the `B` format.
- [x] **4. End-to-end trace.** Kind: config. Conditions: C2. Trace a gate that stays red through `STEP.md` and `build/SKILL.md` at `sonnet` medium, and write each attempt, its effort, and the premise line in this Done line. Then trace the same at `opus` max, and confirm the `B` entry stands.
  - Decision (agent, 2026-11-18): D1 answered B. `build/SKILL.md` Step 2 item 8 writes the resume patch and the premise into the plan, deletes the `B` entry, then dispatches again one effort step up from the effort the parent gave, with the premise in the prompt.
  - Done: AC D holds on a read trace of `STEP.md` section 3, the `B` format, and `build/SKILL.md` Step 2 items 3, 5, and 8.
    - At `sonnet` medium, attempt 1 fixes the gate, and it stays red. Attempt 2 fixes again on the same premise, and the gate stays red.
    - `STEP.md` section 3 then says: write the premise down, test it, save the work, write a `B` entry, and return.
    - The `B` entry holds `Premise: <the sentence>, tested by <observation>: <result>`, `Tried` with two attempts, `Effort: sonnet medium`, and the patch on `Work`.
    - Item 5 passes, because the plan holds the entry. Item 8 is below the ceiling. It writes the resume line and the premise under the step, logs `sonnet` high as a choice, deletes the `B` entry, and dispatches the step again at `sonnet` high with the premise in the prompt.
    - `STEP.md` section 1 item 2 applies the patch. Attempt 3 at `sonnet` high starts with the written premise.
    - Later `B` entries climb to `xhigh`, `max`, then `opus` max.
    - At `opus` max, attempts 1 and 2 fail on one premise, and the step returns a `B` entry with the premise. Item 8 is at the ceiling, so the `B` entry stands, the step is blocked by it, and the run goes on. No gap found.
- [x] **5. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at 2f16b0b. Both hook tests print only `ok` lines, `install_agents_md.spec.py` prints OK, and `check_principles.py` exits 0.
- [x] **6. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-20.md`. This step changes no code.
  - Done: `.ai/review_pstack-20_premise-escalation.html` run 1, base ad1a0e3, head 26365e1 (panel read 6caa33e). Light run: test-quality and comments clean, plus `persona-skills`. One nit, fixed in 26365e1. None open. The fix changes only skill text, so no new round.
- [x] **8. Review fix br.1.** `squash-bugs` still makes 3 fix attempts with no premise and no move up at `skills/engineering/skills/squash-bugs/BUG.md:50`. Source: the `/blast-radius` confirmed risk in Progress. Kind: docs.
  - Done: In `BUG.md` section 4, after 2 fix attempts on one premise leave a gate red, write the premise down and test it, as `principle-attack-the-premise` says, and the verdict is `blocked`. In section 6, the `blocked` Fix holds the red gate, its first output lines, the premise and its test result, the 2 attempts, and the effort. In `squash-bugs/SKILL.md` Step 3, a `blocked` return below the ceiling of rule 1 of the `models` block runs the subagent again in the same worktree, one effort step up, with the hunt doc path. At the ceiling, or with no `models` block, the ticket stays `blocked`. The `/blast-radius` proof in Progress exits 0.
- [x] **7. Push.** Push-only map: run `git push -u origin pstack-20_premise-escalation`, in place of `/create-pr`.
  - Done: pushed head 56f0567 to `origin/pstack-20_premise-escalation`. Ship: go.

## Suggested skills

- `/build @.ai/plan_pstack-20.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-20.md`: one step per session, from the worktree.
- `/tdd`: step 1.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-18: plan written on `pstack-20_premise-escalation`.
- 2026-11-18: step 1 done. The `models` rule 1 holds the ladder and the premise rule.
- 2026-11-18: step 2 done. `diagnose` and `fix` cite both principles. Commit 568af6f.
- 2026-11-18: step 3 done. `STEP.md` and `build/SKILL.md` agree on the `B` format and the escalation.
- 2026-11-18: step 4 done. The trace of `STEP.md` and `build/SKILL.md` found no gap. AC D holds.
- Decision log: decisions_pstack-20.tsv

- 2026-11-18: step 5 done. The gates are green.
- 2026-11-18: step 6 done. One review nit fixed in 26365e1. The loop stops (build 7.3).
- 2026-11-18: step 8 done. `squash-bugs` holds the premise rule and the move up one effort step. The proof exits 0 and the gates are green. Commit 8bde0d8.
- 2026-11-18: `/blast-radius`: verdict `risk`.
  - Safety fact: a `B` entry in the new format still counts as one open entry for `check_plan.py`, the installer renders the new rule 1 (the premise, the ladder, the `opus` max ceiling) into `AGENTS.md`, and no skill keeps the old 3-attempt rule. Rung 4: the proof below. Its first two checks pass. The third check fails on `squash-bugs/BUG.md:50`.
  - Confirmed risk br.1: `skills/engineering/skills/squash-bugs/BUG.md:50` keeps "After 3 fix attempts that leave a gate red", with no premise and no move up. Chance: high on any bug that resists two fixes. Cost: medium. The bug comes back `blocked` with no premise, and `squash-bugs` never tries one effort step up. Clear fix: step 8.
  - Cleared: `check_plan.py` matches only the `### B<n>` heading (`ENTRY` at line 24), so the new `Premise` and `Effort` lines do not break the count. `sitrep` lists the `B` entries by heading. `build` items 7.1 and 7.3 keep their numbers, because the new item is 8. The `Effort` values match the `effort` values that a subagent call takes: `low`, `medium`, `high`, `xhigh`, `max`.
  - Correction: the Context line "With no `models` block, the agent uses the same ladder" no longer holds. Since 26365e1, with no `models` block, the `B` entry stands and `fix` stops.
  - Proof, from the repo root:

    ```sh
    set -e
    R=$(git rev-parse --show-toplevel)
    T=$(mktemp -d)
    sed -n '/^---$/,/^## Pending Decisions/p' "$R/.ai/plan_pstack-20.md" > "$T/plan_x.md"
    cat >> "$T/plan_x.md" <<'P'

    ### B1: step 3, tests stay red
    - Failure: 1 failed
    - Premise: the cache key holds the user id, tested by a print of the key: false
    - Tried: clear the cache, rebuild the key
    - Effort: sonnet medium
    - Work: none
    - Blocks: 3, 5

    ## Follow-ups
    P
    out=$(python3 "$R/skills/primitives/skills/write-to-file/scripts/check_plan.py" "$T/plan_x.md")
    echo "$out" | tail -1
    [ "$(echo "$out" | tail -1)" = "open decisions: 1" ] || { echo "B ENTRY NOT COUNTED"; exit 1; }
    mkdir -p "$T/home/.claude"
    HOME="$T/home" python3 "$R/skills/utility/skills/install-agents-md/scripts/install_agents_md.py" >/dev/null 2>&1 || true
    f="$T/home/.claude/AGENTS.md"
    [ -f "$f" ] || { echo "NO AGENTS.md WRITTEN"; exit 1; }
    for w in 'write the premise down and test it' '`low`, `medium`, `high`, `xhigh`, `max`' 'The ceiling is `opus` at `max`'; do
      tr '\n' ' ' < "$f" | tr -s ' ' | grep -qF -- "$w" || { echo "MISSING: $w"; exit 1; }
    done
    grep -rn 'After 3 fix attempts' "$R/skills" && { echo "OLD RULE LEFT"; exit 1; }
    echo PASS
    ```
- 2026-11-18: `/blast-radius` again after step 8: verdict `clear`. The proof above exits 0 and prints PASS at 79b27b4. No `/interrogate` run: no confirmed risk is left, and the safety fact is at rung 4. Step 8 changes only skill text, so no new review round.
- 2026-11-18: `/ship`: go. Pushed 56f0567. Unit 20 ticked on the map. Next: the home machine opens the PR into `pstack-inspired`, reviews it, and merges it.

## Pending Decisions

## Follow-ups
