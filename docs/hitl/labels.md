# HITL Label Taxonomy

This document is the canonical source of truth for all labels used by the Human-in-the-Loop (HITL) workflow.
Labels must not be created ad-hoc on the repository; all changes must go through a PR that updates this file.

---

## State Labels

Exactly one `state:*` label must be present on every HITL issue at all times.

| Label | Color | Description |
|---|---|---|
| `state:intake` | `#BFD4F2` | Issue submitted; awaiting completeness triage. |
| `state:triage` | `#E4E669` | Being reviewed for completeness and risk classification. |
| `state:awaiting-human` | `#F9A825` | Blocked on a human approve/reject decision. |
| `state:approved` | `#0E8A16` | Approved by an authorized human; execution may proceed. |
| `state:rejected` | `#B60205` | Rejected by an authorized human; execution must not proceed. |
| `state:executing` | `#1D76DB` | Approved action is actively in progress. |
| `state:postmortem` | `#5319E7` | Action complete; post-intervention outcome documentation required. |
| `state:closed` | `#CCCCCC` | All documentation complete; issue closed. |

---

## Event Labels

Used to mark notable points in the lifecycle without replacing the state label.

| Label | Color | Description |
|---|---|---|
| `event:need-info` | `#FEF2C0` | Reviewer has requested additional information from requester. |
| `event:escalated` | `#E99695` | SLA breach or elevated risk triggered an escalation. |

---

## Risk Labels

Exactly one `risk:*` label must be present on every HITL issue.

| Label | Color | Description |
|---|---|---|
| `risk:low` | `#C2E0C6` | Impact is bounded and easily reversible. |
| `risk:medium` | `#FEF2C0` | Moderate impact; rollback is well-defined. |
| `risk:high` | `#F9A825` | Significant impact; rollback is complex or time-consuming. |
| `risk:critical` | `#B60205` | Potentially irreversible or wide-blast-radius impact. |

---

## Decision Labels

Applied at the point of the approve/reject gate decision.

| Label | Color | Description |
|---|---|---|
| `decision:accepted` | `#0E8A16` | Action was accepted and approved. |
| `decision:rejected` | `#B60205` | Action was rejected with documented rationale. |
| `decision:deferred` | `#BFD4F2` | Decision postponed pending additional information or conditions. |

---

## Label Governance

- This file is the canonical source of truth. All label changes must go through a PR that updates this file.
- Labels are applied to the repository by the sync scripts below. Do **not** create or edit labels manually in the GitHub UI.
- Automation must only apply labels from this taxonomy.
- Unauthorized state transitions (e.g. jumping from `state:intake` to `state:approved` without triage) are rejected by the gate workflow.

### Syncing Labels

**Automatic:** The [hitl-label-sync](.github/workflows/hitl-label-sync.yml) workflow runs automatically whenever this file is merged to `main`. It can also be triggered manually from the Actions tab (with an optional `delete_unlisted` flag).

**Local — bash (macOS/Linux/WSL):**
```bash
# Create/update only
.github/scripts/sync-labels.sh

# Also delete any state:/risk:/event:/decision: labels not in the taxonomy
.github/scripts/sync-labels.sh --delete-unlisted

# Target a specific repo
.github/scripts/sync-labels.sh --repo OWNER/REPO
```

**Local — PowerShell (Windows):**
```powershell
# Create/update only
.\.github\scripts\sync-labels.ps1

# Also delete unlisted HITL labels
.\.github\scripts\sync-labels.ps1 -DeleteUnlisted

# Target a specific repo
.\.github\scripts\sync-labels.ps1 -Repo OWNER/REPO
```

Both scripts require the [`gh` CLI](https://cli.github.com/) to be installed and authenticated (`gh auth login`).
