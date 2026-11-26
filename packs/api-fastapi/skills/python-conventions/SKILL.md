---
name: python-conventions
description: Python coding conventions, typing, tooling and pytest practice for backend work in this project. Trigger on .py files, Python, pytest, typing, mypy, ruff, black, pyproject.toml, virtual environment, "write a function/module in Python".
---

# Python Conventions

Use the project's tooling and configuration first (`pyproject.toml`, `ruff`, `black`, `mypy`, `pytest.ini`). Do not change tool config as part of unrelated work. Check the Python version the project targets.

## Code
- Type-hint all function signatures and public attributes; prefer built-in generics (`list[str]`, `dict[str, int]`) and `X | None`.
- Small functions with one job; early returns; no deep nesting. Follow PEP 8 naming; `snake_case` functions, `PascalCase` classes.
- Use `pathlib`, f-strings, context managers and `dataclasses` or Pydantic models for structured data.
- Never use mutable default arguments. Never use a bare `except:`; catch specific exceptions, add context, re-raise or handle deliberately.
- Use the `logging` module with levels, not `print`. Never log secrets or personal data.
- Do not mix blocking calls into `async def` code (see `fastapi`).

## Structure
- One module per cohesive concern; avoid circular imports; keep I/O at the edges and business logic in pure functions where practical.
- Configuration from environment via typed settings, never hard-coded values or committed secrets.

## Testing (pytest)
- Test files mirror the source layout; names describe behavior (`test_rejects_expired_policy`).
- Use fixtures for setup, `parametrize` for variants, and real objects over mocks; mock only external systems.
- Follow `test-driven-development`: red, green, refactor, with real command output reported.

## Checks to run (use the project's commands from `.thunai/config/project.config.json`)
Lint (`ruff` or equivalent), format check, type check, tests. Report each result or say it was not run.
