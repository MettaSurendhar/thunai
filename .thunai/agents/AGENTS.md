# Thunai Agent Registry

## Overview
One coordinator and five bounded specialists. Source of truth: `.thunai/src/agents/`. Run `python .thunai/sync.py` to generate the Copilot, Claude Code and OpenCode files.

## Master agent
| Name (Copilot / Claude, OpenCode) | Role |
|---|---|
| `*Thunai` / `thunai` | Coordinator; owns gates, integration and the user conversation |

## Specialists
| Name | Access | Skill | Trigger |
|---|---|---|---|
| `*Thunai_Planning` / `thunai-planning` | read-only | `plan` | /plan |
| `*Thunai_Coding` / `thunai-coding` | edit + shell | `construct`, `test-driven-development`, domain skills | /code |
| `*Thunai_Testing` / `thunai-testing` | edit + shell | `test-driven-development` | /test |
| `*Thunai_Debugging` / `thunai-debugging` | edit + shell | `systematic-debugging` | /debug |
| `*Thunai_Review` / `thunai-review` | read + shell, no edit | `code-review` | /review |

## Governance
Rules in `.thunai/src/rules/` bind every agent (see `.thunai/instructions/INSTRUCTIONS.md`).

## Skills (canonical in `skills/`)
`test-driven-development` and `systematic-debugging` are imported unmodified from upstream (obra/superpowers, MIT). The rest are Thunai-authored.

| Group | Skills |
|---|---|
| Workflow | `thunai`, `orient`, `plan`, `construct`, `code-review`, `git-workflow`, `memory-curator` |
| Quality | `test-driven-development`, `systematic-debugging` |
| Cross-cutting | `web-security` |
| Stack packs (optional, installed from `packs/`) | `web-nextjs`: `nextjs`, `react-typescript`, `frontend-quality`, `tailwindcss`, `shadcn`, `magicui`, `mapcn`. `api-fastapi`: `fastapi`, `python-conventions`, `sqlalchemy-alembic`, `api-design` |
