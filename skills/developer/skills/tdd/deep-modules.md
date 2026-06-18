# Deep Module Pattern

Prefer **deep modules**: simple interfaces that hide significant complexity.

- **Deep module** = small API surface, rich functionality behind it. The caller gets power without needing to understand internals.
- **Shallow module** = complex interface relative to the functionality it provides. Adds cognitive overhead without meaningful abstraction.

```
Deep module:                    Shallow module (avoid):

┌─────────────────────┐         ┌─────────────────────────────────┐
│   Small Interface   │         │       Large Interface           │
├─────────────────────┤         ├─────────────────────────────────┤
│                     │         │  Thin Implementation            │
│  Deep Implementation│         └─────────────────────────────────┘
│                     │
│                     │
└─────────────────────┘
```

## In practice

- Functions/classes should do meaningful work behind a simple signature
- Avoid pass-through methods that just forward to another layer
- If a caller must understand the implementation to use the interface, the abstraction is leaking
- Fewer, more capable methods > many thin wrappers
- Exceptions and edge cases should be handled internally where possible, not pushed to callers

## Red flags

- Interface is nearly as complex as the implementation
- Changes require modifications across multiple layers
- Method does almost nothing itself, just delegates
- Callers need to coordinate multiple calls in a specific sequence for basic operations

## When designing interfaces, ask

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?
