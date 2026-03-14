# HITL Periodic Audit Checklist

Audits are conducted quarterly (or after any significant incident) by a **Maintainer** (Auditor role).
The goal is to verify that the HITL governance policy is being followed and identify improvement opportunities.

Create a new GitHub Issue titled `[HITL Audit] YYYY-QN` and work through this checklist.
Close the audit issue with a summary of findings and any remediation actions raised.

---

## Section 1: Policy Configuration

- [ ] The issue form at `.github/ISSUE_TEMPLATE/hitl-intervention.yml` has all required fields marked `required: true`.
- [ ] `.github/ISSUE_TEMPLATE/config.yml` disables blank issues (`blank_issues_enabled: false`).
- [ ] Repository labels match the taxonomy in `docs/hitl/labels.md`. Verify no ad-hoc labels exist with `state:`, `risk:`, `decision:`, or `event:` prefixes.
- [ ] `docs/hitl/runbook.md` is current and accurately reflects the live workflow.
- [ ] `docs/hitl/labels.md` is up-to-date and reflects all labels as configured on GitHub.

---

## Section 2: Workflow Health

- [ ] `hitl-intake.yml` has had no unexpected failures in the audit period (check Actions tab).
- [ ] `hitl-gate.yml` has had no unexpected failures in the audit period.
- [ ] `hitl-escalation.yml` has had no unexpected failures in the audit period.
- [ ] `hitl-decision-log.yml` has had no unexpected failures in the audit period.
- [ ] `hitl-metrics.yml` has produced weekly reports without failures.
- [ ] All workflows use `actions/github-script@v7` (or the current pinned version). No unpinned `@latest` references.

---

## Section 3: Issue Completeness

For each HITL issue closed in the audit period, verify:

- [ ] The issue has exactly one `state:closed` label.
- [ ] The issue has exactly one `decision:*` label.
- [ ] The issue has exactly one `risk:*` label.
- [ ] A Decision Evidence Record comment is present in the issue timeline.
- [ ] An ADR is linked from the issue (in the body or a comment).
- [ ] The ADR exists at `docs/adr/` and has a completed `Outcome` section.

**Undocumented decisions (target: 0):**
List any issues found without ADR link: _(none)_

---

## Section 4: Authorization Compliance

- [ ] No `/approve` or `/reject` commands were issued by non-collaborators (spot-check recent issues).
- [ ] No instances of self-approval (approver = requester) occurred.
- [ ] No unauthorized state label changes were made manually (check label event history on sample issues).

---

## Section 5: SLA Performance

Review the weekly metrics issues for the audit period and record:

| Metric | Target | Actual |
|---|---|---|
| Median time-to-decision | ≤ SLA by risk tier | |
| Issues with SLA breach (escalated) | ≤ 5% of total | |
| Undocumented decisions | 0 | |
| Reopen rate (closed → reopened) | ≤ 5% | |

---

## Section 6: Risk Distribution Analysis

- [ ] Review rejection reasons over the period. Are there recurring patterns that suggest systemic issues or process improvements needed?
- [ ] Review `risk:critical` issues. Were they actioned within the 1-hour SLA?
- [ ] Review `risk:low` issues. Could any be auto-approved without a human gate in future?

---

## Section 7: Improvements and Remediation

Document findings, gaps, and recommended improvements:

| Finding | Severity | Recommended Action | Owner | Due Date |
|---|---|---|---|---|
| | | | | |

---

## Audit Sign-off

- **Auditor:** @github-handle
- **Audit Period:** YYYY-QN (YYYY-MM-DD to YYYY-MM-DD)
- **Date Completed:** YYYY-MM-DD
- **Overall Compliance:** [ ] Compliant [ ] Compliant with findings [ ] Non-compliant

Close this issue after completing the sign-off.
