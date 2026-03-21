# ADR-0015: Document ADK-to-VS Code Hook Equivalence

Date: 2026-03-20
Status: Accepted
HITL Issue: [#23](https://github.com/pslits/copilot-session-feedback/issues/23)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Chs. 13–15 provide reference implementations using Google's Agent Development Kit
(ADK), LangGraph, and CrewAI. All code examples in the companion GitHub repository
(PacktPublishing/Agentic-Architectural-Patterns-for-Building-Multi-Agent-Systems) use ADK as the
primary framework.

ADK's lifecycle callbacks (on_agent_start, on_tool_call, on_tool_response, on_agent_end) are the
direct equivalent of VS Code's hook events (SessionStart, PreToolUse, PostToolUse, SessionEnd).
However, nowhere in the `agentic-patterns` skill or catalogue is this equivalence stated.

A developer who has read the book and wants to apply the ADK examples to this framework has no
mapping table. They may conclude the framework is unrelated to the book's code examples, missing
the direct structural parallel.

Similarly, the book's ADK event payloads (which include trace IDs — connecting to ADR-0011) differ
in schema from VS Code hook stdin JSON. Documenting the mapping clarifies both the similarities
and the divergences.

---

## Decision

> **We decide to add an equivalence table to the Lifecycle Callbacks / AgentOps catalogue entry
> mapping ADK lifecycle events to VS Code hook events, and noting schema differences (particularly
> the trace ID gap addressed by ADR-0011).**

Equivalence mapping:

| ADK Event | VS Code Hook | Notes |
|---|---|---|
| on_agent_start | SessionStart | ADK includes trace_id; VS Code does not (see ADR-0011) |
| on_tool_call | PreToolUse | ADK has typed tool schema; VS Code uses stdin JSON |
| on_tool_response | PostToolUse | Similar structure |
| on_agent_end | SessionEnd / Stop | VS Code has two variants; ADK has one |
| on_compact / on_context_compress | PreCompact / PostCompact | VS Code-specific; no ADK equivalent |

---

## Consequences

### Positive
- Developers familiar with ADK can immediately map their knowledge to the VS Code framework.
- The trace ID gap (ADR-0011) is contextualised against ADK's native trace support.
- The catalogue becomes a useful bridge document, not just a reference sheet.

### Negative / Risks
- ADK evolves; the equivalence table may become stale. Add a "verified against ADK version X"
  note and a review trigger in the monthly audit.

### Neutral
- LangGraph and CrewAI equivalences are not in scope for this ADR — they can be added in a
  follow-up if the framework is used alongside those tools.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Add equivalence table to Lifecycle Callbacks catalogue entry | @pslits | 2026-04-03 | Done |
| Note ADK version the table was verified against | @pslits | 2026-04-03 | Done |
| Add review trigger for the equivalence table to monthly audit prompt | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

Equivalence table added to the Lifecycle Callbacks / AgentOps entry in
`.github/skills/agentic-patterns/references/patterns-catalogue.md`. The table maps all five ADK
lifecycle events to their VS Code hook counterparts, notes the `trace_id` schema gap (ADR-0011),
and is marked as verified against ADK 1.x with a review trigger for major version changes.
