# ADR-0002: Position Framework on the LLM Adaptation Spectrum

Date: 2026-03-20
Status: Proposed
HITL Issue: [#10](https://github.com/pslits/copilot-session-feedback/issues/10)
Decider: @pslits
Risk Tier: low

---

## Context

The book's Ch. 3 defines an LLM adaptation spectrum: in-context learning → RAG → fine-tuning. The
framework's memory strategy — injecting rules into `copilot-instructions.md`, re-injecting via
PostCompact hook, and using Copilot Memory — is in-context learning at inference time. This is a
deliberate and correct choice given the VS Code-native constraint.

However, nowhere in the framework is this named as such. The Memory Management catalogue entry
does not declare "this is in-context learning, not RAG or fine-tuning." This makes the design
rationale invisible: a reader cannot tell whether in-context learning was chosen or simply assumed.

The ceiling of this choice is also undocumented: in-context learning is bounded by the context
window. When `copilot-instructions.md` grows beyond ~3000 tokens, later rules are silently
deprioritised. This is the known upper bound of the approach.

---

## Decision

> **We decide to add an explicit paragraph to the Memory Management catalogue entry naming the
> framework's adaptation mechanism as in-context learning and documenting the context-window
> ceiling as a known constraint.**

---

## Consequences

### Positive
- Framework is explicitly positioned on the Ch. 3 spectrum.
- The context-window ceiling is visible as a design constraint, not a surprise failure mode.
- Makes RAG exclusion deliberate and documented rather than implicit.

### Negative / Risks
- None. Documentation-only change.

### Neutral
- May surface questions about whether context-window compression (PostCompact hook) counts as a
  partial mitigation, which it does — and that relationship should be noted.

---

## Follow-up Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| Update Memory Management entry in patterns-catalogue.md | @pslits | 2026-04-03 | Open |
| Cross-reference Ch. 3 of the book in the entry | @pslits | 2026-04-03 | Open |

---

## Outcome (complete after execution)

_To be filled after the change is made._
