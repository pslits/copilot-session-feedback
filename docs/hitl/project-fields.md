# HITL GitHub Projects — Field Definitions

This document defines the recommended fields and values to configure in a GitHub Project
that tracks HITL intervention issues. These fields supplement the label-based state machine
with richer metadata for filtering, sorting, and reporting.

---

## Required Fields

### Status (built-in)
Map to the `state:*` label lifecycle.

| Project Status | Maps to Label |
|---|---|
| Intake | `state:intake` |
| Triage | `state:triage` |
| Awaiting Human | `state:awaiting-human` |
| Approved | `state:approved` |
| Executing | `state:executing` |
| Postmortem | `state:postmortem` |
| Closed | `state:closed` |

---

### Risk Tier
**Field type:** Single select
**Values:**

| Value | Color |
|---|---|
| `low` | Green |
| `medium` | Yellow |
| `high` | Orange |
| `critical` | Red |

---

### Decision
**Field type:** Single select
**Values:**

| Value | Color |
|---|---|
| `accepted` | Green |
| `rejected` | Red |
| `deferred` | Blue |
| `pending` | Grey (default while awaiting gate) |

---

### Deadline / SLA
**Field type:** Date
Populated manually from the intake form value. Used for sorting and overdue filtering.

---

### Approver
**Field type:** Text
GitHub handle of the person who made the gate decision. Populated after decision.

---

### Time-to-Decision (hours)
**Field type:** Number
Calculated manually or via metrics workflow: elapsed time from issue open to `decision:*` label.

---

### Execution Outcome
**Field type:** Single select
**Values:** `success`, `partial`, `failed`, `rolled-back`, `n/a`
Populated during the postmortem phase.

---

### ADR Link
**Field type:** Text (URL)
Link to the ADR created for this intervention.

---

## Recommended Views

1. **Active Board** — Grouped by Status, filtered to open issues. Shows the current pipeline.
2. **Risk Backlog** — Filtered to `state:awaiting-human`, sorted by Deadline ASC. Highlights urgent pending decisions.
3. **Decision Log** — All closed issues, sorted by closed date DESC. Full audit history.
4. **Metrics View** — Grouped by Risk Tier + Decision, all issues. Supports pattern analysis.

---

## Governance Notes

- Project fields are supplementary; the label taxonomy in [labels.md](labels.md) is authoritative.
- If a field and a label disagree, the label is correct — update the project field.
- Project fields should be updated whenever a state transition occurs.
