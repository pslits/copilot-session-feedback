# Facilitation Scripts — Agent-Driven Event Storming

Reference document for the `event-storming` skill. Contains adapted facilitation
scripts for all three Event Storming phases, translated from human-workshop
format to agent-driven execution.

---

## How to Use This Reference

Each phase lists its facilitation steps. Every step specifies:

| Field | Meaning |
|-------|---------|
| **Agent action** | What the agent does (read, analyse, produce, validate) |
| **Expected input** | What must be available before this step runs |
| **Expected output** | Concrete deliverable the step produces |
| **HITL point** | Whether the human reviews before the next step |

Agents must follow steps sequentially within a phase. Do not skip steps.

---

## Phase 1 — Big Picture (16 steps)

Goal: Produce a domain event timeline with hot spots, opportunities, and
bounded context candidates.

### BP-1: Define the scope

- **Agent action:** Read the scope plan from the coordinator handoff. Confirm
  the target (code directory or requirements document) and the business domain.
- **Expected input:** Coordinator scope plan (direction, target path, domain name).
- **Expected output:** Scope confirmation statement (1–2 sentences).
- **HITL point:** No — proceed automatically.

### BP-2: Identify the pivotal events

- **Agent action:** Scan the source material for the 3–5 most significant state
  changes. A pivotal event usually has one or more of these characteristics:
  (1) **irreversible** — cannot be undone once it happens,
  (2) **high-stakes** — significant business or financial impact,
  (3) **phase boundary** — marks a transition between process stages,
  (4) **multi-stakeholder** — referenced by multiple actors or teams,
  (5) **responsibility shift** — marks a handoff between organisational units.
  For code: look for major lifecycle transitions (created, approved,
  shipped, cancelled). For requirements: find milestone outcomes.
- **Expected input:** Target source material + scope confirmation.
- **Expected output:** Ordered list of 3–5 pivotal domain events.
- **HITL point:** No — proceed automatically.

### BP-3: Establish the timeline

- **Agent action:** Place pivotal events on a left-to-right timeline. These
  become the skeleton that all other events cluster around.
- **Expected input:** Pivotal events list.
- **Expected output:** Timeline skeleton (Markdown table: Position | Event).
- **HITL point:** No — proceed automatically.

### BP-4: Domain event exploration (chaotic)

- **Agent action:** Exhaustively scan the source material and list every domain
  event found. For code: examine every method, state change, event emission,
  callback, and side effect. For requirements: extract every "when…then" outcome,
  business trigger, and state transition. Do not filter or organise yet.
- **Expected input:** Source material + timeline skeleton.
- **Expected output:** Unordered list of all discovered domain events (name only).
- **HITL point:** No — proceed automatically.

### BP-5: Place events on the timeline

- **Agent action:** Assign each discovered event to a position relative to the
  pivotal events. Group events that occur in the same temporal neighbourhood.
- **Expected input:** Unordered event list + timeline skeleton.
- **Expected output:** Full event timeline (Markdown table: Position | Event |
  Cluster).
- **HITL point:** No — proceed automatically.

### BP-6: Identify commands

- **Agent action:** For each domain event, identify the command that triggers it.
  For code: the calling method or user action. For requirements: the actor
  intention from the user story.
- **Expected input:** Full event timeline.
- **Expected output:** Event-to-Command mapping table (Event | Command | Source).
- **HITL point:** No — proceed automatically.

### BP-7: Identify actors

- **Agent action:** For each command, identify who or what issues it. For code:
  controllers, endpoints, scheduled jobs, external callers. For requirements:
  named actors, user roles, system actors.
- **Expected input:** Event-to-Command mapping.
- **Expected output:** Command-to-Actor mapping (Command | Actor | Type).
- **HITL point:** No — proceed automatically.

### BP-8: Identify external systems

- **Agent action:** Scan for any system boundary crossing. For code: external
  API calls, message queues, third-party SDKs, file system I/O. For
  requirements: integration mentions, external service dependencies.
- **Expected input:** Source material + event timeline.
- **Expected output:** External Systems list (System | Interaction Type | Events
  Affected).
- **HITL point:** No — proceed automatically.

### BP-9: Identify hot spots

- **Agent action:** Flag areas of uncertainty, conflict, or complexity. For
  code: large methods, high cyclomatic complexity, TODO/FIXME comments,
  exception-heavy paths, shared mutable state. For requirements: ambiguous
  language, contradictory criteria, missing acceptance criteria.
- **Expected input:** Full event timeline + source material.
- **Expected output:** Hot Spots list (Hot Spot | Reason | Related Events).
- **HITL point:** No — proceed automatically.

### BP-10: Identify opportunities

- **Agent action:** Identify positive discoveries: new feature ideas, process
  improvements, quick wins, and business insights. For code: underused
  capabilities, simplification targets, automation candidates, dead code that
  reveals abandoned features worth revisiting. For requirements: unmet needs
  implied by workarounds, cross-cutting improvements, reuse potential.
- **Expected input:** Full event timeline + source material.
- **Expected output:** Opportunities list (Opportunity | Related Events | Impact
  | Source).
- **HITL point:** No — proceed automatically.

### BP-11: Identify bounded context candidates

- **Agent action:** After hot spots and opportunities are placed, look for
  natural clusters of events that use distinct vocabulary, involve different
  actors, or belong to different lifecycle phases. Label each cluster as a
  candidate bounded context. If the same word means something different in two
  clusters, they are different contexts.
- **Expected input:** Full event timeline + hot spots + opportunities.
- **Expected output:** Bounded context candidates list (Candidate Context |
  Key Events | Distinguishing Vocabulary).
- **HITL point:** No — proceed automatically.

### BP-12: Reverse walkthrough

- **Agent action:** Walk through the timeline backwards — start from the final
  event and trace the chain back to the first. For each event, verify: is its
  triggering command present? Is the actor or policy that issues that command
  identified? Flag any gap where the backward trace breaks.
- **Expected input:** Complete Big Picture model so far.
- **Expected output:** Reverse walkthrough report (Gap | Location | Suggestion).
- **HITL point:** No — proceed automatically.

### BP-13: Validate timeline consistency

- **Agent action:** Check timeline for gaps (time periods with no events),
  orphaned events (no trigger command), commands without resulting events, and
  actors/systems mentioned but not connected.
- **Expected input:** Complete Big Picture model so far + reverse walkthrough report.
- **Expected output:** Consistency report (Issues Found | Severity | Suggestion).
- **HITL point:** No — proceed automatically.

### BP-14: Apply notation grammar validation

- **Agent action:** Verify every element follows the notation grammar from
  `notation-reference.md`. Check naming conventions (past tense for events,
  imperative for commands, nouns for aggregates). Flag violations.
- **Expected input:** All Big Picture deliverables.
- **Expected output:** Grammar validation report (Element | Violation | Fix).
- **HITL point:** No — proceed automatically.

### BP-15: Compile Big Picture output

- **Agent action:** Assemble all deliverables into the Big Picture output format
  defined in `output-templates.md`. Include domain event timeline, commands,
  actors, external systems, hot spots, opportunities, bounded context candidates,
  and open questions. Compute goal metrics.
- **Expected input:** All validated Big Picture deliverables.
- **Expected output:** Complete Big Picture document + Goal Metrics (events: N,
  commands: N, hot spots: N, opportunities: N, external systems: N, bounded
  context candidates: N).
- **HITL point:** No — proceed to review step.

### BP-16: Human review gate

- **Agent action:** Present the complete Big Picture output and goal metrics to
  the human. Ask: "Review the Big Picture timeline — approve to proceed to
  Process Modeling, or tell me what to change."
- **Expected input:** Compiled Big Picture document.
- **Expected output:** Human approval or change requests.
- **HITL point:** **Yes — mandatory.** Do not proceed to Phase 2 without approval.

---

## Phase 2 — Process Modeling (10 steps)

Goal: Model detailed business processes with commands, policies, and read models.

### PM-1: Select processes to model

- **Agent action:** From the Big Picture timeline, identify distinct business
  processes. Each process is a coherent sequence of events spanning a bounded
  time period. Group related events into candidate processes.
- **Expected input:** Approved Big Picture output.
- **Expected output:** Process list (Process Name | Start Event | End Event |
  Event Count).
- **HITL point:** No — proceed automatically.

### PM-2: Model the happy path (per process)

- **Agent action:** For each process, trace the primary success path using chain
  notation. Start from the triggering actor or system. Apply the PM grammar at
  each link: `Actor → Command → System → Event`. Embed policies inline where
  they occur using `→ 🟣 Policy Name: "Whenever [event], [action]"` followed by
  the command it triggers. For branching policies, embed the branch tree at the
  point in the chain where the branch occurs. Use 🩷 System (pink) for the
  executor — Aggregates (🟨) only appear in Software Design.
- **Expected input:** Process list + Big Picture timeline.
- **Expected output:** One `✅ Happy Path` chain per process using `→` indented
  notation, with policies embedded inline.
- **HITL point:** No — proceed automatically.

### PM-3: Identify policies (inline)

- **Agent action:** For each event in the happy path chain that triggers a
  subsequent command without direct actor intervention, insert a 🟣 Policy
  inline in the chain at the exact point it occurs. Do **not** produce a
  separate policy section or table. Format:
  `→ 🟣 Policy Name: "Whenever [event], [action]"` followed by the command it
  triggers. For branching policies, use the tree notation inline:
  `├──` for mid-branch, `└──` for last branch.
- **Expected input:** Happy path chains.
- **Expected output:** Policies embedded in the happy path chains (no separate
  policy output).
- **HITL point:** No — proceed automatically.

### PM-4: Identify read models

- **Agent action:** For each command that requires information to be issued,
  identify the Read Model that provides it. For code: query methods, view models,
  DTOs, dashboard data. For requirements: "the user sees…", "display the…",
  decision-supporting data.
- **Expected input:** Happy path chains.
- **Expected output:** Read Model table per process (Read Model | Serves Command |
  Data Source | Notes).
- **HITL point:** No — proceed automatically.

### PM-5: Model alternative paths (per process)

- **Agent action:** For each process, identify alternative paths: error
  scenarios, business rule violations, timeout paths, compensation flows. For
  code: catch blocks, else branches, retry logic. For requirements: edge cases,
  exception paths in acceptance criteria. Write each as a named chain branching
  from the exact command or event where the divergence occurs, using the same
  `→` chain notation as the happy path.
- **Expected input:** Happy path chains.
- **Expected output:** One named chain per variation under `### ⚠️ Alternative Paths`,
  labelled **⑴**, **⑵**, etc. with a short descriptive name.
- **HITL point:** No — proceed automatically.

### PM-6: Enforce grammar across all flows

- **Agent action:** Verify that every flow (happy paths and variations) complies
  with the notation grammar. Every command must map to ≥1 event. Every event
  must have a triggering command or policy. Flag orphaned elements.
- **Expected input:** All process flows (happy + variations).
- **Expected output:** Grammar compliance report (Process | Issue | Fix).
- **HITL point:** No — proceed automatically.

### PM-7: Cross-reference with Big Picture

- **Agent action:** Verify completeness: every Big Picture event appears in at
  least one process model. Identify any Big Picture events not yet modeled and
  flag them as gaps.
- **Expected input:** Big Picture output + all process flows.
- **Expected output:** Coverage report (Big Picture Event | Covered By Process |
  Gap?).
- **HITL point:** No — proceed automatically.

### PM-8: Apply notation grammar validation

- **Agent action:** Final notation pass: verify naming conventions, element
  types, and grammar sequences across all process models using
  `notation-reference.md`.
- **Expected input:** All process model deliverables.
- **Expected output:** Notation validation report.
- **HITL point:** No — proceed automatically.

### PM-9: Compile Process Modeling output

- **Agent action:** Assemble all deliverables into the Process Modeling output
  format defined in `output-templates.md`. Include process flows, policies, read
  models, variations, and goal metrics.
- **Expected input:** All validated process model deliverables.
- **Expected output:** Complete Process Modeling document + Goal Metrics
  (processes: N, commands: N, events: N, policies: N, read models: N).
- **HITL point:** No — proceed to review step.

### PM-10: Human review gate

- **Agent action:** Present the complete Process Modeling output and goal metrics
  to the human. Ask: "Review the process models — approve to proceed to Software
  Design, or tell me what to change."
- **Expected input:** Compiled Process Modeling document.
- **Expected output:** Human approval or change requests.
- **HITL point:** **Yes — mandatory.** Do not proceed to Phase 3 without approval.

---

## Phase 3 — Software Design (9 steps)

Goal: Produce aggregates, bounded contexts, and integration contracts for DDD.

### SD-1: Identify candidate aggregates

- **Agent action:** Apply the PM→SD transition rule: replace each 🩷 System with
  a 🟨 Aggregate for features you plan to build. External systems or tools stay
  pink (🩷). From the process models, identify aggregates. An aggregate
  is a cluster of commands and events that share the same lifecycle (create,
  update, delete, query). For code: classes with both state and behaviour that
  enforce invariants. For requirements: nouns that own a lifecycle.
- **Expected input:** Approved Process Modeling output.
- **Expected output:** Candidate Aggregate list (Aggregate | Commands | Events |
  Lifecycle: Create/Update/Delete/Query).
- **HITL point:** No — proceed automatically.

### SD-2: Answer lifecycle questions

- **Agent action:** For each candidate aggregate, answer the four lifecycle
  questions: (1) How is it created? (2) What updates change its state? (3) When
  and how is it deleted/archived? (4) What queries read its state? Flag
  aggregates that cannot answer all four questions.
- **Expected input:** Candidate aggregate list + process flows.
- **Expected output:** Aggregate lifecycle table (Aggregate | Create | Update |
  Delete | Query | Gaps).
- **HITL point:** No — proceed automatically.

### SD-3: Assign aggregates to bounded contexts

- **Agent action:** Group aggregates into bounded contexts based on cohesion.
  Aggregates that share vocabulary, actors, or lifecycle transitions belong
  together. For code: module/package boundaries suggest contexts. For
  requirements: team/capability boundaries.
- **Expected input:** Aggregate lifecycle table.
- **Expected output:** Bounded Context Map (Context | Aggregates | Owner/Team |
  Key Vocabulary).
- **HITL point:** No — proceed automatically.

### SD-4: Define integration contracts

- **Agent action:** For each pair of bounded contexts that exchange events,
  commands, or data, define an integration contract. Specify: publishing context,
  consuming context, event/data exchanged, and integration pattern. Use the DDD
  strategic patterns: Shared Kernel, Customer/Supplier, Conformist,
  Anti-Corruption Layer (ACL), Open Host Service, or Published Language.
- **Expected input:** Bounded Context Map + process flows.
- **Expected output:** Integration Contracts table (Publisher | Consumer |
  Data/Event | Pattern | Notes).
- **HITL point:** No — proceed automatically.

### SD-5: Extract Five Views

- **Agent action:** Compile the five output views from all prior deliverables:
  1. **Next Actions** — immediate development tasks derived from the model
  2. **Domain Definitions** — ubiquitous language glossary from all named elements
  3. **Context Map** — bounded contexts and their relationships
  4. **User Stories** — generated from command-event pairs (As [Actor], I want
     to [Command] so that [Event outcome])
  5. **Integration Contracts** — from SD-4
- **Expected input:** All Software Design deliverables + Big Picture + Process Models.
- **Expected output:** Five Views document (one section per view).
- **HITL point:** No — proceed automatically.

### SD-6: Validate aggregate completeness

- **Agent action:** Verify every aggregate has: ≥1 command, ≥1 event, answers
  to all 4 lifecycle questions, assignment to exactly 1 bounded context. Flag
  suspect aggregates (those with no commands or events).
- **Expected input:** All Software Design deliverables.
- **Expected output:** Aggregate validation report (Aggregate | Status |
  Issues).
- **HITL point:** No — proceed automatically.

### SD-7: Apply notation grammar validation

- **Agent action:** Final notation pass across the entire Software Design
  output. Verify consistency with Big Picture and Process Model notation. Check
  that aggregate names are singular nouns, event names use past tense, and
  command names use imperative mood per `notation-reference.md`.
- **Expected input:** All Software Design deliverables.
- **Expected output:** Notation validation report.
- **HITL point:** No — proceed automatically.

### SD-8: Compile Software Design output

- **Agent action:** Assemble all deliverables into the Software Design output
  format defined in `output-templates.md`. Include aggregate cards, bounded
  context map, integration contracts, Five Views, and goal metrics.
- **Expected input:** All validated Software Design deliverables.
- **Expected output:** Complete Software Design document + Goal Metrics
  (aggregates: N, bounded contexts: N, integration contracts: N, user
  stories: N).
- **HITL point:** No — proceed to review step.

### SD-9: Human review gate

- **Agent action:** Present the complete Software Design output, Five Views, and
  goal metrics to the human. This is the final deliverable of the entire Event
  Storming session.
- **Expected input:** Compiled Software Design document + Five Views.
- **Expected output:** Human approval or change requests.
- **HITL point:** **Yes — mandatory.** This is the terminal review gate.
