# HITL Operator Runbook

This runbook is the primary reference for anyone involved in operating the Human-in-the-Loop
(HITL) intervention workflow. Read it before opening or actioning an intervention issue.

---

## Roles and Responsibilities

| Role | Who | Responsibilities |
|---|---|---|
| **Requester** | Any contributor | Creates the intervention issue, provides all required intake information, executes the approved action, and completes post-execution documentation. |
| **Reviewer** | Collaborator+ | Validates completeness and risk classification during triage. Uses `/need-info` when information is missing. Advances issue to `state:awaiting-human`. |
| **Approver** | Collaborator+ (authorized) | Makes the final gate decision using `/approve` or `/reject <rationale>`. Must not approve their own requests. |
| **Recorder** | Collaborator+ | Creates the ADR, ensures the closure checklist is completed. May be the same person as the Requester. |
| **Auditor** | Maintainer | Periodically reviews closed issues for compliance. Uses the [audit checklist](audit.md). |

---

## Workflow State Machine

```
state:intake
    │  (auto-triage on issue open)
    ▼
state:triage
    │  (reviewer validates completeness)
    │  (label applied manually: state:awaiting-human)
    ▼
state:awaiting-human
    │  /approve ──────────────────────────────────────────┐
    │  /reject <rationale> ───────────────────────┐       │
    ▼                                             ▼       ▼
state:rejected                            state:approved
    │                                             │
    │  (requester documents alternative)          │  (requester executes action)
    │  (label: state:postmortem)                  │  (label: state:executing → state:postmortem)
    ▼                                             ▼
state:postmortem ◄────────────────────────────────┘
    │  (recorder completes ADR + closure checklist)
    ▼
state:closed
```

---

## Step-by-Step Procedures

### Opening an Intervention Request

1. Go to **Issues → New Issue** and select **HITL Intervention Request**.
2. Complete every required field in the form. See [Required Intake Fields](#required-intake-fields).
3. Submit the issue. Automation will apply `state:intake` and transition to `state:triage`.
4. Monitor the issue for `event:need-info` responses and respond promptly.

### Performing Triage (Reviewer)

1. Open the issue. Verify all triage checklist items in the auto-posted comment.
2. If information is missing, post `/need-info <question>`. Follow up until resolved.
3. If the risk tier appears under-classified, update the label manually.
4. Once satisfied, apply the `state:awaiting-human` label. **Do not approve during triage.**

### Making a Gate Decision (Approver)

> Must not approve your own requests.

**To approve:**
```
/approve
```

**To reject (rationale is mandatory):**
```
/reject The blast radius is unacceptably wide for the current change window. Schedule for maintenance window.
```

**To defer:**
Apply `decision:deferred` manually and leave a detailed comment explaining conditions for re-evaluation.

### Executing an Approved Action (Requester)

1. Change the state label from `state:approved` to `state:executing`.
2. Execute the action exactly as described in the issue.
3. On completion (success or failure), change label to `state:postmortem`.
4. Document the outcome in a comment: what happened, whether rollback was needed, and lessons learned.

### Completing Post-Intervention Documentation (Recorder)

1. Create an ADR at `docs/adr/XXXX-<short-title>.md` using the [ADR template](../adr/0000-template.md).
   - Set status to `Accepted` or `Rejected`.
   - Fill in the `Outcome` section post-execution.
   - Link back to the HITL issue.
2. Work through the [closure checklist](closure-checklist.md).
3. Apply `state:closed` and close the issue with a closing comment.

---

## Command Reference

| Command | Allowed Roles | State Required | Effect |
|---|---|---|---|
| `/approve` | Approver | `state:awaiting-human` | Transitions to `state:approved` + `decision:accepted`. |
| `/reject <rationale>` | Approver | `state:awaiting-human` | Transitions to `state:rejected` + `decision:rejected`. |
| `/need-info <question>` | Reviewer | Any | Applies `event:need-info`. |
| `/escalate` | Anyone | Any | Applies `event:escalated`. |

---

## Required Intake Fields

The issue form enforces these fields:

| Field | Purpose |
|---|---|
| Intervention Summary | One-sentence description of the action. |
| Context and Trigger | Who/what is requesting this, and why now. |
| Risk Tier | `low` / `medium` / `high` / `critical`. |
| Blast Radius | Systems, data, users affected by success or failure. |
| Options Considered | At least two alternatives evaluated. |
| Proposed Action | Exact description of what will be done. |
| Rollback Strategy | How to reverse the action if needed. |
| Deadline / SLA | ISO 8601 UTC timestamp: `YYYY-MM-DDTHH:MMZ`. |
| Required Approver Role | `reviewer` / `approver` / `owner`. |
| Related Artifacts | Links to PRs, runbooks, logs, dashboards. |

---

## SLA and Escalation Policy

| Risk Tier | Recommended SLA |
|---|---|
| `risk:critical` | 1 hour |
| `risk:high` | 4 hours |
| `risk:medium` | 8 hours (business hours) |
| `risk:low` | 24 hours |

The escalation workflow runs hourly. Once the deadline timestamp in the issue body is past,
`event:escalated` is applied automatically and a comment is posted.

After escalation:
1. An Approver must action the issue within 30 minutes.
2. If no Approver is available, the Requester must escalate through out-of-band channels (e.g. PagerDuty, on-call rotation).

---

## Security Constraints

- **Never execute untrusted code** in privileged workflows triggered by issue comments.
- **Only `OWNER`, `MEMBER`, and `COLLABORATOR`** associations may use `/approve`, `/reject`, and `/need-info`.
- **Approvers must not approve their own requests.** This is a policy constraint, not currently enforced by automation.
- Workflow tokens use **minimum necessary permissions**: `issues: write` only.
- Label-based state transitions protect against unauthorized jumps (e.g. `state:intake` → `state:approved` directly is not possible via automation).

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---|---|---|
| `/approve` command not working | Commenter is not `OWNER`/`MEMBER`/`COLLABORATOR` | Ensure the approver has collaborator access to the repository. |
| SLA escalation not firing | Deadline format is not ISO 8601 | Update the deadline field to `YYYY-MM-DDTHH:MMZ` format. |
| State label missing after issue creation | Issue was not created via the HITL form | Manually apply `state:intake` and trigger re-triage. |
| Duplicate decision evidence comment | `decision:*` label applied more than once | Remove duplicate label. Only one `decision:*` label should be present. |

---

## Cloud Copilot Session Harvest

When an issue is assigned to the GitHub Copilot coding agent, work runs in a GitHub-hosted
cloud environment. No local VS Code hooks fire, so nothing is written to `sessions/`
automatically. The `copilot-session-harvest` workflow handles this automatically.

### How It Works

The workflow (`.github/workflows/copilot-session-harvest.yml`) triggers whenever a
`copilot/*` branch PR is merged. It:

1. Checks out the base branch.
2. Derives a `session_id` from the branch name
   (e.g. `copilot/issue-26` → `copilot-issue-26-<YYYYMMDD>`).
3. Appends one row to `sessions/metrics/sessions.jsonl` using the same schema as the VS Code
   `session-end.py` hook (`session_id`, `trace_id`, `start_ts`, `end_ts`,
   `duration_seconds`, `turn_count`).
4. Commits and pushes the updated file.

No manual steps are required for metrics collection.

### Troubleshooting the Harvest Workflow

| Problem | Likely Cause | Resolution |
|---|---|---|
| Workflow does not trigger after PR merge | PR branch does not start with `copilot/` | Verify the branch name; Copilot-created branches follow the `copilot/issue-<n>` pattern. |
| Workflow triggers but push step fails | Branch protection requires PRs for all pushes | Add a bypass rule for `github-actions[bot]` in the branch protection settings. |
| `sessions/metrics/sessions.jsonl` not updated | Workflow run skipped (already up to date) | Check the workflow run log; this is expected if git detects no diff. |

> **Background:** ADR-0016 records the decision to implement this automated approach.
> ADR-0017 (implemented and merged) defines the data-residency policy:
> `sessions/metrics/sessions.jsonl` is the only file committed; transcripts remain local-only.

---

## Related Documents

- [Label Taxonomy](labels.md)
- [Closure Checklist](closure-checklist.md)
- [ADR Template](../adr/0000-template.md)
- [Audit Checklist](audit.md)
- [Project Fields](project-fields.md)
- [ADR-0016: Cloud Copilot Session Harvest Strategy](../adr/0016-cloud-copilot-session-harvest.md)
- [ADR-0017: Session Data-Residency Policy](../adr/0017-session-data-residency.md)
