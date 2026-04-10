# Interface Design for Testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them**

   ```
   // Testable: function accepts its dependencies
   function getItemStatus(item: Item): Status {
     return item.provisioningStatus === "LIVE" ? Status.Active : Status.Pending
   }

   // Hard to test: function fetches its own dependencies
   function getItemStatus(itemId: string): Status {
     item = globalStore.getById(itemId)
     return item.provisioningStatus === "LIVE" ? Status.Active : Status.Pending
   }
   ```

2. **Return results, don't produce side effects**

   ```
   // Testable: returns a result object
   function validateName(name: string): { valid: boolean, error: string | null } {
     if (!name.trim()) return { valid: false, error: "Name is required" }
     if (name.length > 100) return { valid: false, error: "Name must be 100 characters or fewer" }
     return { valid: true, error: null }
   }

   // Hard to test: mutates external state
   function validateName(name: string, errors: ErrorList): void {
     errors.clear()
     if (!name.trim()) errors.add("Name is required")
   }
   ```

3. **Small surface area**
   - Fewer inputs = simpler test setup
   - Fewer outputs / callbacks = fewer assertions needed
   - Extract complex logic into standalone functions — keeps orchestration layers thin and testable
   - If a module is hard to test, it's probably doing too much. Extract logic and test it directly.
