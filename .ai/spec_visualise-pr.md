---
doctype: spec
ticket: none
status: confirmed
goal: A /visualise-pr skill that explains a change set against main in diagrams and pseudocode, and says per dimension if the architecture gets better or worse.
---

# Spec: /visualise-pr

## Intent

- Outcome: An infographic HTML report that shows how a change set moves the architecture against main, and if each move is better or worse.
- User: The user, in self-review of a finished branch before its PR, and in review of other people's PRs.
- Why now: Not stated in the interview.
- Success: The user understands the shape of a change from rich diagrams paired with pseudocode, and each diagram node and `path:line` opens the code.
- Constraint: The report explains and judges. It is not a review, so it has no ticks, no prompt, and no fixes.
- Out of scope: Correctness, security, and performance findings, which belong to /mob-review and its personas.

## Decisions

- The report explains, it does not drive fixes: /mob-review already owns findings, ticks, and fixes. A "worse" verdict can name a follow-up skill in prose.
- Five fixed dimensions (Module shape, Coupling, Pattern fit, Complexity, Testability): a fixed set makes two reports easy to compare. Domain language folds into Pattern fit.
- Each section has at least one diagram and one pseudocode block: the user said rich imagery paired with pseudocode is what helps them understand.
- Pseudocode shows in an `html` visual with a `<pre class="bg-code">` block, in the /show-me pseudocode style: /write-report needs no new visual type for it.
- Two input modes. A PR link sets the change set from `git fetch origin pull/<n>/head`, and the skill ignores the local branch. No link means committed work on the current branch against `origin/main`: the user runs it on a finished branch before its PR.
- Local mode stops on uncommitted changes and asks the user to commit or stash: the report reviews a finished branch, not work in progress.
- Unpushed commits do not stop local mode, and the skill never pushes: before a PR, unpushed commits are normal, and a report skill does not change the branch.
- PR mode links open the PR files view at the line, in a new tab: the template already opens `https://` links with `target="_blank"`.
- Local mode links open the file at the line in the editor that the `Editor` tool role names. On this machine that is Zed, `zed://file/<path>:<line>`: the code is on disk, and the commits may not be on the remote.
- Mermaid nodes link with `click <node> href "<url>" _blank`: the template runs Mermaid with `securityLevel: "loose"`.
- "Why it changed" comes from, in order: the PR body and its ticket, the plan or spec, the commit messages, then the ADRs. With no source, the row says "No stated reason": a missing reason is useful to a reviewer, and a guess is not.
- A deviation from a pattern counts as better only with a stated reason: the reason is what makes a deviation a choice.
- Verdict words `better` (green), `worse` (red), `mixed` (yellow), and `no change` (no tone) are added to /write-report: the current `pass`/`fail` words read as defects.
- The net verdict is a judgement, not a sum: it names the dimension that matters most for this change, and why.
- Complexity comes from `lizard --csv`, per function, for base and head: per-function numbers show which function grew and link to its line. `lizard` has no TSV output. Base files come from `git show` into a temp folder.
- `lizard` is named through a new `Complexity` tool role, and the editor through a new `Editor` tool role, both in the user's `~/.claude/AGENTS.md`: this keeps the per-machine tool-role pattern that `gh`, the tracker, and the browser use.
- A new ADR records that the suite depends on named CLI tools through tool roles: the user wants the move to opinionated tooling written down.
- A missing tool is named in the report `meta` with its install command, and the agent estimates and labels its numbers "estimate": the gap shows, and is not silent.
- The report has two levels. The top visuals show `bars` of the five verdicts and one before/after diagram per dimension. Each row is one change, grouped by dimension: the whole shape comes first, and the four parts (what, why, how, verdict) fit one change best.
- At most about eight rows per dimension. Smaller changes go in a folded table under that dimension's diagram: a large PR stays readable.
- Each diagram shows the touched modules plus one hop of callers and callees: the whole repo is too large to read. (Default chosen by the agent, not raised in the interview.)
- One subagent per dimension, in parallel, in the `reviewer` role. The main agent, in the `judgement` role, collects the shared input once and writes the net verdict: this matches how /mob-review runs, and it keeps each subagent on one question.
- Each subagent uses principles as its yardstick, not personas: principles are language-agnostic rules about shape, and personas are stack checklists that return defects. Module shape reads `minimize-reader-load`, `laziness-protocol`, `redesign-from-first-principles`, and /codebase-design. Coupling reads `boundary-discipline` and `migrate-callers-then-delete-legacy-apis`. Pattern fit reads `model-the-domain`, `type-system-discipline`, and `persona-decisions-log` as a checklist. Complexity reads `minimize-reader-load`, `subtract-before-you-add`, and `explain-the-number`. Testability reads `test-behavior-not-implementation`.
- Architecture prose uses the /codebase-design vocabulary (module, interface, depth, seam, adapter, leverage, locality): the repo already uses these terms.
- The skill is standalone in the `engineering` domain, and no other skill calls it yet: a new skill proves itself before others depend on it.

## Acceptance criteria

- [ ] **A.** Run `/visualise-pr <PR link>` from any branch → the report covers the PR's change set, and nothing from the local branch.
- [ ] **B.** Run `/visualise-pr` with no link on a branch with uncommitted changes → the skill stops, asks the user to commit or stash, and writes no report.
- [ ] **C.** Run `/visualise-pr` with no link on a clean branch with unpushed commits → the report covers `origin/main...HEAD`, and the branch is not pushed.
- [ ] **D.** In a PR-mode report, click a node or a `path:line` → the PR files view opens at that file and line, in a new tab.
- [ ] **E.** In a local-mode report, click a node or a `path:line` → Zed opens that file at that line.
- [ ] **F.** Open any report → it has a section for each of the five dimensions, and a dimension that the diff does not touch shows "no change" and no diagram.
- [ ] **G.** Read the top of a report → the answer gives the net verdict, names the dimension that matters most, and says why.
- [ ] **H.** Read the top visuals → one `bars` visual shows the five verdicts, and each touched dimension has one before/after diagram.
- [ ] **I.** Read a row → it gives what changed, why, how it works, and a verdict, with a close-up diagram and a pseudocode block.
- [ ] **J.** Read a row's verdict → the first column is `better`, `worse`, `mixed`, or `no change`, and the card has the matching tone.
- [ ] **K.** Read a verdict → its commentary names the principle that it rests on.
- [ ] **L.** Run on a change with no reason in any source → the row says "No stated reason".
- [ ] **M.** Run on a dimension with more than eight changes → it has at most about eight rows, and the rest sit in a folded table under its diagram.
- [ ] **N.** Read the Complexity section → each changed function shows base and head numbers from `lizard`, with a link to its line.
- [ ] **O.** Run with `lizard` not installed → `meta` names `lizard` and its install command, and the complexity numbers are labelled "estimate".
- [ ] **P.** Read the Pattern fit section → each deviation from an ADR or `CONTEXT.md` that `persona-decisions-log` checks shows its stated reason, or "No stated reason".
- [ ] **Q.** Watch a run → five dimension subagents run in parallel from one shared input, and the main agent writes the net verdict.
- [ ] **R.** Read a diagram → it shows the touched modules plus one hop of callers and callees.
- [ ] **S.** Write a /write-report run with first cells `better`, `worse`, `mixed`, and `no change` → they show green, red, yellow, and no tone.
- [ ] **T.** Run `check_report.py` on a report with a `zed://file/...` link → it passes, and a link with any other non-web scheme still fails.
- [ ] **U.** Read `~/.claude/AGENTS.md` → the tools table has an `Editor` row for Zed and a `Complexity` row for `lizard`.
- [ ] **V.** Read `docs/adr/` → a new ADR records that the suite depends on named CLI tools through tool roles.
- [ ] **W.** Open one generated GitHub PR line link (`#diff-<sha256 of path>R<line>`) and one `zed://file/<path>:<line>` link → each opens at the right line.
- [ ] **X.** List the skills → `/visualise-pr` is in the `engineering` domain, no other skill calls it, and its report is `visualise_<KEY>.html` in the /write-report folder.
