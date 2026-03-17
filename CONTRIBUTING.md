# Contributing

This repository contains governance tooling and documentation for a GitHub-native
Human-in-the-Loop (HITL) workflow. Contributions are welcome.

## Prerequisites

- [gh CLI](https://cli.github.com/) installed and authenticated (`gh auth login`)
- Access to the `pslits/copilot-session-feedback` repository

## Making Changes

1. Fork or branch from `main`.
2. Follow the [commit message guidelines](.github/copilot-instructions.md) —
   conventional commits format is required.
3. Follow the [file header conventions](.github/copilot-instructions.md) when
   adding new files.
4. Open a pull request against `main`.

## Label Changes

All HITL label changes must go through a PR that updates
[`docs/hitl/labels.md`](docs/hitl/labels.md). The label sync workflow runs
automatically on merge. Do not edit labels manually in the GitHub UI.

## Workflow Changes

Workflows live in `.github/workflows/`. When editing them, note:

- All multiline JavaScript strings inside `script: |` blocks must use
  `[...].join('\n')` — raw template literals that drop to column 0 break
  YAML block scalar parsing.
- Workflow tokens use minimum-necessary permissions (`issues: write` only).
  Do not broaden scopes without justification in the PR description.

## AI-Assisted Contributions

This repo was largely developed with GitHub Copilot. If your contribution
is significantly AI-assisted, include a `Co-Authored-By` trailer in your
commit message:

```
Co-Authored-By: GitHub Copilot <copilot@github.com>
```

## License

By contributing, you agree that your contributions will be licensed under
the [MIT License](LICENSE).
