# Refactor Candidates

After TDD cycle, look for:

- **Duplication** -> Extract function/class
- **Long methods** -> Break into private helpers (keep tests on public interface)
- **Shallow modules** -> Combine or deepen
- **Feature envy** -> Move logic to where data lives
- **Primitive obsession** -> Introduce value objects
- **Existing code** the new code reveals as problematic

## Incremental Modernization

While refactoring, consider if the code you touched can be incrementally migrated toward current project conventions. These are opportunistic — only migrate what you're already touching and when it's safe to do so. Don't expand scope beyond the current task.
