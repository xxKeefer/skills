# Error infrastructure

## The repo's error infrastructure (read before flagging)

Find these in the repo first (`CLAUDE.md`, `AGENTS.md`, the app's query setup). Where they exist they are first-class and already wired: a finding is usually "you hand-rolled a thing that exists."

- **Taxonomy.** The project's error taxonomy, if it has one: a base error class carrying context and a trace id, with concrete subclasses for HTTP errors, session expiry, and schema parse failures.
- **Global query/mutation error handler.** The app's `QueryCache` / `MutationCache` `onError`. It usually owns the display policy (the toast) and may gate it on a per-query `meta` flag. Sentry reporting often happens in the transport, independent of that callback.
- **The display opt-out** is the project's per-query flag (for example `meta: { displayErrors: false }`), not a hand-rolled catch.
- **Retry policy.** The app's shared retry function, if it has one, which typically fails fast on schema drift and 4xx errors.
- **Toast** is the project's toast helper.
- **Cancellation.** Axios `CanceledError` and `AbortError`; the Sentry config often already filters `AbortError`. Look for an in-repo precedent for rethrowing it untouched.
