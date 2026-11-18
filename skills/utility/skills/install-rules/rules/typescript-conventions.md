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

prefer — `as const`, a plural name for the object and a singular name for the type, and derive the type with `ObjectValues`:

```ts
export type ObjectValues<T> = T[keyof T];

export const OrderStatuses = {
  Pending: "PENDING",
  Paid: "PAID",
  Shipped: "SHIPPED",
  Delivered: "DELIVERED",
  Cancelled: "CANCELLED",
} as const;

export type OrderStatus = ObjectValues<typeof OrderStatuses>;
```

Define `ObjectValues` once per codebase, in a shared types file, and import it.

A lookup with a key from outside (a URL, user input, an API) needs a guard. `OrderStatuses["toString"]` finds the inherited function, not `undefined`. Check the key against `Object.values(...)` first.

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

## Types

Make the compiler reject impossible states.

### Brand semantic primitives

Two values that share a primitive type but mean different things get different types. Validate once, when you create the value.

bad:

```ts
function transfer(from: string, to: string, amount: number) {}
```

good:

```ts
type AccountId = string & { readonly __brand: "AccountId" };
type Cents = number & { readonly __brand: "Cents" };

function transfer(from: AccountId, to: AccountId, amount: Cents) {}
```

Principle: `principle-type-system-discipline`.

### Model variants as a discriminated union

Do not use flags that must stay in sync. One `kind` field decides which other fields exist.

bad:

```ts
type Request = { loading: boolean; error?: Error; data?: Order };
```

good:

```ts
type Request =
  | { kind: "loading" }
  | { kind: "failed"; error: Error }
  | { kind: "loaded"; data: Order };
```

Principle: `principle-model-the-domain`.

### End each switch on a union with a `never` check

A new variant then fails at compile time, not at run time.

```ts
function label(request: Request): string {
  switch (request.kind) {
    case "loading":
      return "Loading";
    case "failed":
      return request.error.message;
    case "loaded":
      return request.data.id;
    default: {
      const unreachable: never = request;
      throw new Error(`Unhandled variant: ${JSON.stringify(unreachable)}`);
    }
  }
}
```

Principle: `principle-type-system-discipline`.

### Use `satisfies` before `as`

`satisfies` checks the shape and keeps the narrow type. `as` turns the check off. Use `as` only when no other form works, and write the reason beside it.

bad:

```ts
const routes = { home: "/", orders: "/orders" } as Record<string, string>;
```

good:

```ts
const routes = { home: "/", orders: "/orders" } as const satisfies Record<string, string>;
```

Principle: `principle-type-system-discipline`.

### Parse at the boundary, then trust the type

JSON, API responses, URL params, storage, and environment variables are untyped until a parse function returns the typed model. Inside the boundary, do not validate again and do not cast.

bad:

```ts
const order = (await response.json()) as Order;
```

good:

```ts
const order = parseOrder(await response.json());
```

Principle: `principle-boundary-discipline`.

### Use the simplest type that covers every value

Do not use an optional field that is always set. Do not use `any`; use `unknown` and narrow it. Do not add a generic or a wrapper type that removes no invalid state.

bad:

```ts
type User = { id: string; name?: string };
function load(input: any): User {}
```

good:

```ts
type User = { id: string; name: string };
function load(input: unknown): User {}
```

Principle: `principle-minimize-reader-load`.

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
