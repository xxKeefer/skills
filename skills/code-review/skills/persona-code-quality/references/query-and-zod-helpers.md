# persona-code-quality: query factory and zod id rules

**Don't propose a generic `<T>` helper over vue-query `queryOptions`.** Per-resource query factories that repeat the same `computed` key + `queryOptions` + client call body look like copy-paste, but folding them into `helper<T>(…, schema: z.ZodType<T>)` fails to typecheck: vue-query's `MaybeRefDeep<T>` can't resolve an unconstrained `T` under `exactOptionalPropertyTypes`, and the only way through is a cast. Leave concrete-type factories duplicated.

**Reuse the project's shared zod number primitives for API ids.** Where the project ships shared `int32()`/`uint32()` primitives, an inline `z.number().int()` (with or without `.positive()`) on a DTO id or count reinvents them and skips their int32 bounds. Suggest `int32().positive()` (or `uint32()`). Nit.
