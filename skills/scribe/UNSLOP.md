# Unslop

A catalogue of the tells of machine-written prose. `proof-read` hunts each tell in Pass 4, and names each tell that it flags by its ID. Source: pstack `unslop` (https://github.com/cursor/plugins/tree/main/pstack).

## ID rule

An ID has a group prefix and a number, such as `V3`. An ID never changes and is never reused. A new tell takes the next number in its group. A retired tell keeps its row, marked retired.

A tell is a sign, not a fault. Flag it only when the sentence reads as filler. A term of art, or a word that the document defines, stays.

## V: Vocabulary

| ID | Tell | Example | Fix |
| -- | ---- | ------- | --- |
| V1 | `delve`, `dive into`, `explore` for "look at" | "Let us delve into the cache." | "The cache works like this." |
| V2 | `leverage`, `utilise`, `harness` for "use" | "We leverage the queue." | "We use the queue." |
| V3 | `seamless`, `effortless`, `frictionless` | "A seamless login." | State what the user does. Cut the word. |
| V4 | `robust`, `powerful`, `comprehensive`, `cutting-edge` | "A robust parser." | Name the property: "The parser rejects bad input." |
| V5 | `tapestry`, `landscape`, `realm`, `ecosystem` as a figure | "The tooling landscape." | Name the thing: "The tools." |
| V6 | `crucial`, `pivotal`, `vital`, `paramount` | "It is crucial to back up." | "Back up first." |
| V7 | `streamline`, `elevate`, `unlock`, `empower` | "This unlocks faster builds." | "Builds are faster." |
| V8 | `showcase`, `underscore`, `highlight` for "show" | "The test underscores the fault." | "The test shows the fault." |

## P: Stock phrases

| ID | Tell | Example | Fix |
| -- | ---- | ------- | --- |
| P1 | "It is worth noting that" and its kin | "It is worth noting that the cache expires." | Cut the opener: "The cache expires." |
| P2 | An opener about the age or the world | "In today's fast-paced world, teams ship daily." | Start with the claim. |
| P3 | A guide to the text | "Let's dive in." / "Let us break this down." | Cut it. Start the first step. |
| P4 | A closing summary that restates the body | "In summary, we covered A, B, and C." | Cut it, or give one next action. |
| P5 | A sycophantic opener | "Great question!" | Answer the question. |
| P6 | An offer at the end | "I hope this helps. Let me know if you need more." | Cut it. |
| P7 | "When it comes to", "in terms of", "in order to" | "In order to deploy, run the script." | "To deploy, run the script." |
| P8 | A claim of importance in place of the reason | "This is a game changer." | State the effect and its size. |

## S: Structure

| ID | Tell | Example | Fix |
| -- | ---- | ------- | --- |
| S1 | A "not X, but Y" contrast where nobody claimed X | "This is not a cache, but a contract." | Say Y. |
| S2 | A rule-of-three list that pads the claim | "Fast, reliable, and scalable." | Keep the items that the evidence supports. |
| S3 | An em dash used as a connector | "The job fails -- often at night." | Use a full stop, a comma, or two sentences. |
| S4 | A heading in title case | "## Getting Started With The Queue" | Use sentence case: "Getting started with the queue". |
| S5 | A question that the next sentence answers | "Why does this matter? Because the queue fills." | State the answer. |
| S6 | A bullet list of one-line items that need prose, or the reverse | Five bullets that form one argument. | Match the form to the content. |
| S7 | Bold on a phrase in every paragraph | "The **key insight** is that..." | Keep bold for terms and warnings. |
| S8 | Parallel sentence openers in a run | "It is fast. It is simple. It is safe." | Join the ideas, or vary the shape. |

## H: Hedging and filler

| ID | Tell | Example | Fix |
| -- | ---- | ------- | --- |
| H1 | A stacked qualifier | "This may potentially cause issues." | "This can cause issues." Or state the condition. |
| H2 | `arguably`, `essentially`, `fundamentally`, `basically` | "It is essentially a queue." | "It is a queue." |
| H3 | `very`, `really`, `quite`, `highly` before an adjective | "A highly effective fix." | Cut it, or give the measure. |
| H4 | A hedge on a fact that the author knows | "This should generally return a list." | State what it returns, and the one case that differs. |
| H5 | `Additionally`, `Furthermore`, `Moreover` as a sentence opener | "Furthermore, the job retries." | Cut the connector, or use "also". |
| H6 | A claim of effort or care in place of the work | "We carefully considered every option." | Name the options and the choice. |
| H7 | A vague noun that stands for a real one | "various aspects", "a number of factors" | Name the aspects and the factors. |
