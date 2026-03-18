# Feature Specifications — Pattern-Driven Design

> **Date:** 2026-03-15
> **Status:** In progress
> **Parent design:** [copilot-feedback-system-pattern-design.md](../copilot-feedback-system-pattern-design.md)
> **Pattern sources:** [patterns-catalogue.md](../../../.github/skills/agentic-patterns/references/patterns-catalogue.md)

Each feature is specified using its governing agentic pattern(s) as the structural driver.
The guide ([copilot-session-feedback-guide.md](../../../.github/docs/copilot-session-feedback/copilot-session-feedback-guide.md)) is a domain content reference only — it provides vocabulary, section names, and example values, not structural decisions.

---

## Stage 1 — Capture

---

### Feature #1 — Stop Hook: Auto-archive session transcripts

**Pipeline Stage:** Capture | **Priority:** High | **Artifact:** `.github/hooks/stop.json`

#### Governing Patterns and Structural Constraints

- **Tool Use (Gulli #5):** The hook is a tool invocation boundary. The pattern mandates a strict tool schema (name, inputs, outputs) and requires guardrails against dangerous tool calls. Every shell command in the script must have defined inputs (stdin JSON fields) and defined side effects (files written, exit codes returned). No unbounded shell operations.
- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** The Stop event is one of eight defined lifecycle events. This pattern mandates a consistent event schema, async-safe execution, and < 500ms script execution time constraint. The hook fires deterministically at session end — the design must not assume any prior hook has run.
- **Exception Handling and Recovery (Gulli #12):** The pattern mandates explicit failure classification. Three exit code classes are required: `0` = success (session archived), `2` = soft block with explanatory message (e.g. disk full, destination unwritable), non-zero other = hard fail (logged, developer notified inline). Failures must never be swallowed silently.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `Stop` | Lifecycle Callbacks — fires at session end, broadest capture window |
| **Script language** | Python (`.py`) | Tool Use — script with defined schema; cross-platform via `#!/usr/bin/env python3` and stdlib only (`json`, `shutil`, `pathlib`) |
| **Stdin fields consumed** | `session_id`, `transcript_path`, `stop_hook_active` | Tool Use — strict input schema |
| **Side effects produced** | Copy transcript to `sessions/YYYY-MM-DD/<session_id>/transcript.json` | Tool Use — defined output |
| **Loop guard** | `stop_hook_active` env-var check at line 1 | Exception Handling — prevents the most common hook failure (infinite Stop loop) |
| **Exit codes** | `0` success, `2` soft-block + stderr message, `1` hard fail | Exception Handling — explicit failure classification |
| **Execution budget** | < 500ms | Lifecycle Callbacks — hooks must not noticeably slow the agent |
| **Token injection** | None (pure archival; no `additionalContext`) | Resource-Aware — no context injection needed at Stop |

**Script structure (derived from Tool Use + Exception Handling pattern mechanics):**
```
1. Loop guard — exit 0 if stop_hook_active == 1
2. Read stdin JSON → extract session_id, transcript_path
3. Validate inputs — exit 2 with message if missing
4. Create destination directory sessions/YYYY-MM-DD/<session_id>/
5. Copy transcript — exit 1 with message if copy fails
6. Write metadata.json (session_id, timestamp, size_bytes)
7. Exit 0
```

**Guide's role:** Section 9 troubleshooting table provides the concrete `stop_hook_active` env-var name. The stdin payload is parsed with `json.loads(sys.stdin.read())` (Python stdlib). Section 6c provides the destination path convention `sessions/YYYY-MM-DD/`.

**Success criterion:** Running the script with a sample stdin JSON produces a correctly structured `sessions/YYYY-MM-DD/` directory and exits `0` within 500ms on a cold filesystem.

---

### Feature #2 — `/compact` Prompt: Manual session compaction

**Pipeline Stage:** Capture | **Priority:** High | **Artifact:** `.github/prompts/compact.prompt.md`

#### Governing Patterns and Structural Constraints

- **Memory Management (Gulli #8):** This is the primary memory consolidation artifact. The pattern defines five memory types that must each be explicitly addressed: short-term (current session decisions), long-term (rules to promote), episodic (what the agent tried and why it failed), procedural (workflow steps discovered), and working (in-flight context to restore). The prompt body must have one section per memory type — not a free-form summary.
- **Self-Improvement Flywheel (A&B Ch. 11):** The compaction output is the flywheel's intake. The pattern requires a `Corrections` section that captures what the agent got wrong this session — this is the raw material that the Analyse stage processes into rules. Without a corrections section, the flywheel has no input. The prompt must force the agent to produce at least one correction candidate per session.
- **Resource-Aware Optimization (Gulli #16):** The prompt is the size-enforcement mechanism for the compaction output. The pattern mandates hard budget caps. The prompt must instruct the agent to produce output within `copilot-instructions.md`'s 200-line budget and to use a token-efficient markdown structure (tables, bullets, not prose paragraphs).

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `agent` | Memory Management — needs filesystem access to read current `copilot-instructions.md` and prior session files before summarising |
| **Tools** | `read_file`, `list_dir` (read-only) | Memory Management — consolidation requires reading existing knowledge; Self-Improvement Flywheel — must NOT write during compaction (human gate before promotion) |
| **Frontmatter `description`** | Trigger on explicit `/compact` invocation + context-window-pressure signal | Lifecycle Callbacks — this prompt runs at a specific lifecycle moment, not ad hoc |
| **Output format** | Structured markdown: five named sections + one corrections table | Memory Management — one section per memory type; Flywheel — corrections table as structured intake |
| **Token budget enforcement** | Prompt instructs: total output < 400 lines; each section < 80 lines | Resource-Aware — hard cap, not advisory |
| **Correction format** | Table: `\| Observation \| Pattern \| Candidate Action \|` | Self-Improvement Flywheel — structured so the Analyse stage can consume it directly |

**Body structure (five sections derived from Memory Management's five memory types):**
```
## Session Decisions (short-term)
What was decided this session and why. Max 20 bullets.

## Rules to Promote (long-term)
Rules observed this session that are not yet in copilot-instructions.md. Use rule format.

## What Was Tried (episodic)
Approaches attempted, outcome, reason for abandonment. Table format.

## Workflow Steps Discovered (procedural)
New reusable workflows found this session. Numbered list.

## Corrections (flywheel intake)
| Observation | Pattern triggered | Candidate Action |
```

**Guide's role:** Section 2C provides the concrete markdown headers and the rule format syntax (`Rule: … Reason: …`). Section 1 provides the token budget numbers (200 lines / ~3000 tokens) used to set the hard cap.

**Success criterion:** Running `/compact` at any point in a session produces a markdown file with all five sections populated, a corrections table with ≥ 1 row, and total output within the 400-line cap.

---

### Feature #3 — PreCompact Hook: Export full context snapshot

**Pipeline Stage:** Capture | **Priority:** Medium | **Artifact:** `.github/hooks/pre-compact.json`

#### Governing Patterns and Structural Constraints

- **Memory Management (Gulli #8):** PreCompact fires at the last possible moment before the agent's context window is wiped. This is the only opportunity to capture what the agent currently knows — its working memory. The pattern's "episodic memory" concept applies directly: the snapshot is an episodic record of active context at compression time. The hook must export every in-context artifact the agent is holding, not a summary.
- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** The `PreCompact` event is one of eight defined lifecycle events. The pattern mandates: event schema consistency (same fields as other hooks), async-safe execution, < 500ms budget, and handling the case where the hook fires but compression is then cancelled (the snapshot must be idempotent — re-running produces the same file, not duplicates).

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `PreCompact` | Lifecycle Callbacks — fires before compression, the only window to capture full context |
| **Stdin fields consumed** | `session_id`, `context_window_usage_ratio`, `messages` array | Memory Management — full messages array is the working memory to preserve |
| **Side effects produced** | Write `sessions/precompact/<session_id>-<timestamp>.json` | Memory Management — episodic record, timestamped to distinguish multiple compressions per session |
| **Idempotency** | File named with timestamp suffix — re-runs produce new file, not overwrite | Lifecycle Callbacks — hook may fire multiple times in long sessions |
| **Exit codes** | `0` success, `2` soft-block (write failed, disk space), `1` hard fail | Exception Handling — same contract as all hooks |
| **Execution budget** | < 500ms | Lifecycle Callbacks |
| **Token injection** | None | Resource-Aware — PreCompact is pure capture; no context injection |

**Script structure:**
```
1. Read stdin JSON → extract session_id, context_window_usage_ratio, messages
2. Validate: if messages array empty, exit 0 (nothing to capture)
3. Generate filename: sessions/precompact/<session_id>-<ISO-timestamp>.json
4. Write full stdin payload to file
5. Exit 0
```

**Guide's role:** Section 6 provides the PreCompact hook configuration syntax (`.github/hooks/pre-compact.json` structure). Section 9 provides the diagnostic use case: "agent forgot my rules" debugging starts by inspecting the PreCompact snapshot.

**Success criterion:** After a /compact invocation, a timestamped JSON file exists under `sessions/precompact/` containing the full message array from the session.

---

### Feature #4 — PostCompact Hook: Re-inject critical rules

**Pipeline Stage:** Capture | **Priority:** Medium | **Artifact:** `.github/hooks/post-compact.json`

#### Governing Patterns and Structural Constraints

- **Memory Management (Gulli #8):** PostCompact fires after the agent's context is wiped. This is the memory restoration event. The pattern's "working memory restoration" mechanic applies: the hook must inject the minimum critical knowledge the agent needs to continue productively. The key constraint from the pattern: "pass only relevant output" — the injection must be < 200 tokens, containing only the highest-priority rules, not the full knowledge base.
- **Exception Handling and Recovery (Gulli #12):** After compaction the agent is in a degraded state (context reset). The pattern's "graceful degradation" strategy applies: the hook's job is to recover the agent to a minimally functional state, not a fully loaded state. If the injection fails (file missing, too large), the recovery path is to inject a single mandatory reminder rather than fail silently.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `PostCompact` | Lifecycle Callbacks — fires after compression, first opportunity to restore state |
| **Stdin fields consumed** | `session_id`, `summary` (the compact summary produced) | Memory Management — the summary tells us what the agent retained; injection fills the gaps |
| **Side effects produced** | None (pure injection via `additionalContext`) | Memory Management — PostCompact is read-only from filesystem perspective |
| **`additionalContext` content** | Top 5 rules from `copilot-instructions.md` by marked priority | Memory Management — "pass only relevant output"; Resource-Aware — hard 200-token cap |
| **Token budget** | `additionalContext` ≤ 200 tokens | Resource-Aware — hard cap; excess tokens waste context window post-compression |
| **Fallback injection** | If priority rules file missing → inject single line: "Review .github/copilot-instructions.md before proceeding" | Exception Handling — graceful degradation, never silent failure |
| **Exit codes** | `0` always (injection is best-effort; failures are degraded, not fatal) | Exception Handling — a failed PostCompact degrades quality but must not block the session |

**Script structure:**
```
1. Read stdin JSON → extract session_id
2. Read .github/copilot-instructions.md → extract lines tagged # PRIORITY: HIGH (custom marker)
3. If no priority lines found → set additionalContext to fallback message
4. Else → build additionalContext from top 5 priority lines, truncate to 200 tokens
5. Output JSON: {"additionalContext": "<content>"}
6. Exit 0
```

**Guide's role:** Section 6d specifies the `additionalContext` field constraint (200 tokens) and suggests "critical project rules" as the injection content. Section 1 provides the convention for marking high-priority rules.

**Success criterion:** After any compaction event, the agent's next response correctly references at least one project-specific rule that was not in its compressed summary, confirming re-injection worked.

---

### Feature #5 — SessionStart Hook: Inject project metadata

**Pipeline Stage:** Capture | **Priority:** Medium | **Artifact:** `.github/hooks/session-start.json`

#### Governing Patterns and Structural Constraints

- **Tool Use (Gulli #5):** SessionStart must invoke read-only subprocess calls (e.g. `git rev-parse`, parsing `package.json` with Python's `json` module) to retrieve live metadata — project name, current branch, version. The pattern requires a strict tool schema: inputs are implicit (the workspace filesystem), outputs are the `additionalContext` JSON payload. The tools invoked must be safe (read-only, no shell expansion).
- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** This is the orientation hook — it fires once at session start. The pattern mandates the event fires exactly once per session and that the `additionalContext` payload follows the consistent event schema. The hook should provide orientation data, not instructions — instructions live in `copilot-instructions.md`.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `SessionStart` | Lifecycle Callbacks — single orientation event at session open |
| **Tools invoked** | `subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])`, `subprocess.run(['git', 'log', '-1', '--format=%H'])`, `json.load(open('package.json'))['version']` | Tool Use — read-only subprocess calls and stdlib JSON; no shell expansion |
| **`additionalContext` fields** | `project`, `branch`, `commit_sha`, `version`, `timestamp` | Tool Use — strict output schema |
| **Token budget** | ≤ 100 tokens (5 key-value pairs) | Resource-Aware — orientation, not instruction; minimal footprint |
| **Failure mode** | Any tool failure → omit that field, continue (no exit 2) | Exception Handling — graceful degradation; partial metadata is better than no session start |
| **Exit codes** | `0` always | Exception Handling — SessionStart must never block session opening |

**Guide's role:** Section 6a provides the hook configuration format and the specific `git` commands to use for branch and commit extraction.

**Success criterion:** Session opens and the agent's first response correctly names the current branch when asked about the project context.

---

### Feature #6 — SessionEnd Hook: Log session metrics

**Pipeline Stage:** Capture | **Priority:** Low | **Artifact:** `.github/hooks/session-end.json`

#### Governing Patterns and Structural Constraints

- **Evaluation & Monitoring (Gulli #19):** SessionEnd is the primary metrics collection point. The pattern requires systematic measurement with defined metrics and automated collection. The hook must record a fixed schema per session — timestamp, session duration, session ID — to enable the trend analysis (corrections per session trending down) that the Validate stage depends on.
- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** SessionEnd fires once per session close. The pattern stipulates async-safe, non-blocking emission. The hook must not block session closure (exit 0 always). The metrics file (`sessions/metrics/sessions.jsonl`) is the observability pipeline output.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `SessionEnd` | Lifecycle Callbacks — fires at session close, last capture opportunity |
| **Metrics recorded** | `session_id`, `start_ts`, `end_ts`, `duration_seconds`, `turn_count` | Evaluation & Monitoring — minimum viable metric set for trend analysis |
| **Output file** | Append one JSON line to `sessions/metrics/sessions.jsonl` | Evaluation & Monitoring — JSONL enables incremental analysis without rewriting history |
| **Exit codes** | `0` always | Lifecycle Callbacks — metrics collection must never block session close |
| **Token injection** | None | Resource-Aware — SessionEnd is post-session; no context injection needed |

**Guide's role:** Section 6e provides the `sessions.jsonl` field schema and the five metrics to track (corrections/session, time to first correct output, feedback debt size, stale rule count, hook failure rate). This hook captures the timestamp/duration subset; corrections are manually tallied.

**Success criterion:** After 3 sessions, `sessions/metrics/sessions.jsonl` contains 3 newline-delimited JSON objects each with `session_id`, `start_ts`, and `end_ts` populated.

---

### Feature #7 — Notification Hook: Route agent notifications externally

**Pipeline Stage:** Capture | **Priority:** Low | **Artifact:** `.github/hooks/notification.json`

#### Governing Patterns and Structural Constraints

- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** The `Notification` event fires whenever the agent produces a user-facing notification. The pattern stipulates that this hook is purely an observability emission point — it records or forwards the notification but must not alter agent behaviour. Async emission is mandatory (webhook call must be fire-and-forget with a timeout, not a blocking HTTP call).
- **Exception Handling and Recovery (Gulli #12):** Webhook calls fail. The pattern's "graceful degradation" strategy applies: if the webhook URL is unreachable or returns non-2xx, the hook must exit `0` (soft fail) and log the failure locally. The external system is non-critical — a failed notification must never block the agent.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `Notification` | Lifecycle Callbacks — notification emission point |
| **Activation** | Opt-in via `.env` file: `COPILOT_WEBHOOK_URL=<url>` | Exception Handling — if not configured, hook exits 0 immediately; no webhook = no risk |
| **Payload forwarded** | Full stdin JSON (notification type, message, session_id) | Lifecycle Callbacks — consistent event schema; consumer decides what to use |
| **HTTP method** | POST with `Content-Type: application/json`, 2s timeout | Exception Handling — hard timeout prevents blocking; fire-and-forget |
| **Failure handling** | Any non-2xx or timeout → log to `sessions/metrics/webhook-errors.log`, exit `0` | Exception Handling — graceful degradation, never blocks |
| **Supported targets** | Any webhook URL (Slack, Teams, custom) | Tool Use — generic tool invocation; target-agnostic |
| **Token injection** | None | Resource-Aware — pure forwarding; no `additionalContext` |

**Guide's role:** Section 6f provides the opt-in configuration pattern and notes this hook is "only needed for team-scale adoption." The webhook payload schema is not prescribed — any notification-capable endpoint works.

**Success criterion:** With a valid `COPILOT_WEBHOOK_URL` set, an agent notification produces a POST to the configured URL within 2 seconds. With no URL configured, the hook exits `0` silently.

---

## Stage 2 — Analyse

---

### Feature #8 — Four Diagnostic Lenses Instruction

**Pipeline Stage:** Analyse | **Priority:** High | **Artifact:** `.github/instructions/feedback-lenses.instructions.md`

#### Governing Patterns and Structural Constraints

- **Routing (Gulli #2):** The four lenses ARE a routing implementation. Each lens is a classifier that assigns a session finding to one of four destination surfaces. The pattern mandates: the router must be lightweight, the classification criteria must be explicit (not fuzzy), and errors cascade to every downstream path. The instruction must provide unambiguous routing rules — one finding cannot match two lenses simultaneously.
- **Reflection (Gulli #4):** Lens application is structured self-critique. The pattern requires a fixed revision budget and a quality gate — not open-ended review. The instruction must specify exactly which session artifacts to inspect (the compact summary's `Corrections` table and `Episodic` section), not "review the session." The lenses are the quality gate threshold.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact type** | `*.instructions.md` with `applyTo: "sessions/**"` | Routing — scoped to session analysis context only; not always-on |
| **Lens count** | Exactly 4 (no more, no fewer) | Routing — pattern requires reliable classification; more lenses increase misclassification |
| **Routing table** | Each lens: symptom → surface → test (is this a recurring correction? → `copilot-instructions.md`) | Routing — explicit, testable routing rules, not descriptions |
| **Classification rule** | Each finding must match exactly one lens; if ambiguous → use the highest-priority lens | Routing — prevents dual-routing errors |
| **Session input scope** | Only the `/compact` output's Corrections table and Episodic section | Reflection — fixed scope prevents over-auditing; these two sections have the densest signal |
| **Output format** | One routing decision per finding: `Lens N → [surface] → [action]` | Routing — lightweight router output that feeds the Document stage directly |
| **Revision budget** | One pass per lens; no iterating | Reflection — fixed budget; avoid audit fatigue |

**Lens routing table (derived from Routing pattern's classification requirement):**

| Lens | Classification criterion | Target surface | Test |
|------|--------------------------|----------------|------|
| 1 — Recurring Correction | Agent made the same mistake in ≥ 2 sessions | `copilot-instructions.md` rule | "Did this appear in last session's corrections too?" |
| 2 — Domain Vocabulary | Agent used wrong term / didn't know a project-specific name | `*.instructions.md` with `applyTo` scoped to file type | "Would a project glossary prevent this?" |
| 3 — Workflow Friction | Developer repeated the same multi-step action ≥ 2 times | `*.prompt.md` or `*.agent.md` | "Would a slash command remove this friction?" |
| 4 — Quality Guardrail | Agent nearly deleted / overwrote something it shouldn't | Hook (PreToolUse exit 2) | "Was this a dangerous tool call that slipped through?" |

**Guide's role:** Section 3 names the four lenses and provides the `applyTo: "sessions/**"` scoping pattern. The target surface names (copilot-instructions.md, *.instructions.md, etc.) come from the guide's six integration surfaces table.

**Success criterion:** Applying the instruction to any `/compact` output produces exactly N routing decisions (one per finding), each specifying a lens number, target surface, and proposed action — no findings left unrouted.

---

### Feature #9 — `/research` Prompt: Structured codebase research

**Pipeline Stage:** Analyse | **Priority:** Medium | **Artifact:** `.github/prompts/research.prompt.md`

#### Governing Patterns and Structural Constraints

- **Routing (Gulli #2):** This prompt is the first step of the RPI (Research → Plan → Implement) chain. Its sole job is to gather and classify information; it must not route findings to surfaces or write any files. The Routing pattern's "router must be lightweight" constraint applies — this prompt does one thing: explore and report.
- **Prompt Chaining (Gulli #1):** The research output is a chain link. The pattern mandates: pass only the relevant prior output to the next stage, not the full conversation. This prompt must produce a structured output that `@planner` can consume without needing to re-read the research conversation. The output format is designed for downstream consumption, not human readability.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `ask` | Routing — research is read-only; `ask` mode prevents accidental writes; human reviews before chaining |
| **Tools** | `read_file`, `list_dir`, `grep_search`, `semantic_search` (read-only set) | Tool Use — research requires filesystem exploration; no write tools |
| **Output format** | Structured Markdown: Findings table + File Index + Open Questions | Prompt Chaining — structured for downstream consumption; findings table is the chain handoff payload |
| **Findings table schema** | `\| File \| Line \| Finding \| Relevance (High/Med/Low) \| Lens \|` | Routing — each finding pre-classified by lens so the chain does not re-classify |
| **Scope constraint** | Prompt accepts `${input:scope}` parameter — research is bounded to a specific directory or file pattern | Resource-Aware — unbounded research wastes tokens; explicit scope required |
| **Chain handoff** | Output section `## Handoff to Planner` contains the findings table only (no prose) | Prompt Chaining — "pass only relevant output"; prose is for human review, table is for the chain |
| **Read-only guard** | Prompt explicitly instructs: no file creation, no edits, no git operations | Tool Use — research phase must produce zero side effects |

**Guide's role:** Section 3 provides the RPI workflow framing and names `/research` as "Phase 1 — Exploration." The six integration surfaces (from Section 2) provide the Lens column values for the findings table.

**Success criterion:** Running `/research` with a specific scope produces a findings table with ≥ 1 row, each row with a pre-assigned Lens value, and a clean `## Handoff to Planner` section that `@planner` can consume without reading the research prose.

---

### Feature #10 — `@researcher` Agent: Codebase exploration specialist

**Pipeline Stage:** Analyse | **Priority:** Medium | **Artifact:** `.github/agents/researcher.agent.md`

#### Governing Patterns and Structural Constraints

- **Multi-Agent (Gulli #7):** `@researcher` is the first node in a pipeline topology (Researcher → Planner → Implementer). The pattern mandates clear agent contracts: `@researcher` accepts a research scope and produces a structured findings report — nothing else. It does not plan or implement. The pattern's "prevent context bloat by summarising inter-agent messages" constraint means the agent's output must be a compact structured table, not a full conversation transcript.
- **Routing (Gulli #2):** Within its contract, `@researcher` applies the four diagnostic lenses to classify each finding. The agent is a specialist router — its sole output is pre-classified findings. The Routing pattern's "router must be reliable" constraint means the agent must use the lens routing table from Feature #8 as its classification algorithm, not ad hoc judgement.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `agent` with read-only tool set | Multi-Agent — agents act autonomously within scope; must not require human intervention during research |
| **Tools** | `read_file`, `list_dir`, `grep_search`, `semantic_search` only | Tool Use + Multi-Agent — research agent has no write permissions; scope contract enforced via tool restriction |
| **Handoff target** | `@planner` (explicit `handoffs: [planner]` in frontmatter) | Multi-Agent — pipeline topology; must declare downstream agent in contract |
| **Handoff payload** | Structured `## Handoff to Planner` section with findings table only | Prompt Chaining — "pass only relevant output"; the table is the inter-agent message |
| **Scope parameter** | Accepts `research_scope` (directory, file pattern, or question) from the invoking human | Multi-Agent — agent contract specifies accepted input; prevents unbounded exploration |
| **Read-only enforcement** | System prompt explicitly prohibits `write_file`, `edit_file`, `run_in_terminal` | Tool Use — research phase produces zero side effects |
| **Adoption phase** | Week 4 | GenAI Maturity Model — multi-agent topology requires Week 1–2 foundations to be stable first |

**Agent frontmatter:**
```yaml
---
name: researcher
description: Read-only codebase exploration specialist. Accepts a research scope,
  applies the four diagnostic lenses, and produces a structured findings table
  for handoff to @planner.
tools: [read_file, list_dir, grep_search, semantic_search]
handoffs: [planner]
---
```

**Guide's role:** Section 4 (Template 4a) provides the researcher agent persona description and the output template fields. The lens classifications come from Feature #8's routing table, not the guide.

**Success criterion:** Invoking `@researcher` with a defined scope produces a `## Handoff to Planner` table with ≥ 1 finding per lens category observed, and the agent makes zero file writes during execution.

---

### Feature #11 — `feedback-analyser` Skill: Apply lenses to session artifacts

**Pipeline Stage:** Analyse | **Priority:** Low | **Artifact:** `.github/skills/feedback-analyser/SKILL.md`

#### Governing Patterns and Structural Constraints

- **Routing (Gulli #2):** The skill codifies the four-lens routing algorithm as portable procedural memory. Once the routing procedure is stable (after Week 4 validation), it should be extracted from the `@researcher` agent into a standalone skill that any agent or prompt can invoke. The Routing pattern's "router must be lightweight and reliable" constraint means the skill must contain the exact lens routing table (from Feature #8), not a verbal description.
- **Reflection (Gulli #4):** The skill includes the self-critique mechanics: fixed scope (only compact summaries and corrections tables), fixed revision budget (one pass per lens), and a quality gate (minimum signal threshold — only act on findings with ≥ 2 occurrences).

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Skill surface** | `SKILL.md` with `triggers` list in frontmatter | Multi-Agent — skills are procedural memory callable by any agent; frontmatter makes them discoverable |
| **Triggers** | `analyze session`, `apply lenses`, `classify findings`, `feedback analysis` | Routing — trigger words match the routing use case |
| **Body structure** | Section 1: When to use; Section 2: Input requirements; Section 3: Lens routing table; Section 4: Output format; Section 5: Quality thresholds | Routing + Reflection — procedure maps directly to pattern mechanics |
| **Quality threshold** | Only classify findings that appear in ≥ 2 sessions' corrections tables | Reflection — avoids over-auditing one-off issues; pattern's "avoid infinite loops" translated to recurrence gating |
| **Adoption phase** | Week 4+ (after the lens procedure has been validated in ≥ 4 sessions) | GenAI Maturity Model — skills codify proven procedures, not experimental ones |
| **Bundled reference** | Include Feature #8's lens routing table as a bundled resource | Resource-Aware — skill ships with the reference it needs; no external dependency |

**Skill frontmatter:**
```yaml
---
name: feedback-analyser
description: Applies the four diagnostic lenses (Recurring Correction, Domain
  Vocabulary, Workflow Friction, Quality Guardrail) to a compaction summary and
  returns a structured routing table mapping each finding to an integration surface.
  Use after running /compact when analysis of the session is needed.
---
```

**Guide's role:** Section 3 provides the lens names and their target surface mappings. The procedure in this skill supersedes the guide's prose description with a structured routing algorithm.

**Success criterion:** Any agent that loads this skill can apply the four lenses to a compact summary and produce a routing table in a single pass, without needing to re-read the guide.

---

## Stage 3 — Document

---

### Feature #12 — Rule Writing Checklist Instruction

**Pipeline Stage:** Document | **Priority:** High | **Artifact:** `.github/instructions/rule-writing.instructions.md`

#### Governing Patterns and Structural Constraints

- **Guardrails / Safety (Gulli #18):** This instruction is the Document stage's primary guardrail. The pattern mandates input validation before content reaches downstream systems. Here the "input" is a candidate rule and the "downstream system" is `copilot-instructions.md`. The six checklist items are the validation layer — a rule that fails any item must be revised or discarded before promotion. The pattern also specifies the trajectory principle: guardrails must reject negatively framed content (instructions that describe what to avoid increase reproduction probability).
- **Instruction Fidelity Auditing (A&B Ch. 6):** The checklist is a pre-commit quality gate. The IFA pattern requires a structured log of what instructions were received and how they were interpreted. Applied here: each rule must include a `Reason:` clause that documents why the rule was created, creating an auditable trace that the `/audit` prompt can later verify.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact type** | `*.instructions.md` with `applyTo: "**/*.instructions.md,**/copilot-instructions.md"` | Guardrails — applies whenever the agent is editing any instruction file; the validation fires at the right moment |
| **Checklist item count** | Exactly 6 (no more) | Guardrails — more items increase gate fatigue; pattern requires friction-minimised guardrails |
| **Item format** | Each item is a binary pass/fail test: "Does the rule use positive framing? (✓ 'Do X' not ✗ 'Don't X')" | Guardrails — binary checks, not judgment calls; reduces rubber-stamping |
| **Mandatory `Reason:` clause** | Every rule must include `Reason: <why this rule was created>` | Instruction Fidelity Auditing — the reason is the audit trace; without it the `/audit` prompt cannot assess whether the rule is still valid |
| **Failure action** | If any checklist item fails → revise the rule, do not commit | Guardrails + HITL — human review gate is enforced by explicit instruction |
| **Gate fatigue mitigation** | Instruction includes: "Apply this checklist to at most 2 new rules per session" | HITL — pattern warns against gate fatigue; the instruction encodes the mitigation |

**The six checklist items (derived from Guardrails pattern's validation layer requirements):**
1. **Positive framing** — Does the rule say what TO do, not what to avoid?
2. **Includes reasoning** — Does the rule end with `Reason: <why>`?
3. **Specific enough** — Could the agent apply this rule without asking a follow-up question?
4. **Correctly scoped** — Should this be in `copilot-instructions.md` (always-on) or a scoped `*.instructions.md`?
5. **Non-contradictory** — Does this rule conflict with any existing rule in the file?
6. **Tested** — Has this rule been confirmed to produce the intended behaviour in at least one session?

**Guide's role:** Section 4 names the six checklist items and provides the `Reason:` clause syntax. The trajectory principle (positive framing) is explained in Section 4 with examples.

**Success criterion:** Any rule added to `copilot-instructions.md` after this instruction is active passes all six checklist items and includes a `Reason:` clause.

---

### Feature #13 — Token Budget Reference Instruction

**Pipeline Stage:** Document | **Priority:** Medium | **Artifact:** Entry in `copilot-instructions.md` (or `.github/instructions/token-budget.instructions.md`)

#### Governing Patterns and Structural Constraints

- **Resource-Aware Optimization (Gulli #16):** This is the pattern's direct implementation artifact. The pattern mandates hard budget caps — not advisory limits. The instruction must encode the exact token counts as hard constraints, not recommendations, and must specify the behaviour when a limit is exceeded (split into a scoped `*.instructions.md`, not truncate).

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact placement** | Rule in `copilot-instructions.md` (always-on) | Resource-Aware — token budgets apply to all surfaces; scoping would allow bypass |
| **Constraint type** | Hard caps with explicit overflow action | Resource-Aware — "set hard budget caps; soft caps only work if enforced" |
| **Format** | Table: Surface → Max size → Overflow action | Resource-Aware — structured reference, not prose; agent can check a table |
| **Caps defined** | `copilot-instructions.md` ≤ 200 lines; `*.instructions.md` ≤ 100 lines; `SKILL.md` ≤ 500 lines; hook `additionalContext` ≤ 200 tokens | Resource-Aware — guide's numbers validated against the guide's context window budget section |
| **Overflow action** | Each cap row specifies: "if exceeded → [specific action]" e.g. split by domain into scoped files | Resource-Aware — hard cap with defined overflow prevents truncation as a workaround |

**Budget table (the instruction's content, derived from Resource-Aware pattern's "track cost per invocation, set hard caps" requirement):**

| Surface | Hard cap | If exceeded |
|---------|----------|-------------|
| `copilot-instructions.md` | 200 lines | Split domain-specific rules into `*.instructions.md` with `applyTo` |
| `*.instructions.md` | 100 lines per file | Create a second scoped file for the same domain |
| `SKILL.md` | 500 lines | Split into core SKILL.md + bundled reference documents |
| Hook `additionalContext` | 200 tokens | Select only the 3–5 highest-priority rules; summarise |
| `*.prompt.md` body | 150 lines | Extract reusable sections into a skill reference |

**Guide's role:** Section 1's "Managing Your Context Window Budget" table provides the exact numbers used in this instruction. The overflow actions are derived from the guide's "split aggressively" and "scoped instructions" recommendations.

**Success criterion:** The agent correctly rejects (or flags for splitting) any knowledge artifact that exceeds its cap when this instruction is active.

---

### Feature #14 — Integration Surface Templates (Template Library Skill)

**Pipeline Stage:** Document | **Priority:** Medium | **Artifact:** `.github/skills/template-library/SKILL.md`

#### Governing Patterns and Structural Constraints

- **Resource-Aware Optimization (Gulli #16):** The template library is a context injection optimiser. Rather than including all six template structures in every prompt, the skill bundles them as on-demand references. The pattern's "caching" strategy applies: templates are loaded once into the skill, not repeated in every instruction file.
- **Guardrails / Safety (Gulli #18):** Each template encodes guardrails: the correct structure for each surface prevents common quality failures (missing `applyTo`, missing `Reason:` clauses, missing exit codes in hooks). Templates are validated guardrails, not blank scaffolds.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Skill surface** | `SKILL.md` with bundled template files in `references/` subdirectory | Resource-Aware — on-demand loading; templates are referenced not inlined |
| **Templates bundled** | One per surface: T1 `copilot-instructions.md` rule, T2 `*.instructions.md`, T3 `*.prompt.md`, T4 `*.agent.md`, T5 `SKILL.md`, T6 hook JSON | Guardrails — each template encodes the mandatory fields for that surface |
| **Template format** | Each template includes mandatory fields (marked `# REQUIRED`), optional fields (marked `# OPTIONAL`), and validation notes | Guardrails — binary: required fields are non-negotiable guardrails |
| **Trigger phrases** | `create rule`, `write instruction`, `write prompt`, `create agent`, `write skill`, `configure hook` | Resource-Aware — skill loads only when a template is needed |
| **Guardrail encoding** | T1 includes `Reason:` clause; T2 includes `applyTo`; T6 includes exit code schema | Guardrails — the template IS the guardrail; correct use prevents the most common quality failures |

**Guide's role:** Section 4 contains all six template structures. This skill wraps those templates with REQUIRED/OPTIONAL annotations and validation notes that are not present in the guide. The guide templates become the content; the pattern adds the validation layer.

**Success criterion:** An agent using this skill to create any of the six surface types produces an artifact with all required fields populated correctly, without needing to consult the guide.

---

## Stage 4 — Route

---

### Feature #15 — Routing Decision Tree Instruction

**Pipeline Stage:** Route | **Priority:** High | **Artifact:** `.github/instructions/routing.instructions.md`

#### Governing Patterns and Structural Constraints

- **Routing (Gulli #2):** The decision tree IS the Routing pattern's core artifact. The pattern mandates: the router is lightweight, classification rules are explicit and non-overlapping, and errors cascade downstream. This instruction must encode the routing algorithm as a decision tree (not a prose description) with explicit terminal nodes (one surface per path) and unambiguous branch conditions.
- **Human-in-the-Loop (Gulli #13):** The Route stage has a mandatory human review gate before any artifact is committed. The pattern specifies three gate types: approval (block until approved), notification (inform, continue), and review (human can amend). This instruction must include the human review gate as a step in the routing procedure — not as an optional suggestion.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact type** | `*.instructions.md` with `applyTo: "sessions/**,docs/design/**"` | Routing — applies during Document/Route stages; not always-on |
| **Tree format** | Nested decision questions with terminal surface nodes | Routing — decision tree, not flowchart description; agent can execute it step by step |
| **Branch count** | 6 terminal nodes (one per integration surface) | Routing — six surfaces = six paths; no path leads to "unclear" |
| **Human gate placement** | Explicit step after routing decision, before file write | HITL — the gate is a mandatory procedure step, not advisory |
| **Gate format** | "Stop. Present the routing decision and proposed artifact to the human for approval before writing any file." | HITL — approval gate (block until approved); unambiguous stop instruction |
| **Override path** | If human rejects routing decision → return to Analyse stage | HITL — review gate allows amendment; routing is not final until human approves |

**Decision tree (derived from Routing pattern's explicit classification requirement):**
```
Is the finding a recurring agent correction?
  → YES: → copilot-instructions.md rule [→ HUMAN GATE]
  → NO:  Is it domain vocabulary / project-specific naming?
           → YES: → *.instructions.md (applyTo: relevant file type) [→ HUMAN GATE]
           → NO:  Is it a repeated manual workflow?
                    → YES: → *.prompt.md (slash command) [→ HUMAN GATE]
                            Should it involve multi-step agent actions?
                              → YES: → *.agent.md [→ HUMAN GATE]
                    → NO:  Is it reusable procedural knowledge?
                              → YES: → SKILL.md [→ HUMAN GATE]
                              → NO:  Is it a tool call safety issue?
                                       → YES: → Hook (PreToolUse) [→ HUMAN GATE]
```

**Guide's role:** Section 5 contains the Mermaid decision tree that this instruction linearises. The six surface names and their file conventions come from Section 2.

**Success criterion:** Any finding from the Analyse stage can be entered into this decision tree and reach exactly one terminal surface node within 5 decision steps, followed by a human gate before any file is written.

---

### Feature #16 — `@planner` Agent: Phased implementation planning

**Pipeline Stage:** Route | **Priority:** Medium | **Artifact:** `.github/agents/planner.agent.md`

#### Governing Patterns and Structural Constraints

- **Multi-Agent (Gulli #7):** `@planner` is the second node in the RPI pipeline topology. Its contract is specific: accept the `@researcher` handoff table, produce a phased implementation plan, hand off to `@implementer`. The pattern's "clear agent contracts" requirement means the agent's frontmatter must declare its accepted input format (the findings table) and its output format (phased plan). Context bloat prevention: the plan must be a structured document, not a conversation.
- **Prompt Chaining (Gulli #1):** The planner is a chain link. Each stage output must be a clean handoff payload. The pattern mandates: "pass only relevant prior output." The planner's output contains only the phased plan — not the research findings, not prose explanations. The `@implementer` consumes the plan, not the planning process.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `agent` | Multi-Agent — autonomous planning within defined scope; does not require per-step human intervention |
| **Tools** | `read_file`, `list_dir` (read-only during planning; no writes until implementer) | Prompt Chaining — "each link is stateless"; planner reads context but does not execute |
| **Input contract** | Accepts the `## Handoff to Planner` table from `@researcher` | Multi-Agent — explicit input schema; rejects unstructured input |
| **Output format** | Phased plan: Phase A (files to create), Phase B (files to modify), Phase C (validation steps), each with concrete file paths | Prompt Chaining — structured for implementer consumption; no prose |
| **Handoff target** | `@implementer` (explicit in frontmatter `handoffs: [implementer]`) | Multi-Agent — pipeline topology declared in contract |
| **Planning scope** | Planner may ask at most 2 clarifying questions before producing the plan | HITL — bounded human interaction; plan gate is explicit, not conversational |
| **Adoption phase** | Week 4 | GenAI Maturity Model — multi-agent chain requires stable Week 1–2 single-agent workflows |

**Agent frontmatter:**
```yaml
---
name: planner
description: Phased implementation planner. Accepts the researcher handoff table,
  produces a structured Phase A/B/C implementation plan, and hands off to @implementer.
  Does not write any files.
tools: [read_file, list_dir]
handoffs: [implementer]
---
```

**Guide's role:** Section 4 (Template 4b) provides the planner persona description and the Phase A/B/C naming convention. The concrete file path formats come from the guide's six integration surfaces (Section 2).

**Success criterion:** Invoking `@planner` with a researcher handoff table produces a phased plan with concrete file paths for every finding, a clean `## Handoff to Implementer` section, and zero file writes during execution.

---

### Feature #17 — `@implementer` Agent: Plan execution

**Pipeline Stage:** Route | **Priority:** Medium | **Artifact:** `.github/agents/implementer.agent.md`

#### Governing Patterns and Structural Constraints

- **Multi-Agent (Gulli #7):** `@implementer` is the third and final node in the RPI pipeline. Its contract: accept the planner's phased plan, execute each phase using write tools, verify after each phase. The pattern's "clear agent contracts" requirement means the agent must declare its write tool set explicitly — this is the only agent in the chain with write permissions.
- **Tool Use (Gulli #5):** `@implementer` is the only RPI agent that produces side effects. The pattern mandates a strict tool schema and guardrails against dangerous tool calls. All file operations must be auditable: the agent must produce a log of every file written, modified, or deleted during execution.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `agent` | Multi-Agent + Tool Use — autonomous execution within planner-defined scope |
| **Tools** | `read_file`, `write_file`, `edit_file`, `list_dir`, `run_in_terminal` (scoped to test/verify commands only) | Tool Use — write tools required for implementation; terminal scoped to verification, not arbitrary commands |
| **Input contract** | Accepts the `## Handoff to Implementer` phased plan from `@planner` | Multi-Agent — explicit input schema; rejects unstructured "just do X" instructions |
| **Execution contract** | Implements one phase at a time, reports completion, waits for human confirmation before next phase | HITL — phased execution with human gate between phases prevents runaway implementation |
| **Verification step** | After each file write, reads back and confirms the file is syntactically valid | Tool Use — "add guardrails to prevent dangerous tool calls"; verification is the post-write guardrail |
| **Audit log** | Produces `## Changes Made` section listing every file written/modified with its path and change summary | Instruction Fidelity Auditing — auditable trace of every side effect |
| **Adoption phase** | Week 4 | GenAI Maturity Model — requires stable planner handoff |

**Agent frontmatter:**
```yaml
---
name: implementer
description: Plan execution specialist. Accepts the planner handoff document,
  implements each phase step by step, verifies each file after writing, and
  produces a Changes Made log. Requires human confirmation between phases.
tools: [read_file, write_file, edit_file, list_dir, run_in_terminal]
---
```

**Guide's role:** Section 4 (Template 4c) provides the implementer persona and the "one phase at a time" execution pattern. The phase naming (Phase A/B/C) comes from the planner's output format.

**Success criterion:** `@implementer` executing a three-phase plan produces exactly three human confirmation gates (one before each phase), a `## Changes Made` log after execution, and all written files pass a read-back syntax check.

---

### Feature #18 — PreToolUse Hook: Security Gate

**Pipeline Stage:** Route | **Priority:** High | **Artifact:** `.github/hooks/pre-tool-use.json`

#### Governing Patterns and Structural Constraints

- **Guardrails / Safety (Gulli #18):** This is the input validation layer at the tool call boundary. The pattern mandates: input filtering before processing, with PII/dangerous content detection. Applied here: the hook intercepts every tool call before execution and applies a blocked-patterns list. The pattern specifies semantic similarity gates — the blocked list must match intent, not just exact strings (e.g. `rm -rf` AND `Remove-Item -Recurse -Force` both match the "recursive delete" pattern).
- **Exception Handling and Recovery (Gulli #12):** The hook must use exit code `2` (soft block) not `1` (hard fail) for security violations. The pattern's "human escalation" recovery strategy applies: a soft block provides an explanation and prompts the developer to override if the operation is legitimate. Hard fails with no explanation frustrate developers and get disabled.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `PreToolUse` | Lifecycle Callbacks — fires before every tool call; the only place to intercept before side effects |
| **Stdin fields consumed** | `tool_name`, `tool_input` (full parameters) | Guardrails — both the tool name and its parameters are inspected; name alone is insufficient |
| **Blocked categories** | (1) Protected file deletion, (2) Dangerous terminal commands, (3) Credential/secrets access | Guardrails — three categories cover the highest-risk operations; not an exhaustive deny list |
| **Block type** | `exit 2` with a human-readable explanation on stderr | Exception Handling — soft block with explanation; developer can override; hard fail disabled the hook |
| **Protected files list** | `.github/copilot-instructions.md`, `.github/hooks/**`, `.env`, `package.json` | Guardrails — the project knowledge base and hook infrastructure must never be deleted by the agent |
| **Dangerous terminal patterns** | `rm -rf`, `git push --force`, `DROP TABLE`, `Remove-Item -Recurse` | Guardrails — highest-damage patterns; kept short to minimise false positives |
| **False positive mitigation** | Blocked patterns list is project-specific (loaded from `.github/hooks/security-patterns.json`); developer can edit it | Guardrails — "false positive rates affect usability"; configurable list |
| **Override mechanism** | Developer re-runs the command manually (exit 2 blocks the agent, not the terminal) | Exception Handling — graceful degradation; human retains full control |

**Guide's role:** Section 6d provides the hook JSON configuration format and the `stop_hook_active`-equivalent guard for PreToolUse. Section 9 provides the troubleshooting pattern for "hook is blocking legitimate operations."

**Success criterion:** The hook allows all normal file operations, blocks at least one attempt to delete a protected file (exit 2 with message), and causes zero false positives during a normal coding session.

---

## Stage 5 — Validate

---

### Feature #19 — `/verify` Prompt: Check all surfaces are loaded

**Pipeline Stage:** Validate | **Priority:** High | **Artifact:** `.github/prompts/verify.prompt.md`

#### Governing Patterns and Structural Constraints

- **Evaluation & Monitoring (Gulli #19):** `/verify` is the primary evaluation artifact for the Validate stage. The pattern mandates systematic measurement with defined metrics. Applied here: the prompt must check all six surfaces against binary pass/fail criteria — not "does this seem right?" but "is this specific file loaded and producing the correct behaviour?" Each check must be testable with an observable output.
- **Goal Setting & Monitoring (Gulli #11):** The pattern requires specific, testable goals. Each `/verify` check is a goal statement: "Surface X is loaded if [observable condition] is true." Vague checks ("does the agent know the project?") are not permitted — every check must have a concrete pass condition.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `ask` | Evaluation & Monitoring — verification is read-only; `ask` mode prevents accidental writes during a sanity check |
| **Tools** | `read_file`, `list_dir` only | Tool Use — checks require reading files; no writes |
| **Output format** | Status table: `\| Surface \| File \| Check \| Status (✓/✗) \| Action if ✗ \|` | Evaluation & Monitoring — binary status per surface; systematic, not subjective |
| **Surface coverage** | All six surfaces checked: global instructions, scoped instructions, prompts, agents, skills, hooks | Goal Setting — every surface must have at least one specific, testable check |
| **Check design** | Each check has an observable verification method (e.g. "Ask: what is the project name?" → verifies SessionStart hook injection) | Goal Setting — "goals must be specific and testable"; vague checks excluded |
| **Action column** | Each ✗ row includes the specific corrective action (e.g. "Reload VS Code window" / "Check hook JSON syntax") | Exception Handling — failure recovery is part of the verification artifact |
| **Frequency** | Run at: session start (first use of a new artifact); after any hook reconfiguration; after any `copilot-instructions.md` edit | Goal Setting — monitoring triggers are defined, not ad hoc |

**Verification table structure (derived from Evaluation & Monitoring pattern's "ground truth" requirement):**

| Surface | Check | Pass condition | Action if fail |
|---------|-------|----------------|----------------|
| `copilot-instructions.md` | Agent applies project naming convention unprompted | Correct name used in first response | Reload VS Code; check file path |
| `*.instructions.md` | Agent applies scoped rule when editing target file type | Rule applied in correct file context | Verify `applyTo` glob matches file |
| `*.prompt.md` | `/compact` appears in slash command menu | Command visible in `/` list | Check file is in `.github/prompts/` |
| `*.agent.md` | `@researcher` appears in agent selector | Agent visible via `@` | Check file is in `.github/agents/` |
| `SKILL.md` | Agent cites skill content when trigger phrase used | Correct procedural output | Check file is in `.github/skills/` |
| Hook | Stop hook fires and writes to `sessions/` | File present after session end | Check hook JSON syntax via `jq` |

**Guide's role:** Section 10 provides the `/verify` prompt's conceptual purpose and the six surfaces to check. The binary status table format and the "action if fail" column are pattern-derived additions.

**Success criterion:** Running `/verify` at the start of a session produces a complete status table in under 60 seconds, with ✓ for every surface that is correctly loaded and ✗ with a specific action for any that is not.

---

### Feature #20 — Success Metrics Tracking Instruction

**Pipeline Stage:** Validate | **Priority:** Medium | **Artifact:** Entry in `copilot-instructions.md`

#### Governing Patterns and Structural Constraints

- **Goal Setting & Monitoring (Gulli #11):** This instruction is the Goal Setting pattern's direct implementation. The pattern requires: goals must be specific, measurable, and observable; OKR-style objectives with milestone gating. Applied here: five metrics are defined, each with a target value and a trending direction, so the developer and agent can monitor progress without ambiguity.
- **Evaluation & Monitoring (Gulli #19):** The instruction defines the measurement schema. The pattern requires automated collection where possible and human review for validation. Applied here: the SessionEnd hook auto-collects timestamps; corrections per session is the single manual tally; stale rule count is auto-calculated by `/audit`.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact placement** | Rule in `copilot-instructions.md` | Goal Setting — always-on; the agent must know the success metrics to monitor them |
| **Metric count** | Exactly 5 (no more) | Evaluation & Monitoring — more metrics create measurement overhead; pattern warns against vanity metrics |
| **Format** | Table: Metric → Collection method → Healthy target → Anti-metric warning | Goal Setting — each metric must have a specific, testable target |
| **Anti-metric column** | Explicitly lists the vanity metric to avoid for each row | Goal Setting — "vague goals cannot be monitored reliably"; anti-metrics make the distinction concrete |
| **Collection method** | Each row specifies: auto (hook), manual (tally), or auto+verify (audit) | Evaluation & Monitoring — automated where possible, manual only when necessary |

**Metrics table (derived from Goal Setting pattern's "specific and testable" requirement):**

| Metric | Collection | Healthy target | Anti-metric (do not track) |
|--------|-----------|----------------|---------------------------|
| Corrections per session | Manual tally at session end | Trending ↓ over 4 weeks | Rule count (more ≠ better) |
| Time to first correct output | Manual: note when agent first gets it right | Trending ↓ | Session duration |
| Feedback debt backlog | Auto: count open items in `feedback-debt.md` | ≤ 5 open items | Items added per session |
| Stale rule count | Auto: `/audit` output | 0 stale rules | Total rule count |
| Hook failure rate | Auto: `sessions/metrics/sessions.jsonl` | 0 failures per week | Hook count |

**Guide's role:** Section 8's "Measuring Success" table provides the five metric names and healthy targets. The anti-metric column and collection method column are pattern-derived additions that the guide does not include.

**Success criterion:** After 4 sessions with this instruction active, the developer can answer "Is the system improving?" using the five metrics with data, not intuition.

---

### Feature #21 — PostToolUse Hook: Auto-format after file edits

**Pipeline Stage:** Validate | **Priority:** Medium | **Artifact:** `.github/hooks/post-tool-use.json`

#### Governing Patterns and Structural Constraints

- **Tool Use (Gulli #5):** The hook fires as a post-condition check on every tool output. The pattern mandates defined outputs — after a file write, the "output" includes formatting correctness. PostToolUse is the tool schema's output validation step: the file was written, but is it formatted correctly?
- **Guardrails / Safety (Gulli #18):** Auto-format is an output guardrail. The pattern specifies output filtering/validation before delivery. Applied here: the formatter validates that the file produced by the agent meets project formatting standards before it is committed. This is cheaper than post-commit formatting and avoids noisy diffs.
- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** This hook fires on every `PostToolUse` event that matches a file-write tool. The pattern mandates: async-safe, < 500ms, consistent event schema. Because this hook can fire many times per session (once per file write), execution time is critical.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `PostToolUse` (filtered by `tool_name == "write_file" OR "edit_file"`) | Lifecycle Callbacks — fires after file writes only; filtering prevents running on every tool call |
| **Tools invoked** | `subprocess.run(['npx', 'prettier', '--write', file])`, `subprocess.run(['black', file])`, or `subprocess.run(['dotnet', 'format', file])` — selected by file extension | Tool Use — formatters invoked as subprocesses from Python; no shell expansion |
| **Formatter selection** | Derive from file extension; load formatter config from existing project config files | Tool Use — strict tool schema: input = file path, output = formatted file |
| **Execution budget** | < 500ms (async formatter invocation with timeout) | Lifecycle Callbacks — fires on every file write; must not add perceptible latency |
| **Formatter failure handling** | Non-zero formatter exit → log to stderr, exit `0` (continue session) | Exception Handling — formatting failure is non-fatal; the file is still valid code |
| **Token injection** | None | Resource-Aware — PostToolUse is a side-effect hook; no context injection |
| **Adoption phase** | Week 2 | GenAI Maturity Model — requires project formatter to be configured; not Week 1 |
| **File type filter** | Only apply to `.md`, `.ts`, `.js`, `.py`, `.json`, `.yaml` — configurable allowlist | Guardrails — prevent running formatter on binaries or files with no project formatter |

**Guide's role:** Section 6b provides the hook configuration JSON format and the `npx prettier` invocation as the reference implementation. The file extension allowlist is project-specific and not prescribed by the guide.

**Success criterion:** Every Markdown or code file written by the agent during a session is correctly formatted (passes `prettier --check` or equivalent) with zero manual formatter invocations by the developer.

---

## Stage 6 — Maintain

---

### Feature #22 — `/audit` Prompt: Self-audit instruction quality

**Pipeline Stage:** Maintain | **Priority:** High | **Artifact:** `.github/prompts/audit.prompt.md`

#### Governing Patterns and Structural Constraints

- **Reflection (Gulli #4):** `/audit` is the Reflection pattern's primary artifact in this system. The pattern mandates a fixed revision budget and a quality gate to avoid infinite loops. Applied here: the audit has a fixed scope (three flag categories only — contradicted, orphaned, redundant), and actions are triggered only above defined thresholds (contradicted: always act; orphaned: always act; redundant: only act if rule count > 50). The prompt must forbid open-ended critique.
- **Instruction Fidelity Auditing (A&B Ch. 6):** The IFA pattern requires a structured log of instructions received, how they were interpreted, and whether the output they specify still holds. Applied here: each rule in `copilot-instructions.md` is checked against the codebase for evidence that the rule is still valid. A rule without codebase evidence is flagged as orphaned. The `Reason:` clause (from Feature #12) is the primary evidence source.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Agent mode** | `ask` | Reflection — audit is read-only; write mode risks auto-deleting rules without human review |
| **Tools** | `read_file`, `list_dir`, `grep_search` only | Tool Use — audit requires reading the codebase to verify rule evidence; no writes |
| **Flag categories** | Exactly 3: (1) Contradicted, (2) Orphaned, (3) Redundant | Reflection — fixed scope prevents over-auditing; three categories capture 95% of quality issues |
| **Action thresholds** | Contradicted → always flag + delete candidate; Orphaned → always flag + delete candidate; Redundant → only flag if rule count > 50 | Reflection — "set a fixed revision budget"; thresholds prevent audit fatigue |
| **Output format** | Audit report table: `\| Rule \| Category \| Evidence \| Recommended Action \|` | IFA — structured log; Recommended Action column is the deletion cycle input |
| **Evidence requirement** | Each flag must cite `file:line` from the codebase as evidence | IFA — "instructions received and how they were interpreted"; file:line citation is the audit trace |
| **Scope** | Only `copilot-instructions.md` (global rules). Scoped `*.instructions.md` files audited separately if rule count > 15. | Reflection — fixed scope; unbounded audit is the failure mode the pattern guards against |
| **Cadence** | Monthly; skip if rule count < 15 | Reflection + HITL — "run audit monthly, not per-session"; low rule counts need no audit |

**Body structure (derived from Reflection pattern's fixed-scope critique mechanics):**
```
## Audit Scope
List the files being audited and their current rule counts.

## Pass 1 — Contradictions
For each rule: does any other rule in the file contradict it?
Flag: | Rule text | Contradicted by | Recommended Action |

## Pass 2 — Orphaned Rules
For each rule: does the codebase contain evidence this rule is needed?
Flag: | Rule text | Expected evidence | Actual evidence (file:line or NONE) | Recommended Action |

## Pass 3 — Redundancy (only if rule count > 50)
Are any two rules saying the same thing?
Flag: | Rule A | Rule B | Overlap | Recommended deletion |

## Audit Summary
Total rules reviewed. Flags by category. Rules recommended for deletion.
```

**Guide's role:** Section 7 provides the monthly cadence, the rule count thresholds, and the "deletion exercise not review exercise" framing. The file:line citation requirement and the three-category structure are IFA pattern additions.

**Success criterion:** Running `/audit` on `copilot-instructions.md` with 20+ rules produces an audit report in one pass, with every flag citing `file:line` evidence, total execution time < 3 minutes.

---

### Feature #23 — Feedback Debt Tracker (`sessions/feedback-debt.md`)

**Pipeline Stage:** Maintain | **Priority:** Medium | **Artifact:** `sessions/feedback-debt.md`

#### Governing Patterns and Structural Constraints

- **Self-Improvement Flywheel (A&B Ch. 11):** The feedback debt tracker is the flywheel's intake queue. The pattern requires evaluation → feedback → improvement cycle. Without a structured intake queue, observations get lost between sessions. The tracker provides the persistent buffer where unactioned observations wait for the developer's attention. The flywheel operates on the tracker's contents, not on raw session transcripts.
- **Goal Setting & Monitoring (Gulli #11):** The tracker must have testable goals: backlog size ≤ 5 open items (from Feature #20's metrics). The Goal Setting pattern requires milestone gating — each item in the tracker must have a priority and a "session added" counter so the developer knows how long it has been waiting.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact type** | Markdown file (not instruction, not prompt) | Self-Improvement Flywheel — the tracker is the flywheel's working state, not an agent instruction |
| **Update trigger** | Add an item: any session producing a finding that doesn't get actioned immediately | Goal Setting — items accumulate; the tracker is the backlog |
| **Close trigger** | Mark item complete when a corresponding rule/artifact is committed | Self-Improvement Flywheel — the flywheel cycle closes when the observation becomes a rule |
| **Schema per item** | `ID`, `Observation`, `Pattern triggered`, `Sessions seen`, `Priority (P0–P3)`, `Status (Open/In Progress/Done)`, `Linked artifact` | Goal Setting — each item has a testable completion condition (Linked artifact field) |
| **Backlog health check** | If ≥ 5 open items: address P0 first; do not add new items until below 5 | Goal Setting — "backlog size ≤ 5" is the health target; the rule is encoded in the document |
| **Priority scheme** | P0 (blocks work), P1 (recurring friction), P2 (quality improvement), P3 (nice-to-have) | HITL — priority matrix structures human decision-making at Document stage |
| **Sessions counter** | Increment `Sessions seen` each session the issue recurs | Self-Improvement Flywheel — recurrence > 2 is the lens classification trigger for Feature #8 |

**Document structure (derived from Self-Improvement Flywheel's feedback→improvement cycle):**
```markdown
# Feedback Debt Tracker

## Health Check
Open items: N / 5 (target: ≤ 5)
Oldest open item: <ID> (<sessions seen> sessions)

## Open Items
| ID | Observation | Pattern | Sessions | Priority | Status | Linked artifact |

## Closed Items (last 30 days)
| ID | Observation | Closed in session | Artifact created |
```

**Guide's role:** Section 7 provides the tracker template and the P0–P3 priority definitions. The `Sessions seen` counter and the flywheel cycle closing condition (Linked artifact field) are Self-Improvement Flywheel additions.

**Success criterion:** After 4 sessions, the tracker has ≤ 5 open items, all items have a `Sessions seen` count ≥ 1, and at least one item is in `Done` status with a linked artifact.

---

### Feature #24 — Progressive Adoption Roadmap Instruction

**Pipeline Stage:** Maintain | **Priority:** Low | **Artifact:** `.github/instructions/adoption-roadmap.instructions.md`

#### Governing Patterns and Structural Constraints

- **GenAI Maturity Model (A&B Ch. 5):** The roadmap IS the maturity model's application to this system. The pattern mandates four things: explicit maturity target-setting, sequenced level progression, success criteria per level, and a guard against skipping levels. Each week in the roadmap maps to a maturity level with observable entry and exit criteria — not just a list of features to implement.
- **Goal Setting & Monitoring (Gulli #11):** The roadmap provides the macro-level goals. The pattern requires milestone gating: each week has explicit success criteria that must be met before advancing. The instruction must encode the gate conditions as binary checks, not aspirational statements.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Artifact type** | `*.instructions.md` with `applyTo: "sessions/plans/**"` | GenAI Maturity Model — applies during planning sessions; prevents over-engineering |
| **Maturity mapping** | Each week maps to a maturity level with entry criteria | GenAI Maturity Model — "skipping levels creates fragile systems"; entry criteria enforce the sequence |
| **Gate conditions** | Each week has explicit binary exit criteria (must all pass before advancing) | Goal Setting — "goals must be specific and testable"; vague milestones excluded |
| **Level skip guard** | Instruction includes: "Do not implement Week N+1 features until Week N exit criteria are all ✓" | GenAI Maturity Model — explicit skip guard; the most common adoption failure mode |
| **Friction check** | Each week lists friction risk(s) and the mitigation from the Risks table | HITL — gate fatigue awareness baked into the roadmap |

**Roadmap structure (derived from GenAI Maturity Model's five levels and the Goal Setting pattern's milestone gating):**

| Week | Maturity Level | Features | Entry criteria | Exit criteria (all must pass) |
|------|---------------|----------|----------------|-------------------------------|
| **1** | Level 2 — Assisted | #2, #8, #12, #15, #19, #22 | VS Code + GitHub Copilot installed | ✓ `/compact` produces all 5 sections; ✓ Lenses instruction active; ✓ `/verify` shows all ✓ |
| **2** | Level 3 — Automated | #1, #18, #21, #9, #13 | Week 1 exit criteria all ✓ | ✓ Stop hook archives transcripts; ✓ Security gate tested; ✓ PostToolUse formats files |
| **4** | Level 4 — Coordinated | #3, #4, #5, #10, #16, #17, #14, #20, #23 | Week 2 exit criteria all ✓; ≥ 4 sessions completed | ✓ `@researcher` handoff works; ✓ Feedback debt tracker has ≥ 1 closed item |
| **Ongoing** | Level 4–5 | #6, #7, #11, #24, #25 | Week 4 exit criteria all ✓ | ✓ Corrections per session trending ↓ over 4 weeks |

**Guide's role:** The guide's Week 1→2→4→Ongoing structure provides the feature groupings. The maturity level mapping, entry criteria, and exit criteria gate conditions are GenAI Maturity Model additions.

**Success criterion:** A developer following this roadmap reaches Week 4 with ≥ 4 validated sessions and zero "skipped" weeks — confirmed by the exit criteria gates.

---

### Feature #25 — End-of-Session Feedback Checklist (Stop Hook Injection)

**Pipeline Stage:** Maintain | **Priority:** Low | **Artifact:** Addition to `.github/hooks/stop.json` (`additionalContext` field)

#### Governing Patterns and Structural Constraints

- **Self-Improvement Flywheel (A&B Ch. 11):** The end-of-session checklist is the flywheel's prompt — the nudge that keeps observations flowing into the intake queue (Feature #23). Without a systematic reminder, developers forget to capture feedback after focused work sessions. The Flywheel pattern requires the feedback collection step to be frictionless and automatic — injecting it as `additionalContext` at Stop means it fires without developer initiative.
- **Lifecycle Callbacks / AgentOps (A&B Ch. 10):** The injection is added to the Stop hook's `additionalContext` field. The pattern mandates: the event schema is consistent, the injection is < 200 tokens, and the hook remains < 500ms. This injection must be added to Feature #1's stop hook (not a new hook) — it reuses the existing lifecycle event.

#### Design Specification

| Dimension | Decision | Pattern Rationale |
|-----------|----------|------------------|
| **Hook event** | `Stop` (same hook as Feature #1, adds `additionalContext`) | Lifecycle Callbacks — reuses existing event; no new hook infrastructure |
| **Injection mechanism** | `additionalContext` field in `stop.json` | Lifecycle Callbacks — the correct field for context injection at Stop |
| **Checklist item count** | Exactly 6 (no more) | Self-Improvement Flywheel + HITL — more items increase abandonment; 6 is the guide's validated count |
| **Format** | Six binary yes/no questions | Self-Improvement Flywheel — frictionless; developer can answer in 30 seconds |
| **Token budget** | ≤ 150 tokens (6 short questions) | Resource-Aware — combined with Feature #1's archival, the Stop hook stays well under limits |
| **Flywheel connection** | Question 6 explicitly asks: "Add any un-actioned observations to `sessions/feedback-debt.md`?" | Self-Improvement Flywheel — directly feeds the intake queue; the loop closes here |

**The six checklist questions (derived from Self-Improvement Flywheel's evaluate→feedback→improve cycle):**
1. Did the agent make a correction it has made before? (→ Lens 1, `copilot-instructions.md`)
2. Did the agent use a wrong project term? (→ Lens 2, `*.instructions.md`)
3. Did you repeat a multi-step action manually? (→ Lens 3, `*.prompt.md`)
4. Did a dangerous tool call nearly slip through? (→ Lens 4, hook)
5. Run `/compact` to preserve session context?
6. Any un-actioned observations to add to `sessions/feedback-debt.md`?

**Guide's role:** Section 10 provides the six end-of-session checklist items. This feature injects them as `additionalContext` rather than relying on the developer to remember to run them manually.

**Success criterion:** At every session end, the Stop hook injects the six-item checklist and the developer answers each question in ≤ 60 seconds, with resulting observations either actioned immediately or logged in `feedback-debt.md`.

---

## Feature Cross-Reference

| # | Feature | Stage | Priority | Artifact | Week |
|---|---------|-------|----------|----------|------|
| 1 | Stop hook | Capture | High | `.github/hooks/stop.json` | 2 |
| 2 | `/compact` prompt | Capture | High | `.github/prompts/compact.prompt.md` | 1 |
| 3 | PreCompact hook | Capture | Medium | `.github/hooks/pre-compact.json` | 4 |
| 4 | PostCompact hook | Capture | Medium | `.github/hooks/post-compact.json` | 4 |
| 5 | SessionStart hook | Capture | Medium | `.github/hooks/session-start.json` | 4 |
| 6 | SessionEnd hook | Capture | Low | `.github/hooks/session-end.json` | Ongoing |
| 7 | Notification hook | Capture | Low | `.github/hooks/notification.json` | Ongoing |
| 8 | Lenses instruction | Analyse | High | `.github/instructions/feedback-lenses.instructions.md` | 1 |
| 9 | `/research` prompt | Analyse | Medium | `.github/prompts/research.prompt.md` | 2 |
| 10 | `@researcher` agent | Analyse | Medium | `.github/agents/researcher.agent.md` | 4 |
| 11 | `feedback-analyser` skill | Analyse | Low | `.github/skills/feedback-analyser/SKILL.md` | Ongoing |
| 12 | Rule writing checklist | Document | High | `.github/instructions/rule-writing.instructions.md` | 1 |
| 13 | Token budget instruction | Document | Medium | `copilot-instructions.md` (entry) | 2 |
| 14 | Template library skill | Document | Medium | `.github/skills/template-library/SKILL.md` | 4 |
| 15 | Routing decision tree | Route | High | `.github/instructions/routing.instructions.md` | 1 |
| 16 | `@planner` agent | Route | Medium | `.github/agents/planner.agent.md` | 4 |
| 17 | `@implementer` agent | Route | Medium | `.github/agents/implementer.agent.md` | 4 |
| 18 | PreToolUse security gate | Route | High | `.github/hooks/pre-tool-use.json` | 2 |
| 19 | `/verify` prompt | Validate | High | `.github/prompts/verify.prompt.md` | 1 |
| 20 | Success metrics instruction | Validate | Medium | `copilot-instructions.md` (entry) | 4 |
| 21 | PostToolUse auto-format | Validate | Medium | `.github/hooks/post-tool-use.json` | 2 |
| 22 | `/audit` prompt | Maintain | High | `.github/prompts/audit.prompt.md` | 1 |
| 23 | Feedback debt tracker | Maintain | Medium | `sessions/feedback-debt.md` | 4 |
| 24 | Adoption roadmap instruction | Maintain | Low | `.github/instructions/adoption-roadmap.instructions.md` | Ongoing |
| 25 | End-of-session checklist | Maintain | Low | `.github/hooks/stop.json` (addition) | Ongoing |

