# Harden Criteria

Decision framework for replacing fragile language with durable alternatives.

## The Replacement Test

Before replacing a specific term, ask: "Does the specificity add value that the general term
loses?" If yes, keep it. If no, generalise.

## Categories

### Tool References

| Fragile | Durable | Keep specific when... |
|---------|---------|----------------------|
| "run Jest/Vitest/pytest" | "run the test suite" | the skill IS about that tool |
| "use grep/ripgrep" | "search for" | the command syntax matters |
| "open in VS Code" | "open in editor" | never -- editor choice is user's |
| "run ESLint" | "run the linter" | the skill configures that specific linter |

### Language References

| Fragile | Durable | Keep specific when... |
|---------|---------|----------------------|
| "TypeScript interface" | "type contract" or "interface" | the skill targets TS specifically |
| "Python decorator" | "wrapper/annotation pattern" | the skill targets Python specifically |
| "write a class" | "define the module/unit" | the pattern is class-specific |

### Framework References

| Fragile | Durable | Keep specific when... |
|---------|---------|----------------------|
| "React component" | "UI component" or "view unit" | the skill is React-specific |
| "Express middleware" | "request interceptor" or "middleware" | the concept is universal enough |
| "Redux store" | "state container" | the skill is Redux-specific |

### Temporal References

| Fragile | Durable |
|---------|---------|
| "as of v3.2" | remove or state the principle without version |
| "currently" | remove -- the skill IS the current state |
| "in 2024" | remove or replace with the underlying constraint |

### Prescriptive vs Intent-Based

| Over-prescribed | Intent-based |
|-----------------|-------------|
| "create a file called utils.ts" | "create a utility module" |
| "add a try-catch block" | "handle the error case" |
| "use a HashMap" | "use an appropriate lookup structure" |

## Edge Cases

- **Skill IS domain-specific**: if the skill only makes sense in one context (e.g. a TTRPG
  skill), domain language is not fragile -- it is precise. Do not generalise away the domain.
- **Specificity aids clarity**: "run the linter" is better than "run eslint", but "validate
  the schema" is worse than "run the JSON schema validator" when schema validation is the
  whole point.
- **User-facing output**: if the skill produces output the user reads, specific formatting
  instructions are durable (they define the skill's contract, not an implementation detail).
