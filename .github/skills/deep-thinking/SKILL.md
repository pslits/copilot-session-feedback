---
name: deep-thinking
description: "Applies the four-phase deep-thinking methodology to any coding or design task. Combines the Planning pattern (goal decomposition into ordered atomic steps with preconditions and effects), the Reflection pattern (adversarial self-critique of assumptions and failure modes), the Goal Setting and Monitoring pattern (observable success criteria per phase), and the Human-in-the-Loop gate (plan approval before execution begins). Use when: a task requires careful reasoning before action, when asked to 'plan first', 'think before acting', 'reason through', 'deep think', 'beast mode', 'thorough analysis', or 'don't rush'. Triggers on: 'plan first', 'think through', 'reason deeply', 'deep think', 'beast mode', 'thorough plan', 'analyze before acting', 'planning pattern', 'reflect before'."
metadata:
  version: "1.0.0"
  patterns:
    - "Planning (Ch.6) — goal decomposition, ordered atomic steps"
    - "Reflection (Ch.4) — iterative self-critique loop"
    - "Goal Setting & Monitoring (Ch.11) — observable success criteria"
    - "Human-in-the-Loop (Ch.13) — approval gate before execution"
    - "Prompt Chaining (Ch.1) — structured output feeds next phase"
---

## Deep-Thinking Methodology

Five patterns from agentic design theory, composed into a single sequenced procedure.

---

### Phase 1 — Understand  *(Planning pattern: goal decomposition)*

**Do not act. Do not propose solutions. Read and map only.**

1. Identify all files, modules, and configurations relevant to this task. List them.
2. Read each relevant file completely. Never skim or assume from filenames.
3. Map the current state:
   - What exists today
   - What it does
   - How the parts connect
4. Classify all constraints:

   | Type | Definition |
   |------|-----------|
   | **Hard** | Must not be violated — tests, interfaces, contracts |
   | **Soft** | Conventions, style, preferences |
   | **Unknown** | Rules you cannot yet determine — name them explicitly |

5. State the goal in your own words based on what you read, not the original request.

**Phase 1 output:** A factual current-state map. No opinions, no solutions.

---

### Phase 2 — Reflect  *(Reflection pattern: adversarial self-critique)*

With the full picture from Phase 1, critique before you plan.

1. **Restate the goal** in your own words based on what you actually read.
2. **Decompose into sub-problems.** Break the task into its smallest independent units.
3. **Generate ≥2 approaches** for any non-trivial sub-problem:

   | Field | Content |
   |-------|---------|
   | Approach name | Brief label |
   | What it does | One sentence |
   | Advantages | List |
   | Disadvantages / risks | List |
   | When it is correct | The condition |

4. **Audit your assumptions.** Name three assumptions you are making. For each: what would you do if it were false?
5. **Map failure modes.** What could go wrong during or after implementation? How would each manifest?
6. **Select your approach** for each sub-problem. State the one-sentence reason.

**Phase 2 output:** Reasoned approach selection with explicit tradeoffs and failure mode inventory.

---

### Phase 3 — Plan  *(Goal Setting & Monitoring pattern: observable success criteria)*

Produce a phased plan. Every step must satisfy these properties:

| Property | Requirement |
|----------|-------------|
| **Atomic** | A single, verifiable action |
| **Preconditioned** | States what must be true before this step |
| **Referenced** | Cites the exact file and line range being changed |
| **Ordered** | Does not depend on work not yet completed |
| **Success-tested** | Has an observable criterion for completion |

Plan format:

```
### Phase A: <Name>
Precondition: <what must already be true>

- [ ] Step 1 — <action> (file: <path>, lines: <X–Y>)
  Success: <observable check — test name, linter output, expected state>
- [ ] Step 2 — <action>
  Success: <observable check>

Phase A done when: <aggregate success criterion>

### Phase B: <Name>
...
```

End the plan with an explicit **Out of scope** section: list everything that will *not* be touched.

**Phase 3 output:** A complete, human-readable plan ready for approval.

---

### Phase 4 — Gate  *(Human-in-the-Loop pattern: approval before execution)*

**Do not execute until the human has confirmed the plan.**

Present the plan clearly. Ask one focused question:

> "Does this plan match your intent? Approve to proceed, or tell me what to change."

Wait for explicit approval. If the human requests changes, return to Phase 3 (mini-loop — no need to redo Phases 1 and 2 unless the goal itself changes).

Only after approval: proceed to Phase 5.

---

### Phase 5 — Act  *(Prompt Chaining pattern: phase output feeds next phase)*

Execute the approved plan phase by phase.

After **each phase**:

1. Run the phase's success criteria (tests, linter, type checker as appropriate).
2. Report the outcome: pass/fail for each criterion.
3. If a step produces an unexpected result:
   - Stop.
   - Run a Phase 2 mini-loop on the unexpected result only.
   - Revise the remaining plan steps.
   - Report the revision before continuing.
4. Do not start the next phase until the current phase's aggregate success criterion is met.

---

### Constraints (apply throughout all phases)

- Never speculate about code you have not opened and fully read.
- Never make changes outside the scope defined in Phase 3.
- Never skip a phase. The order exists to prevent premature action.
- Surface uncertainty explicitly rather than guessing.
- Implement changes; do not merely describe them.
- The H-i-t-L gate in Phase 4 is mandatory. The human must confirm before execution starts.
