# persona-api-integrity diff signals

One line per catalogue case this persona owns that can be seen in a diff. After applying your numbered rules, check every changed hunk against these lines. Report a match only when you can name the changed line, the input or steps that break it, and the wrong result; otherwise drop it. Lines marked `(rule N)` are already covered by that rule. The full case (cause, inputs, fix, sources) is in the linked catalogue under the same ID.

## [persona-form-behaviour catalogue](../../persona-form-behaviour/references/catalogue.md)

- FM-D13: Magic numbers in a Zod schema such as `.max(10000)`, or bound constants duplicated instead of taken from the API or spec → Source bounds from product metadata or the generated schema [default: change-requested]

## [persona-value-display catalogue](../../persona-value-display/references/catalogue.md)

- DS-L2: Response Zod schema uses `.optional()` where the spec says `nullable: true`, or `.parse()` on a response where `.safeParse()` with fallback was meant → `.nullish()` or `.nullable()` to match the spec [default: change-requested] (rule 3)
