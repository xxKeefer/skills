# Tree-shaking

### B. Tree-shaking

6. **Non-tree-shakable import of a dependency (Change Requested / Nit).**
   - `import * as X from '<lib>'` or a default import of a whole utility/icon/date library where named imports exist.
   - A CommonJS-only package where an ESM build or sibling exists (`lodash` → `es-toolkit` where the project already uses it).
   - A deep `dist/` bundle path that bypasses the package's ESM `exports`.

   **Change Requested** when the lib is heavy or the import is on an eager path, **Nit** otherwise. Namespace imports of small first-party modules (`import * as Sentry` in a Sentry setup file) are fine; don't flag them.
7. **Side effects vs `sideEffects` (Change Requested / Future).**
   - **Change Requested:** a new lib `package.json` without a `sideEffects` field.
   - **Change Requested:** a module with a real top-level side effect (global registration, `window.*` assignment, a polyfill, `app.use`, CSS import) added to a lib declared `"sideEffects": false`. This is a correctness risk as well as a size one, because the bundler may drop the side effect.
   - **Nit:** new module-scope work in shared lib code that blocks tree-shaking, such as `const x = createThing()` at top level. Wrap it in a function or annotate it `/* @__PURE__ */`.
   - **Future:** when a diff touches a lib whose `package.json` declares no `sideEffects`, once per review. Suggest the ticket to declare it, not a drive-by fix.
8. **Whole-file JSON / locale import (Change Requested / Nit).**
   - **Change Requested:** in an app that splits locales into tiers (a build plugin plus a namespace loader), a direct `import en from '.../i18n/en.json'` (or any locale file) from app code. It bypasses the tier split and ships the whole locale in that chunk. Use the namespace loader instead.
   - **Change Requested:** in an embeddable widget, statically importing every language's dictionary when the widget needs one.
   - **Nit:** a default import of a large JSON file where only a field is read. Use a named import (`import { field } from './x.json'` tree-shakes).
9. **Dev-only code on a prod path (Change Requested).** Mocks, MSW handlers, fixtures, Storybook helpers, dev panels, or `@faker-js`/test builders that are statically importable from shipped code. Guard with `if (import.meta.env.DEV)` plus a dynamic `import()` so the code is dead in the prod build, following the repo's existing lazy pattern for dev panels. Whether the dev override is *readable* in prod is `persona-security`'s. You own the bytes.
