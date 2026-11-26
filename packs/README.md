# Stack packs

The core of this template (`skills/`, `AGENTS.md`, `.thunai/`) is stack-agnostic. A **pack** adds skills for one technology stack. Packs are opt-in: nothing in `packs/` is active until it is copied into `skills/`.

## Included packs
| Pack | Skills | Use when |
|---|---|---|
| `web-nextjs` | `nextjs`, `react-typescript`, `frontend-quality`, `tailwindcss`, `shadcn`, `magicui`, `mapcn` | Next.js App Router, React, TypeScript, Tailwind v4 |
| `api-fastapi` | `fastapi`, `python-conventions`, `sqlalchemy-alembic`, `api-design` | Python FastAPI, SQLAlchemy 2.0 + Alembic, pytest. `api-design` also references the `web-nextjs` skills, so it is best used with both packs |

### Provenance
Some pack skills are copied or adapted from upstream projects (`mapcn`, `shadcn`, `magicui`); the others are written for this template. Sources, licences and copyright notices are in [THIRD_PARTY.md](../THIRD_PARTY.md). The skills are guidance for AI assistants and are not affiliated with, or endorsed by, the libraries they describe.

## Install

```text
python init.py --list-packs
python init.py --packs web-nextjs,api-fastapi        # first run, or add --non-interactive --name "My App"
```
`init.py` copies `packs/<pack>/skills/*` to `skills/`, records the pack in `packs` and `stack` in `.thunai/config/project.config.json`, and runs `python .thunai/sync.py`. Manual equivalent: copy the folders, add the pack name to `packs` in the config, run `python .thunai/sync.py`.

Remove a pack: delete its skill folders from `skills/`, remove it from `packs` in the config, run `python .thunai/sync.py` (it prunes the stale entry points).

## Write your own pack
Short version below; the full guide, including validation and the contribution checklist, is [.thunai/docs/adding-a-pack.md](../.thunai/docs/adding-a-pack.md).

1. Create `packs/<name>/skills/<skill>/SKILL.md`. The frontmatter `name` must equal the folder name; the `description` must contain trigger words, because agents match skills by description.
2. Add `packs/<name>/pack.json`:
```json
{
  "name": "<name>",
  "description": "One line.",
  "skills": ["<skill>"],
  "detect": ["files or package:deps that suggest this stack"],
  "stack": "Human-readable stack, written to the config",
  "routing": { "frontend|backend|cross-cutting": ["<skill>"] }
}
```
3. Keep skills short: when to use, rules that differ from defaults, a checklist, references. Skills must not duplicate the core rules.
4. Test with `python init.py --packs <name>` in a scratch copy, then `python .thunai/sync.py --check`.