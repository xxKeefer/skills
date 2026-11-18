---
doctype: spec
ticket: none
status: confirmed
goal: "A third fix attempt starts with a written premise and a higher effort."
---

# Spec: Two failures and model escalation

## Intent

- Outcome: when two fixes that share one premise fail, the agent writes the premise down and tests it before a third fix. The third attempt runs one effort step up, to a ceiling of `opus` at max effort. The decision log records each step.
- User: the user, who reads the decision log after a run, and the agent, which today makes three attempts at one effort and then gives up.
- Why now: map unit 20 (r1.13). The `models` block already holds the rule, but no skill applies it. `build` `STEP.md` makes three attempts at one effort, and `diagnose` and `fix` cite only `principle-fix-root-causes`.
- Success: `diagnose` and `fix` cite both principles; a step that fails twice on one premise returns a written, tested premise; the next attempt runs one effort step up, and the log records the step.
- Constraint: the ladder lives once, in the `models` section of `install-agents-md`. Skills point to it and do not copy it. Add no script and no new skill.
- Out of scope: a change to the review loop's round count, a new role in the `models` table, and a change to `fable`.

## Decisions

- Models rule 1, from the map Models decision: after two failed fixes on one premise, the next attempt moves one effort step up, to a ceiling of `opus` at max effort. The decision log records each step.
- A subagent cannot raise its own effort, so the parent raises it. A build step that fails twice on one premise writes the premise, tests it, saves the work, and returns a `B` entry with the premise and the test result. `build` dispatches the step again, one effort step up, until the ceiling. At the ceiling, the `B` entry stands.
- The ladder: `low`, `medium`, `high`, `xhigh`, `max`. At `max` on a model below `opus`, the next step is `opus` at `max`. It lives in rule 1 of the `models` section.
- `fix` runs in the user's session. After two failed fixes on one premise, it writes and tests the premise, then runs the third attempt in a subagent one effort step up.

## Acceptance criteria

- [ ] **A.** Read `diagnose` and `fix` → each cites `principle-attack-the-premise` and `principle-fix-root-causes` by sibling path.
- [ ] **B.** Read `build` `STEP.md` and `build` `SKILL.md` → after two failed fixes on one premise, the step writes the premise down, tests it, and returns it, and `build` runs the next attempt one effort step up, to a ceiling of `opus` max, and logs the step through `/update-plan`.
- [ ] **C.** Run `install_agents_md.py` against a scratch home → the `models` block holds the effort ladder in rule 1.
- [ ] **D.** Fail a fix twice on one premise → the third fix attempt starts with a written premise and a higher effort.
