# Agentic Design Patterns Catalogue

**Source 1:** *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems* — Antonio Gulli  
GitHub: <https://github.com/evoiz/Agentic-Design-Patterns>

**Source 2:** *Agentic Architectural Patterns for Building Multi-Agent Systems* — Dr. Ali Arsanjani & Juan Pablo Bustos (Packt, 2026)  
GitHub: <https://github.com/PacktPublishing/Agentic-Architectural-Patterns-for-Building-Multi-Agent-Systems>

---

## Part 1 — Core Patterns

### 1. Prompt Chaining
**What it is:** Break a complex task into a sequence of simpler sub-prompts where the output of one becomes the input of the next.  
**When to use:** The task has natural serial stages (research → summarise → format); when each step benefits from its own focused prompt.  
**Example structure:** `Extract entities` → `Classify entities` → `Generate report`  
**Key consideration:** Each link is stateless. Pass only the relevant prior output, not the full conversation history.

---

### 2. Routing
**What it is:** A classifier prompt inspects input and routes it to one of several specialised sub-agents or prompt chains.  
**When to use:** Inputs fall into distinct categories that require different handling (e.g., billing vs. technical vs. general enquiries).  
**Example structure:** `Router` → (`Path A` | `Path B` | `Path C`)  
**Key consideration:** The router must be lightweight and reliable. Errors here cascade to every downstream path.

---

### 3. Parallelization
**What it is:** Decompose a task into independent sub-tasks and execute them concurrently, then aggregate results.  
**When to use:** Sub-tasks do not depend on each other's output; throughput and latency matter.  
**Variants:** Map-reduce (many identical tasks), voting/consensus (same task, multiple LLM calls for reliability).  
**Key consideration:** Design the aggregation step explicitly. Decide how conflicts or contradictory outputs are resolved.

---

### 4. Reflection
**What it is:** An LLM evaluates and critiques its own (or another agent's) previous output, then revises it.  
**When to use:** Quality sufficiency is hard to guarantee in one pass; errors are costly; output accuracy is critical.  
**Variants:** Self-critique loop, peer review (two separate LLM instances), judge-scorer pattern.  
**Key consideration:** Avoid infinite loops. Set a fixed revision budget (e.g., max 3 iterations) or a quality gate threshold.

---

### 5. Tool Use
**What it is:** The agent is given access to external tools (web search, code execution, databases, APIs) and can decide when to invoke them.  
**When to use:** The task requires real-time data, computation, or side effects the LLM cannot perform alone.  
**Key consideration:** Define a strict tool schema (name, inputs, outputs). Add guardrails to prevent dangerous tool calls.

---

### 6. Planning
**What it is:** The agent decomposes a high-level goal into an ordered list of executable sub-tasks before taking any action.  
**When to use:** Tasks are long-horizon, ambiguous, or require sequencing many steps. Prevents premature action.  
**Variants:** ReAct (Reason + Act interleaved), Plan-and-Execute (plan first, execute second), HTN (hierarchical task networks).  
**Key consideration:** Surface the plan to the user before execution (human gate). Allow plan amendment.

---

### 7. Multi-Agent
**What it is:** Multiple specialized agents collaborate, each owning a distinct role, communicating via messages or shared memory.  
**When to use:** No single agent can do everything well; tasks naturally decompose into expert roles; parallelism is beneficial.  
**Topologies:** Pipeline (sequential), hierarchy (coordinator + workers), mesh (peer-to-peer).  
**Key consideration:** Define clear agent contracts (what each agent accepts and produces). Prevent context bloat by summarising inter-agent messages.

---

## Part 2 — Advanced Patterns

### 8. Memory Management
**What it is:** Persistent storage of information across sessions or agent invocations — short-term (in-context), long-term (vector store / DB), episodic (past interactions).  
**When to use:** The agent needs to remember user preferences, past decisions, or domain knowledge beyond a single session.  
**Key consideration:** Retrieval quality determines output quality. Invest in chunking and embedding strategies.

---

### 9. Learning and Adaptation
**What it is:** The agent updates its behaviour over time based on feedback signals, examples, or environment outcomes (fine-tuning, few-shot updates, RLHF-style loops).  
**When to use:** The task distribution shifts over time; user preferences vary; initial performance is insufficient.  
**Key consideration:** Learning loops must be audited. Unchecked adaptation can degrade or drift.

---

### 10. Model Context Protocol (MCP)
**What it is:** A standardised interface layer (request/response schema) between agents and tools or external systems, enabling plug-and-play integration.  
**When to use:** Building multi-tool or multi-model systems that need maintainability. Avoids tight coupling between agent logic and tool implementation.  
**Key consideration:** Define the contract (schema) before implementation. Version the protocol.

---

### 11. Goal Setting and Monitoring
**What it is:** The agent explicitly tracks observable, measurable goals throughout execution and monitors progress toward them.  
**When to use:** Long-running tasks; tasks where partial completion has value; tasks requiring human checkpoints.  
**Variants:** OKR-style objectives, milestone gating, progress percentage reporting.  
**Key consideration:** Goals must be specific and testable. Vague goals cannot be monitored reliably.

---

## Part 3 — Production Patterns

### 12. Exception Handling and Recovery
**What it is:** Explicit strategies for detecting, classifying, and recovering from failures — tool errors, LLM refusals, timeouts, malformed outputs.  
**When to use:** Production systems where reliability is required. Any workflow that calls external services.  
**Strategies:** Retry with backoff, fallback agent, graceful degradation, human escalation.  
**Key consideration:** Log all exceptions with enough context to debug. Don't silently swallow errors.

---

### 13. Human-in-the-Loop (HITL)
**What it is:** Insert human review or approval gates at key decision points in an otherwise automated flow.  
**When to use:** High-stakes actions (delete, deploy, send); low-confidence outputs; regulatory or audit requirements.  
**Gate types:** Approval gate (block until approved), notification gate (inform, continue), review gate (human can amend).  
**Key consideration:** Design the gate UI/UX. Humans will skip gates if they are too slow or unclear. Gate fatigue is real.

---

### 14. Knowledge Retrieval (RAG)
**What it is:** Retrieve relevant documents from an external knowledge base and inject them into the LLM context at inference time.  
**When to use:** The LLM's training data is stale or insufficient; domain-specific facts are needed; hallucination risk is high.  
**Key consideration:** Retrieval quality is the bottleneck. Invest in chunking strategy, embedding model selection, and re-ranking.

---

## Part 4 — Enterprise Patterns

### 15. Inter-Agent Communication (A2A)
**What it is:** Formal protocols for agents to exchange structured messages, share state, and coordinate actions across process or service boundaries.  
**When to use:** Distributed multi-agent systems; microservice-style agent architectures; cross-team agent collaboration.  
**Key consideration:** Standardise message envelopes (sender, receiver, intent, payload, trace ID). Implement idempotency.

> **Informal A2A in VS Code:** The VS Code handoff mechanism used between `@researcher`, `@planner`, and `@implementer` is _informal_ A2A — accumulated context is forwarded at the UI layer without a structured message envelope, trace ID, or idempotency guarantee. This satisfies the spirit of A2A for a single-developer, single-process context. Formal A2A (with protocol envelopes and trace IDs) is warranted when agents operate across process boundaries, network hops, or team boundaries. See ADR-0004 for the upgrade path.

---

### 16. Resource-Aware Optimization
**What it is:** The agent (or orchestrator) measures and optimises resource consumption — token budgets, API costs, latency, memory — during planning and execution.  
**When to use:** Cost-sensitive deployments; latency-sensitive applications; token-limited models.  
**Strategies:** Model routing by complexity, prompt compression, caching, batching.  
**Key consideration:** Track cost per invocation. Set hard budget caps; soft caps only work if enforced.

---

### 17. Reasoning Techniques
**What it is:** Structured internal reasoning processes — Chain-of-Thought, Tree-of-Thought, self-consistency, scratchpad — to improve decision quality before producing output.  
**When to use:** Complex reasoning tasks (maths, logic, multi-step deduction); tasks where error rate is high without explicit reasoning steps.  
**Key consideration:** Reasoning tokens cost money and add latency. Use selectively. Consider distilling reasoning into a cheaper model.

---

### 18. Guardrails / Safety Patterns
**What it is:** Input and output validation layers that detect and block harmful, off-topic, or policy-violating content before it reaches users or downstream systems.  
**When to use:** Customer-facing deployments; regulated industries; any system that processes untrusted input.  
**Layers:** Input filtering, output filtering, content classifiers, PII detection, semantic similarity gates.  
**Key consideration:** Guardrails add latency. Profile and cache where possible. False positive rates affect usability.

---

### 19. Evaluation and Monitoring
**What it is:** Systematic measurement of agent output quality, reliability, and performance using automated evals, human review, or both.  
**When to use:** Before and after deployment; continuously in production; when changing models or prompts.  
**Metrics:** Accuracy, faithfulness, relevance, latency, cost, refusal rate, hallucination rate.  
**Key consideration:** Ground truth is expensive. Start with LLM-as-judge evals, then validate a sample with human review.

---

### 20. Prioritization
**What it is:** The agent ranks and schedules tasks based on urgency, importance, dependencies, or resource constraints.  
**When to use:** Multi-task agents with limited concurrency; queue-based systems; agents that must triage incoming work.  
**Strategies:** Priority queues, dependency graphs, time-sensitive scoring.  
**Key consideration:** Starvation risk. Ensure low-priority tasks eventually execute.

---

### 21. Exploration and Discovery
**What it is:** The agent autonomously explores an environment, builds a model of its structure, and discovers new capabilities or information without explicit instructions for each step.  
**When to use:** Autonomous agents in partially known environments; research/discovery tasks; adaptive systems.  
**Key consideration:** Exploration without bounds is dangerous. Set exploration budget, scope limits, and safety rails before deploying.

---

---

## Part 5 — Arsanjani/Bustos Architectural Patterns *(Packt, 2026)*

> These patterns complement the Gulli set with enterprise-grade architectural depth: hierarchical orchestration, the three-layer agentic stack, explainability, fault tolerance specific patterns, human-agent interaction modes, and production observability.

### Foundational Concepts

#### The Agentic Stack (Three Layers)
**What it is:** A layered architectural model for composing agentic systems:
1. **Function Calling** — LLM invokes discrete functions/tools with typed parameters  
2. **Tool Protocols (MCP)** — Standardised discovery and invocation of tools across services  
3. **Agent-to-Agent (A2A)** — Structured communication and delegation between autonomous agents  

**When to use:** As the design framework for any multi-component agentic system. Determines which integration layer to use for each external capability.  
**Key consideration:** Build layers in order. A2A coordination depends on reliable MCP tool access, which depends on reliable function-calling.

> **VS Code handoffs as informal A2A:** In a single-developer VS Code context, agent handoffs (e.g., `@researcher → @planner → @implementer`) operate at the A2A layer informally — context is forwarded through the chat UI without a formal protocol envelope. This is sufficient for single-process, single-developer use. Formal A2A (message envelopes, trace IDs, idempotency) becomes necessary when agents span process boundaries, network hops, or team collaboration. See ADR-0004 for details on the informal vs formal distinction and the upgrade path.

---

#### GenAI Maturity Model
**What it is:** A five-level maturity model for assessing and planning enterprise agentic AI adoption:
- **Level 1 – Foundational:** Prompt-based interaction, no automation, human-driven
- **Level 2 – Assisted:** LLM-augmented workflows, basic tool use, human in the loop
- **Level 3 – Automated:** Single-agent task automation with structured tool use
- **Level 4 – Coordinated:** Multi-agent collaboration, orchestration, A2A protocols
- **Level 5 – Autonomous:** Self-improving, self-healing systems with minimal human oversight

**When to use:** At the start of any agentic system design to set scope and guard against over-engineering. Forces explicit maturity target-setting.  
**Key consideration:** Skipping levels creates fragile systems. Production readiness requires completing levels 1–3 before deploying level 4 or 5 architectures.

---

### Coordination Patterns *(Ch. 5)*

#### Hierarchical Orchestrator
**What it is:** A high-level Orchestrator agent decomposes a complex business workflow and delegates entire sub-processes to specialised Sub-agents using A2A. The orchestrator holds the workflow state; sub-agents own domain execution.  
**When to use:** Enterprise workflows too complex for a single agent; when domain specialisation across multiple agents is required; when workflow auditability is a requirement.  
**Structure:** `User → Orchestrator → [Sub-agent A | Sub-agent B | Sub-agent C] → Orchestrator → User`  
**Key consideration:** The orchestrator becomes a single point of failure. Design for orchestrator resilience (Circuit Breaker, Fallback). Sub-agents must have clearly scoped contracts.

---

#### Agent Router (Intent-Based Routing)
**What it is:** A lightweight classifier agent inspects incoming requests, determines intent, and routes to the appropriate specialised agent — combining routing logic (Gulli #2) with a dedicated agent persona for intent classification.  
**When to use:** Entry point for multi-agent systems where input type determines which agent should handle it; replaces hard-coded `if/else` routing with LLM-based intent detection.  
**Key consideration:** Intent classification errors propagate. Require confidence thresholds; route low-confidence inputs to a human or default handler.

---

#### Blackboard (Shared State)
**What it is:** Agents read from and write to a shared knowledge structure (the blackboard), enabling asynchronous, decoupled collaboration without direct agent-to-agent messaging.  
**When to use:** Multi-agent tasks where agents contribute partial results asynchronously; when the order of agent contributions cannot be predetermined.  
**Key consideration:** Concurrent writes create consistency risks. Implement optimistic locking or partition the blackboard by domain.

---

### Explainability and Compliance Patterns *(Ch. 6)*

#### Instruction Fidelity Auditing
**What it is:** Each agent records a structured log of the instructions it received, how it interpreted them, what tools it invoked, and what output it produced — creating an auditable trace of each decision step.  
**When to use:** Regulated industries (finance, healthcare, legal); any system where compliance teams must verify agent behaviour; debugging complex multi-agent failures.  
**Key consideration:** Audit logs contain sensitive data. Apply access controls and retention policies. Log storage costs at scale.

---

#### Decision Audit Trail
**What it is:** A cross-agent chain-of-custody record that links each output back to its source inputs, intermediate reasoning steps, and the agents responsible — enabling end-to-end explainability.  
**When to use:** Whenever a human or regulator must be able to explain why an agentic system produced a specific output. Required for Level 4/5 maturity systems.  
**Key consideration:** The trail is only as reliable as the agents' self-reporting. Pair with Instruction Fidelity Auditing and external observability (Lifecycle Callbacks).

---

### Robustness and Fault Tolerance Patterns *(Ch. 7)*

#### Parallel Execution Consensus
**What it is:** The same task is dispatched to multiple agents or LLM instances in parallel. Their outputs are compared; a consensus or majority-vote result is selected as the final answer.  
**When to use:** High-stakes decisions where a single LLM response is unreliable; when output correctness must be statistically verified; production systems with low error budgets.  
**Variants:** Majority vote (3+ agents), confidence-weighted average, judge agent (one agent evaluates others).  
**Key consideration:** Cost multiplies with parallelism. Reserve for genuinely high-stakes outputs. Pre-define the consensus resolution strategy before deployment.

---

#### Circuit Breaker
**What it is:** A state machine that monitors failure rates for a downstream agent or tool. When failures exceed a threshold, the circuit "opens" — halting calls for a cool-down period before retrying.  
**When to use:** Any agent that calls external services or sub-agents that can fail or degrade; prevents cascading failures from propagating through an agent chain.  
**States:** Closed (normal) → Open (failing, requests blocked) → Half-open (test probe)  
**Key consideration:** Set thresholds based on real failure data, not guesses. Pair with Fallback Agent to serve degraded responses when the circuit is open.

---

#### Secure Agent (Input/Output Validation)
**What it is:** A validation wrapper applied at agent boundaries — inputs are sanitised and validated before processing; outputs are checked against a schema or policy before delivery. Defends against prompt injection and data exfiltration.  
**When to use:** Any agent that accepts untrusted input (user-supplied text, external data feeds); any agent that writes to external systems or returns sensitive data.  
**Key consideration:** Validation rules must be maintained as agent capabilities evolve. Static rules quickly become stale. Consider LLM-as-validator for semantic checks.

---

### Human-Agent Interaction Patterns *(Ch. 8)*

#### Agent Calls Human (HITL Escalation)
**What it is:** The agent autonomously determines it cannot proceed safely or confidently and proactively escalates to a human, providing context, the reason for escalation, and a recommended next action.  
**When to use:** When the agent encounters ambiguity above a confidence threshold; when actions would be irreversible without human sanction; regulatory or compliance-mandated review points.  
**Key consideration:** Escalation quality depends on the context the agent provides. Poor escalation messages lead to human confusion, not resolution. Define the escalation message schema.

---

#### Human Delegates to Agent
**What it is:** A human explicitly assigns a task to an agent with defined scope, time horizon, and outcome criteria. The agent operates autonomously within those bounds and reports back at completion or at defined checkpoints.  
**When to use:** Repetitive or time-consuming tasks a human initiates but should not supervise step-by-step; batch processing; background research.  
**Key consideration:** Scope creep is the primary risk. The delegation contract (boundaries, success criteria, escalation triggers) must be explicit and machine-readable.

---

#### Collaborative Co-piloting
**What it is:** Human and agent work on the same task simultaneously, with the agent providing real-time suggestions, completions, or alternative options while the human retains final authority.  
**When to use:** Creative, knowledge-intensive, or judgment-heavy tasks; onboarding scenarios where humans are learning; tasks where human context cannot be fully specified in advance.  
**Key consideration:** If the agent overwhelms the human with suggestions, cognitive load increases and the human disengages. Tune the intervention frequency and confidence threshold.

---

### Agent-Level Patterns *(Ch. 9)*

#### Single Agent Baseline
**What it is:** A single LLM-powered agent with a defined role, tool set, and memory handles the full task end-to-end. The simplest viable agentic unit and the starting point before adding complexity.  
**When to use:** Always start here. Validate that a problem actually requires multi-agent complexity before adding orchestration. Use as the Maturity Level 3 reference implementation.  
**Key consideration:** The tendency is to over-engineer. A well-tuned single agent often outperforms a poorly coordinated multi-agent system.

---

#### ReAct Agent (Reason + Act)
**What it is:** The agent interleaves a reasoning step (think about what to do next) with an action step (invoke a tool or produce output), then observes the result before reasoning again. Explicit thought-action-observation loops.  
**When to use:** Tasks requiring dynamic, multi-step decision-making where the next action depends on previous observations; debugging or diagnostic tasks; tool-heavy workflows.  
**Key consideration:** Reasoning steps consume tokens and add latency. Set a maximum number of reason-act iterations to prevent infinite loops.

> **Design Rationale — Why this framework uses fixed procedures instead of ReAct (ref. ADR-0010)**
>
> ReAct is more adaptive than fixed-procedure agents but less predictable. In this feedback loop
> system, predictability is the superior property: each agent run must produce a comparable,
> reproducible output so that session-over-session improvement can be measured against a stable
> baseline. ReAct's dynamic reason-act loops introduce output variability that would make that
> measurement unreliable.
>
> Adaptability is achieved through the feedback loop itself — weekly rule updates and structured
> session analysis — not through per-invocation dynamic reasoning.
>
> **Note:** Some tasks (e.g., open-ended codebase research) could genuinely benefit from ReAct's
> adaptive probing. If you are considering ReAct for such a task, raise an ADR to assess the
> auditability trade-off before introducing it. See ADR-0010 for the full decision record.

---

#### Memory-Augmented Agent
**What it is:** The agent is equipped with structured memory: short-term (in-context), working (scratchpad), and long-term (vector store or DB). It explicitly reads, updates, and queries memory as part of its procedure.  
**When to use:** Agents operating across multiple sessions or turns; personalisation scenarios; tasks where earlier context influences later decisions.  
**Key consideration:** Memory retrieval quality is the bottleneck. Invest in chunking and embedding quality. Implement memory expiry and relevance scoring.

---

### System-Level Patterns for Production Readiness *(Ch. 10)*

#### Tool and Agent Registry
**What it is:** A centralised catalogue of available tools and agents — their identities, capabilities, input/output schemas, versioning, and health status. Agents discover and invoke capabilities through the registry.  
**When to use:** Multi-agent systems with more than 3–4 agents or tool sets; systems that evolve over time with new capabilities added; enterprise deployments requiring governance of available capabilities. Introduce when the system reaches 5+ active agents OR 10+ active skills, whichever comes first.  
**Key consideration:** The registry is a new single point of failure. Implement caching and failover. Enforce schema versioning to prevent breaking changes.

---

#### Lifecycle Callbacks / AgentOps
**What it is:** Structured hooks fired at key agent lifecycle events (task start, tool call, tool response, reasoning step, task end, error) that feed an observability pipeline — enabling tracing, logging, metrics, and cost tracking per agent invocation.  
**When to use:** All production agentic systems. Non-negotiable for debugging, compliance, cost management, and performance optimisation.  
**Key consideration:** Callback overhead adds latency. Use async emission where possible. Define a consistent event schema across all agents from day one.

**ADK ↔ VS Code hook equivalence** *(verified against ADK 1.x — review if ADK major version changes)*

| ADK Event | VS Code Hook | Schema notes |
|---|---|---|
| `on_agent_start` | `SessionStart` | ADK includes `trace_id`; VS Code does not (see ADR-0011) |
| `on_tool_call` | `PreToolUse` | ADK has typed tool schema; VS Code passes stdin JSON |
| `on_tool_response` | `PostToolUse` | Similar structure; both carry tool name and output |
| `on_agent_end` | `SessionEnd` / `Stop` | VS Code has two variants (graceful vs. interrupted); ADK has one |
| *(no equivalent)* | `PreCompact` / `PostCompact` | VS Code-specific; context compression has no ADK analogue |

---

### Advanced Adaptation *(Ch. 11)*

#### Self-Improvement Flywheel
**What it is:** A continuous learning loop where agent outputs are evaluated, feedback is collected (human or automated), and the agent's prompts, fine-tuning data, or retrieval corpus is updated — creating a compounding improvement cycle.  
**When to use:** Production agents with measurable output quality; systems with enough volume to generate statistically significant feedback; agents where the task distribution shifts over time.  
**Key consideration:** Feedback loops can amplify errors if evaluation quality is poor. Require human validation of a sample before feeding data back into the improvement cycle.

---

#### R⁵ Model (Production Agent Framework)
**What it is:** A five-phase operational framework for production agents: **Receive** (accept task), **Reason** (plan approach), **Retrieve** (gather knowledge), **React** (execute with tools), **Report** (produce verifiable output). Each phase has defined inputs, outputs, and quality gates.  
**When to use:** As the internal architecture template for any production-grade agent. Ensures all five operational concerns are explicitly addressed rather than left implicit.  
**Key consideration:** Not a rigid sequential pipeline — phases can loop (Reason → Retrieve → Reason). Design transition conditions between phases explicitly.

---

## Pattern Selection Guide

| Situation | Recommended Pattern(s) |
|-----------|------------------------|
| Task has clear serial stages | Prompt Chaining (Gulli 1) |
| Input can be one of several types | Agent Router (A&B) or Routing (Gulli 2) |
| Independent sub-tasks exist | Parallelization (Gulli 3) |
| Output quality must be verified | Reflection (Gulli 4) or Parallel Execution Consensus (A&B) |
| Task requires external data or actions | Tool Use (Gulli 5) |
| Task is long-horizon or ambiguous | Planning (Gulli 6) + R⁵ Model (A&B) |
| Task requires many expert roles | Hierarchical Orchestrator (A&B) + Multi-Agent (Gulli 7) |
| Agent needs cross-session memory | Memory-Augmented Agent (A&B) + Memory Management (Gulli 8) |
| Knowledge is stale or insufficient | RAG (Gulli 14) |
| High-stakes or irreversible actions | Agent Calls Human (A&B) + HITL (Gulli 13) |
| Production reliability required | Circuit Breaker (A&B) + Exception Handling (Gulli 12) |
| Cost or latency must be controlled | Resource-Aware Optimization (Gulli 16) |
| User-facing or regulated system | Guardrails (Gulli 18) + Secure Agent (A&B) |
| Compliance or audit required | Instruction Fidelity Auditing (A&B) + Decision Audit Trail (A&B) |
| Need to assess org readiness | GenAI Maturity Model (A&B) |
| Building first agent for a new domain | Single Agent Baseline (A&B) |
| Dynamic multi-step tool workflows | ReAct Agent (A&B) |
| Production observability required | Lifecycle Callbacks / AgentOps (A&B) |
| Multiple agent capabilities to manage | Tool and Agent Registry (A&B) |

## Common Combinations

- **Reliable assistant:** Tool Use (Gulli 5) + Reflection (Gulli 4) + Guardrails (Gulli 18) + Secure Agent (A&B)
- **Autonomous research agent:** Planning (Gulli 6) + R⁵ Model (A&B) + Parallelization (Gulli 3) + RAG (Gulli 14) + Memory-Augmented Agent (A&B)
- **Production workflow:** Agent Router (A&B) + Circuit Breaker (A&B) + Agent Calls Human (A&B) + Lifecycle Callbacks (A&B) + Evaluation (Gulli 19)
- **Enterprise multi-agent:** Hierarchical Orchestrator (A&B) + A2A (Gulli 15) + Tool Registry (A&B) + Goal Setting (Gulli 11) + Decision Audit Trail (A&B)
- **Cost-optimised pipeline:** Prompt Chaining (Gulli 1) + Resource-Aware (Gulli 16) + Reasoning Techniques (Gulli 17)
- **Compliant regulated system:** Instruction Fidelity Auditing (A&B) + Decision Audit Trail (A&B) + Agent Calls Human (A&B) + Guardrails (Gulli 18) + Evaluation (Gulli 19)
- **New enterprise adoption:** GenAI Maturity Model (A&B) → Single Agent Baseline (A&B) → Hierarchical Orchestrator (A&B) + AgentOps (A&B)
