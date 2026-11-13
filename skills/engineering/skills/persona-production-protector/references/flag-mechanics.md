# Feature-flag mechanics

## Feature-flag mechanics

Find the project's flag mechanisms in the repo (`CLAUDE.md`, `AGENTS.md`, the shared libs). Typical roles:

| Mechanism | Use |
|---|---|
| a flag composable or hook | component/composable gating; check whether it **falls back to off** when its provider is not registered |
| a store or provider flag check | store- and provider-level gating |
| route meta that requires a flag | whole-route gating, with optional off-redirect |
| a visibility config (`featureFlag` plus permission, company feature, account type) | declarative nav/element gating |
| a typed known-flags list | **source of truth**: types the flag string and drives any dev override panel |

A new flag must be created in the project's flag service **and** added to the known-flags list, or it is untyped and untoggleable in dev. Follow the project's flag naming convention and do not flag a documented exception to it.
