---
description: Generate event-storming artifacts from requirements to produce domain events, aggregates, and bounded contexts.
agent: event-storming
tools:
  - read
  - search
argument-hint: "requirements file (e.g., docs/requirements.md or docs/user-stories.md)"
---

Generate Event Storming artifacts from the requirements document specified below.

**Direction: Forward (requirements → Event Storming)**

## Target Requirements

`${input:requirements file:path to requirements document (e.g., docs/requirements.md or docs/prd.md)}`

## Instructions

1. Use the requirements file above as the analysis scope.
2. The direction is **forward** — do not ask. Proceed directly with requirements analysis.
3. Produce a scope plan, then execute all three phases: Big Picture, Process Modeling, Software Design.
4. Apply the requirements-intake heuristics to extract domain events, commands, actors, and external systems from the requirements.
5. Present output and goal metrics at the end of each phase for review.

## Constraints

- Read the requirements document fully before producing any output — never speculate about requirements you have not read.
- Follow the event-storming skill notation and grammar rules exactly.
- Do not skip human review gates between phases.
- Do not generate implementation code — the output is domain models, not source code.
