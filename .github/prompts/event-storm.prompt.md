---
description: Run an event-storming session on code or requirements to produce domain events, aggregates, and bounded contexts.
agent: event-storming
tools:
  - read
  - search
argument-hint: "direction and scope (e.g., reverse-engineer src/ or forward from requirements.md)"
---

Run a full Event Storming session (Big Picture → Process Modeling → Software Design) on the target described below.

## Target

`${input:scope:direction and target (e.g., reverse src/orders/ or forward from docs/requirements.md)}`

## Instructions

1. Detect whether the target above implies **reverse** (code → ES) or **forward** (requirements → ES).
2. Identify the specific files, directories, or documents to analyse.
3. Produce a scope plan covering direction, target, domain, phases, and expected deliverables.
4. Present the scope plan for confirmation before starting analysis.
5. Execute all three phases sequentially: Big Picture, Process Modeling, Software Design.
6. At the end of each phase, present the output and goal metrics for review before proceeding.

## Constraints

- Read all source material fully before producing any output — never speculate about code or requirements you have not read.
- Follow the event-storming skill notation and grammar rules exactly.
- Do not skip human review gates between phases.
- Do not generate implementation code — the output is domain models, not source code.
