---
doctype: spec
ticket: none
status: confirmed
goal: "One run compares two versions of a skill and reports a winner or \"no difference\"."
---

# Spec: `eval-skill`

## Intent

- Outcome: a new `meta/eval-skill` runs a blind A/B test of a skill change. Candidates get one neutral prompt that a user could type, in folders with no eval words. One blind judge scores both outputs on one scale. The skill reports a winner or "no difference".
- User: the user, who changes a skill that `/work-on` calls and today has no test that the change helps.
- Why now: map unit 21 (r1.23). The skill maturity moves are manual, with no test.
- Success: one run on two versions of a skill names a winner or "no difference", with the rubric, the judge's scores, and the agent's own read of each output.
- Constraint: adapt pstack's eval playbook. Credit it in one line of prose. Everything-agnostic: no language, framework, or tool beyond the agent and git.
- Out of scope: a required eval gate, a model arena across model families, and transcript mining.

## Decisions

- Source: pstack `poteto-mode/playbooks/eval.md`. Keep its blinding rules, its frame step, its one judge on one scale, and its "read every output yourself" step. Drop the model arena and the transcript reads.
- Two versions: version A and version B of one skill, each a git ref or the working tree. Default A: the last commit that changed the skill before the edit. Default B: the working tree.
- Candidates: two runs of each version, on the same model, so the model is not a variable. Each runs in its own folder with a project-shaped name, with its version of the skill planted where the project's skills live.
- The judge: one fresh subagent on a different model from the candidates. It sees the outputs under neutral labels, never which version made them, and scores all four outputs in one pass on one scale against a rubric of 3 to 6 criteria.
- Verdict: a winner when both runs of one version beat both runs of the other on the judge's total. Else "no difference".
- `/retro` offers `/eval-skill` in its summary for each applied row that edits a skill that a `work-on` playbook calls. Never a required step.
- Model-invoked, so `/retro` can offer it and the user can type it.

## Acceptance criteria

- [ ] **A.** Read `meta/eval-skill` → it frames the change with a rubric that only the judge sees, sets up folders and one prompt with no eval words, runs two candidates for each version, and has one blind judge score all outputs in one pass.
- [ ] **B.** Read `/retro` → its summary offers `/eval-skill` for each applied row that edits a skill that a `work-on` playbook calls, and never requires it.
- [ ] **C.** Run the leak check of `eval-skill` on a folder and a prompt that hold an eval word → it names the word and the path. On clean names → it prints nothing.
- [ ] **D.** Run `eval-skill` on two versions of a skill → it reports a winner or "no difference".
