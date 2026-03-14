## Commit Message Guidelines

Keep commit messages clear, consistent and machine-friendly so changelogs and code review history are useful.

Recommended format (based on Conventional Commits, adapted for this repo):

- Header: type(scope?): short summary
- Blank line
- Body: more detailed explanation (wrap at ~72 chars)
- Blank line
- Footer: references (e.g., issue numbers, breaking changes)

Rules:
- Use imperative, present-tense verb in the header ("Add", "Fix", "Remove").
- Keep the header <= 50 characters when possible.
- Use a scope when it helps clarify the area changed, e.g., `ValueObject`, `Tests`, `CI`.
- Limit body lines to ~72 characters.
- Reference issue or PR numbers in the footer using `Fixes #123` or `Refs #123`.
- Mark breaking changes in the footer using `BREAKING CHANGE: description`.

Common types we use:
- feat: a new feature
- fix: a bug fix
- docs: changes to documentation
- style: formatting, missing semicolons, whitespace (no code change)
- refactor: code change that neither fixes a bug nor adds a feature
- test: adding or updating tests
- chore: tooling, build processes, package updates, ci
- ci: changes to CI configuration

Examples:

- feat(ValueObject): add RepositoryIdentity value object

   Introduce a new immutable value object to represent repository identity.
   Includes validation and unit tests.

- fix(Email): validate email addresses with stricter regex

   Fixes an edge case where emails with plus addressing were rejected.

- docs: update CONTRIBUTING.md with testing instructions

Prefixing with ticket IDs (e.g., `ABC-123: ...`) is optional—use it when your workflow links commits to issue trackers.

When in doubt, write a short, descriptive header and a body that explains the why, not only the what.

---
