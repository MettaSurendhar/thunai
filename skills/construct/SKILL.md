---
name: construct
description: Implement an approved plan for one issue inside the assigned paths with minimal, pattern-following changes and a verified result. Trigger on /code, "implement", "build this", after plan approval (G2).
---

# Construct

**Purpose:** implement the approved plan, nothing more.

## Preconditions
Gate G2 approved. Issue number and exact paths known. On a compliant branch (not `main`).

## Workflow
1. Load `test-driven-development` for any behavior change.
2. Read neighboring code and follow its patterns.
3. Per plan step: failing test, minimal change, passing test, small refactor.
4. Run the relevant checks from `.thunai/config/project.config.json`.
5. Report changed files, exact commands and real results, and anything not run.

## Domain skills (load the ones that match the files you touch)
Core skill: `web-security` for auth, user input, secrets, CORS and dependencies.

Stack skills come from the packs installed in `skills/` (see `packs` in `.thunai/config/project.config.json` and `packs/README.md`). Match them by the skill `description` triggers, not by name. Examples: `web-nextjs` provides `nextjs`, `react-typescript`, `frontend-quality`; `api-fastapi` provides `python-conventions`, `fastapi`, `sqlalchemy-alembic`, `api-design`. If no installed skill covers the stack, follow the neighbouring code and `AGENTS.md`.

Check the installed framework versions before applying version-specific advice. Do not preload every skill.

## Quality gates
- Diff touches only assigned paths.
- No new abstraction without a stated need.
- No secrets, generated artifacts or unrelated edits.
- Nothing staged, committed or pushed.
