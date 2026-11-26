---
name: code-review
description: Independent review of the current branch against the issue, project rules, tests and security before a PR. Trigger on /review, "review my changes", "ready for PR".
---

# Code Review

**Purpose:** catch problems before a human reviewer does. Read-only.

## Workflow
1. Read the issue and its acceptance criteria.
2. Inspect `git status`, `git diff main...HEAD` and the branch name.
3. Walk the checklist in [references/checklist.md](./references/checklist.md). For auth, input, secrets or dependency changes, also apply `web-security`.
4. Report findings by severity.

## Output
| Severity | File:line | Finding | Suggested fix |
|---|---|---|---|

Severities: **Blocker** (must fix), **Major**, **Minor**, **Note**.

End with a verdict: **Ready** or **Not ready**, and a list of checks you could not verify.
