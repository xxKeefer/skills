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

## Flag identity rules

These rules belong to section A of the persona.

4. **Unknown / mistyped flag string (Change Requested).** A flag literal that isn't in the known-flags list (or isn't in the flag service) is off forever: dead feature, or worse, a gate that reads as "shipped". Also flag names that only differ by app suffix (`x_enabled` vs `x_enabled_qt`) used interchangeably.
6. **Stale gate reused (Nit).** Reusing a flag that's already 100%-on in production, or one that belongs to a different feature, as this change's gate. That's not a gate.
