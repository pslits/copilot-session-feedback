---
name: Feedback Lenses
description: Route compacted session findings through the four diagnostic lenses for surface selection.
applyTo: "sessions/**"
---

# Feedback Lenses

Apply the four diagnostic lenses when analysing a session artifact under `sessions/**`.

## Input Scope

- Read findings from the `/compact` output sections `## What Was Tried` and `## Corrections` only. Reason: scoped evidence keeps the analysis consistent and lightweight.
- Evaluate each finding once in lens order from 1 through 4. Reason: one ordered pass prevents duplicate routing.
- Assign the first matching lens and stop routing that finding after the match. Reason: each finding needs exactly one destination surface.

## Lens Routing Table

| Lens | Classification criterion | Target surface | Observable test |
|---|---|---|---|
| 1 — Recurring Correction | The agent made the same mistake in two or more sessions. | `copilot-instructions.md` rule | Ask: did this appear in a prior session correction? |
| 2 — Domain Vocabulary | The agent used the wrong project term or missed a project-specific name. | Scoped `*.instructions.md` | Ask: would a glossary or naming rule prevent this? |
| 3 — Workflow Friction | The developer repeated the same multi-step action two or more times. | `*.prompt.md` or `*.agent.md` | Ask: would a named command or delegated workflow remove the repetition? |
| 4 — Quality Guardrail | The agent nearly deleted, overwrote, or otherwise mishandled a sensitive operation. | Hook or safety guard | Ask: was this a dangerous tool action that needs a guardrail? |

## Output Rules

- Produce one routing decision per finding with lens number, target surface, and proposed action. Reason: the next stage needs a complete routing record.
- Keep findings that do not match Lens 1 in the original order while checking Lenses 2 through 4. Reason: stable ordering improves review traceability.
- Present the routed findings in a compact table before any promotion decision. Reason: reviewers need a single view of the session output.
