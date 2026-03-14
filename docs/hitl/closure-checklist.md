# HITL Closure Checklist

Use this checklist before closing any HITL intervention issue.
**All items must be checked.** Issues closed without completing this checklist are non-compliant
with the HITL governance policy and may be reopened by an Auditor.

---

## Pre-Closure Checklist

### 1. Decision Documentation
- [ ] A `decision:accepted` or `decision:rejected` label is applied.
- [ ] The Decision Evidence Record comment is present in the issue timeline.
- [ ] An ADR has been created in `docs/adr/` and linked in the issue.

### 2. Execution Outcome (Required for `decision:accepted` issues)
- [ ] The issue was transitioned through `state:executing`.
- [ ] The issue is now in `state:postmortem`.
- [ ] Post-execution outcome is described in the issue (success, partial success, or failure).
- [ ] If execution failed or rolled back: the rollback was executed and verified, and the impact is documented.

### 3. Rejection / Deferral Follow-up (Required for `decision:rejected` or `decision:deferred` issues)
- [ ] Alternative action plan is documented or linked.
- [ ] Requester has acknowledged the rejection rationale.

### 4. ADR Completeness
- [ ] ADR status is `Accepted` or `Rejected` (not `Proposed`).
- [ ] ADR `Outcome` section is filled in (post-execution section).
- [ ] ADR is linked from the issue.

### 5. Label Hygiene
- [ ] Exactly one `state:*` label is present (should be `state:postmortem` before closing to `state:closed`).
- [ ] Exactly one `risk:*` label is present.
- [ ] Exactly one `decision:*` label is present.
- [ ] No stray or unrecognized labels remain.

### 6. Final Close
- [ ] Apply `state:closed` label.
- [ ] Close the issue with a closing comment summarising: decision, execution outcome, and ADR link.

---

## Closing Comment Template

Use the following template as the final comment before closing:

```
## Issue Closed

**Decision:** [ACCEPTED / REJECTED / DEFERRED]
**Execution Outcome:** [Success / Failure / Rolled back / N/A — rejected]
**ADR:** [link to docs/adr/XXXX-title.md]
**Summary:** [One or two sentences describing what happened and what was learned.]
```
