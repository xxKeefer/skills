# Node.js: modern-API reference (written against Node 24.11.0)

This file was written against Node **24.11.0**. Below: what's first-class across the **22 / 23 / 24** line, so
tooling, scripts, and config in the diff use the built-in instead of a dependency or a
hand-rolled shim. This matters for `*.ts`/`*.mjs` tooling files, not app runtime code (that
runs in the browser).

## Stable across 22 → 24 (prefer built-ins)

- **`node:test` + `node:assert`**: built-in test runner. (Repo uses Vitest for app tests; this
  is only relevant to standalone Node scripts.)
- **Global `fetch`/`Request`/`Response`/`FormData`**: no `node-fetch`/`axios` for simple
  script HTTP.
- **`node:util` `parseArgs`**: CLI arg parsing over `minimist`/`yargs` for small scripts.
- **`structuredClone`**: deep clone without `lodash.clonedeep`.
- **`fs.glob` / `fs.promises.glob`** (stable in 22+): over the `glob` package for simple globs.
- **Built-in `.env`**: `node --env-file=.env` over `dotenv` for script env loading.
- **`AbortSignal.timeout(ms)`** / `AbortSignal.any([...])`: over manual timeout+controller.
- **`require(esm)`** (unflagged in 22.12+/23/24): CJS can require sync ESM; stop shipping
  dual CJS shims for that reason alone.

## Node 24 highlights

- **npm 11** bundled.
- **`URLPattern`** global: over a regex route matcher in scripts.
- V8 13.6: `Float16Array`, `RegExp.escape`, `Array.fromAsync` all available.
- Stable `node --run <script>`: over `npm run` indirection in CI shims.

## Flag when

A changed tooling/script file pulls a dependency (or hand-rolls) for something now built in
(`node-fetch`, `dotenv`, `minimist`, `lodash.clonedeep`, the `glob` package for a trivial
glob). → **Nit**. Never flag browser/app code for this: Node built-ins aren't in scope there.

## Not yet: Node 25 and 26

Node 25 and 26 have shipped. If the project stays on the 24 LTS line, **do not raise a finding from a
26-only built-in**: CI, Docker images, and `.nvmrc` all resolve 24. Checklist for whoever moves
the pin: bump `.nvmrc`, the `engines` field, and the Docker base images together, then re-check
the package manager's supply-chain gates in the workspace config against the newer bundled npm.
