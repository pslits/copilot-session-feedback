# Agent Anti-Pattern Quick Check

Scan for these when creating, updating, or correcting agents:

| # | Anti-Pattern | Signal | Fix |
|---|-------------|--------|-----|
| 1 | **The Omniscient** | Agent has all tools and no restrictions | Apply principle of least privilege — restrict tools to what's needed |
| 2 | **The Ghost** | Agent never activates — name mismatch between filename and frontmatter | Fix `name` to match filename exactly |
| 3 | **The Uninvited** | Agent activates when it shouldn't — too broad description | Narrow description, add `disable-model-invocation: true` if handoff-only |
| 4 | **The Novel** | Body is 200+ lines of verbose instructions | Shorten procedure, make steps imperative, extract domain knowledge to skills |
| 5 | **The Rule-Breaker** | Agent edits files when it should be read-only | Remove `edit/editFiles`/`execute/runInTerminal` from tools list |
| 6 | **The Lone Wolf** | Chain agent has no handoff configuration | Add `handoffs` field with target agent |
| 7 | **The Echo Chamber** | Agent persona repeats the description verbatim | Persona should add behavioural nuance, not repeat metadata |
| 8 | **The Drifter** | Agent has no rules section — behaviour is unpredictable | Add explicit rules with hard boundaries |
| 9 | **The Hoarder** | Agent tries to do research, planning, AND implementation | Split into separate agents (RPI pattern) |
| 10 | **The Phantom Handoff** | Handoff target doesn't exist or name is misspelled | Verify target agent file exists and `name` matches |
| 11 | **The Free-for-All** | Mid-chain agent is user-invokable but should be handoff-only | Add `user-invokable: false` or `disable-model-invocation: true` |
| 12 | **The Hallucinator** | Agent invents content not present in its input | Add rules: "Only report documented facts", "Do not invent" |
| 13 | **The Identity Crisis** | Persona mixes multiple roles ("You are a researcher and implementer") | One agent, one role — split if needed |
| 14 | **README Creep** | README.md or other documentation files alongside agent files | Remove — agent files are self-contained |
| 15 | **The Prompter** | Agent file contains one-shot task instructions, not a persona | Move to `*.prompt.md` — agents are for persistent personas |
| 16 | **The Vague Spec** | `description` says "Helps with code" or similarly generic | Rewrite with specific role, active voice, and concrete domain |
| 17 | **The Deprecated Field** | Uses old `infer` field | Replace with `user-invokable` and `disable-model-invocation` |
| 18 | **The Textbook** | Agent body reads like reference documentation, not a job description | Extract domain knowledge to skills; keep body as role + workflow + guardrails |
| 19 | **The Open Subagent** | `agents: ['*']` on a focused workflow agent | Explicitly list allowed subagents to prevent wrong delegation |
| 20 | **The Secret Keeper** | API keys or tokens embedded in agent instructions | Remove secrets — agent files are version-controlled plain text |
