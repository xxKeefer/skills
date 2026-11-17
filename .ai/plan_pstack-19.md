---
doctype: plan
ticket: none
worktree: /home/xxkeefer/studio/code/skills
branch: pstack-19_no-comments
status: approved
goal: "A branch with an added comment gets a finding with the replacement, and a hack gets a step or a follow-up."
spec: .ai/spec_pstack-19.md
---

# Plan: pstack-19 No comments

## Goal

On the user's own branch, `persona-comments` turns each added comment into a finding with a ladder replacement, and a hack comment ends as a plan step or a Follow-up. Scope: SCOPED, one PR: one new script with its test, and edits to five skill files and one section file.

## Spec

`.ai/spec_pstack-19.md`. This plan builds all of it.

## Acceptance criteria

- [x] **A.** Run `scripts/added_comments.py` on a diff that adds a comment in a `#` language, a `//` language, and a block comment → it prints one `<file>:<line>: <text>` line for each added comment line, and none for removed lines, context lines, or a string that holds `#` or `//`.
- [x] **B.** Read `persona-comments` on the user's own branch → each added comment is a finding whose `suggestion` names a ladder rung and the replacement, except the two exceptions; the other-PR rules are not in `SKILL.md`.
- [x] **C.** Read `persona-comments` on another person's PR → it reads the reference file and applies the current rules unchanged.
- [x] **D.** Read `mob-review` `FIX.md` → a hack finding runs `/blast-radius` on the architectural fix, and becomes a new plan step when small and in scope, else a `Follow-ups` entry.
- [x] **E.** Read `create-pr` → the PR body lists the plan's Follow-ups, and removes the section when there are none.
- [x] **F.** Run `install_agents_md.py` against a scratch home → the `coding` block holds "No comments. Two exceptions: tool directives and comments that lint requires."
- [x] **G.** Review a branch with an added comment → it gets a finding with the replacement, and a hack gets a step or a follow-up.

## Context

- Map: `.ai/map_pstack-program.md`, unit 19. Done line: a branch with an added comment gets a finding with the replacement, and a hack gets a step or a follow-up.
- Approval: the map (H0).
- Focus: `principle-subtract-before-you-add`, by the user's request. Step 1 removes before any step adds. Move the other-PR rules out of `persona-comments/SKILL.md`; do not copy them. Do not add a guard, an option, or a language that the spec does not need. Keep the three existing reference files as they are.
- Intent and Decisions: see the spec. The comment ladder: 1. a better name, 2. a type, 3. a test whose title states the fact, 4. a check that fails with the fix in its error, 5. delete it. It lives once, in `persona-comments`.
- The lens: `mob-review` Step 1 already decides own code (every commit by the current git user) or someone else's code. The persona takes that answer from its brief. When the brief gives none, it uses the other-PR lens, as `mob-review` says "when in doubt".
- Model: each subagent runs at `sonnet`, by the map's `subagent_model`.
- Production gate: none. The change is skill text and one script. It takes effect when the user reloads the plugin and runs `/install-agents-md`.
- Push-only map: this run uses no `gh` command on this repo. The push step runs `git push -u origin pstack-19_no-comments`.
- Commit convention: conventional commits with the domain as scope. No Claude attribution line. Change no `plugin.json` version.
- Gates: `sh .githooks/pre-commit_test.sh`, `sh .githooks/commit-msg_test.sh`, `python3 skills/engineering/skills/persona-comments/scripts/added_comments.spec.py`, `python3 skills/utility/skills/install-agents-md/scripts/install_agents_md.spec.py`, and `python3 skills/engineering/skills/work-on/scripts/check_principles.py .`.

## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | the script lists added comment lines | M | new code with many branches: comment syntax by extension, strings, diff parsing |
| B | own-branch lens finds each comment | M | skill text; a wrong lens fixes another person's code |
| C | other-PR lens keeps the rules | L | text moves, no rule changes |
| D | a hack becomes a step or a Follow-up | L | skill text |
| E | the PR body lists Follow-ups | L | skill text |
| F | the coding block holds the rule | L | section text; the installer has tests |
| G | the end-to-end flow | M | joins A, B, and D |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | an added `#` comment in `.py` and `.sh`, a `//` comment in `.ts`, and a `/* */` block over lines are each listed, with the new-file line number | EP | Unit | `added_comments.spec.py` |
| C2 | A | removed lines, context lines, and an unknown extension give no output | EP | Unit | `added_comments.spec.py` |
| C3 | A | a `#` or `//` inside a string, such as a URL, is not listed; a trailing comment after code is listed | EP | Unit | `added_comments.spec.py` |
| C4 | A | a diff with no added comment exits 0 with no output | BVA | Unit | `added_comments.spec.py` |
| C5 | F | the real `coding` section renders the rule into the block | EP | Unit | `install_agents_md.spec.py` |
| C6 | G | the script, run on a scratch branch that adds a comment, lists it; the persona text maps it to a rung | EP | Manual | a scratch run in step 6 |

### Not testing

- B, C, D, E: skill text. The review step reads each against its AC.
- A full `mob-review` run on a scratch branch: expensive. C6 runs the script and reads the persona in its place.

## Steps

- [x] **1. Subtract: move the other-PR rules out of `persona-comments`.** Kind: mechanical. Create `skills/engineering/skills/persona-comments/references/other-pr.md`. Move into it, word for word, the sections `## What you review` (rules 1 to 10 and 18, with the two pointers to the reference files and the orphan-comment line), `## Severity`, and the e2e JSDoc exception from `## Out of lane`. Fix each relative link so it still resolves. Delete the moved text from `SKILL.md`. Keep the persona contract line, the title, `## Output`, and the group-by-root-cause rule in `SKILL.md`.
  - Done: `SKILL.md` holds no numbered rule; `references/other-pr.md` holds each moved rule word for word; each link resolves. AC C holds on a read.
- [x] **2. `added_comments.py`, test first.** Seam: `persona-comments/scripts/added_comments.py`, which reads a unified diff on stdin or from a path argument. Conditions: C1, C2, C3, C4. Write `added_comments.spec.py` first, in the style of `install_agents_md.spec.py`, and see it fail. Then write the script: track the new-file line number from each `@@` hunk header; for each added line, find a comment start by the file extension (`#` for `py sh bash zsh nix yaml yml toml rb pl r`; `//` and `/* */` for `ts tsx js jsx mjs cjs vue java kt go rs c h cpp cs swift scala php css scss`; `<!-- -->` for `vue html`; `--` for `sql lua hs`), skip a start inside a string quote, and track an open block comment across lines. Print `<file>:<line>: <text>`. Skip a `#!` line on line 1. Add no other filter.
  - Done: `added_comments.spec.py` passes, C1 to C4. AC A holds.
- [x] **3. Add the two lenses to `persona-comments`.** Kind: docs. In `SKILL.md`: a short `description` that names the two lenses. `$SKILL_DIR` is this skill's base directory. `## Guard`: run `python3 "$SKILL_DIR/scripts/added_comments.py"` on the diff; with no line out, return zero findings. This replaces the frontend-only guard and `## Scope`. `## Lens`: take own code or someone else's code from the brief; with none, use someone else's. **Own code:** each listed line is one finding, except a tool directive whose reason a check enforces and a comment that the repo's lint requires. Write the ladder once (name, type, test title, check, delete); the `suggestion` names the highest rung that works and the replacement. When the comment marks a hack (a workaround, a TODO, a quirk), start the `summary` with `hack:` and name the architectural fix in `detail`. Group by root cause as before. **Someone else's code:** read `references/other-pr.md`, and follow it. Keep `## Out of lane` for naming and structure. In `skills/engineering/skills/mob-review/PANEL.md`, change the `persona-comments` trigger to: an added comment line that `scripts/added_comments.py` lists.
  - Done: AC B and C hold on a read, and the pre-commit `$SKILL_DIR` check passes.
- [x] **4. The hack flow and the PR notes.** Kind: docs. In `skills/engineering/skills/mob-review/FIX.md`: one item for a finding whose `summary` starts `hack:`. Apply its rung now. Then run `/blast-radius` on the architectural fix in `detail`. When the fix is small and inside the change's scope, add it as a new plan step; else add a `Follow-ups` entry with `/update-plan`. No stop. In `skills/engineering/skills/create-pr/SKILL.md` Step 4 and `templates/body.md`: a `## Follow-ups` section that lists the plan's Follow-ups, removed when there are none.
  - Done: AC D and E hold on a read.
- [x] **5. The `coding` block.** Seam: `install-agents-md/sections/coding.md`. Conditions: C5. Add a test to `install_agents_md.spec.py` that renders the real `coding` section and finds the rule, and see it fail. Then add to `coding.md` a `## Comments` section: "No comments. Two exceptions: tool directives and comments that lint requires." Add a `lists:` header line for the old wording that it repeats, such as "comments sparingly", if the `lists` match works on a substring; read the script to check.
  - Done: `install_agents_md.spec.py` passes, C5. AC F holds.
- [x] **6. End-to-end check.** Kind: config. Conditions: C6. On a scratch git repo in `/tmp`, commit a file, then add a `.py` file with a plain comment and a `# HACK:` comment on a branch. Run `added_comments.py` on `git diff main...HEAD`, and confirm two lines. Read `persona-comments` and `FIX.md` for each line, and write in this Done line the rung and the outcome (plan step or Follow-up). Delete the scratch repo.
  - Done: AC G holds. Scratch run printed `b.py:2: # this sets the retry count` and `b.py:4: # HACK: sleep because the api races`. Line 2: ladder rung 1 (a better name, such as `retry_count`), else rung 5 (delete); a finding, not a hack, so no plan step and no Follow-up. Line 4: a `hack:` finding with rung 4 (a check that fails with the fix in its error) applied now; FIX.md item 6 then runs `/blast-radius` and gives a plan step when the architectural fix (remove the race at the api) is small and in scope, else a Follow-ups entry. The text does not say which case a given hack falls in beyond "small and inside the change's scope"; the outcome is set at run time.
- [x] **7. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at 17ab3c9. Both hook tests print only `ok` lines, `added_comments.spec.py` and `install_agents_md.spec.py` print OK, and `check_principles.py` exits 0.
- [x] **8. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-19.md`. This step changes no code.
  - Done: `.ai/review_pstack-19_no-comments.html`, base b86fe6d, head 4f0fd8f (panel read cbd39c4). Light run, plus `persona-skills`. 10 of 12 findings fixed in 4f0fd8f. Two nits stay open, each with a reason. The fix changes the script's behaviour, so round 2 follows.
- [ ] **9. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green.
- [ ] **10. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-19.md`. This step changes no code. Rows that stay open from run 1: the `comments` generator split and the `lists:` line. Do not raise them again, and do not raise a row that only repeats them.
  - Done: the report path and the reviewed base and head SHAs are in this line.
- [ ] **11. Push.** Push-only map: run `git push -u origin pstack-19_no-comments`, in place of `/create-pr`.
  - Done: the pushed head SHA is in this line.

## Suggested skills

- `/build @.ai/plan_pstack-19.md`: every step, then the test and review loop, from the worktree.
- `/implement @.ai/plan_pstack-19.md`: one step per session, from the worktree.
- `/tdd`: steps 2 and 5.
- `/engineering:mob-review`: the review step.

## Progress

- 2026-11-17: plan written on `pstack-19_no-comments`.
- 2026-11-17: step 2 done in 45c8571. Script and 14 tests added; AC A holds.
- 2026-11-17: step 3 done in b224d5d. `persona-comments` has the Guard, Lens, and ladder; `PANEL.md` trigger changed; AC B and C hold.
- 2026-11-17: step 4 done in 6e58afc. `FIX.md` item 6 handles `hack:` findings; `create-pr` and its body template list Follow-ups; AC D and E hold.
- 2026-11-17: step 5 done in b7e820e. `coding.md` has a `## Comments` section and two `lists:` lines; 28 tests pass; AC F holds.
- 2026-11-17: step 6 done. Scratch run listed both comments; each maps to a rung and an outcome. AC G holds.
- Decision log: decisions_pstack-19.tsv

## Pending Decisions

## Follow-ups
