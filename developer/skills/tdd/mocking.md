# When to Mock

Mock at **system boundaries** only:

- **API / HTTP layer** — mock the SDK or API client module
- **Data-fetching / caching layer** — mock query factories or use a test client
- **External services** — third-party APIs, analytics, feature flags
- **Platform APIs** — storage, geolocation, clipboard, browser globals
- **Routing layer** — mock or stub the router
- **Time / clock** — fake timers for debounce, polling, animation

Don't mock:

- **Your own modules** — render them, call them, use them directly
- **Your own state stores** — use real instances initialized fresh per test
- **Internal collaborators** — if you need to mock it and you own it, the design needs work

---

## API / HTTP Mocking

Mock the SDK or API client at the module level:

```
mock("api/sdk", {
  getItem: stub().resolves(mockItem),
  listItems: stub().resolves([mockItem]),
})
```

Only provide the methods your test exercises. Unlisted methods should be undefined — surfaces unexpected calls immediately.

If your project provides a dedicated SDK mock utility, prefer that over raw module mocking.

---

## Data-Fetching Layer Mocking

Mock query/cache factories at the module level, then override per-test:

```
// Default mock (colocated mock file)
mock("api/queries/billing", {
  balanceQuery: () => ({
    key: ["balance"],
    fetcher: stub().resolves({ balance: 1000, currency: "USD" }),
  }),
})

// Override in specific test
test("shows zero balance state")
  mocked(balanceQuery).returns({
    key: ["balance"],
    fetcher: stub().resolves({ balance: 0, currency: "USD" }),
  })
  render(BillingDashboard)
  expect(findByText("No balance")).toBeVisible()
```

---

## Module Mocking

```
mock("./usePermissions", {
  usePermissions: () => ({
    canEdit: true,
    canDelete: false,
  }),
})
```

Place module mocks at the top of the file — most test runners hoist them automatically.

---

## Router Mocking

Create a mock router, inject it before each test:

```
router = createMockRouter({ initialPath: "/items/abc-123" })

beforeEach()
  injectRouter(router)

test("navigates to detail page")
  render(ItemList)
  click(findByText("My Item"))
  expect(router.push).toHaveBeenCalledWith({ name: "item-detail" })
```

If your project's render wrapper handles routing automatically, you may not need this.

---

## Time Mocking

```
beforeEach()
  useFakeTimers()

afterEach()
  useRealTimers()

test("debounces search input")
  render(SearchBar)
  type(findByRole("searchbox"), "query")
  expect(findByText("Results")).not.toBeVisible()

  advanceTime(300)
  expect(findByText("Results")).toBeVisible()
```
