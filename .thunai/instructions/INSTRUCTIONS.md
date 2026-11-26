# Instruction Map

Source: `.thunai/src/rules/`. Copilot reads the generated `.github/instructions/*.instructions.md`; Claude Code imports the sources through `CLAUDE.md`; OpenCode loads them through the `instructions` list in `opencode.jsonc`.

| Rule | Governs | applyTo | Precedence |
|---|---|---|---|
| git-governance | Branching, staging, commits, pushes | `**` | 1 |
| branch-naming | Branch name format and conventions | `**` | 1 |
| issue-and-pr | Issue/PR conventions, gh auth, tracking files | `**` | 2 |
| scope-and-boundaries | Assigned issue/paths, `outOfScope` exclusion | `**` | 3 |
| verification-honesty | No unrun claims; test-first | `**` | 4 |
| security-and-privacy | Secrets, personal emails | `**` | 5 |
| engineering-principles | DRY, SOLID, KISS | `**` | 6 |
