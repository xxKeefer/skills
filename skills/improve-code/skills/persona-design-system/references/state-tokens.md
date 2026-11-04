# State and emphasis tokens

2. **State & emphasis tokens in the wrong place (Change Requested).** The `[-{emphasis}][-{state}]` segments must match the selector they sit behind, **and** must resolve to a colour that actually differs from what they sit against. Never judge this from the token name; resolve it first:

   ```bash
   rg -n -- '--neutral-background-disabled:|--surface-border-raised:' <the project's generated token CSS>
   ```

   Check the light and dark blocks **independently**; a token can be correct in one theme and collide in the other. Failure modes:
   - **State/selector mismatch.** A `-disabled` token outside a disabled selector, or a disabled selector painting a non-`-disabled` token (e.g. `disabled:text-neutral-foreground-subtle` where every sibling control uses `-subtle-disabled`. Same for a `-hover` token at rest, or a `hover:` rule repainting the resting token.
   - **No-op state.** The state token resolves to the same primitive as the state it must be distinguishable from, so the state is invisible. E.g. a disabled row on `neutral-background-disabled` (dark-2) sitting on a surface already at `surface-background-raised` (dark-2); or a `-disabled` border equal to the resting border. Compare against the *sibling* state, not just against the background.
   - **Rule that can never paint.** A `disabled:border-*` on an element that also sets `border-0`, or a colour rule outranked by a more specific one. Trace width and cascade before assuming a state rule works.
   - **Wrong disabled guard for the element.** `disabled:`/`enabled:` only match native form controls. A `<div>` zone needs `aria-disabled:`, a Reka primitive needs `data-disabled:`/`in-data-disabled:`, a wrapper around a disabled input needs `has-[:disabled]:`. That variation is essential. Do **not** flag it as inconsistency. Do flag two spellings of one guard for the same rule in a single change (`enabled:` and `not-disabled:` both used on native controls).
   - **Interaction state clobbering a selected state.** A `hover:`/`focus:` colour at equal-or-higher specificity than the `checked`/`selected`/`on` rule repaints an active control on hover. It must be scoped (`data-[state=unchecked]:hover:`) or sit below the selected rule.
