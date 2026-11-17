## Models

A skill names a role, not a model. Find the role in this table, and use its model and effort. With
no row for a role, use the session model.

| Role              | Who                                                          | Model     | Effort |
| ----------------- | ------------------------------------------------------------ | --------- | ------ |
| judgement         | `/work-on`, `spec`, `plan`, `grill`, `retro`, review triage  | `opus`    | medium |
| worker            | each `build` step, `implement`, `fix`                        | `opus`    | medium |
| mechanical worker | a step that `/plan` marks mechanical: rename, codemod, move  | `sonnet`  | medium |
| reviewer          | each persona lane                                            | `opus`    | medium |
| mechanical reviewer | a lane whose `PANEL.md` line names the mechanical reviewer | `sonnet`  | medium |
| verifier          | a driver that checks a running build                         | `sonnet`  | medium |
| prover            | a check that tries to disprove a claim                       | `opus`    | high   |
| panel             | a set of views on one question                               | `opus` high, `sonnet` high, the session model | as listed |
| explorer          | read-only search, source checks                              | `haiku`   | low    |

1. After two failed fixes on one premise, move the next attempt one effort step up. The ceiling is
   `opus` at max effort. Record each step in the decision log.
2. Run `fable` only when the user asks, in the prompt or in a plan step.
3. The user can override a mechanical mark when they approve a plan. A `PANEL.md` line can override
   the reviewer role for one lane.
