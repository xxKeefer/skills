# Risk and technique

Use this file to plan the tests for a change before you write code. Risk sets how deep to test. The shape of the code picks the technique. The method is the risk-based testing of the ISTQB Foundation syllabus (v4.0).

A plan handoff keeps the result in a Test approach section. A reviewer reads that section later and compares it with the tests that the change adds.

## The Test approach section

```markdown
## Test approach

### Risks

| AC | Behaviour | Risk | Why |
| --- | --- | --- | --- |
| A | <AC, short> | H | money: changes the price shown before checkout |
| B | <AC, short> | L | copy only |

### Conditions

| ID | AC | Condition | Technique | Level | Planned test |
| --- | --- | --- | --- | --- | --- |
| C1 | A | quantity 1 and 99 accepted | EP | Unit | `<test file>` |
| C2 | A | quantity 0 and 100 rejected | BVA | Unit | `<test file>` |
| C3 | A | a read-only user sees no Delete button | decision table | Integration | `<test file>` |
| C4 | — | <behaviour the change adds that no AC covers> | … | … | … |

### Variations

| Dimension | Values |
| --- | --- |
| Plan | free, pro |
| Role | admin, member, read-only |
| Flag | on, off |

- **Plan:** pairwise set, 6 rows, as one table-driven test in `<test file>`.
- **Not covered:** <combination>: <why this is acceptable>.

### Not testing

- <condition>: <why this is acceptable, or the follow-up ticket>.
```

- `AC` is the letter of the acceptance criterion, such as `A` or `B.2`.
- `ID` names one condition. A handoff step names the IDs of the conditions it tests.
- `—` marks behaviour that no AC covers. Ask the user whether the ticket needs an AC for it.
- Write the Variations part only when the change touches two or more dimensions.

## Step 1: Rate the risk of each AC

Risk is likelihood × impact. Rate each AC, or each behaviour, as **H**, **M**, or **L**. Write the reason in a few words.

**Impact:**

| Tier | Areas |
| --- | --- |
| **H** | Money: prices, quotes, billing, invoices, terms, discounts. Auth: login, tokens, MFA, permissions, roles, account switch, cross-tenant access. Provisioning: create, change, or cancel a resource that a customer pays for or runs on. Data loss and one-way changes: deletes, migrations, data fixes. Anything a customer cannot undo. An internal tool that changes what a customer pays is also H. |
| **M** | Customer-visible flows that fail loudly and recover: lists, filters, forms that the server validates, settings, notifications. Internal tools and admin pages, unless they change what a customer pays. |
| **L** | Copy, layout, styles, internal refactors with existing coverage, developer tools. |

**Likelihood goes up** for:

- new code, not edited code
- many branches or conditions
- async work and races
- code that crosses a boundary: client to API, or service to queue
- a defect hotspot
- an area that the team does not know well
- a library upgrade under the code

**Find the hotspots.** Count the fix commits on each file that the change touches:

```bash
git log --oneline -i -E --grep 'fix|bug' -- <file> | wc -l
```

A file with many fix commits is a hotspot. Raise the likelihood one step.

**Combine them.** An H impact with high likelihood is **H**. An H impact with low likelihood, such as a one-line edit with good coverage, can drop to **M** or **L**. No area has a floor. The written reason is the requirement, because a reviewer checks that judgement. Challenge a rating below the area's impact tier that has no reason, or a reason that the diff contradicts.

**Depth by risk:**

- **H**: the happy path, every invalid partition, the boundaries, and the permission, error, and empty states. Variations at least pairwise.
- **M**: the happy path and the most likely failure, such as the main invalid input or the error state.
- **L**: one test at the cheapest level, or none, with a reason under Not testing.

## Step 2: Derive the conditions with the technique that the code needs

Use only the H and M rows. Pick the technique from the shape of the change:

| Shape of the change | Technique | What it gives you |
| --- | --- | --- |
| A validated or numeric input: a length limit, a quantity, a date range, a page size | **Equivalence partitioning (EP)** and **boundary values (BVA)** | One value for each valid and invalid partition. Each edge and its neighbours: min−1, min, max, max+1. |
| Two or more conditions decide one outcome together: role × account type × flag → button shown | **Decision table** | One rule for each combination that changes the outcome. Merge the rules where a condition does not change the outcome. |
| A lifecycle, a status, or a wizard: an order's status, a subscription, the steps of a form | **State transition** | Each valid transition. Also the invalid ones: cancel a cancelled order, go back after submit. |
| Independent dimensions that multiply: plan × role × flag × locale × state | **Pairwise** | Each pair of values together at least once. This is usually 6 to 15 rows, not hundreds. Put the rows in one table-driven test. |
| Anything a user does over time | **Heuristics** | *Zero, one, many*: an empty list, one item, page 2. *CRUD*: create, read, update, and delete, each with the permission off. *Goldilocks*: too small, too big, correct. *Interruptions*: double-submit, leave the page during a write, session expiry, account switch during a flow, a slow or failed network. |

Take the project's dimensions from its domain glossary (`CONTEXT.md`) or its `CLAUDE.md`: its products, roles, account types, flags, states, and locales.

Take each expected value from a fixture or the spec, never from the code under test.

## Step 3: Pick the cheapest level that proves each condition

- **Unit**: pure logic, formats, validation, the branches of one function or module. Partition, boundary, and pairwise tables go here.
- **Integration**: a unit with its real collaborators, such as a store, a database, a router, or a rendered component. Permission-driven behaviour. Decision-table rows that need the wired-up code.
- **Contract**: the shape between a client and an API, or between two services. Check it against the spec or a shared schema.
- **E2E**: a flow across pages or services, or a result that only real backend data proves. Test only the happy path and the one or two failures that matter most.
- **Manual**: only when automation is not practical. Write the reason.

Prove each edge case at the cheapest level. Move a condition up a level only when the lower level cannot prove it.

## What escapes

An escaped defect is a bug that reached users. Each one escaped through one gap. Use the gaps as a checklist for the H rows: which gaps does this change open?

| Escape type | What escaped | The technique that catches it |
| --- | --- | --- |
| `boundary` | A value or partition edge: the last day of a month, page 2, the maximum length | EP and BVA |
| `combination` | Two or more dimensions together: role × account type, plan × add-on | Decision table or pairwise |
| `state-transition` | A change after another change: cancel then modify, an upgrade after a renewal | State transition |
| `interruption` | Double-submit, a race, a retry, a session or account switch | Interruption heuristics |
| `contract` | The shape between a client and an API, or between two services. An event that no listener handles. Drift from the spec | A contract test |
| `authz` | One user reads or changes another user's record, cross-tenant access, a permission or role gap | Decision table on role, CRUD with the permission off |
| `data-config` | Seed data, environment config, a migration | A test on the data or the config, or a manual check |
| `secrets-logging` | A secret or personal data in a log, a response, or the repo | A test that reads the log or the response |
| `regression` | It worked before, and a later change broke it | A test on the old behaviour |
| `other` | None of the types above | No fixed technique |

The cheapest level that would catch an escape is one of `unit`, `integration`, `contract`, `e2e`, or `none`. Use `none` for data or config with no code path.
