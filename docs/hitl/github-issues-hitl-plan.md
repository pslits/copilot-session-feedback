# Human-in-the-Loop via GitHub Issues

Date: 2026-03-14

## Goal
Implement a GitHub-native Human-in-the-Loop (HITL) system where:
- interventions are initiated and governed through GitHub Issues,
- human approval gates are enforced,
- decisions are documented during and after intervention,
- outcomes are auditable over time.

## Research Basis
This design is inspired by agentic patterns (planning, reflection, goal monitoring, human gate) and GitHub-native platform capabilities:
- GitHub Issue Forms (structured required intake)
- GitHub Actions issue/issue_comment events (workflow state machine)
- GitHub deployment review patterns (required human approvals)
- ADR practice (decision rationale and consequences)

## Recommended v1 Architecture
Use an Issue + Workflow State Machine + ADR Log approach.

Core elements:
1. One issue per intervention request.
2. Label/state transitions managed by automation.
3. Human commands (e.g. `/approve`, `/reject`) restricted to authorized roles.
4. Decision evidence captured in issue timeline and ADR file.
5. Closure blocked unless post-intervention outcomes are documented.

## Lifecycle Model
States (labels/project fields):
- `state:intake`
- `state:triage`
- `state:awaiting-human`
- `state:approved` or `state:rejected`
- `state:executing`
- `state:postmortem`
- `state:closed`

Suggested event labels:
- `event:need-info`
- `event:escalated`
- `risk:low|medium|high|critical`
- `decision:accepted|rejected|deferred`

## Role Model
- Requester: creates intervention issue.
- Reviewer: validates completeness/risk.
- Approver: authorized human who can gate approve/reject.
- Recorder: ensures ADR and closure documentation are complete.
- Auditor: periodically verifies compliance and metrics.

## Implementation Plan

### Phase A — Governance Scaffolding
Precondition: role/risk model agreed.

- Create issue form: `.github/ISSUE_TEMPLATE/hitl-intervention.yml`
- Create issue template config: `.github/ISSUE_TEMPLATE/config.yml`
- Document taxonomy: `docs/hitl/labels.md`

Success criteria:
- Required form fields are enforced.
- Label taxonomy is canonical and documented.

### Phase B — Workflow State Machine
Precondition: forms and labels exist.

- Add intake workflow: `.github/workflows/hitl-intake.yml`
- Add gate workflow: `.github/workflows/hitl-gate.yml`
- Add escalation workflow: `.github/workflows/hitl-escalation.yml`

Success criteria:
- New intervention issues are auto-triaged.
- Only authorized identities can approve/reject.
- SLA breaches auto-escalate.

### Phase C — Decision Documentation During and After Intervention
Precondition: gate workflow operational.

- Add ADR template: `docs/adr/0000-template.md`
- Add decision-log workflow: `.github/workflows/hitl-decision-log.yml`
- Add closure checklist: `docs/hitl/closure-checklist.md`
- Add operator runbook: `docs/hitl/runbook.md`

Success criteria:
- Every approve/reject action produces linked decision evidence.
- Issues cannot be closed without outcome and follow-up documentation.

### Phase D — Monitoring and Auditability
Precondition: phases A–C complete.

- Define project fields: `docs/hitl/project-fields.md`
- Add metrics workflow: `.github/workflows/hitl-metrics.yml`
- Add periodic audit checklist: `docs/hitl/audit.md`

Success criteria:
- Weekly governance metrics available.
- Quarterly audit can verify decision completeness and policy adherence.

## Required Intake Fields (Issue Form)
- Intervention summary
- Context and trigger
- Risk tier and blast radius
- Options considered
- Proposed action
- Rollback strategy
- Deadline/SLA
- Required approver role
- Related artifacts (links)

## Command Surface (Minimal)
- `/approve` — only approver role
- `/reject` — only approver role with rationale required
- `/need-info` — reviewer requests missing data
- `/escalate` — escalation when SLA/risk requires

## Security and Reliability Constraints
- Do not run untrusted code in privileged workflows.
- Keep privileged write actions in narrowly scoped workflows.
- Protect against unauthorized state transitions.
- Require explicit rationale for reject and bypass-like actions.

## Metrics (Initial)
- Median time to human decision
- Approval rate by risk tier
- Rejection reasons distribution
- Reopen rate after closure
- Undocumented-decision count (target: 0)

## Out of Scope (v1)
- Separate external dashboard/UI
- Full compliance framework implementation (SOC2/ISO mapping)
- Cross-ticketing integrations (Jira/ServiceNow)

## Next Steps
1. Approve this design.
2. Implement Phase A files first.
3. Validate with one dry-run intervention issue.
4. Iterate based on observed friction and missed controls.
