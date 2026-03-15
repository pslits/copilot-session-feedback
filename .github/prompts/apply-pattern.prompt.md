---
description: Explain a named agentic design pattern (from Gulli or Arsanjani/Bustos) and show how to apply it to a given scenario.
agent: ask
argument-hint: "pattern name and scenario (e.g., Circuit Breaker for a loan processing agent, or Reflection pattern for a code review agent)"
---

Apply the agentic design pattern specified in the request to the described scenario.

Read [.github/skills/agentic-patterns/references/patterns-catalogue.md](../skills/agentic-patterns/references/patterns-catalogue.md) to look up the pattern before answering. The catalogue covers both Gulli (Parts 1–4, 21 patterns) and Arsanjani/Bustos (Part 5, 20 architectural patterns).

## Instructions

1. Identify the pattern named in `${input:pattern and scenario (e.g., Reflection pattern for a code review pipeline)}`.
2. Look up the pattern in the catalogue: read its description, when-to-use guidance, variants, and key considerations.
3. Explain the pattern in plain language (2–3 sentences).
4. Describe exactly how it applies to the user's scenario:
   - What inputs enter the pattern
   - What the pattern does (step by step, specific to this scenario)
   - What output it produces
5. List 1–3 concrete implementation tips relevant to this scenario.
6. Call out the most important key consideration from the catalogue as a warning.
7. Suggest one complementary pattern from the catalogue that pairs well with this one, with a one-sentence reason.

## Constraints

- Only use information from the patterns catalogue. Do not invent pattern behaviours.
- Do not write code or create files.
- If the named pattern is not in the catalogue, say so and list the closest match.

## Output Format

### Pattern: [Name] — [Tier]
[Plain-language explanation of the pattern]

### Applied to: [Scenario Summary]
**Flow:**
1. [Input] → [Step] → [Output]
2. ...

**Implementation tips:**
- ...

**Key consideration:** [Warning from catalogue]

**Pairs well with:** [Pattern name] — [One sentence reason]
