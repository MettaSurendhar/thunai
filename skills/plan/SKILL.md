---
name: plan
description: Turn one assigned issue into a bounded implementation and verification plan with affected paths, ordered steps, risks and checks. Trigger on /plan, "plan this issue", "break this down", before any implementation.
---

# Plan

**Purpose:** a plan small enough to approve in one read.

## Inputs
Issue number and text, paths in scope, the relevant specification and architecture documents from the team docs folder (`docs.root` and `docs.teamFolder` in the config, as listed by `/orient`), `.thunai/config/project.config.json`.

## Workflow
1. Restate the outcome from the issue's acceptance criteria. Do not add requirements.
2. Inspect only what is needed to name real paths.
3. Fill [templates/plan-template.md](./templates/plan-template.md).
4. Order steps so each is independently verifiable, tests first.
5. List open questions instead of assuming.

## Outputs
The filled template. Read-only: do not edit files or run commands.

## Quality gates
- Every step names a path or a check.
- Every acceptance criterion maps to at least one check.
- No paths from `outOfScope` (config) unless the user authorized them.
- Ends with gate G2: waiting for user approval.
