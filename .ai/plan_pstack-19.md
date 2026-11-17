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
- [x] **9. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at f620eef. `added_comments.spec.py` runs 19 tests, OK.
- [x] **10. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-19.md`. This step changes no code. Rows that stay open from run 1: the `comments` generator split and the `lists:` line. Do not raise them again, and do not raise a row that only repeats them.
  - Done: `.ai/review_pstack-19_no-comments.html` run 2, base b86fe6d, head c5dd0ae (panel read 35c34ca). 5 of 5 findings fixed in c5dd0ae. None open. The fix changes the script's behaviour, so round 3 follows. It is the last round: the third review step stops the loop.
- [x] **11. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at 987ddf7. `added_comments.spec.py` runs 22 tests, OK.
- [x] **12. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-19.md`. This step changes no code. Rows that stay open from run 1: the `comments` generator split and the `lists:` line. Do not raise them again, and do not raise a row that only repeats them.
  - Done: `.ai/review_pstack-19_no-comments.html` run 3, base b86fe6d, head 98c6194 (panel read 499afdb). Two test-design nits, both fixed in 98c6194 with new tests. Four lanes clean. None open. The loop stops at the third review step.
- [x] **13. Review fix r1.1.** A path that git quotes (a non-ASCII name) is skipped at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Decode a C-quoted `+++ "b/..."` path before the extension lookup. Test first with the octal-escaped header. Done in 6589c1d. Two new tests in `added_comments.spec.py`, 26 tests OK.
- [x] **14. Review fix r1.2.** An added line inside a block comment that a context line opened, or that spans a context line, is not listed at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Track the block state on context lines too, and print only added lines. In a `/* */` language, list an added line whose text starts with `*` as a block continuation. Test first: a JSDoc continuation line, and a new block that spans a context line. Done in 1c1d27a. Five `Blocks` tests went red on the old script, then green; 31 tests pass. A C line that starts with `*`, such as `*ptr = 0;`, is listed: the rule fails toward listing.
- [x] **15. Review fix r1.3.** CSS has no line comments, so `url(//...)` is listed at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Give `css` a row with the `/* */` block only. `scss` keeps `//`. Test first. Done in cc9ba4c. Two new tests in `added_comments.spec.py`, 33 tests OK; the `url(//...)` test went red on the old script.
- [x] **16. Review fix r1.4.** A form feed inside an added line shifts each later line number at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Split the diff on `\n` only, not with `splitlines`. Test first with a form feed. Done in 18bfeae. One new test, 34 tests OK; it went red on the old script.
- [x] **17. Review fix r1.5.** A `'"'` char literal hides a trailing comment at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: A `"` with a `'` on each side is a char literal, not a string start. Test first. Done in 9a186be. One new test, 35 tests OK; it went red on the old script.
- [x] **18. Review fix r1.6.** A `#` with no space before it is missed at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Replace the word-start rule: a `#` right after `$` or `{` is not a comment; any other `#` is. Keep the `$#` and `${#arr[@]}` tests. Test first with `f(1)# hack`. Done in 720f410. One new test, 36 tests OK; it went red on the old script. A `#` inside a word, such as `a#b`, is now listed: the rule fails toward listing.
- [x] **19. Review fix r1.8.** Files with no extension, such as `Dockerfile` and `Makefile`, are never scanned at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Look up the file name when it has no extension. Add `Dockerfile` and `Makefile` to the `#` row. Test first. Done in 753dd60. One new test, 37 tests OK; it went red on the old script, and a mutation that removed the two names made it red again.
- [x] **20. Review fix r1.9.** SQL and nix `/* */` block comments are not listed at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Add the `/* */` block to `sql`, and give `nix` a row with `#` and the `/* */` block. Test first. Done in 4ab0ed8. Three new tests, 40 tests OK; two went red on the old script. A `*` line in sql or nix is listed as a block continuation: the rule fails toward listing.
- [x] **21. Review fix r1.10.** A line inside a Python triple-quoted string that starts with `#` is listed at `skills/engineering/skills/persona-comments/scripts/added_comments.py`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: In `py`, treat a `"""` or `'''` string as a block that the script skips and does not print. Test first. Done in f6cb2b2. Seven new tests, 47 tests OK; three went red on the old script, and two mutations went red. A real comment after the closing quotes on the same line is listed. A string that never closes in the hunk is scanned again as code, so its lines are listed: the rule fails toward listing.
- [x] **22. Review fix r1.7.** The build review step runs `light-review`, which leaves out `persona-comments` at `skills/engineering/skills/light-review/SKILL.md`. Report: `.ai/interrogate_pstack-19_no-comments.html`.
  - Done: Add `persona-comments` to the essential lanes, and change "eight" to "nine" in `light-review/SKILL.md` (description and body), `engineering/CLAUDE.md`, `engineering/README.md`, and `mob-review/SKILL.md`. Kind: docs. Done in 4ff945c. Nine lanes in each place; the README lane list now ends with comments. Gates green.
- [x] **23. Review fix br.1.** The `PANEL.md` guard of `persona-comments` asks the orchestrator to run a script, but `mob-review` Step 2 matches guards against `files.txt` only at `skills/engineering/skills/mob-review/PANEL.md:16`. Source: `/blast-radius` in Progress.
  - Done: Make the guard file-based: a changed file whose extension or name the script knows. The persona's own Guard still runs the script. Kind: docs. Source: the `/blast-radius` confirmed risk in Progress. Done in 8fae289. The guard names the file types in `ROWS` of the script; the persona's own Guard still runs the script. Gates green.
- [x] **24. Test.** Run the gates from Context. This step changes no behaviour.
  - Done: the gates are green at 5802b5d. `added_comments.spec.py` runs 47 tests, OK.
- [x] **25. Review.** Depends on every earlier step. Review the branch with this plan: `.ai/plan_pstack-19.md`. This step changes no code. Rows that stay open from run 1: the `comments` generator split and the `lists:` line. Do not raise them again, and do not raise a row that only repeats them.
  - Done: `.ai/review_pstack-19_no-comments.html` run 4, base b86fe6d, head e91e147 (panel read 6dfe6ee). Nine light lanes plus `persona-skills`. 4 of 6 findings fixed in e91e147. Two stay open on D1. `persona-comments` ran with `Lens: own code` and dropped each string line that the script listed.
- [ ] **26. Push.** Push-only map: run `git push -u origin pstack-19_no-comments`, in place of `/create-pr`.
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
- 2026-11-17: step 13 done in 6589c1d. `added_comments.py` decodes a C-quoted `+++` path.
- 2026-11-17: `/blast-radius`: verdict `risk`.
  - Safety fact: on a real `git diff --merge-base` patch, each `file:line` that `added_comments.py` prints holds the printed text on the branch, and the move kept every rule number (1 to 14, 17 to 19). Rung 4: the proof below exits 0. A one-line shift in the hunk counter makes it exit 1.
  - Confirmed risk: `skills/engineering/skills/mob-review/PANEL.md:16` gives the `persona-comments` guard as "an added comment line that `scripts/added_comments.py` lists". `mob-review` Step 2 (`skills/engineering/skills/mob-review/SKILL.md:83`) matches each guard against `files.txt` only, and runs no script. Chance: medium. Cost: on the user's branch the lane can skip, and the no-comments rule does not run. Clear fix: make the `PANEL.md` guard file-based (a changed file with an extension that the script knows), and keep the script run in the persona's own Guard.
  - Cleared: `persona-architecture/SKILL.md:59` says `persona-comments` raises a comment that names another package as Change Requested; both lenses still do. `persona-shell`, `persona-github-actions`, `persona-i18n`, `persona-naming`, and `persona-code-quality` route comments to `persona-comments`; the new guard covers shell and YAML, which the old frontend-only guard did not. `sad-path` lists no `persona-comments` guard. `light-review` does not run `persona-comments`, so the new `Lens:` line does not touch it. A deleted file (`+++ /dev/null`) has no known extension, so the script lists nothing for it.
  - Proof, from the repo root:

    ```sh
    set -e
    D=skills/engineering/skills/persona-comments
    git diff --merge-base origin/pstack-inspired HEAD > /tmp/br19.patch
    python3 $D/scripts/added_comments.py /tmp/br19.patch > /tmp/br19.out
    n=0
    while IFS= read -r row; do
      f=${row%%:*}; rest=${row#*:}; l=${rest%%:*}; t=${rest#*: }
      sed -n "${l}p" "$f" | grep -qF -- "$t" || { echo "MISMATCH $row"; exit 1; }
      n=$((n+1))
    done < /tmp/br19.out
    [ "$n" -gt 0 ] || { echo "NO ROWS"; exit 1; }
    echo "rows checked: $n"
    rules() { grep -oE '^ *[0-9]+\. \*\*' | grep -oE '[0-9]+' | sort -n | tr '\n' ' '; }
    old=$(for f in SKILL.md references/comment-style.md references/file-headers.md references/reach-and-placement.md; do git show "origin/pstack-inspired:$D/$f"; done | rules)
    new=$(cat $D/references/*.md | rules)
    echo "old: $old"; echo "new: $new"
    [ "$old" = "$new" ] || { echo "RULE NUMBERS CHANGED"; exit 1; }
    echo PASS
    ```
- 2026-11-17: `/work-on` map playbook, batch of unit 19. Stopped at H3 on D1, in playbook step 5 (the fix round after `/interrogate`). Steps 1 to 25 are done. Next: answer D1, then `/work-on @.ai/map_pstack-program.md`. That run resumes at playbook step 5: it applies the D1 answer, runs the test and review steps again, then playbook step 6 (`/ship` steps 1 to 3, then `git push -u origin pstack-19_no-comments`) and step 7 (tick unit 19).

## Pending Decisions

### D1: How does `added_comments.py` handle a string that holds a comment marker? (found in step 25)
- A: Delete the string rules. The script lists each added line that holds a marker, and the persona drops a line that is a string. Remove the string clause from AC A and condition C3. The script loses about a third of its code, and every quote miss goes away. Cost: a URL in a string is listed, so `persona-comments` runs more often. (recommended: five review and interrogate rounds found a new quote shape that the per-line scan gets wrong each time, so the premise is false, and `principle-subtract-before-you-add` says to remove before you add)
- B: Keep the string rules as a hint only. The persona's Guard becomes file-based, as in `PANEL.md`, and on own code the persona reads every added line for comments, with the script list as a start. Change the spec Decision that the script is the guard for both lenses.
- C: Keep the design, and add a narrow rule for a double quote inside a single-quoted string. This is a third fix on a failed premise.
- Work: none. Open report rows: run 4 of `.ai/review_pstack-19_no-comments.html`, the quote row and the `Found` tuple row.
- Blocks: 26

## Follow-ups
