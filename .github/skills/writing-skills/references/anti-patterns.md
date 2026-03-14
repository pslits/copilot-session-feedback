# Anti-Pattern Quick Check

Scan for these when creating, updating, or correcting (10 most common — see [skill-writer-guide.md](skill-writer-guide.md) `## 12. Anti-Patterns Gallery` for all 15):

| # | Anti-Pattern | Signal | Fix |
|---|-------------|--------|-----|
| 1 | Encyclopedia | Body > 200 lines with exhaustive docs | Move to `references/` |
| 2 | Ghost Trigger | Description too vague, skill never fires | Add "Use when" + "Triggers on:" |
| 3 | False Positive | Activates on unrelated queries | Narrow keywords, add "Do not use for:" |
| 4 | Duplication Trap | Same info in body and references | Pick one canonical location |
| 5 | Orphan Resource | Files in skill dir not referenced from body | Reference or delete |
| 6 | Context Hog | Massive resources loaded unconditionally | Apply progressive disclosure |
| 7 | README Creep | README.md, CHANGELOG.md in skill dir | Remove — skills are for the agent |
| 8 | Monolith | One skill covers unrelated domains | Split into focused skills |
| 9 | Rules Skill | Declarative rules, not procedures | Move to `copilot-instructions.md` |
| 10 | First-Person Desc | "I help you…" or "You can use…" | Rewrite in third person |
