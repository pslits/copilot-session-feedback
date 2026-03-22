---
description: Design the Copilot Session-to-Knowledge Feedback Loop system using agentic patterns from Gulli and Arsanjani/Bustos. Saves a design document to docs/design/ for use in the next planning phase.
agent: planner
tools:
  - read/readFile
  - edit/createFile
---

Apply the agentic pattern design process to the Copilot Session-to-Knowledge Feedback Loop system defined in the guide below.

Read these files in full before proceeding — all three are mandatory:

- [.github/skills/agentic-patterns/SKILL.md](../skills/agentic-patterns/SKILL.md)
- [.github/skills/agentic-patterns/references/patterns-catalogue.md](../skills/agentic-patterns/references/patterns-catalogue.md)
- [.github/docs/copilot-session-feedback/copilot-session-feedback-guide.md](../docs/copilot-session-feedback/copilot-session-feedback-guide.md)

Do not answer from memory. Extract all system details from the guide.

## System Context

See [.github/skills/feedback-analyser/references/pipeline-context.md](../skills/feedback-analyser/references/pipeline-context.md) for the full system description (goal, inputs, outputs, constraints, sub-systems).

## Instructions

Follow the full procedure from the agentic-patterns skill:

1. Parse the system description above (goal, inputs, outputs, constraints, sub-systems).
2. Identify applicable patterns across **all five tiers** using the catalogue:
   - Gulli Core: serial stages, multiple input types, independent sub-tasks, self-correction, external tools, planning, multiple expert roles
   - Gulli Advanced: persistent memory, knowledge base evolution, explicit goal tracking
   - Gulli Production: cascading failures, high-stakes or irreversible actions, external knowledge
   - Gulli Enterprise: distributed agents, cost/latency bounds, regulated or user-facing
   - Arsanjani/Bustos Architectural: maturity assessment, hierarchical orchestration, explainability, fault tolerance, human-agent interaction modes, agent internal architecture, production observability, capability governance
3. Select the minimum set of patterns — each must have a specific justification referencing the system above.
4. Design the composition: entry point, data flow, human gates.
5. Identify risks and mitigations for each pattern in the context of this system.
6. Derive a **Features to Implement** list: for each selected pattern, identify the concrete VS Code / GitHub Copilot artefact or capability it maps to (agent file, prompt file, skill, hook, instruction file). Group by pipeline stage.
7. **Reflect** — before saving, critique your own design against these three checks (this step is mandatory — do not skip it):
   - Are all pattern justifications tied to a *named element* of the feedback loop (Capture / Analyse / Document / Route / Validate / Maintain)? If not, remove the pattern.
   - Did you check all five tiers? List any tier where you found no applicable pattern and state why.
   - Does any selected pattern conflict with the "lightweight enough to use" constraint? If yes, flag it in Risks.
   Revise the design based on this critique before proceeding.
8. Save the complete design document to `docs/design/copilot-feedback-system-pattern-design.md`.
9. Recommend the next artefacts to build, referencing the saved file.

## Constraints

- Every pattern must be justified against a named element of the feedback loop system described above.
- Check all five tiers before finalising the selection.
- When two patterns conflict in this system, explain the trade-off in terms of the feedback loop's "lightweight enough to use" constraint.
- Do not invent patterns not in the catalogue.
- Do not write code or create agent files.

## Output Format

Produce the full document below and save it verbatim to `docs/design/copilot-feedback-system-pattern-design.md`.

---

### System Summary
[Restate the feedback loop system as you understood it — goal, inputs, outputs, essential constraints]

### Success Criteria

Define what a good design looks like for this system. These criteria are used in the Reflection step and by reviewers evaluating the design.

| # | Criterion | How to verify |
|---|-----------|---------------|
| 1 | Every pipeline stage (Capture/Analyse/Document/Route/Validate/Maintain) has at least one pattern assigned | Check Composition Design |
| 2 | Every pattern has a justification tied to a named pipeline stage | Check Recommended Patterns table |
| 3 | No pattern increases session friction beyond the current manual workflow | Check Risks table |
| 4 | All High-priority features can be implemented without external dependencies beyond VS Code + GitHub Copilot | Check Features to Implement |
| 5 | The design handles the "sensitive transcript" constraint — no PII/code leaks to external services | Check Risks table |

### Reflection Notes
[Populated during step 7 — list any patterns removed after critique, tiers with no applicable patterns and why, and any "lightweight" conflicts flagged]

### Recommended Patterns
| # | Pattern | Source | Tier | Justification (specific to this system) |
|---|---------|--------|------|----------------------------------------|
| 1 | | Gulli / A&B | | |

### Composition Design
[Mermaid diagram or numbered flow mapping patterns to the six pipeline stages: Capture → Analyse → Document → Route → Validate → Maintain]

### Risks and Mitigations
| Pattern | Risk in this system | Mitigation |
|---------|---------------------|------------|
| | | |

### Features to Implement

For each pipeline stage, list the concrete artefacts to build. Each row is one implementable unit of work — the input to the next planning phase.

| # | Pipeline Stage | Feature / Artefact | Pattern(s) | Type | Priority |
|---|---------------|--------------------|------------|------|----------|
| 1 | Capture | | | Agent / Prompt / Skill / Hook / Instruction | High / Medium / Low |

**Priority guidance:**
- **High** — required for the loop to function at all (e.g., transcript capture hook)
- **Medium** — improves loop quality or reduces friction (e.g., compaction prompt)
- **Low** — nice-to-have or advanced capability (e.g., parallel consensus review)

### Next Steps

The design document has been saved to `docs/design/copilot-feedback-system-pattern-design.md`.

To move to the planning phase:
1. Open `docs/design/copilot-feedback-system-pattern-design.md`
2. Use `@pattern-designer` with the Features to Implement table as input to produce a phased implementation plan
3. Or use `@writing-agents` directly to scaffold the High-priority artefacts
