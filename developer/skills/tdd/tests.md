# Good and Bad Tests

## Good vs Bad

**Good**: Tests observable behavior through public output and user interaction.

```
// GOOD: Tests what the user sees
test("displays item name when loaded")
  render(ItemCard, { item: mockItem })
  expect(screen.findByText("My Item")).toBeVisible()
```

**Bad**: Tests implementation details — internal state, method calls, private internals.

```
// BAD: Tests internal state
test("sets itemName field")
  component = mount(ItemCard, { item: mockItem })
  expect(component.internal.itemName).toBe("My Item")
```

Red flags:

- Accessing internal state to check values that are visible in output
- Mocking child modules you own
- Asserting on internal events when you could test the consumer's reaction instead
- Test name describes HOW not WHAT
- Querying by CSS class or internal selector instead of accessible/semantic queries

---

## UI / Component Tests

Render the component, interact with it as a user would, assert on visible output.

```
test("displays item name in heading")
  render(ItemDetail, { id: "abc-123" })
  expect(findByRole("heading", { name: "My Item" })).toBeVisible()

test("shows validation error for empty name")
  render(ItemDetail, { id: "abc-123" })
  clearInput(findByLabel("Item Name"))
  tabAway()
  expect(findByText("Item name is required")).toBeVisible()
```

If your project has a custom render wrapper (auto-injects stores, routing, etc.), prefer that over raw framework render utilities.

### With framework context

When a component needs framework services (state store, router, etc.), provide them at render time:

```
test("renders component with store and router defaults")
  render(ItemList, {
    props: { items: mockItems },
    plugins: [createTestStore(), testRouter],
  })
  expect(findByRole("list")).toBeVisible()
```

---

## Stateful Logic Tests

Functions with stateful or reactive inputs — call directly, assert on outputs.

**No dependencies** — call directly:

```
test("filters items by search term")
  items = observable([
    { name: "Alpha Widget", id: "1" },
    { name: "Beta Service", id: "2" },
  ])
  search = observable("Widget")

  result = filterItems(items, search)

  expect(result).toHaveLength(1)
  expect(result[0].name).toBe("Alpha Widget")
```

**With dependencies** (DI context, router, store) — use a thin test harness that provides the context:

```
test("returns current environment from context")
  result = callWithContext(
    () => useEnvironment(),
    { provide: { environment: "staging" } }
  )
  expect(result.currentEnv).toBe("staging")
```

**Reactive updates** — verify logic responds to input changes:

```
test("re-filters when search term changes")
  items = observable([{ name: "Alpha" }, { name: "Beta" }])
  search = observable("")

  result = filterItems(items, search)
  expect(result).toHaveLength(2)

  search.set("Alpha")
  awaitUpdate()
  expect(result).toHaveLength(1)
```

---

## State Store Tests

Initialize a fresh store instance per test. Use real stores, not mocks.

```
describe("notificationStore")
  beforeEach()
    store = createFreshStore()

  test("adds notification")
    store.addNotification({ message: "Item created", type: "success" })
    expect(store.notifications).toHaveLength(1)
    expect(store.notifications[0].message).toBe("Item created")

  test("removes notification by id")
    store.addNotification({ id: "n1", message: "Done", type: "success" })
    store.removeNotification("n1")
    expect(store.notifications).toHaveLength(0)
```

---

## Pure Logic Tests

No framework setup needed — just import and call:

```
describe("validateItemName")
  test("accepts valid name")
    result = validateItemName("My Item")
    expect(result).toEqual({ valid: true, error: null })

  test("rejects empty name")
    result = validateItemName("")
    expect(result).toEqual({ valid: false, error: "Item name is required" })

  test("rejects name exceeding max length")
    result = validateItemName("a" * 101)
    expect(result).toEqual({ valid: false, error: "Name must be 100 characters or fewer" })
```

### Schema validation

```
test("rejects item without required fields")
  result = itemSchema.validate({ name: "" })
  expect(result.success).toBe(false)

test("accepts valid item data")
  result = itemSchema.validate({ name: "My Item", rateLimit: 1000 })
  expect(result.success).toBe(true)
```


