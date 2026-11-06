# Engineering

Engineering workflows from ticket to PR: refine, scope, split, and plan a ticket, fix a batch of QA
bugs, and open the PR. Builds, debugging, and manual QA come from `developer`, and code review from
`review`. Framework-agnostic, language-agnostic -- pure best-practice software engineering
principles.

## Dependencies

Requires primitives, developer, and review. Engineering skills reference `/grill`,
`/write-to-file`, `/write-report`, `/look-up`, and `/do-next` from `primitives`, `/claim` and
`/tdd` from `developer`, and `/review:mob-review` and `/review:self-improve` from `review`. Install
all four domains.

Name a review skill with its `review:` prefix, such as `/review:mob-review`. Each skill name lives
in one domain. Developer's `CLAUDE.md` lists what each developer skill keeps for its callers.

Engineering loads in work sessions only. [ADR 0009](../../docs/adr/0009-review-domain.md), "How
engineering loads", says how.

## Skills

[`README.md`](README.md) holds the only skill table for this domain. Edit a skill row there.

[`TEST-APPROACH.md`](TEST-APPROACH.md) holds the risk and technique method. `start-ticket` and
`create-pr` read it. Developer's `tdd` holds the same text in `risk-and-technique.md`. A change to
one file needs the same change to the other.

The marketplace loads this domain in place from the repo
([ADR 0001](../../docs/adr/0001-how-plugins-load.md)). An edit is live at the next session start,
or after `/reload-plugins`. The entry in `installed_plugins.json` is a record. It does not decide
what loads.
