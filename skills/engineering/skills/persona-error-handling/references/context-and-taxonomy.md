# Context and taxonomy (rules 8 to 10)

8. **`throw new Error('...')` with no context**: the message must say what failed, why, and with what input. `throw new Error('Invalid response')` is unactionable in Sentry. Change Requested.
9. **A new operational error type that doesn't extend the project's base error**, where the project has an error taxonomy: it loses its context and the trace id, so the report can't be joined to the backend trace. Change Requested.
10. **Re-wrapping a typed error in a bare `Error`**, discarding an HTTP error's status or the trace id. Rethrow the original, or wrap with `cause`. Change Requested.
