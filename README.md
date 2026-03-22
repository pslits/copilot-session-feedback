# copilot-session-feedback

A GitHub-native system that turns raw GitHub Copilot agent sessions into
durable, reusable knowledge — so each session starts better than the last.

---

## What This Is

Every time you work with GitHub Copilot, you correct it, teach it domain
vocabulary, and discover better workflows. Without a feedback loop, that
knowledge disappears the moment the session ends. This repository implements
a **Session-to-Knowledge Feedback Loop** that captures those signals and
promotes them into the surfaces Copilot reads at the start of every session.

The loop runs entirely inside GitHub Copilot's VS Code extension — no
external services, no infrastructure to maintain.

---

## How It Works

```
Session → Capture → Analyse → Document → Route → Validate
   ↑                                                  │
   └──────────────────────────────────────────────────┘
```

| Stage | What happens |
|-------|-------------|
| **Capture** | Lifecycle hooks archive session events (start, stop, compaction) to `sessions/`. The `/compact` prompt creates a structured summary before context is compressed. |
| **Analyse** | Four diagnostic lenses classify each finding: Recurring Correction, Domain Vocabulary, Workflow Friction, Quality Guardrail. |
| **Document** | Findings are written as candidates for one of six Copilot surfaces (see below). |
| **Route** | Each finding is mapped to exactly one surface. The routing instructions prevent duplication and scope drift. |
| **Validate** | The next session confirms the new knowledge changed Copilot's behaviour. |
| **Maintain** | Stale rules are pruned; conflicts are resolved; the feedback-debt backlog is kept to ≤ 5 open items. |

---

## The Six Knowledge Surfaces

| Surface | File pattern | When to use |
|---------|-------------|-------------|
| Custom instructions | `.github/copilot-instructions.md` | Always-on project rules (commit format, naming, priorities) |
| Conditional instructions | `.github/instructions/*.instructions.md` | Rules scoped to specific files via `applyTo` |
| Prompt files | `.github/prompts/*.prompt.md` | Repeatable slash commands (`/compact`, `/research`, ...) |
| Agent files | `.github/agents/*.agent.md` | Specialist agents in the RPI chain (researcher → planner → implementer) |
| Skill files | `.github/skills/*/SKILL.md` | Domain knowledge bundles loaded on demand |
| Hooks | `.github/hooks/*.py` + `*.json` | Lifecycle callbacks (PreToolUse, Stop, SessionEnd, ...) |

---

## Lifecycle Hooks

Eight hooks instrument the Copilot session lifecycle:

| Hook | Trigger | Purpose |
|------|---------|---------|
| `session-start.py` | Session opened | Injects project metadata (version, branch, trace ID) into context |
| `pre-tool-use.py` | Before any tool call | Blocks file writes to protected paths; guards credential access |
| `post-tool-use.py` | After any tool call | Increments the turn counter; logs file writes |
| `pre-compact.py` | Before context compression | Snapshots the current session state to `sessions/precompact/` |
| `post-compact.py` | After context compression | Re-injects priority rules so they survive compaction |
| `notification.py` | Agent sends a notification | Logs the notification |
| `stop.py` | Session stopped by user | Writes the final session record to `sessions/metrics/sessions.jsonl` |
| `session-end.py` | Session closed | Writes the final metrics record; resets the turn counter |

All hooks are pure-Python, stdlib-only, and run from the repository root as the
working directory. Exit `0` = allow, exit `2` = soft-block (Copilot shows the
message but the developer can override).

---

## The RPI Workflow

For non-trivial changes, three specialist agents handle the work in sequence:

```
@researcher  →  @planner  →  @implementer
```

- **`@researcher`** — read-only codebase exploration; produces a findings table
  with file:line references and diagnostic lens classification.
- **`@planner`** — converts findings into a phased, human-approved plan saved
  to `sessions/plans/YYYY-MM-DD-<slug>.md`.
- **`@implementer`** — executes the approved plan step-by-step with inline
  validation evidence.

Use the `/research` prompt to start the chain.

---

## The HITL Workflow

High-risk or irreversible actions go through a Human-in-the-Loop gate before
execution:

1. Open an issue using the **HITL Intervention Request** template.
2. The `hitl-intake.yml` workflow auto-triages it to `state:triage`.
3. A Reviewer works through the checklist and advances it to
   `state:awaiting-human`.
4. An Approver posts `/approve` or `/reject <rationale>` as an issue comment.
5. The `hitl-gate.yml` workflow applies the decision label and posts an audit
   record.
6. The `hitl-decision-log.yml` workflow records the decision evidence.
7. The `hitl-escalation.yml` workflow fires hourly to detect SLA breaches.

**Available commands** (authorized collaborators only):

| Command | Who | Description |
|---------|-----|-------------|
| `/approve` | Approver | Accept the proposed action |
| `/reject <rationale>` | Approver | Reject — rationale required |
| `/need-info <question>` | Reviewer | Request missing information |
| `/escalate` | Anyone | Manually escalate |

---

## Feedback Debt

`sessions/feedback-debt.md` is the intake queue for observations not yet
promoted to rules. The target is ≤ 5 open items. When `Sessions seen` reaches
2 for any item, it is a Lens 1 signal — promote it to `copilot-instructions.md`.

---

## Repository Layout

```
.github/
  agents/             # RPI specialist agents (researcher, planner, implementer)
  hooks/              # Lifecycle hook scripts + JSON configs
  instructions/       # Scoped instruction files (applyTo)
  prompts/            # Slash-command prompt files
  skills/             # Reusable domain knowledge bundles
  workflows/          # GitHub Actions (HITL gate, escalation, metrics harvest)
  copilot-instructions.md   # Always-on project rules
docs/
  adr/                # Architecture Decision Records
  design/             # Pattern design documents
  hitl/               # HITL runbook, labels, closure checklist
sessions/
  feedback-debt.md    # Intake queue for unactioned findings
  metrics/            # sessions.jsonl — one record per session
  plans/              # RPI plan files
  precompact/         # Pre-compaction snapshots
tests/                # pytest suite for hook scripts
pyproject.toml        # Project metadata + pytest config
```

---

## Getting Started

### Prerequisites

- VS Code with the **GitHub Copilot** extension (agent mode enabled)
- Python 3.11+ (for hook scripts and tests)
- `gh` CLI authenticated (`gh auth login`)

### Hook Configuration

Register the hooks in your Copilot settings
(`settings.json` → `github.copilot.chat.agent.thinkingTool` or the Copilot
hooks configuration UI). Point each hook at the corresponding
`.github/hooks/*.json` file in this repository.

### Running the Tests

```bash
pip install pytest
pytest
```

### Starting a Session

When you open VS Code with this repository, `session-start.py` fires
automatically and injects `project`, `branch`, `commit`, `version`,
`session_opened`, and `trace_id` into the session context.

At the end of a session, run `/compact` to capture a structured summary before
context is compressed.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All changes go through a branch and PR
— direct pushes to `main` are not permitted.

---

## License

[MIT](LICENSE)
