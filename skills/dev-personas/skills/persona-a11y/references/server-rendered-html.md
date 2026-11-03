# Server-rendered HTML rules

### Server-rendered HTML / Thymeleaf

**There are NO Reka or design-system components here. It is plain, hand-written HTML.** Nothing wires focus, roles, ids, or ARIA for you, so EVERY concern below is 100% hand-review with zero framework safety net. Same semantics as the Vue lane, retargeted to raw HTML/Thymeleaf:

- **Clickable non-interactive elements (Change Requested).** `<div onclick>`/JS-wired `<div>`/`<span>` acting as a control → use a real `<button>` (or `<a>` when it navigates). No native keyboard/role/focus otherwise.
- **Navigation rendered as a button (Change Requested).** A control whose job is to navigate to a URL/route must be an `<a href>`/`th:href`, not a `<button>`. Buttons act, links navigate: a button breaks middle-click / open-in-new-tab / copy-link / context menu / SR link role.
- **Icon-only buttons/links without an accessible name (Change Requested).** An icon-only `<button>`/`<a>`, including an inline `<svg>` with no text, needs `aria-label` (or visually-hidden text). Flag the missing accessible name.
- **Unlabelled form controls (Change Requested).** A bare `<input>`/`<select>`/`<textarea>` with no associated label, or a `<label>` with no `for`/`id` association to its control. Every control needs a programmatic label.
- **`target="_blank"` without `rel="noopener noreferrer"` (Change Requested).** Report from the a11y/markup angle. NOTE: this also overlaps persona-security's reverse-tabnabbing check. Flag it here regardless.
- **Landmarks, heading order, images, colour-only state (Nit).** Page shell should have `<main>`; primary nav in `<nav>`. No skipped heading levels (h1→h3), one logical `<h1>`. Meaningful `<img>` needs `alt`; decorative `<img>` needs `alt=""`; an inline decorative `<svg>` needs `aria-hidden="true"`. State signalled by colour alone (no icon/text/aria).
- **Focusable-but-hidden / duplicate id (Change Requested).** A focusable element (native control or `tabindex="0"`) that is also `aria-hidden="true"`, reachable by keyboard yet hidden from AT. A duplicate hardcoded `id` (e.g. same `id` emitted in a `th:each` loop) silently breaks `for`/`aria-labelledby`/`aria-describedby` association.
- **Out of lane:** the *quality* of the string/`th:text` translation → persona-i18n. You own the markup and the accessible-name plumbing, not the copy.
