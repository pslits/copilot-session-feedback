````markdown
# Prompt Anti-Patterns

## Quick Diagnosis — Check These Three First

1. **The Invisible Prompt** (#6) — if it doesn't load, nothing else matters
2. **The Tab-Indented YAML** (#17) — silent failure, extremely common
3. **The Magic Dependency** (#9) — works for author, fails for everyone else

---

## Full Gallery

| # | Name | Severity | Symptom | Fix |
|---|------|----------|---------|-----|
| 1 | **The Wall of Text** | 🟡 Medium | Body exceeds 150 lines; agent loses focus | Split into multiple prompts or upgrade to a skill |
| 2 | **The Vague Command** | 🟠 High | "Do some stuff" — no specific steps or deliverables | Replace with numbered steps and clear deliverables |
| 3 | **The Swiss Army Knife** | 🟠 High | One prompt tries to research, generate, review, and deploy | Split into focused prompts, one per phase |
| 4 | **The Phantom Input** | 🟡 Medium | `${input:}` used without `argument-hint` — user sees blank box | Always pair `${input:}` with `argument-hint` |
| 5 | **The Context Bomb** | 🟠 High | Too many or too large file references (~3,000+ lines injected) | Reference only essential files; reduce total to <3,000 lines |
| 6 | **The Invisible Prompt** | 🔴 Critical | Prompt doesn't appear in `/` picker at all | Check location (`.github/prompts/`), filename (`.prompt.md`), and YAML validity |
| 7 | **The Tool Hoarder** | 🟢 Low | Explicit `tools` list that just lists all tools | Omit `tools` entirely for full access; list only to restrict |
| 8 | **The Negative Framing** | 🟡 Medium | Instructions written as "Don't do X" — agent confused about what TO do | Rephrase instructions positively; negation is fine for constraints only |
| 9 | **The Magic Dependency** | 🟠 High | Works for author but fails for others — relies on prior context | Make self-contained; must pass cold invocation test |
| 10 | **The Format Ambiguity** | 🟡 Medium | Output varies wildly between invocations | Add explicit output format section with structural template |
| 11 | **The Stale Reference** | 🟡 Medium | File reference points to moved/deleted file | Audit file references whenever refactoring |
| 12 | **The Description Novel** | 🟢 Low | Description is a paragraph instead of a concise phrase | Keep description <80 chars, verb-first |
| 13 | **The Overengineer Enabler** | 🟠 High | Agent adds features, refactors code, or changes beyond scope | Add anti-overengineering clause: "Only make changes that are directly requested" |
| 14 | **The Silent Hallucinator** | 🟠 High | Agent confidently describes code it never opened | Add anti-hallucination clause: "Never speculate about code you have not opened" |
| 15 | **The Copy-Paste Prompt** | 🟡 Medium | Prompt copied from another project with stale references | Audit all file references and paths after copying |
| 16 | **The God Prompt** | 🟠 High | Tries to handle every edge case — 200+ lines, still incomplete | Handle the 80% case; let users refine in follow-up |
| 17 | **The Tab-Indented YAML** | 🔴 Critical | Frontmatter uses tabs — YAML silently fails | Always use spaces; enable "Render Whitespace" in editor |
| 18 | **The Missing Verb** | 🟡 Medium | Description starts with a noun — less discoverable | Start description with an action verb |
| 19 | **The Agent Confusion** | 🟡 Medium | Prompt defines a persistent persona with complex handoffs | Move persona to `.agent.md`; prompts are for tasks, not roles |
| 20 | **The Absolute Path** | 🟠 High | File references use absolute paths — break on other machines | Always use relative paths (relative to the prompt file) |
| 21 | **The Secret Leaker** | 🔴 Critical | Secrets, API keys, or credentials embedded in the prompt | Never embed secrets; audit referenced files for sensitive data |

---

## Diagnosis Workflow

When updating or correcting a prompt, scan this list top-to-bottom:

1. Start with the **Quick Diagnosis** three (items 6, 17, 9).
2. Check severity 🔴 items next (6, 17, 21).
3. Check severity 🟠 items (2, 3, 5, 9, 13, 14, 16, 20).
4. Check severity 🟡 items (1, 4, 8, 10, 11, 12, 15, 18, 19).
5. Check severity 🟢 items (7, 12).

For each anti-pattern found, apply the fix from the table above and re-validate.

````