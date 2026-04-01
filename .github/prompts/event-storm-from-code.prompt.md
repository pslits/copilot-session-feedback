---
description: Reverse-engineer event-storming artifacts from existing code to discover domain events, aggregates, and bounded contexts.
agent: event-storming
tools:
  - read
  - search
argument-hint: "code path or pattern (e.g., src/orders/ or **/*.py)"
---

Reverse-engineer Event Storming artifacts from the existing code specified below.

**Direction: Reverse (code → Event Storming)**

## Target Code

`${input:code path:code path or glob pattern to analyse (e.g., src/orders/ or **/*.py)}`

## Instructions

1. Use the target code path above as the analysis scope.
2. The direction is **reverse** — do not ask. Proceed directly with code analysis.
3. Produce a scope plan, then execute all three phases: Big Picture, Process Modeling, Software Design.
4. Apply the code-analysis heuristics to extract domain events, commands, actors, and external systems from the source code.
5. Present output and goal metrics at the end of each phase for review.

## Constraints

- Read all source files fully before producing any output — never speculate about code you have not opened.
- Follow the event-storming skill notation and grammar rules exactly.
- Do not skip human review gates between phases.
- Do not generate implementation code — the output is domain models, not source code.
