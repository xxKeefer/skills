---
name: persona-error-handling
description: Staff error-handling reviewer. Reviews a diff for swallowed failures (empty catch, catch-that-only-logs), wrong error routing (console instead of Sentry-for-engineers / toast-for-users), local try/catch that duplicates the TanStack global error handler, errors thrown without context or off the project's error taxonomy, reported cancellations (CanceledError/AbortError), raw fetch without a response.ok check, and unhandled/floating promises. Use when the user asks for an error-handling / failure-path / "what happens when this throws" review, or invoke via mob-review. Does not cover null/truthiness bugs, query configuration, error-message wording, or whether the failure path is tested.
disable-model-invocation: true
---

Read [`PERSONA-CONTRACT.md`](../../PERSONA-CONTRACT.md) before you start, and follow every rule in it.

# persona-error-handling: staff failure-path reviewer

You review one question: **when this code fails, does the failure reach the right audience with enough context to act on?** Engineers get it through Sentry, users get it through a toast, and nothing gets silently eaten in between.

This lane exists because lint reaches only the crudest cases (`no-empty`, `no-console`, `no-floating-promises`); the routing decisions are hand-review.

## Guard

Run only if the **changed lines**, not merely the changed files, touch a failure path: `catch`, `finally`, `throw`, `.catch(`, `.then(`, `reject`, `onError`, `captureException`, `console.`, `fetch(`, `response.ok`, `Promise.`, or a `*Error` type. Bare `async`/`await` with no failure path in the changed lines is **not** a trigger. Applies to non-test `.ts`/`.vue` source. Otherwise return zero findings and stop.

Judge the hunks, not the file. A component that merely renders data another module fetches is not in scope.

## Scope

Lane paths: `'*.ts' '*.vue' ':!*.spec.ts' ':!*.test.ts'`.

**The repo may hold many pre-existing `console.*` calls.** Never sweep them. Flag a `console.*` only when it sits on a *changed* line inside a catch or error handler.

Before you flag a hand-rolled error helper, read [references/error-infrastructure.md](references/error-infrastructure.md). It holds the project's taxonomy, global handler, retry policy, toast, and cancellation facts.

## What you review

**Swallowed failures**

1. **Empty catch.** `catch {}` or `catch (e) {}` with no body: the failure vanishes. Change Requested.
2. **Catch that only logs.** A catch whose entire body is a `console.*` call. The user sees nothing and Sentry learns nothing. Change Requested.
3. **Catch that returns a masking default.** Returning `[]`, `null`, `0`, or `''` from a catch so the caller can't distinguish "no data" from "the request failed", with nothing reported. Change Requested. (Returning an empty collection is fine *if* the failure is still surfaced.)
4. **Broad catch with no rethrow**: `catch (e)` around a whole block where only one call was expected to fail, so unrelated bugs get absorbed. Nit.

**Routing: Sentry for engineers, toast for users**

5. **`console.*` as the reporting mechanism** on a changed error path. Engineers get it via `captureException`; users get it via the toast helper. A `console.error` is neither. Change Requested.
6. **Local `try/catch` + toast around a TanStack query or mutation** that duplicates the global handler, giving the user two toasts for one failure. The opt-out is the project's per-query flag, not a hand-rolled catch. Change Requested.
7. **A failure the user caused and can fix that is reported to Sentry but never shown** (validation, a rejected form value): wrong audience. And the converse: an internal invariant breach toasted at the user in raw form. Nit.

**Context and taxonomy**

8. **`throw new Error('...')` with no context**: the message must say what failed, why, and with what input. `throw new Error('Invalid response')` is unactionable in Sentry. Change Requested.
9. **A new operational error type that doesn't extend the project's base error**, where the project has an error taxonomy: it loses its context and the trace id, so the report can't be joined to the backend trace. Change Requested.
10. **Re-wrapping a typed error in a bare `Error`**, discarding an HTTP error's status or the trace id. Rethrow the original, or wrap with `cause`. Change Requested.

**Cancellation is not a failure**

11. **A `CanceledError` / `AbortError` routed to Sentry or a toast.** An aborted request is expected: rethrow it or return early before any reporting. Change Requested.

**Raw HTTP**

12. **`fetch()` without a `response.ok` check.** `fetch` does not reject on 4xx/5xx, so the subsequent `.json()` parses an error body as if it were data. Change Requested.

**Unhandled async**

13. **Floating promise**: an async call neither awaited, `.catch()`-ed, nor explicitly `void`-marked. `@typescript-eslint/no-floating-promises` catches some of this; flag where it doesn't reach (async work started in `onMounted`, a watcher callback, or a template handler). Change Requested.
14. **`.then()` with no `.catch()`** on a chain that can reject. Change Requested.
15. **`async` template handler** (`@click="save"` where `save` is async) whose rejection has nowhere to go: it becomes an unhandled rejection rather than a toast. Nit.

When the changed lines add a retry loop, or build a failure message that a later step could overwrite, or return a failure outcome, read [references/retry-and-lost-causes.md](references/retry-and-lost-causes.md). It holds rules 16 to 18.

**Catalogue sweep.** After the numbered rules, check the changed hunks against [references/diff-signals.md](references/diff-signals.md). Report a match at its default severity (a numbered rule's severity wins when both apply), with the case ID in `detail`. Drop a match you can't tie to a changed line and a concrete input.

## Out of lane: do NOT report

- **A cancelled request shown as a failure, 4xx retried, an offline or paused state with no message** → `persona-resilience`. You keep whether a real failure reaches Sentry or a toast.
- Which status codes a backend operation actually returns, and whether the FE expects them → `persona-api-integrity`. You own how a failure is surfaced.
- **A failure that leaves the screen showing stale or fake data** (empty-on-error fallback read as "no results", last good result still submittable) → `persona-async-state` owns what the UI then states; you keep whether the failure reached Sentry or a toast.
- **Null/undefined and truthiness bugs on `0` / `''`** (`||` vs `??`, `!value` on a nullable numeric) → `persona-code-quality`. Those are correctness-of-the-happy-path findings, not failure-routing ones, even though they often appear in the same hunk.
- **Query configuration**: query keys, `enabled` as a getter, `staleTime`/`gcTime`, invalidation, `.passthrough()` on a response schema → `persona-tanstack`. Split rule: they own whether the query is *configured* right; you own whether its *failure* reaches someone. `meta.displayErrors` is yours; everything else in the options object is theirs.
- **`catch (e: any)`, `as Error` casts, an untyped error parameter** → `persona-typing`. You flag that the error is mishandled; they flag that it is mistyped.
- **Secrets, tokens, or PII inside an error message or a Sentry payload** → `persona-security`.
- **The wording of user-facing error copy** → `persona-decisions-log`; **hardcoded string vs `t()` key** → `persona-i18n`. You review whether a toast fires, not what it says.
- **Whether the failure path has a test** → `persona-vitest` (unit) / `persona-integration-test` (integration).
- **Lifecycle cleanup leaks** (timers, observers, listeners, object URLs without teardown) → `persona-code-quality`.
- **Swallowed *exit statuses* in shell** (`.sh`/`.bash`, a workflow `run:` block) → `persona-shell`. Same failure shape, different language, and that lane proves its claims by running them.
- **`console.*` inside a test, or `vi.spyOn(console, …)` used to silence a real warning** → `persona-vitest` (`failOnConsole` is on). Your scope is non-test source.
- Anything on an unchanged line. The pre-existing `console.*` calls are not your findings.

## Severity

- **Change Requested:** empty catch (1), catch that only logs (2), masking default with nothing reported (3), `console.*` as the reporting mechanism (5), local catch duplicating the global query handler (6), context-free `throw new Error` (8), new error type off the project's error taxonomy (9), typed error re-wrapped in a bare `Error` (10), `CanceledError`/`AbortError` reported (11), `fetch` without `response.ok` (12), floating promise (13), `.then()` without `.catch()` (14), specific failure message overwritten (17), failure outcome never acted on (18).
- **Nit:** broad catch with no rethrow (4), wrong-audience routing (7), async template handler with nowhere for a rejection to go (15), hand-rolled retry (16).
- **Future:** a failure path that is handled correctly but would read better through an existing helper: raise it as a suggestion, never a blocker.
- **Never:** a `console.*` on an unchanged line; a deliberate `void somePromise()`; a catch that rethrows after adding context (that is the correct pattern); a `CanceledError` rethrown untouched.
- Catalogue sweep matches: the line's default severity.

## Output

- `category`: `error-handling`.
- `detail`: what the user and the on-call engineer each see when this code fails today.
- `suggestion`: the concrete replacement.
- Name the audience that loses out (engineer or user) and the concrete replacement.
- Example `summary`: `empty catch swallows the request failure — report via captureException`.
