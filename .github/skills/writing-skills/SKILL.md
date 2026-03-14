---
name: writing-skills
description: "Creates, updates, and corrects Agent Skills following the agentskills.io open standard and the Skill Writer's Guide. Covers the full skill lifecycle: scaffolding directory structure, writing frontmatter with trigger-engineered descriptions, composing procedural body content, planning bundled resources (scripts, references, assets), and validating structure and behaviour. Use when: creating a new skill, updating or improving an existing skill, correcting or fixing a broken skill, converting session knowledge or documentation into a skill, reviewing a skill for anti-patterns, or writing SKILL.md files. Triggers on: 'create skill', 'write skill', 'new skill', 'update skill', 'fix skill', 'correct skill', 'review skill', 'SKILL.md', 'skill writer', 'agent skill'. Do not use for: writing copilot-instructions.md, agent.md, prompt.md, or hook configurations."
metadata:
  version: "1.0.0"
  author: "Paul Slits"
---

# Writing Skills

Create, update, or correct Agent Skills following the agentskills.io open standard.

## Mode Selection

Determine the mode from the user's request:

| Signal | Mode | Section |
|--------|------|---------|
| "Create a skill", "write a skill", "new skill", convert knowledge | **Create** | Create Mode below |
| "Update", "improve", "refactor", "the skill is too verbose" | **Update** | Update Mode below |
| "Fix", "correct", "skill doesn't activate", "skill is broken" | **Correct** | Correct Mode below |

---

## Create Mode (7-Step Process)

### Step 1: Gather Concrete Scenarios

Ask or infer 3–5 concrete usage scenarios covering simple, medium, and edge cases:

| Column | Content |
|--------|---------|
| User Says | The natural-language trigger phrase |
| Skill Should Do | The expected agent behaviour |

Conclude when you have clear scenarios with at least one edge case.

### Step 2: Plan Resources

For each scenario, identify reusable elements:

| Element Type | When to Use | Path |
|-------------|-------------|------|
| **Script** | Same code rewritten repeatedly; deterministic reliability needed | `scripts/` |
| **Reference** | Detailed docs needed on demand (schemas, API docs, checklists) | `references/` |
| **Asset** | Templates, boilerplate, images copied into output | `assets/` |

Output a resource list with justification for each item. If none are needed, skip subdirectories.

### Step 3: Scaffold Directory

Create the skill directory. Name: 1–64 chars, lowercase + hyphens only. Prefer gerund form (`processing-pdfs`, `reviewing-code`). Noun phrases and action-oriented names are also acceptable:

```
.github/skills/<skill-name>/
├── SKILL.md
├── scripts/        (if needed)
├── references/     (if needed)
└── assets/         (if needed)
```

### Step 4: Write the Skill

Work in this order: resources → frontmatter → body.

**4a. Resources first.** Create scripts, references, and assets identified in Step 2. For scripts: avoid hardcoded credentials, include `--dry-run` for destructive operations, pin dependency versions, and design for non-interactive (CLI arguments, not prompts).

**4b. Frontmatter + Body.** Read [references/frontmatter-guide.md](references/frontmatter-guide.md) for the frontmatter template, description rules, body patterns, and body writing rules. Apply them in order: frontmatter first (the description is the most critical field — it determines whether the skill ever activates), then write the procedural body.

### Step 5: Validate

**Structural checks:**

- [ ] `name` matches directory name
- [ ] `description` ≤ 1,024 characters, non-empty, no XML tags
- [ ] `name`: 1–64 chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens, no reserved words (`anthropic`, `claude`)
- [ ] Body ≤ 500 lines
- [ ] No extraneous files (README.md, CHANGELOG.md, INSTALLATION_GUIDE.md)
- [ ] All resources referenced from body (no orphan files)
- [ ] All resource links resolve to existing files

**Functional checks:**

- [ ] Trigger test: a relevant query activates the skill
- [ ] Negative trigger test: an unrelated query does not activate it
- [ ] Procedure test: following the steps produces correct output
- [ ] Edge case test: ambiguous inputs and missing context handled gracefully
- [ ] Multi-model test: consistent behaviour on at least two model sizes
- [ ] Scripts execute successfully (if any)

### Step 6: Iterate

Observe agent behaviour on real tasks. If struggles occur:

1. Identify the gap (missing step, unclear instruction, wrong freedom level).
2. Apply the fix.
3. Re-validate (Step 5 above).

### Step 7: Cross-Model Convergence

Ensure the skill produces equivalent output on GPT 4.1 compared to the Claude Opus baseline.

1. **Establish baseline.** Set the agent model to Claude Opus. Run a representative test scenario and save the output as the reference baseline.
2. **Switch model.** Change the agent model to GPT 4.1.
3. **Run the same scenario.** Execute the identical test scenario on GPT 4.1.
4. **Compare outputs.** Diff the GPT 4.1 output against the Opus baseline. Focus on:
   - Structural completeness (all sections/steps present)
   - Correctness of content (no hallucinated or missing details)
   - Consistent terminology and tone
   - Resource references resolve and are used properly
5. **Diagnose divergences.** If GPT 4.1 output differs materially:
   - **Skipped steps** → Make instructions more explicit; remove ambiguity the model could exploit.
   - **Over-verbose or under-verbose** → Tighten length guidance or add output examples.
   - **Wrong format** → Add concrete format templates or examples inline.
   - **Hallucinated content** → Add guardrails ("Only use information from …", "Do not invent …").
   - **Missed context** → Move critical context from references into the body, or add explicit read instructions.
6. **Apply fixes and re-test.** After each adjustment, re-run the scenario on GPT 4.1 and compare again.
7. **Verify Opus is not regressed.** Switch back to Claude Opus and confirm the baseline output is still equivalent.
8. **Repeat until acceptable.** Iterate steps 3–7 until GPT 4.1 output is the same or acceptably close to the Opus baseline.

---

## Update Mode

1. Read the existing skill's SKILL.md and all bundled resources.
2. Identify the user's concern or improvement goal.
3. Diagnose against [references/anti-patterns.md](references/anti-patterns.md) (Encyclopedia, Ghost Trigger, False Positive, Duplication Trap, Orphan Resource, Context Hog, README Creep, Monolith, Rules Skill, First-Person Desc).
4. Apply improvements:
   - **Body too long** → Move detail to `references/`, keep body procedural.
   - **Description misses triggers** → Rewrite with the description formula (Step 4b above).
   - **Overlapping with another skill** → Narrow descriptions, add "Do not use for:" boundaries.
   - **Missing resources** → Add scripts for deterministic tasks, references for deep docs.
   - **Inconsistent terminology** → Pick one term, use it everywhere.
5. Re-validate (Step 5 above).

---

## Correct Mode

1. Validate structure (Step 5 structural checks).
2. If structural issues found, fix them first.
3. Use diagnostic tooling: `skills-ref to-prompt` to see what the agent sees, `skills-ref validate` for structural checks, and VS Code Chat Diagnostics (settings gear → Diagnostics) for activation logs.
4. Diagnose the behavioural issue:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Skill never activates | Description too vague or missing keywords | Rewrite description with trigger formula |
| Activates for wrong tasks | Description too broad | Narrow keywords, add anti-triggers |
| Agent ignores body sections | Body too long or verbose | Shorten, move detail to references/ |
| References not loaded | Broken relative paths | Verify link paths resolve to existing files |
| Scripts fail | Missing deps or wrong interpreter | Add `compatibility` field, test script standalone |
| Conflicts with another skill | Overlapping trigger domains | Narrow descriptions on both skills |
| Slash command missing | `name` mismatch or `user-invokable: false` | Fix `name` to match directory, check frontmatter |
| Agent doesn't follow steps | Instructions too vague or too verbose | Rewrite with more specific imperative steps |

5. Apply fixes.
6. Re-validate (Step 5 above).

---

## Deep Reference

For detailed guidance on any aspect, read specific sections from [references/skill-writer-guide.md](references/skill-writer-guide.md):

- Description / trigger engineering → search for `## 7. Writing Effective Descriptions`
- Body content patterns → search for `## 8. Writing Effective Body Content`
- Progressive disclosure patterns → search for `## 6. Progressive Disclosure Patterns`
- Anti-patterns (full gallery) → search for `## 12. Anti-Patterns Gallery`
- Worked examples → search for `## 13. Examples and Case Studies`
- Naming conventions → search for `## 15. Naming Conventions`
- Security considerations → search for `## 16. Security Considerations`
- Debugging and troubleshooting → search for `## 18. Debugging and Troubleshooting`
- Skill composition → search for `## 19. Skill Composition`
- Quick-reference card → search for `## 21. Quick-Reference Card`
