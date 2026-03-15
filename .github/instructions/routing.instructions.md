---
name: Routing Decision Tree
description: Route analysed findings to one integration surface and stop for human approval before file creation.
applyTo: "sessions/**,docs/design/**"
---

# Routing Decision Tree

Use this decision tree to route one analysed finding to exactly one integration surface.

## Decision Procedure

1. Ask whether the finding is a recurring agent correction. Reason: repeated corrections belong in workspace-wide guidance.
   - Route to `copilot-instructions.md` when the answer is yes. Reason: recurring behaviour needs an always-on rule.
   - Stop. Present the routing decision and proposed artifact to the human for approval before writing any file. Reason: routing requires an approval gate before side effects.
2. Ask whether the finding is domain vocabulary or project-specific naming when step 1 is false. Reason: terminology rules belong in scoped instruction files.
   - Route to a scoped `*.instructions.md` file when the answer is yes. Reason: vocabulary guidance should load only where the domain context applies.
   - Stop. Present the routing decision and proposed artifact to the human for approval before writing any file. Reason: routing requires an approval gate before side effects.
3. Ask whether the finding is a repeated manual workflow when steps 1 and 2 are false. Reason: repeated workflow friction maps to reusable commands or agents.
   - Ask whether the workflow needs multi-step agent actions when the answer is yes. Reason: agent handoff is only justified for multi-step execution.
     - Route to `*.agent.md` when multi-step agent actions are required. Reason: agents own persona-driven multi-step workflows.
     - Stop. Present the routing decision and proposed artifact to the human for approval before writing any file. Reason: routing requires an approval gate before side effects.
     - Route to `*.prompt.md` when a named command is sufficient. Reason: prompts fit repeatable workflows that do not need a specialist persona.
     - Stop. Present the routing decision and proposed artifact to the human for approval before writing any file. Reason: routing requires an approval gate before side effects.
4. Ask whether the finding is reusable procedural knowledge when steps 1 through 3 are false. Reason: durable procedural knowledge belongs in a skill.
   - Route to `SKILL.md` when the answer is yes. Reason: skills package reusable procedures and references.
   - Stop. Present the routing decision and proposed artifact to the human for approval before writing any file. Reason: routing requires an approval gate before side effects.
5. Ask whether the remaining finding is a tool-call safety issue when steps 1 through 4 are false. Reason: safety interventions belong at the tool boundary.
   - Route to a hook when the answer is yes. Reason: hooks intercept risky behaviour before the side effect occurs.
   - Stop. Present the routing decision and proposed artifact to the human for approval before writing any file. Reason: routing requires an approval gate before side effects.

## Review Override

- Return the finding to the Analyse stage when the human rejects the proposed route. Reason: human review can amend the routing decision before implementation begins.
