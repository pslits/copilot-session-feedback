# Pipeline Context

Reference description of the Copilot Session-to-Knowledge Feedback Loop for use in
design and analysis prompts.

## System Context

The **Copilot Session-to-Knowledge Feedback Loop** turns raw GitHub Copilot agent sessions into durable, reusable knowledge. It is a six-stage pipeline:

```
Session → Capture → Analyse → Document → Route → Validate
   ↑                                                  │
   └──────────────────────────────────────────────────┘
```

**Goal:** Ensure every agent session produces at least one improvement to the agent's knowledge base, so each subsequent session starts with better context than the last.

**Inputs:**
- Raw session transcripts (JSON, from Stop hooks or GitHub cloud agent logs)
- PreCompact snapshots (JSON, exported before context compression)
- Manual compaction summaries (Markdown, from `/compact` prompt)
- Research / Plan / Implement plan files (Markdown, from RPI workflows)

**Outputs:**
- Rules added to `copilot-instructions.md`
- Conditional instruction files (`*.instructions.md`) with `applyTo` scoping
- Prompt files (`*.prompt.md`) for repeatable slash commands
- Agent files (`*.agent.md`) with handoff chains
- Skill files (`SKILL.md`) with bundled references
- Hook configurations (JSON lifecycle callbacks)

**Constraints:**
- The system must operate within GitHub Copilot's VS Code extension surfaces
- Human review is required before any knowledge is promoted to permanent instructions (guard against encoding bad patterns)
- The feedback loop must be lightweight enough that developers actually use it — high friction = abandonment
- Session transcripts may contain sensitive code or proprietary logic — storage and routing must respect privacy
- The system itself is the thing being improved by the loop: meta-feedback matters

**Key sub-systems (from the guide):**
1. **Capture** — Hook-based transcript archiving (Stop + PreCompact hooks), cloud agent log access, manual compaction prompts, RPI plan file generation
2. **Analyse** — Four diagnostic lenses: Recurring Corrections, Domain Vocabulary Gaps, Workflow Friction, Quality Guardrail Patterns
3. **Document** — Six integration point templates, route decision tree, rule writing checklist
4. **Route** — Mapping each finding to one of six surfaces (custom instructions, conditional instructions, prompt files, agents, skills, hooks)
5. **Validate** — Confirmation the new knowledge is picked up and changes behaviour in the next session
6. **Maintain** — Conflict resolution, self-audit prompt, pruning stale rules
