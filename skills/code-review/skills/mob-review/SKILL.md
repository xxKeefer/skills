---
name: mob-review
description: Run the full staff-engineer review panel over a PR or branch. Spawns every in-scope persona reviewer (a11y, i18n, reactivity, design-system, decisions-log, tanstack, vitest, comments, naming, code-quality, correctness, error-handling, async-state, form-behaviour, text-input, url-state, value-display, resilience, charts, file-upload, typing, best-practice, architecture, security, shell, skills, github-actions, api-spec, production-protector, bundle-size, analytics, integration-test, browser-e2e, test-design, api-integrity, ac-check, pr-size), plus the project's own rubric when the repo names a rubric skill or has a CODING_STANDARDS.md or CONTRIBUTING.md, in parallel against the diff, and writes their findings to one ranked HTML report through /write-report. On your own branch, the ticks in the report build a /code-review:apply-review prompt. On someone else's, each finding gets a draft reply, and the ticks build a /code-review:post-review-comments prompt. In a handoff, it records the report in the review step. It applies no fix and never pushes. Takes an optional handoff or spec path for the AC and test-design checks. Use when the user says "mob review", "mob-review", "run the panel", "full review", or wants a broad multi-lens review of the current branch.
---

# Mob Review: staff-engineer review panel

Spawn every in-scope `persona-*` reviewer in parallel over one diff, then aggregate their findings into a single ranked HTML report. Each persona is a narrow, non-overlapping specialist; this skill is the orchestrator.

`light-review` follows Steps 0 to 7 of this skill with seven lanes only, so a change to a step here also changes `light-review`.

## The panel

| Persona skill | Reviews | Guard (runs only if…) |
|---|---|---|
| `persona-a11y` | semantic HTML, ARIA, labels, focus, keyboard | `.vue` changed, or a server-rendered HTML template (Thymeleaf, plain `.html`, or any other server-rendered `.html`) changed. A `.vue` whose changed hunks sit only inside `definePage({...})` / route `meta` does not count |
| `persona-i18n` | hardcoded strings, dynamic keys, product names, namespaces | the app's source-locale file (`en.json`) changed; or a `.vue`/`.ts` in an app that uses the i18n library whose **changed lines** add or change user-facing text or `t()`/`<i18n-t>` callsites (not one whose hunks only swap a data source, an import or a binding, or sit only inside `definePage`/route `meta`; apps that do not use the i18n library never spawn it). Judge the hunks, not the file |
| `persona-vue-reactivity` | computed/ref/watch correctness, needless re-renders, composable call sites (outside setup, inside a computed, repeated inline calls, inline `.value` snapshots), watchers that should be event handlers or one-off setup code | `.vue` or composable (`use*.ts`) changed |
| `persona-design-system` | semantic tokens, reinvented design-system components, CSS hygiene, long-value layout (truncate without `min-w-0`, no tooltip, unbroken values) | `.vue`, `.styles.ts`, or class strings changed. A `.vue` whose changed hunks sit only inside `definePage({...})` / route `meta` does not count |
| `persona-decisions-log` | conformance with the project's recorded decisions (ADRs, `CONTEXT.md`, or a decision log the repo's instructions name): accepted versus convention versus proposed decisions, decisions reversed with no new record | the repo records decisions (ADRs in `docs/adr/`, `CONTEXT.md` decisions, or a decision log the repo's `CLAUDE.md`/`AGENTS.md` names) **and** the diff changes source, config or user-facing copy a decision could govern |
| `persona-tanstack` | query keys, invalidation, caching, API client usage | the **changed lines** touch `@tanstack/vue-query`, `useQuery`/`useMutation`/`useQueries`/`queryOptions`/`invalidateQueries`/`setQueryData`, a `use*Query`/`use*Mutation` composable, or a queryFn/API client call. Judge the hunks, not the file. A store that seeds a query elsewhere is not in scope when the diff leaves that code alone |
| `persona-vitest` | unit-test quality, selectors, builders, flakiness | `*.spec.ts` / `*.test.ts` changed (a standalone browser E2E suite's Playwright specs → `persona-browser-e2e`; `tests/integration/**` → `persona-integration-test`) |
| `persona-comments` | needless/stale/what-not-why comments, over-long comments, comments reaching outside their codebase, dead code | added or changed comment lines in frontend source (`//`, `/* */`, JSDoc, `<!-- -->` in `.vue`) |
| `persona-naming` | file/folder/export/variable naming + units | new files added, or files renamed, or exported/declared identifiers changed, in `.ts`/`.vue`/`.mjs`/`.cjs`/`.js` |
| `persona-code-quality` | extraction, dedup (including a duplicate speed/money/date formatter), misplaced code, vueuse/es-toolkit, Python stdlib reuse, the Fowler smells that no other lane owns (any language) | **non-test** source in any language changed (`*.spec.*`, `*.test.*`, `test_*.py`, `*_test.*`, and files under `tests/` do not count) |
| `persona-correctness` | logic errors that give a wrong result or a crash: wrong conditions, off-by-one boundaries, crashes on a reachable input, missed cases, wrong values, lost or early results, broken callers, coercion and equality. Every finding carries a counterexample | any diff that adds or changes executable code in any language: source, scripts, build and CI logic, and code in a fenced block that a skill or doc tells someone to run. Not a diff of only prose, locale strings, lockfiles, generated files, or tests |
| `persona-error-handling` | swallowed failures (empty catch, catch-that-only-logs), `console.*` instead of the error reporter/toast, local catch duplicating the global query error handler, context-free `throw`, errors off the app's error taxonomy, reported `CanceledError`, `fetch` without `response.ok`, floating promises | the **changed lines** touch a failure path (`catch`, `finally`, `throw`, `.catch(`, `.then(`, `reject`, `onError`, `captureException`, `console.`, `fetch(`, `response.ok`, `Promise.`, a `*Error` type) in **non-test** `.ts`/`.vue`. Judge the hunks, not the file. Bare `async`/`await` is **not** a trigger on its own, and matches inside test files never count: counting those spawns the persona on diffs with no failure path in them |
| `persona-async-state` | races and stale async state: out-of-order responses, in-flight writes into reset state (logout, company switch, revert), reactive route/context re-read after an `await`, conflicting writes left enabled, `initialData` faking a loaded query, last good data kept after a failure | the **changed lines** touch async state: `await`, `.then(`, an async `watch`/`watchEffect`, `useMutation`/`mutate`/`mutateAsync`, `isPending`/`isFetching`/`isError`, `initialData`/`placeholderData`, `AbortController`/`signal`, `onWatcherCleanup`, a `$reset`/logout/company-switch handler, or a `route.params`/`route.query` read inside an async callback. Non-test `.ts`/`.vue` only. Judge the hunks, not the file. Changing which function an event binding or import points at (`@logout="…"`, a swapped composable source) doesn't count. The handler's own body has to change |
| `persona-form-behaviour` | what Enter, Escape, and submit do (`@keydown.enter` on the design system's input, IME Enter, raw buttons with no type, Enter in a combobox/modal), missing or self-contradictory min/max/length bounds, number inputs for identifiers or empty numbers sent as `''`, stale hidden-field values and errors, cross-field rules not re-run, typed dates past the picker's limits, and failed submits losing input | **changed lines** of non-test `.vue`/`.ts` under `apps/**` or `libs/**` touch a form: a form control (the design system's input, `<input`, `<textarea`, `<select`, a date picker, a combobox), its bounds (`min`/`max`/`maxlength`/`step`, `type="number"`, `v-model.number`), its schema (zod/yup `.min(`/`.max(`/`.length(`/`.refine(`/`.superRefine(`/`.when(`/`.required(`/`.optional(`, `z.coerce.`), its registration (`useField`, `<Field :name`, `initialValues`), its keyboard and submit wiring (`@keydown`, `@keyup`, `@submit`, the design system's form component, `useForm`, `handleSubmit`, a `<button>` inside a form, a dialog's dismiss props), or a wizard step's routing (`beforeEnter`, a step route). Judge the hunks, not the file. A hunk that sits only inside `definePage({...})`/route `meta`, or only swaps an import, doesn't count. |
| `persona-text-input` | what happens to the characters typed or pasted: whitespace-only passing required, trim on secrets, validators rejecting real names/emails/keys, comparisons ignoring case/whitespace/normalisation, autocapitalise and smart quotes on code-like fields, UTF-16 length and `slice()` splitting emoji, user text in URLs/regexes/queries unescaped, bidirectional text isolation, IME composition firing search, masks breaking paste, and CSV quoting and encoding | **changed lines** of non-test `.vue`/`.ts` under `apps/**` or `libs/**` touch how user text is accepted, compared, or passed on: a string schema rule (zod `z.string()`/`.trim(`/`.regex(`/`.email(`/`.min(`/`.max(`, yup `string()`) or a network identifier validator (IP, CIDR, MAC, ASN), a string operation on user input (`.trim(`, `.toLowerCase(`, `.normalize(`, `.length`, `.slice(`/`.substring(`), input wiring (`v-model.trim`, `@input`, `@paste`, `@compositionstart`/`@compositionend`, an input mask or formatter), input attributes (`autocapitalize`, `autocorrect`, `spellcheck`, `inputmode`, `autocomplete`), user text put into a URL, query or regex (`encodeURIComponent`, a template-string URL, `new RegExp(`, a search filter), a user-entered URL bound to `:href`, or CSV/file import and export. Judge the hunks, not the file. |
| `persona-url-state` | what refresh, a shared link, Back, and Forward do: filters/search/tabs not in the URL, query read once, push versus replace (Back traps), query writes dropping params, unparsed query values, page/selection not reset on filter change, hidden rows, `router.back()` with no fallback, overlays and scroll on Back, sort by display string, and "no data" versus "no matches" | **changed lines** of non-test `.vue`/`.ts` under `apps/**` or `libs/**` touch the URL, history or a list control: `route.query`/`route.params`, `useRoute`, `useRouteQuery`, the project's URL-filter composable, `router.push`/`router.replace`/`router.back`/`router.go`, `history.`, `scrollBehavior`, a `queryParam`/`searchQueryParam` prop, list filter/search/sort/pagination/selection state, a tab's active value, a `.sort(`/`.toSorted(` on list data, a list fetch's page size or limit, an export or download (`window.open`, `<a :href … download>`), or a permission check on a control or route guard (`beforeEach`/`beforeEnter`). Judge the hunks, not the file. A hunk that only declares a route in `definePage({...})`/route `meta` doesn't count. |
| `persona-value-display` | what a value looks like when missing, zero, huge, or awkward: `undefined`/`NaN`/`Invalid Date` as text, null shown as 1970/2000/$0, placeholder and enum drift, dates outside the design system's date component or the project's date formatter (date-only UTC shift, zone labels), money by hand, unit conversion (1024, bits/bytes), ratios with a zero total, relative-time oddities, range edges, and copy buttons | **changed lines** of non-test `.vue`/`.ts` under `apps/**` or `libs/**` render or format a value: a template interpolation (`{{ }}`), template literal, or nested property read of an API field, a formatter (the project's date, money or speed formatter, or a currency formatter class), `toLocaleString`, `Intl.`, `toFixed(`, `new Date(`, `Date.parse`, Luxon `DateTime`, a status or label map, a prop validator, a sentinel default (`?? -1`, `Number.MAX_SAFE_INTEGER`), a ratio or percentage, or a copy-to-clipboard value. Judge the hunks, not the file. |
| `persona-resilience` | what happens when the session, network, another tab or a deploy changes under a task: work lost on session expiry, parallel 401s, 4xx retries, cross-tab logout/company switch, full-resource PUT overwrites, duplicate creates, unguarded or unscoped storage, offline and hung requests, polling, stale chunks after deploy, cancelled requests shown as failures | **changed lines** of non-test `.ts`/`.vue` under `apps/**` or `libs/**` touch an HTTP client or interceptor, 401/403 handling, the auth or session store, `QueryClient`/`QueryCache`/`MutationCache` config, `retry`/`retryDelay`/`networkMode`/`refetchInterval`/`refetchOnWindowFocus` options, `BroadcastChannel` or `storage` events, `localStorage`/`sessionStorage`, `AbortController`/`signal` handling in a client, `router.onError` or dynamic-import handling, or a save (PUT/PATCH) that sends a whole resource. Judge the hunks, not the file. A hunk that only swaps an import, or adds an ordinary lazy route to a route table, doesn't count. |
| `persona-charts` | Unovis telemetry and billing charts: empty, single-point and gappy data, nulls drawn as zero, misleading y axes, chart time zone vs page, bucketing and partial buckets, axis units, tooltips, sizing and lifecycle, colour-only series | **changed lines** of non-test `.ts`/`.vue` touch a chart: an `@unovis/*` import or a `Vis*` component (`<VisXYContainer`, `<VisLine`, `<VisArea`, `<VisAxis`, `<VisCrosshair`, `<VisTooltip`, `<VisSankey`, …), a chart component's own directory, a telemetry data composable or its time-range and unit-format helpers, or a chart data transform (bucketing, null handling, an axis or tick formatter, a tooltip template). Judge the hunks, not the file. A hunk in a chart directory that only renames, swaps an import, or changes copy doesn't count. |
| `persona-file-upload` | file pickers, drop zones and imports: type and size checks, SVG where raster is meant, input reset and re-selecting the same file, drops outside the zone, progress and cancel, `File` in serialised state, filenames, hand-split CSV, values converted before validation | **changed lines** of non-test `.vue`/`.ts` under `apps/**` or `libs/**` touch a file upload or import: `<input type="file"`, the design system's upload component or another upload component, an `accept=` attribute, a drop zone (`useDropZone`, `@drop`, `@dragover`, `@dragenter`, `@dragleave`, `dataTransfer`), file handling (`FileReader`, `File`, `Blob`, `FormData`, `file.size`, `file.type`, `file.name`), or CSV/text import parsing (`readAsText`, `.text()` on a file, `.split(` on file contents, a CSV parser). Judge the hunks, not the file. A hunk that only swaps an import, or only builds a CSV for download, doesn't count. |
| `persona-architecture` | cross-layer coupling, logic in wrong layer, shell↔page coupling | non-test `.ts`/`.vue` source under an app (`apps/*/src`) or a shared library (`libs/*/src`) changed, or source in a standalone test repo with its own layering (e.g. a browser E2E suite's `src/*/specs`, `src/*/pages`, `src/*/fixtures`) changed |
| `persona-security` | reverse-tabnabbing, wildcard postMessage, v-html XSS, dev-flag-in-prod, CSV formula injection, secrets/PII to Sentry | **non-test** `.ts`/`.vue` source changed |
| `persona-best-practice` | outdated framework/lang APIs, deprecated patterns, snapshot dependencies, stale README, `@Deprecated` without the why and the replacement | **non-test** `.ts`/`.vue`/`.mjs`/`.cjs`/`.js` source changed (test-runner API currency is `persona-vitest`) |
| `persona-typing` | casts (`as`, `as unknown as`, `!`), inferred-type gymnastics (`ReturnType<>`), `Omit<>` over-use, missing generics, mutable global consts that should be `readonly`/`as const` | `.ts`/`.mts`/`.d.ts`/`.vue` source changed, tests included |
| `persona-github-actions` | GHA workflow/action CI-security + best practice (injection, permissions, action pinning, secrets) | `.github/workflows/*` or `.github/actions/**` changed, or a composite/reusable workflow referenced by those |
| `persona-shell` | shell correctness: swallowed exit statuses, `set -euo pipefail`, SIGPIPE, quoting, unstable-output parsing, signal semantics | `*.sh`/`*.bash` or a file with a shell shebang changed, or a multi-line `run:` block changed in a workflow/action |
| `persona-skills` | agent-instruction correctness: dangling skill/tool/path references, contradictions between skills, non-invocable targets, unset placeholders, single-user assumptions, unbounded waits, manifest drift, drifting counts, a `SKILL.md` over 10 KB, a cheaper subagent model where the default belongs | `SKILL.md` or anything under `skills/<name>/`, `agents/*.md`, `commands/*.md`, `.claude/**`, `CLAUDE.md`/`AGENTS.md`, or a `.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` / `hooks/hooks.json` changed |
| `persona-api-spec` | OpenAPI spec ↔ code drift: undocumented endpoints/status/enum values, contradicted presence or `required`, renamed error codes, hand-edited generated files, spec changed without regenerating | the repo has an OpenAPI spec (committed or generated from code) **and** the spec changed, **or** a route handler/controller, request/response schema or DTO, or an enum/constant reaching a response body changed, in any language. A code-side change with **no** spec change is precisely what this catches. Never skip it on that basis |
| `persona-integration-test` | Playwright + MSW flakiness/perf | `apps/*/tests/integration/**` changed |
| `persona-browser-e2e` | a standalone browser E2E suite (real backend, no MSW) | a standalone browser E2E suite's specs, page objects, fixtures, API helpers or `playwright.config.ts` changed. Frontend only: never spawn it on a backend-only diff |
| `persona-api-integrity` | frontend call ↔ backend, cross-repo: request/response vs the spec and the handler (params, body, Zod strictness vs nullability/enums, envelope, status codes), frontend permission/context gate vs the handler's authorization check and the roles granted the permission, unmerged-backend dependencies, missing server-side checks, the spec's visibility marker versus the handler's authorisation, replaced or removed endpoints left behind | the **changed lines** of non-test `.ts`/`.vue` add or change an API call (a path constant/builder or DTO schema in the project's API client, a `queryOptions`/`mutationOptions`/`useQuery`/`useMutation` or the project's query/mutation wrapper whose fn, path, params or body changed, a legacy API-client method, or a raw `fetch(`/axios call to an API path), **or** the gate in front of an existing call (`definePage` `meta.permissions`, an argument to the project's permission helper, an account-type/partner/flag condition) on a page or component that calls an endpoint. Judge the hunks, not the file. Backend-only diffs → `persona-api-spec` |
| `persona-test-design` | what *should* be tested: risk-rated behaviours (likelihood × impact), conditions from partitions/boundaries, decision tables, state transitions, pairwise across product/role/account/flag/state, interruption heuristics; high-risk gaps, wrong test level, PR "Tested by"/Conditions claims no test backs, plan-time test-approach conditions dropped without a Gaps entry. Capped at five findings | **non-test behavioural source** changed in any language (frontend, backend, library or script code), **whether or not the diff touches a test**. Type-only, style-only, `definePage`/route-`meta`-only, locale JSON, Storybook-only, docs, CI and lockfile hunks don't count, and a test-only diff doesn't either |
| `persona-ac-check` | PR (code + description) ↔ acceptance-criteria coverage, from a handoff, a spec, or the ticket; recommends update-ticket vs update-PR | Step 1 has a handoff or spec path, or a ticket (a key or issue number per the repo's `docs/agents/issue-tracker.md`) is resolvable from the argument, branch or PR title, and the tracker is reachable from this session |
| `persona-pr-size` | PR too big / splittable; proposes the `gh stack` split layout | diff is large by **changed-line count** (~≥400) or obviously bundles unrelated concerns. File count on its own is not a split signal. A shared-lib change plus one small config edit per consuming app is one coherent change however many files it spans |
| `persona-production-protector` | production blast radius: missing/leaking/fail-open feature gates, flipped defaults, in-place shared-lib changes, global-scope edits, delete-before-proven, one-way changes, tightened contracts, rollback story | shipped non-test source changed under `apps/**` or `libs/**` (`.ts`/`.vue`/`.css`, app config/bootstrap) (skip test-/docs-/CI-only diffs; a Storybook-only file under `src/**` imported only by `*.stories.ts`/`.storybook/**` is not shipped and counts as test-only; **except** a test/e2e diff that provisions privileged accounts, grants roles, or mutates a shared environment) |
| `persona-bundle-size` | shipped bytes and load timing: heavy/rare components statically imported behind `v-if`/flag/modal (should be `defineAsyncComponent`), static routes, top-level heavy imports for handler-only use, eager globs, whole-locale imports, dev code on prod paths, non-tree-shakable imports, `sideEffects`, new/duplicate heavy deps, deps inlined into a lib `dist`, chunk/compile-flag config | the **changed lines** of non-test `.vue`/`.ts`/`.js`/`.mjs` under `apps/**` or `libs/**` add/change an `import`, `import()`, `defineAsyncComponent`, `import.meta.glob`, a route definition, or a `v-if`/`v-show`/`<component :is>` around a component; **or** a `package.json` deps/`sideEffects`/`exports` field changed; **or** a `vite.config.*`/build config changed. Judge the hunks, not the file |
| `persona-analytics` | product event tracking both ways: over-tracking (backend-measurable events, hot-path volume, duplicates of page views, free-text/high-cardinality props, identity/PII passed around the consent gate, untyped `posthog.*` calls, off-vocabulary events) and event-name conventions (literal snake_case domain-first names, no variable segments, suffix meanings, renames that split a metric, duplicates of live PostHog events) and under-tracking (new flow/wizard/experiment with no milestone, broken flow start/complete/abandon lifecycle, missing exposure or entry-point attribution), plus changes to the analytics consent gate | the **changed lines** touch the project's analytics wrapper or `posthog.`; **or** they add a user-facing flow in an app that activates the analytics lib. A new page, a wizard/stepper, a confirm dialog that fires a mutation, a new order/checkout/signup/billing entry point, or a flag-gated alternate experience. Judge the hunks, not the file |
| project rubric (a review rubric skill the repo's `CLAUDE.md` or `AGENTS.md` names, else the repo's `CODING_STANDARDS.md` or `CONTRIBUTING.md`; not a persona) | the project's own code standards, as that skill or file defines them | the repo names a rubric skill or has one of those files, and the diff touches code the rubric covers. See Step 3 |

## Step 0: Run the panel in a clean thread

**The panel is cheap; the thread it runs in is not.** Reviewing a diff needs the diff, the ticket and the repo. Not the conversation that produced the change. Run at the tail of an implementation session, the panel pays for that whole history on every one of its hundreds of orchestration turns: spawns, every persona report, fixes, verification. Measured: the persona subagents are a fifth of a review's cost, the orchestrator's own turns are the rest, purely from running at ~320K context instead of ~45K.

- **Arriving from a session that just wrote the code** → the implementation is committed, so the branch is the whole handoff. Ask the user to `/clear` and re-run `mob-review`; nothing is lost, since the branch carries the state.
- **Already in a fresh or short thread** (a session opened to review) → straight to Step 1.
- **User declines** → run anyway. Say once that it will cost several times more, then drop it.

## Step 1: Resolve target and compute the diff scope

Accept an optional target: a PR number/URL, a branch name, or nothing. Also accept an optional handoff or spec path. Step 3 passes it to `persona-ac-check` and `persona-test-design`. A handoff has steps for `/do-next` to run, and a spec has none. With a handoff, Step 6 records the report in its review step.

**Run from inside the repo.** The panel reviews one repo's diff; one run per repo. Never check a PR out over someone's uncommitted work.

A caller can name the repo folder, such as the worktree that `/code-review:review-pr` claims. Then run every command of this skill in that folder, and add `Repo under review: <path>` to each lane brief in Step 3. The subagents start in the session's folder, not in the repo.

```bash
git fetch origin main --quiet
```

- **No arg / branch:** review the current (or named) branch vs `origin/main`.
- **Stacked PR** (`gh pr view --json baseRefName` is not `main`): review vs `origin/<baseRefName>` instead, in every git command below and in what the personas are told. The base branch's commits are its own PR's to review.
- **PR number/URL:** `gh pr checkout <n>` first (only if the working tree is clean; otherwise ask), then review that branch vs `origin/main`.

Compute the changed-file list and the diff **once, to disk**, and hand every persona those paths instead of a command each one re-runs:

```bash
SCRATCH="${TMPDIR:-/tmp}/mob-$(git rev-parse --abbrev-ref HEAD | tr / -)-$(git rev-parse --short HEAD)"
mkdir -p "$SCRATCH"
git diff --name-only --merge-base origin/main HEAD > "$SCRATCH/files.txt"
git diff        --merge-base origin/main HEAD > "$SCRATCH/diff.patch"
git diff --stat --merge-base origin/main HEAD | tail -1
cat "$SCRATCH/files.txt"
```

The path is keyed by branch **and sha**, so a later run after a fix commit computes its own patch and can never read a stale one.

**Uncommitted work.** If the branch has no commits ahead of `origin/main` but the working tree is dirty, the change hasn't been committed yet. Review the working tree instead: drop `HEAD` from the three `git diff` commands (`git diff --merge-base origin/main` includes staged and unstaged changes), and suffix `SCRATCH` with `-wt`. `/code-review:apply-review` then leaves its fixes in the working tree.

If `files.txt` is empty, report "no changes vs origin/main" and stop.

Record the two SHAs the panel reads. Step 5 prints them, so a later push step can compare the branch with what the panel read:

```bash
git rev-parse --short "$(git merge-base origin/main HEAD)"   # base
git rev-parse --short HEAD                                   # head
```

**Branch behind `main`.** A merge-base diff still carries commits that already landed on `main` by squash merge (a sibling ticket's PR, or an earlier slice of a stack), so the panel would review code that is not this PR's change. When `git rev-list --count HEAD..origin/main` is non-zero, compare `git diff --stat --merge-base origin/main HEAD` against the diff a merge would leave: `git diff --stat origin/main $(git merge-tree --write-tree origin/main HEAD | head -1)`. If the second is clearly smaller, stop and offer to merge `origin/main` first (own code) or tell the author (someone else's), then recompute the scope. Conflicts reported by `merge-tree` are part of the offer.

**Never print the patch body into this thread.** The orchestrator needs the file list (Step 2 guards) and the `--stat` line (size); the personas need the diff, and they read it from `diff.patch` themselves. A diff pasted here is re-sent on every remaining turn of the review. Every persona report, the fixes and the verification all sit behind it.

Also record **whose code this is**. It decides the ticks and the prompt of the report in Step 5:

```bash
git config user.email                                          # you
git log --format='%ae' $(git merge-base origin/main HEAD)..HEAD | sort -u   # branch authors
```

**Own code** = every commit on the branch is authored by the current git user. Anything else (a commit by another author, or a PR you checked out from someone else) is **someone else's code**. When in doubt, treat it as someone else's.

**What Copilot already said.** The panel never re-reports an issue Copilot has already raised on the PR. The author has seen it there, and a second copy is noise. If the branch has a PR (`gh pr view --json number -q .number`; none, or uncommitted work → skip this), save every Copilot comment to the scratch dir, resolved and outdated ones included:

```bash
PR=$(gh pr view --json number -q .number)
{
  gh api --paginate "repos/{owner}/{repo}/pulls/$PR/comments" \
    --jq '.[] | select(.user.login | test("copilot"; "i")) | {path, line: (.line // .original_line), body}'
  gh api --paginate "repos/{owner}/{repo}/pulls/$PR/reviews" \
    --jq '.[] | select(.user.login | test("copilot"; "i")) | select(.body != "") | {path: null, line: null, body}'
} > "$SCRATCH/copilot.jsonl"
wc -l < "$SCRATCH/copilot.jsonl"
```

Review bodies count too: Copilot lists its low-confidence comments there with a file and line instead of posting them inline. Don't print the file here; Step 4 reads it.

## Step 2: Select in-scope personas

Match the changed-file list against the guard column above. Only launch personas whose guard matches. This is a coarse pre-filter to avoid spawning obviously-irrelevant reviewers. Each persona also self-guards as a backstop and returns zero findings if truly out of scope. Note which personas you skipped and why (shown in the final table).

## Step 3: Spawn the in-scope personas in parallel

Launch **one subagent per in-scope persona, all in a single message** (multiple `Agent` tool calls) so they run concurrently. Use the `general-purpose` agent type. The harness runs at most 20 subagents at once and refuses the rest; when the panel exceeds that, launch the overflow as the first reports come back.

**Model per persona.** A persona reads a bounded diff and answers against a written rubric, so pass `model: "sonnet"` on the `Agent` call for every persona *except* the following, which stay on the default model because their misses are silent and expensive:

- `persona-security`
- `persona-production-protector`
- `persona-architecture`
- `persona-skills` (its defects are relational: it has to read across files to find them)
- `persona-api-integrity` (cross-repo and relational: it has to trace a frontend call to a spec, a handler, its service and a permission changeset)
- `persona-test-design` (a missing test is invisible in the diff: it has to reason from the source to conditions nobody wrote, and rate risk)
- `persona-correctness` (the lane for logic bugs: a miss ships a wrong result, and no step after the panel looks for it)

Ticket context in the prompt is fine. The author's beliefs about behaviour are not facts. Pass a claim like "the old component rendered aria-hidden" only as something to verify, or leave it out, because a persona that accepts it as given skips the check its lane exists for.

The persona skills ship in the same domain as this one, as sibling directories: set `PERSONAS` to the parent of this skill's base directory (shown when the skill loads) and substitute the absolute path into the prompt — a subagent cannot resolve `$SKILL_DIR` or a plugin-relative path on its own. The shared persona contract sits at `<PERSONAS>/../PERSONA-CONTRACT.md`.

Give each the same diff context and this exact brief:

> Read `<PERSONAS>/../PERSONA-CONTRACT.md`, then `<PERSONAS>/<persona-name>/SKILL.md`. Follow both as a code review of the diff below. Inside the persona file, `$SKILL_DIR` means `<PERSONAS>/<persona-name>`, and a relative link resolves from that directory.
>
> Return the JSON that the contract's "When a caller asks for JSON" section gives, as your final message.
>
> Diff scope: branch vs `origin/main`, already computed: **do not recompute it**.
> - Full patch: `<SCRATCH>/diff.patch`
> - Changed files: `<SCRATCH>/files.txt`

When Step 1 has a handoff or spec path, add one line to the `persona-ac-check` and `persona-test-design` briefs: `Handoff or spec: <absolute path>`.

**Project rubric, same message, when the repo has one.** The rubric is a review rubric skill that the repo's `CLAUDE.md` or `AGENTS.md` names. With no such skill, it is the repo's `CODING_STANDARDS.md` or `CONTRIBUTING.md`. If the diff touches code the rubric covers, spawn one more `general-purpose` subagent with `model: "sonnet"`. It reads a written rubric, like a persona:

> Invoke the `<rubric skill name>` skill via the Skill tool, or read `<absolute path to the rubric file>`. If the file states no rule about how to write code, return `{"persona":"<rubric>","inScope":false,"findings":[]}`. Apply the rubric as a **review only** of the diff at `<SCRATCH>/diff.patch` (changed files in `<SCRATCH>/files.txt`): no edits, no PR comments. Only report problems on changed lines, verified against the code. Read `<PERSONAS>/../PERSONA-CONTRACT.md`, and follow its Findings and Code references sections. Return raw JSON only (no prose, no code fences), in the form that its "When a caller asks for JSON" section gives, with `"persona"` set to the skill name or the file name, and `category` set to the rubric section. Skip a rule that the repo's tooling already enforces. Severity: a defect the rubric calls out as a bug or contract violation → `change-requested`; a standards deviation → `nit`; a larger refactor idea → `future`.

## Step 4: Aggregate

Collect each persona's JSON (`.filter(Boolean)` any that failed). Combine all `findings`. Do not re-litigate or merge across personas: lanes don't overlap by design, so duplicates indicate a persona strayed; drop the out-of-lane one.

The project rubric overlaps the personas by design. When one of its findings names the same file, line, and problem as a persona finding, keep the persona's. Its remaining findings stand.

These known persona pairs can land on the same line. Resolve them the same way every time:

- **`persona-code-quality` #10 (truthiness guard) vs `persona-value-display` #2 (null shown as a believable value)** on the same line → keep `persona-value-display`'s (it names the wrong value the user sees) and fold code-quality's `??`/`isNil` fix into its `suggestion`.
- **`persona-test-design` versus a `persona-correctness` / `persona-form-behaviour` / `persona-text-input` / `persona-url-state` / `persona-value-display` finding** on the same field → keep both: one names the defect, the other the missing test. Put them next to each other in the report.

**Drop anything Copilot already raised.** If Step 1 saved a non-empty `$SCRATCH/copilot.jsonl`, compare every remaining finding against it and drop the ones Copilot already covered: same file, within a few lines (or cited in a review body), and the same underlying problem, however differently worded. Severity doesn't matter. A `change-requested` that Copilot flagged as a passing remark still goes. A finding on the same line but about a different problem stays. When unsure whether it's the same problem, drop it. Keep a count of drops per persona for the Step 5 coverage table.

Hold the `persona-ac-check` findings apart. Step 5 puts them first. Rank the rest: **change-requested → nit → future**, then group by persona within each tier.

## Step 5: Write the report

The findings go to an HTML report, not to the chat. Write the report with `/write-report`. A
second run on a new head then adds a run to the same file.

The coverage table shows the user what ran. Counts are after the Copilot filter:

```
Persona            CR  Nit  Future   Status
a11y                1    2       0   ran
i18n                0    0       0   ran (clean)
vue-reactivity      —    —       —   skipped (no .vue/composable changes)
...
project rubric      0    1       0   ran (rubric covers changed files)
correctness         1    0       0   ran
```

Give `/write-report` these inputs:

- `kind`: `review`.
- `key`: the ticket key from the handoff, the branch name, or the PR title. Else `pr-<n>` when the
  branch has a PR. Else the branch name with each `/` changed to `-`.
- `title`: `Review of PR #<n>`, else `Review of <branch>`.
- `skill`: `/code-review:post-review-comments` on someone else's code, and `/code-review:apply-review` on
  your own code.
- The run:
  - `title`: `Panel run`.
  - `head`: the head SHA from Step 1. For uncommitted work, add `+ working tree`.
  - `meta`: `Base` (the base branch and the base SHA), `PR` (the PR URL from
    `gh pr view --json url -q .url`, when the branch has a PR), `Folder` (the absolute path of the
    repo folder), `Spec` (the source of the acceptance criteria, when `persona-ac-check` ran), and
    `Copilot` (`dropped N (<persona>: n, …)`, when the filter dropped a finding).
    `/code-review:post-review-comments` reads `PR`, `Base`, and `Folder`.
  - `answer`: the count in each tier, and what the user does next. If every persona is clean,
    say so plainly. A clean panel is a valid result.
  - `visuals`: one `table` with the question "Which lanes ran, and what did each find?". It holds
    the coverage table, one row for each lane. Set `fold`, so the findings start after the answer.
  - `columns` and `rows`: below.

Give each finding one row. The `persona-ac-check` findings come first. A PR can pass every lane
and still build the wrong thing, so spec gaps do not compete in the lane ranking. The findings of
every other lane follow, in the Step 4 order.

| Key | Label | Holds |
|---|---|---|
| `tier` | Tier | Change Requested, Nit, or Future |
| `persona` | Persona | the name without the `persona-` prefix, such as `a11y` |
| `where` | File:line | the `file:line` of the finding. Set `mono` |
| `issue` | Issue | the summary, a blank line, then the detail |
| `recommendation` | Recommendation | the suggestion. On your own code, the sort comes first |
| `draft` | Draft reply | on someone else's code only. Set `fold` |

- Keep the personas' markdown links to `main`. If a finding cites out-of-diff code as a bare
  `path:line`, convert it to a link first (resolve the line on `origin/main`).
- Write each draft reply in the comment layout of
  [`post-review-comments`](../post-review-comments/SKILL.md#the-comment-layout), and follow the
  rules under that layout. `/code-review:post-review-comments` checks the anchor and scans the draft
  before it posts.
- On someone else's code, give each row the tick `reply`. On your own code, give each row the
  tick `fix`.

**The sort, on your own code.** Start each recommendation with `Small.` or with
`You decide: <reason>.`, so the user knows which rows to tick. Judge the size and the certainty of
the fix, not its tier. A `change-requested` can be a one-liner, and a `nit` can be a redesign.

- `Small.` The fix is mechanical or local, and it has one obvious right answer. Examples: delete a
  redundant wrapper, a duplicate mapping, or a vacuous assertion. Extract a helper or a test
  fixture that is already duplicated word for word. Add a test case for an uncovered branch that
  the existing harness supports. Rename, add a missing `readonly` or `as const`, make a loose type
  tight, or extract an i18n key.
- `You decide: <reason>.` The fix changes a public API, a component contract, or an exported
  type. Or it changes behaviour that no test pins down, or it needs a product or design decision.
  Or it spans several files, or restructures a module. Or two reasonable fixes exist, and the
  choice is the author's. Or the persona marked it `future` and framed it as a ticket of its own.

Then print only these in the chat. Print no finding.

1. `Reviewed: base <base>, head <head>`, with the two SHAs from Step 1. For uncommitted work, add
   `+ working tree` after the head.
2. The coverage table. When the Copilot filter dropped a finding, add one line under the table:
   `Dropped N findings Copilot already raised (<persona>: n, …).` Don't list them.
3. The report path.

## Step 6: Pick what to act on

**On someone else's code, apply nothing.** Editing another person's branch is theirs to invite,
and the findings are the deliverable. Say in one line that the panel applied no fix because the
branch is not yours. Tell the user to tick the rows to reply to in the report, then paste the
prompt that the report builds. The prompt runs `/code-review:post-review-comments` on the ticked rows.

**On your own code** (per the Step 1 ownership check), also apply nothing here. Tell the user to
tick the rows to fix in the report, then paste the prompt that the report builds. The prompt runs
`/code-review:apply-review` on the ticked rows. It fixes test-first and commits once. It pushes only
when the branch has an open PR.

**In a handoff from Step 1**, on your own code, the review step writes the report and stops:

1. Tick the review step. Write the report path, and the base and head SHAs from Step 1, into its
   done line. `/create-pr` reads the two SHAs.
2. Under `/run-wave` (you follow its `STEP.md`), the user cannot tick the report during the
   run. Write a `D` entry in the `STEP.md` form. It names the report path. Its options are to
   tick the rows and run the prompt, or to fix nothing. Its `Blocks` line lists the push step, the
   step that pushes or opens a PR.
3. Stop. The user runs the prompt before the push step. The fix commit comes after the reviewed
   head, so the push step shows it as drift.

## Step 7: Record calibration signals (never edit)

The panel improves by watching itself. After the report, scan **this run** for signs that a persona, or this skill, got something wrong. Record each sign in the calibration backlog. **Change no persona and no part of this skill here.** `/code-review:self-improve` puts the backlog to the user, and `update-personas` applies the entries the user approves.

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

End the summary with the entries this run added or extended. If nothing surfaced, say "no calibration signals."

## Notes

- The personas themselves are read-only: they review, they never edit. The fixes are the job of `/code-review:apply-review`, and only on your own code.
- Personas are independently invocable too (e.g. run just `persona-tanstack`). This skill is for the full sweep.
- Scale is bounded by the diff: a small PR launches few personas; a broad one launches many. That's intended.
