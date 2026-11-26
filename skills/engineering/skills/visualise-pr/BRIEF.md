# Theme brief

Set `SKILLS` to the absolute parent of this skill's base directory. A subagent cannot resolve a
relative path. Give each subagent this brief, with `<THEME>` and the paths filled:

> You explain and judge one theme of a change set: **<THEME>**, from `<SCRATCH>/themes.md`. Show
> how the theme works in the context of the repo, and say if each of its changes makes the
> architecture better or worse. You do not review for bugs, security, or speed.
>
> Repo: `<repo path>`. Base `<BASE>`, head `<HEAD>`. Read code with `git show <HEAD>:<path>` and
> `git show <BASE>:<path>`, not from the working tree. Already computed, do not recompute:
>
> - Themes, areas, and the files of your theme: `<SCRATCH>/themes.md`
> - Full patch: `<SCRATCH>/diff.patch`
> - Stated reasons: `<SCRATCH>/why.md`
> - Complexity: `<SCRATCH>/complexity.tsv`, or `none: estimate each number`
>
> Judge in five dimensions. For each one, read `<SKILLS>/<name>/SKILL.md` for each name in its
> yardstick:
>
> <the yardstick table from SKILL.md Step 3>
>
> Write about architecture in the words of `<SKILLS>/codebase-design/SKILL.md`: module, interface,
> depth, seam, adapter, leverage, and locality.
>
> Link form for `path:line`: `<link form>`. Write each link as `[path:line](<url>)`.
>
> Rules:
>
> 1. Start broad. `story` says what the theme does for the repo and how it works, before any
>    detail.
> 2. A change is one move in one dimension, such as a new seam or a function that grew. Give each
>    a verdict: `better`, `worse`, `mixed`, or `no change`. The theme verdict is your judgement of
>    its changes, not a sum.
> 3. `why` quotes or sums up a reason from `why.md`. With none, write "No stated reason". Never
>    guess a reason.
> 4. A deviation from a pattern, an ADR, or `CONTEXT.md` is `better` only with a stated reason.
> 5. `reason` names the principle that the verdict rests on first, such as
>    `boundary-discipline: the payload type now crosses the seam`.
> 6. The diagram shows the theme's modules inside their areas from `themes.md`, plus one hop of
>    callers and callees. Use `subgraph Before` and `subgraph After` when the shape changes.
> 7. Pseudocode shows the logic of the theme in short indented lines, such as
>    `if content is unchanged` then `return cached result`. It is not the source code.
> 8. Complexity: each change names the function, and gives base and head numbers from
>    `complexity.tsv`, such as `CCN 4 → 9, NLOC 20 → 48`. With no file, add "estimate" after each
>    number.
> 9. Pattern fit: apply each check of `persona-decisions-log` to the changed code. Each deviation
>    is a change, and its `why` gives the stated reason, or "No stated reason".
>
> Mermaid rules. A broken diagram shows as an error on the page:
>
> - Start each node ID with `n`, then letters and digits only, such as `nSaveSeam`. A bare word
>   such as `call`, `end`, `class`, or `click` is a keyword, and it breaks the parse.
> - Put each label in double quotes, such as `nSave["useCartSubmit"]`. Put no `"` inside a label.
>   Write a generic as words, such as `Partial of Config`.
> - Mark touched nodes with `classDef changed fill:#fde68a,stroke:#b45309`.
> - Give each node a click line, `click <node> href "<url>" _blank`, with `_self` in place of
>   `_blank` for a non-web URL.
>
> Return only this JSON as your final message:
>
> ```json
> {
>   "theme": "<THEME>",
>   "verdict": "better | worse | mixed | no change",
>   "areas": "apps/web, packages/api",
>   "story": "The theme in one sentence.\n\nHow it works in the repo, in up to four sentences.",
>   "why": "The stated reason, or No stated reason.",
>   "dimensions": "Coupling better: boundary-discipline, … Complexity worse: …",
>   "diagram": "flowchart LR …",
>   "pseudocode": "the logic as plain pseudocode",
>   "changes": [
>     {
>       "verdict": "worse",
>       "dimension": "Complexity",
>       "where": "[src/cart.ts:42](<url>)",
>       "change": "What changed, in one sentence.",
>       "why": "The stated reason, or No stated reason.",
>       "reason": "<principle name>: why the verdict follows from it."
>     }
>   ]
> }
> ```
