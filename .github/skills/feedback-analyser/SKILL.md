---
name: feedback-analyser
description: Applies the four diagnostic lenses (Recurring Correction, Domain Vocabulary, Workflow Friction, Quality Guardrail) to a compaction summary and returns a structured routing table mapping each finding to an integration surface. Use after running /compact when analysis of a session is needed. Triggers on: "analyze session", "apply lenses", "classify findings", "feedback analysis", "route findings", "session routing", "lens analysis", "compact analysis".
---

# Feedback Analyser

Apply the four diagnostic lenses to a `/compact` output and produce a structured
routing table that maps each finding to the correct integration surface.

## Section 1 — When to Use

Use this skill after `/compact` has been run and a session summary with a
`## Corrections` table exists. Do **not** use it on raw transcripts or
partial session notes — the compact summary is the required input format.

**Adoption phase:** Week 4 and later. The lens procedure must be validated in
at least four sessions before this skill is loaded into an automated agent.
Prior to that, apply the lenses manually using
`.github/instructions/feedback-lenses.instructions.md`.

**Do not use when:**
- No `/compact` output exists for the session.
- The `## Corrections` table has zero rows.
- The session is still in progress.

## Section 2 — Input Requirements

Before starting, confirm the compact summary contains both of these sections:

| Required section | Content expected |
|-----------------|-----------------|
| `## What Was Tried` | Table of approaches attempted, outcomes, and reasons for abandonment |
| `## Corrections` | Table rows with `Observation`, `Pattern triggered`, `Candidate Action` |

If either section is absent or empty, report: _"Input incomplete — `[section name]`
is missing. Run `/compact` first."_ and stop.

**Quality gate before classifying:** only classify findings that appear in the
`## Corrections` table of **two or more** sessions. Single-occurrence findings
should be noted as observations but must not be routed to a surface.
Reason: routing one-off issues wastes Document stage capacity.

## Section 3 — Lens Routing Table

Apply lenses in order 1 → 4. Assign the **first matching** lens and stop
routing that finding. A finding must match exactly one lens.

| Lens | Classification criterion | Target surface | Observable test |
|------|--------------------------|----------------|-----------------|
| 1 — Recurring Correction | The agent made the same mistake in two or more sessions. | `copilot-instructions.md` rule | Ask: did this appear in a prior session correction? |
| 2 — Domain Vocabulary | The agent used the wrong project term or missed a project-specific name. | Scoped `*.instructions.md` | Ask: would a glossary or naming rule prevent this? |
| 3 — Workflow Friction | The developer repeated the same multi-step action two or more times. | `*.prompt.md` or `*.agent.md` | Ask: would a named command or delegated workflow remove the repetition? |
| 4 — Quality Guardrail | The agent nearly deleted, overwrote, or otherwise mishandled a sensitive operation. | Hook or safety guard | Ask: was this a dangerous tool action that needs a guardrail? |

**Ambiguity rule:** if a finding could match two lenses, assign the lower-numbered
lens. Reason: lower lenses address broader, higher-impact issues first.

**No-match rule:** if a finding matches no lens, log it in `sessions/feedback-debt.md`
under priority P3 and do not route it. Reason: unclassifiable findings may
become classifiable after recurrence.

## Section 4 — Output Format

Produce a single routing table after one pass through all findings:

```
## Session Routing — <date>

| # | Finding (from Corrections table) | Sessions seen | Lens | Target surface | Proposed action |
|---|-----------------------------------|---------------|------|----------------|-----------------|
| 1 | <observation text>                | 2             | 1    | copilot-instructions.md | Add rule: ... |
```

After the table, add a one-line summary:

> Routed N findings: L1=N, L2=N, L3=N, L4=N. Unrouted: N (logged to feedback-debt.md).

Keep the table and summary within **40 lines total**. Reason: the Document stage
needs a compact handoff, not a prose report.

## Section 5 — Quality Thresholds and Revision Budget

| Threshold | Value | Reason |
|-----------|-------|--------|
| Minimum recurrence to classify | 2 sessions | Prevents one-off issues consuming Document capacity |
| Passes per lens | 1 (one ordered pass) | Fixed revision budget; no re-iteration |
| Maximum findings to route per session | 2 (P0 or P1 only, excess → feedback-debt.md) | HITL gate-fatigue mitigation |
| Maximum output length | 40 lines | Resource-Aware; compact handoff for Document stage |

**Stop condition:** after completing the single ordered pass through all four
lenses, output the routing table and stop. Do not re-examine findings or attempt
a second pass. Reason: the Reflection pattern requires a fixed revision budget
to prevent audit fatigue.
