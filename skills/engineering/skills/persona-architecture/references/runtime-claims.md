# persona-architecture: verify before claiming a runtime failure

A layering finding is about *where responsibility lives*: it stands on its own without a rendering bug attached. If you reach for one anyway ("and therefore it renders blank/undefined/broken"), you now owe evidence, because a wrong failure scenario discredits the real architectural point beside it.

- **CSS custom properties: check the base `:root` before claiming one resolves empty.** Theme files often override a *subset* of tokens; the full set is declared at base `:root` (and the dark variant). A token absent from one theme still resolves from base. Grep both before asserting a var is unset.
- Prefer running the check (a browser-mode test reading `getComputedStyle`, a grep across theme + design-token files) over reasoning about the cascade. State what you ran.
