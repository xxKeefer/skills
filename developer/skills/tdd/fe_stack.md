# Frontend Stack Context

> Load this context when the TDD task touches frontend code.

**Test runner:** Vitest
**Component testing:** `@testing-library/vue` with `render` / `screen` / `userEvent`
**Mocking:** `vi.mock`, `vi.fn`, `vi.useFakeTimers`
**State management:** Pinia (`setActivePinia(createPinia())` per test)
**Data fetching:** TanStack Query (mock query option factories)
**Routing:** `vue-router-mock` (`createRouterMock` / `injectRouterMock`)
**Validation:** Zod schemas
**File conventions:** `*.spec.ts` (tests), `*.mocks.ts` (mocks), colocated as siblings

---

## Component Tests

### Using `@testing-library/vue`

```typescript
import { render, screen } from "@testing-library/vue"
import userEvent from "@testing-library/user-event"

describe("EditServiceDetails", () => {
  test("displays service name in heading", () => {
    render(EditServiceDetails, { props: { serviceUid: "abc-123" } })
    expect(screen.getByRole("heading", { name: "My Service" })).toBeInTheDocument()
  })

  test("shows validation error for empty name", async () => {
    const user = userEvent.setup()
    render(EditServiceDetails, { props: { serviceUid: "abc-123" } })

    const input = screen.getByLabelText("Service Name")
    await user.clear(input)
    await user.tab()

    expect(screen.getByText("Service name is required")).toBeInTheDocument()
  })
})
```

If your project has a custom `render` wrapper (auto-creates store, router, etc.), prefer that over the raw `@testing-library/vue` render.

### With framework defaults (Pinia, Router stubs, etc.)

When a component needs framework context, provide plugins via `global`:

```typescript
import { render, screen } from "@testing-library/vue"

test("renders component with store and router defaults", () => {
  render(ServiceList, {
    props: { services: mockServices },
    global: {
      plugins: [createTestingPinia(), router],
    },
  })
  expect(screen.getByRole("list")).toBeInTheDocument()
})
```

### Red flags

- Accessing `wrapper.vm` to check internal state
- Mocking child components you own
- Asserting on emitted events when you could test the parent's reaction instead
- Using `wrapper.find('.class-name')` instead of accessible queries

---

## Composable Tests

Composables are just functions — test them by calling them with reactive inputs and asserting on reactive outputs.

**No injection dependencies** — call directly:

```typescript
import { ref } from "vue"
import { useServiceFilter } from "./useServiceFilter"

test("filters services by search term", () => {
  const services = ref([
    { name: "Sydney VXC", uid: "1" },
    { name: "Melbourne Port", uid: "2" },
  ])
  const search = ref("VXC")

  const { filtered } = useServiceFilter(services, search)

  expect(filtered.value).toHaveLength(1)
  expect(filtered.value[0].name).toBe("Sydney VXC")
})
```

**With injection dependencies** (inject, provide, router, store) — mount a thin wrapper component:

```typescript
import { defineComponent, h } from "vue"
import { render, screen } from "@testing-library/vue"

function renderComposable<T>(composable: () => T, options?: { provide?: Record<string, unknown> }) {
  let result!: T
  const Wrapper = defineComponent({
    setup() {
      result = composable()
      return () => h("div")
    },
  })
  render(Wrapper, { global: { provide: options?.provide } })
  return result
}

test("returns current environment from injection", () => {
  const { currentEnv } = renderComposable(() => useEnvironment(), {
    provide: { environment: "staging" },
  })
  expect(currentEnv.value).toBe("staging")
})
```

**Reactive updates** — verify composables respond to input changes:

```typescript
test("re-filters when search term changes", async () => {
  const services = ref([{ name: "Alpha" }, { name: "Beta" }])
  const search = ref("")

  const { filtered } = useServiceFilter(services, search)
  expect(filtered.value).toHaveLength(2)

  search.value = "Alpha"
  await nextTick()
  expect(filtered.value).toHaveLength(1)
})
```

---

## Pinia Store Tests

```typescript
import { setActivePinia, createPinia } from "pinia"
import { useNotificationStore } from "./notificationStore"

describe("notificationStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test("adds notification", () => {
    const store = useNotificationStore()
    store.addNotification({ message: "Service created", type: "success" })
    expect(store.notifications).toHaveLength(1)
    expect(store.notifications[0].message).toBe("Service created")
  })

  test("removes notification by id", () => {
    const store = useNotificationStore()
    store.addNotification({ id: "n1", message: "Done", type: "success" })
    store.removeNotification("n1")
    expect(store.notifications).toHaveLength(0)
  })
})
```

---

## Mocking

### API/SDK Mocking

Mock the SDK or API client at the module level:

```typescript
vi.mock("@/api/sdk", () => ({
  getService: vi.fn().mockResolvedValue(mockService),
  listServices: vi.fn().mockResolvedValue([mockService]),
}))
```

Only provide the methods your test exercises. Unlisted methods will be `undefined`, which surfaces unexpected calls immediately.

If your project provides a dedicated SDK mock utility, prefer that over raw `vi.mock`.

### TanStack Query Mocking

Mock query option factories at the module level, then override per-test as needed:

```typescript
// In colocated mock file alongside the real module
vi.mock("@/api/queryOptions/billing", () => ({
  balanceQuery: () => ({
    queryKey: ["balance"],
    queryFn: vi.fn().mockResolvedValue({ balance: 1000, currency: "USD" }),
  }),
}))
```

Then in tests:

```typescript
vi.mock("@/api/queryOptions/billing")

test("displays balance from query", () => {
  render(BillingDashboard)
  expect(screen.getByText("$1,000.00")).toBeInTheDocument()
})
```

Override default mock data for specific tests:

```typescript
import { balanceQuery } from "@/api/queryOptions/billing"

test("shows zero balance state", () => {
  vi.mocked(balanceQuery).mockReturnValue({
    queryKey: ["balance"],
    queryFn: vi.fn().mockResolvedValue({ balance: 0, currency: "USD" }),
  })
  render(BillingDashboard)
  expect(screen.getByText("No balance")).toBeInTheDocument()
})
```

### Module / Composable Mocking

```typescript
vi.mock("./usePermissions", () => ({
  usePermissions: () => ({
    canEdit: ref(true),
    canDelete: ref(false),
  }),
}))
```

Place `vi.mock` calls at the top of the file — Vitest hoists them automatically.

### Vue Router Mocking

Use `vue-router-mock` for router testing:

```typescript
import { createRouterMock, injectRouterMock } from "vue-router-mock"

const router = createRouterMock({ initialLocation: "/services/abc-123" })

beforeEach(() => {
  injectRouterMock(router)
})

test("navigates to detail page", async () => {
  render(ServiceList)
  await userEvent.click(screen.getByText("My Service"))
  expect(router.push).toHaveBeenCalledWith(expect.objectContaining({ name: "service-detail" }))
})
```

If your project's `render` wrapper handles router automatically, you may not need this.

### Time Mocking

```typescript
beforeEach(() => {
  vi.useFakeTimers()
})

afterEach(() => {
  vi.useRealTimers()
})

test("debounces search input", async () => {
  render(SearchBar)
  await userEvent.type(screen.getByRole("searchbox"), "query")
  expect(screen.queryByText("Results")).not.toBeInTheDocument()

  await vi.advanceTimersByTimeAsync(300)
  expect(screen.getByText("Results")).toBeInTheDocument()
})
```

---

## Interface Design

### Accept dependencies via reactive inputs

```typescript
// Testable: composable accepts reactive input
function useServiceStatus(service: Ref<Service>) {
  return computed(() => service.value.provisioningStatus === "LIVE")
}

// Hard to test: composable hides Vuex dependency
function useServiceStatus(serviceUid: string) {
  const store = useStore()
  const service = store.getters["Services/byUid"](serviceUid)
  return computed(() => service.provisioningStatus === "LIVE")
}
```

### Vue-specific surface area

- Fewer props/emits = fewer tests needed
- Prefer composables for complex logic — keeps components thin and testable
- If a component is hard to test, it's probably doing too much. Extract logic into a composable and test that directly.

---

## Migration Opportunities

While refactoring, consider if the code you touched can be incrementally migrated:

- Options API -> `<script setup>` Composition API
- JavaScript -> TypeScript
- Legacy UI library -> modern component library
- SCSS / `<style>` blocks -> utility-first CSS (Tailwind, UnoCSS, etc.)
- Legacy state management -> Pinia
- Direct API calls -> TanStack Query
- `@vue/test-utils` mount/wrapper -> `@testing-library/vue` render/screen

These are opportunistic — only migrate what you're already touching and when it's safe to do so. Don't expand scope beyond the current task.

---

## Zod Schema Testing

```typescript
import { serviceSchema } from "./schemas"

test("rejects service without required fields", () => {
  const result = serviceSchema.safeParse({ name: "" })
  expect(result.success).toBe(false)
})

test("accepts valid service data", () => {
  const result = serviceSchema.safeParse({ name: "My Service", rateLimit: 1000 })
  expect(result.success).toBe(true)
})
```
