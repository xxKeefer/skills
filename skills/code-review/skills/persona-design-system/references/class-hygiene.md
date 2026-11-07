# Class hygiene and theme tokens

6. **Class soup / CVA hygiene (Nit).** Long conditional class ternaries in templates or duplicated class clusters belong in a styles file using `cva`, with `compoundVariants` over nested ternaries. Variant maps must use semantic tokens.
7. **Arbitrary values (Nit).** `tw:w-[137px]`, `tw:text-[10px]` etc. Flag when a scale/token exists; allow when genuinely one-off.
8. **`@apply`-heavy CSS / JS `tailwind.config` theme extension (Nit/Future).** Tokens belong in the CSS-first `@theme` layer (the project's Tailwind config package or CSS), not JS config or `@apply` sheets.
