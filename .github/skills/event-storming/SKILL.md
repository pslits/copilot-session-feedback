```skill
---
name: event-storming
description: "Performs Event Storming analysis in three phases (Big Picture, Process Modeling, Software Design) following Brandolini's methodology with agent-adapted facilitation scripts. Supports reverse (code to ES artifacts) and forward (requirements to ES artifacts) directions. Produces domain event timelines, process models, aggregate cards, bounded context maps, integration contracts, and Five Views. Use when: analysing code to discover domain events, modelling business processes from code or requirements, extracting aggregates and bounded contexts, or performing DDD discovery. Triggers on: 'event storm', 'event storming', 'big picture', 'process model', 'software design', 'domain events', 'domain events from code', 'requirements to events', 'bounded context', 'aggregate discovery', 'DDD discovery', 'ubiquitous language'. Do not use for: code generation, writing agents or skills or prompts, implementing domain models, or running workshops."
metadata:
  version: "1.0.0"
  author: "Paul Slits"
---

# Event Storming

Perform agent-driven Event Storming analysis on code or requirements.

## Mode Selection

Determine the mode from the user's request and the input material:

| Input Material | Direction | Start Phase | Phases Run |
|---------------|-----------|-------------|------------|
| Source code (files, directories, repository) | Reverse | Big Picture | All 3 in sequence |
| Requirements (user stories, PRD, acceptance criteria) | Forward | Big Picture | All 3 in sequence |
| Existing Big Picture output | Either | Process Modeling | Phase 2 → 3 |
| Existing Process Model output | Either | Software Design | Phase 3 only |

All phases run sequentially. Each phase produces a reviewable artifact and
pauses for human approval before the next phase begins.

---

## Phase 1 — Big Picture

Goal: Produce a domain event timeline with hot spots, opportunities, external
systems, and bounded context candidates.

### Reverse direction (code → events)

1. Read [references/notation-reference.md](references/notation-reference.md) for the notation system.
2. Read [references/code-analysis-heuristics.md](references/code-analysis-heuristics.md) for extraction patterns.
3. Read [references/facilitation-scripts.md](references/facilitation-scripts.md) — follow steps BP-1 through BP-16.
4. Analyse the target code using the heuristics. For each file or module, identify domain events, commands, actors, external systems, policies, and hot spots.
5. Produce the Big Picture output using [references/output-templates.md](references/output-templates.md) — Big Picture Output Template.
6. Validate all notation elements against the notation reference grammar rules.
7. Present the timeline and goal metrics. Wait for human approval before proceeding.

### Forward direction (requirements → events)

1. Read [references/notation-reference.md](references/notation-reference.md) for the notation system.
2. Read [references/requirements-intake-guide.md](references/requirements-intake-guide.md) for extraction patterns.
3. Follow the intake contract: declare input format, extract verbatim quotes, assign confidence levels, flag gaps.
4. Read [references/facilitation-scripts.md](references/facilitation-scripts.md) — follow steps BP-1 through BP-16.
5. Produce the Big Picture output using [references/output-templates.md](references/output-templates.md) — Big Picture Output Template.
6. Validate all notation elements against the notation reference grammar rules.
7. Present the timeline, extraction summary, and goal metrics. Wait for human approval.

---

## Phase 2 — Process Modeling

Goal: Model detailed business processes with commands, policies, and read models.

1. Receive the approved Big Picture output from Phase 1 (or as input if starting at Phase 2).
2. Read [references/facilitation-scripts.md](references/facilitation-scripts.md) — follow steps PM-1 through PM-10.
3. For each process identified, model the happy path using the PM grammar: `Actor → Command → System → Event`.
4. Identify policies (reactive rules), read models (decision-supporting data), and variations (exception paths).
5. Cross-reference with the Big Picture timeline to verify all events are covered.
6. Produce the Process Modeling output using [references/output-templates.md](references/output-templates.md) — Process Modeling Output Template.
7. Validate grammar compliance: every command maps to ≥1 event, no orphaned events.
8. Present the process models and goal metrics. Wait for human approval before proceeding.

---

## Phase 3 — Software Design

Goal: Produce aggregates, bounded contexts, integration contracts, and the Five Views.

1. Receive the approved Process Model output from Phase 2 (or as input if starting at Phase 3).
2. Read [references/facilitation-scripts.md](references/facilitation-scripts.md) — follow steps SD-1 through SD-9.
3. Identify candidate aggregates by grouping commands and events that share a lifecycle (create, update, delete, query).
4. Answer the four lifecycle questions for each aggregate.
5. Assign aggregates to bounded contexts based on cohesion (shared vocabulary, actors, lifecycle transitions).
6. Define integration contracts between bounded contexts.
7. Compile the Five Views: Next Actions, Domain Definitions, Context Map, User Stories, Integration Contracts.
8. Produce the Software Design output using [references/output-templates.md](references/output-templates.md) — Software Design Output Template + Five Views Template.
9. Validate aggregate completeness (≥1 command, ≥1 event, lifecycle answers, context assignment).
10. Present the full Software Design deliverable, Five Views, and goal metrics. This is the final review gate.

---

## Notation Rules (Quick Reference)

All phases must follow these rules from the notation reference:

- Domain events: past tense, space-separated (`Order Placed`, not `Place Order`)
- Commands: imperative mood, space-separated (`Place Order`, not `Order Placed`)
- Aggregates: singular nouns (`Order`, not `Orders`)
- Policies: "Whenever [event], then [command]" — always state trigger and result
- Grammar flow: `Actor → Command → Aggregate → Event → (Read Model | Policy → Command | External System)`
- Process Modeling grammar: `Event → Policy → Command → System → Event`
- Hot spots mark uncertainty — they are questions, not answers
- Opportunities mark positive discoveries — ideas, not problems

For the full notation system, read [references/notation-reference.md](references/notation-reference.md).

---

## Recovery Procedures

| Situation | Action |
|-----------|--------|
| Zero domain events found in code analysis | Broaden scope (parent directory, additional modules). If still zero, escalate to human with scope and heuristics tried. |
| Zero domain events found in requirements | Check if input is too high-level (epic-level). Flag as Hot Spot and ask human for more detailed requirements. |
| Ambiguous aggregate boundaries | Present candidates with reasoning. Let human decide grouping. |
| Contradictory domain events | Create Hot Spots for each contradiction. Include both versions. Do not resolve silently. |
| Output exceeds practical length | Split into bounded-context-scoped deliverables. Present an index document linking to each context's output. |
| Prior phase output missing or corrupt | Do not proceed. Escalate to human: "Phase N output is required but missing. Please provide it or re-run Phase N." |
```
