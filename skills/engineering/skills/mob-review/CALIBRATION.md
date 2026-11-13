# Calibration signals

Step 7 runs this after the report. Change no persona and no part of `mob-review` here.

The panel improves by watching itself. Scan **this run** for signs that a persona, or `mob-review`, got something wrong, and record each sign in the calibration backlog. `/engineering:self-improve` puts the backlog to the user, and `update-personas` applies the entries the user approves.

The backlog sits outside every repo:

```bash
BACKLOG="${XDG_STATE_HOME:-$HOME/.local/state}/self-improve/improve-personas.md"
mkdir -p "$(dirname "$BACKLOG")"
```

Signals to look for:

- **Convention conflict → false positive.** A finding contradicts a documented convention (`CLAUDE.md`, `AGENTS.md`, the lint config, or a recalled memory). The persona is missing that exception. → An exception in its "What you review". *(Example: persona-naming flags a project's API-client composables for CRUD-verb names until that exception is added.)*
- **Lane stray.** A persona reported something another lane owns (a finding you dropped in Step 4). → A tighter "Out of lane" list.
- **Mis-guard.** A persona was spawned but returned `inScope:false` (guard too loose), or a clearly-relevant persona got skipped (guard too tight). → A guard change, in the persona and in the panel table.
- **Repeated noise or miss.** A persona keeps firing the same low-value nit, or misses a pattern its lane claims. → A severity or scope change.
- **Contract slip.** A persona broke [`PERSONA-CONTRACT.md`](../../PERSONA-CONTRACT.md): a wrong `persona` name, a `file:line` from the patch instead of the branch file, or JSON that does not parse. → A check in Step 4 of this skill, or a clearer contract line.

Read the backlog before you add an entry. If an `open` entry names the same target and the same problem, add this run's evidence to it. If a `rejected` entry covers it, add nothing. Otherwise append:

```markdown
## <persona-name or mob-review>: <the problem in a few words>

- Signal: <one of the five signals above>
- Evidence: <YYYY-MM-DD>, <repo> at <head>: <what happened, with file:line>
- Edit: <one line: the change to make>
- Status: open
```

Write the Edit line in general words, with no names, paths, keys, URLs, or counts, because it becomes rule text in a shared repo. The Evidence line holds the specifics. Back each entry with evidence from this run. No speculative rewrites.
