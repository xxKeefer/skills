---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.vue"
---

## Code Style

- Follow the project's eslint/prettier config
- Terse simplicity is king; variable names excepted — as long as necessary to be descriptive
- Functional programming by default, other paradigms when it makes sense
- Explicit typing in TypeScript
- **IMPORTANT** do not ever use typescript enums, prefer POJO as const instead. "ObjectEnum Pattern"
- Wrap at 120 characters
- Prefer file-based routing for new pages
- Prefer @testing-library/vue over @vue/test-utils
- Prefer deep modules over shallow ones. See "Deep Module Pattern" below.
  - seek to combine and migrate shallow modules to deep ones
- Colocate tests as `*.spec.ts` siblings (not in `__tests__/` folders)
- Colocate mocks as `*.mocks.ts` siblings (not in `__mocks__/` folders)

### Avoid

#### Asserting On Styles In Unit Tests

bad:

```ts
expect(disabledOption.innerHTML).toContain("tw:cursor-not-allowed");
expect(enabledOption.innerHTML).toContain("tw:cursor-pointer");
```

good:

```ts
expect(disabledOption).toBeDisabled();
expect(enabledOption).toBeEnabled();
```

#### Typescript Enums

bad:

```ts
export enum ORDER_STATUS {
  PENDING = 'PENDING',
  PAID = 'PAID',
  SHIPPED = 'SHIPPED',
  DELIVERED = 'DELIVERED',
  CANCELLED = 'CANCELLED'
}
```

also bad — `Object.freeze` on an array widens to `readonly string[]`, and one codebase should use one form:

```ts
export const ORDER_STATUS = Object.freeze({
  PENDING: "PENDING",
  PAID: "PAID",
  SHIPPED: "SHIPPED",
  DELIVERED: "DELIVERED",
  CANCELLED: "CANCELLED",
});
```

prefer — `as const`, and derive the value type from it:

```ts
export const ORDER_STATUS = {
  PENDING: "PENDING",
  PAID: "PAID",
  SHIPPED: "SHIPPED",
  DELIVERED: "DELIVERED",
  CANCELLED: "CANCELLED",
} as const;

export type OrderStatus = (typeof ORDER_STATUS)[keyof typeof ORDER_STATUS];
```

#### Bang Operators

bad:

```ts
function findWidgetByName(name: string) {
  return screen.getAllByTestId("widget").find((w) => within(w).queryByText(name))!;
}
```

good:

```ts
function findWidgetByName(name: string) {
  const widget = screen.getAllByTestId("widget").find((w) => within(w).queryByText(name));
  if (!widget) throw new Error(`Widget "${name}" not found`);
  return widget;
}
```

## Separation of Concerns

- Vue `<script setup>` = **component UI logic only** (state, refs, event handlers, computed display values)
  - Extract all data-fetching to composables (useQuery/useMutation belong in composables, not components)
  - Extract complex business logic to utility functions
- Composables: **one product or resource each** (e.g. `useOrders`, not `useAllTheThings`)
  - Hide query/mutation internals behind a simple return interface
- Utils: **one domain per file** — don't group unrelated helpers together

## Deep Module Pattern

Prefer **deep modules**: simple interfaces that hide significant complexity.

- **Deep module** = small API surface, rich functionality behind it. The caller gets power without needing to understand internals.
- **Shallow module** = complex interface relative to the functionality it provides. Adds cognitive overhead without meaningful abstraction.

### In practice

- Functions/classes should do meaningful work behind a simple signature
- Avoid pass-through methods that just forward to another layer
- If a caller must understand the implementation to use the interface, the abstraction is leaking
- Fewer, more capable methods > many thin wrappers
- Exceptions and edge cases should be handled internally where possible, not pushed to callers

### Red flags

- Interface is nearly as complex as the implementation
- Changes require modifications across multiple layers
- Method does almost nothing itself, just delegates
- Callers need to coordinate multiple calls in a specific sequence for basic operations
