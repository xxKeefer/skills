# Dependencies, assets, and build configuration

### C. Dependencies and assets

10. **New or heavier dependency (Change Requested / Nit).** A package added to `dependencies`, or a major bump that grows it. Check and state:
    - Its minified + gzipped size (bundlejs / pkg-size). Quote the source.
    - Whether it's ESM with `sideEffects` declared (`pnpm view <pkg> module exports sideEffects type`).
    - Whether it lands on an eager path.
    - Whether the repo already covers the job: `es-toolkit`, `@vueuse/core`, the project's UI library, native `Intl.*` / `structuredClone` / `URL` / `crypto.randomUUID`, Node 24 / evergreen-browser built-ins in place of polyfills.

    Severity:
    - **Change Requested:** heavy (roughly 20 kB+ gzip) and eager; or it duplicates a capability an existing dependency already provides (a second date/utility/icon/HTTP lib); or it's CJS-only where an ESM alternative exists; or it's a polyfill for something every supported browser has.
    - **Nit:** small, or lazily loaded.
11. **Dependency inlined into a lib's `dist` (Change Requested).** A lib's source imports a package that is not in that lib's `dependencies`/`peerDependencies`. It's only in `devDependencies`, or it's transitive. A lib's Vite config typically externalises only declared `dependencies` and `peerDependencies`, so the package gets **bundled into the lib's output**, and every consuming app ships it again beside its own copy. Declare it as a peer or dependency. (Resolved-version skew between two declared copies is `persona-best-practice`'s.)
12. **Large inlined or eager assets (Nit / Change Requested).**
    - **Nit:** an image, SVG or font imported into JS that is large enough to inline as base64 against `assetsInlineLimit`, or one that sits on an eager path.
    - **Nit:** a raised `assetsInlineLimit`.
    - **Change Requested:** a whole icon or flag set pulled in when a few are used. A lazy `import.meta.glob` loader, where the repo has one, is the model to follow.

### D. Build configuration

13. **Chunk / compile-flag config that grows the eager bundle (Change Requested / Nit).**
    - **Change Requested:** a `define` turning on `__VUE_PROD_DEVTOOLS__` or `__VUE_PROD_HYDRATION_MISMATCH_DETAILS__` in a prod config.
    - **Change Requested:** re-enabling the Options API where the app turns it off (`features.optionsAPI: false`) without a named library that needs it.
    - **Change Requested:** aliasing `vue` to the runtime-compiler build, or adding a string `template:` option. Either ships the ~14 kB compiler.
    - **Change Requested:** a chunk rule that forces lazy modules into an eager chunk.
    - **Nit:** raising `chunkSizeWarningLimit` to silence a warning instead of splitting.
    - **Nit:** turning on `sourcemap: 'inline'` for prod.
    - **Nit:** a new chunk config written as Rollup `rollupOptions`/`manualChunks` in a Vite 8 app. Current is `build.rolldownOptions.output.codeSplitting.groups`.
    - **Nit:** removing the Codecov bundle-analysis plugin, or not adding it to a new app. It's often the only size signal a repo has.
