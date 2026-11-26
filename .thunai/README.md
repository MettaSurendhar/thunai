# Thunai Agent Kit

An orchestrator-led engineering agent (Thunai + 5 specialists, core skills plus optional stack packs, 7 rules, 7 commands, memory, git guardrails) for **VS Code Copilot**, **Claude Code** and **OpenCode**. Set it up with `python init.py` or [TEMPLATE.md](../TEMPLATE.md).

## One source, three tools
Edit only `.thunai/src/` (agents, rules, commands), `skills/` (canonical skills) and `AGENTS.md`, then run:

```text
python .thunai/sync.py           # regenerate
python .thunai/sync.py --check   # CI / pre-commit: fails if generated files drifted
```

| Generated for | Files |
|---|---|
| Copilot | `.github/agents/*.agent.md`, `.github/instructions/*`, `.github/prompts/*`, `.github/skills/*` (entry points), `.github/copilot-instructions.md` |
| Claude Code | `.claude/agents/*`, `.claude/commands/*`, `.claude/skills/*` (entry points), `CLAUDE.md` (imports rules and memory) |
| OpenCode | `.opencode/agents/*`, `.opencode/commands/*`; skills via `.claude/skills` (and a `skills` entry in your own `opencode.jsonc`, see below) |

Skills are never copied: `skills/<name>/SKILL.md` is the only copy, and the runtimes get tiny entry points (see `skills/README.md`, which also records the upstream hashes). Never hand-edit generated files. `.thunai/memory/`, `.thunai/config/` and the hooks are shared and hand-edited.

## Start it
- **Copilot:** open the repo, pick `*Thunai` (set as default in `.vscode/settings.json`), run `/orient`.
- **Claude Code:** `claude` (settings set `agent: thunai`), then `/orient`. Subagent delegation works when Thunai runs as the main-thread agent.
- **OpenCode:** `opencode` (default agent is `thunai`), then `/orient`.

## Fill in before first use
`python init.py` does steps 1 and 2 of the config; the rest is yours.
1. `.thunai/config/project.config.json`:
   - `project`, `scope`, `outOfScope`: who this repo is for and what Thunai must not touch.
   - `teams` (default `["core"]`) and `activeTeam`: with one team, branch names have no team segment and `/orient` reads the whole `docs.root`. With several teams, branch names get `-team-<team>`, `/orient` reads only the active team's folder and never the others.
   - `packs` and `stack`: written by `init.py`; informational for agents.
   - `commands.install/build/test/lint`: Thunai asks instead of guessing while empty.
   - `docs`: where `/orient` looks. `root` is `docs`. With several teams it finds the active team's folder (`docs/web`, `docs/team-web`, `docs/Team_Web`, any casing); set `teamFolder` if yours has another name and `shared` for extra common paths. **`/orient` reports sprint and milestone work only from those docs plus GitHub milestones**; anything missing is reported as "Not able to find".
   - `branch`: `prefix`, `types`, `requireIssueNumber`, `maxLength`; the validator and `/orient` read it.
2. `.thunai/memory/who-owns-what.md`: replace the TBD row.
3. `.gitignore` entries (`.thunai/tracking/*`, `.thunai/memory/session/`) ship with the template; merge them if you copy the kit into an existing repo.

### Optional `opencode.jsonc` (repo root)
Example, adjust to your OpenCode version:
```jsonc
{
  "default_agent": "thunai",
  "instructions": ["AGENTS.md", ".thunai/memory/*.md", ".thunai/src/rules/*.md"],
  "skills": ["./skills"]
}
```

## Project name
The name appears in `AGENTS.md` (title and persona line), `.thunai/src/agents/thunai.md` (description) and `.thunai/config/project.config.json` (`project`). `init.py` fills the `{{PROJECT_NAME}}` placeholders once; to rename later, edit those three places and run `python .thunai/sync.py`.

## Adding the kit to an existing repo
Easiest: from a clone of the template, run `python adopt.py ../my-repo` (add `--dry-run` to preview). It copies the kit, merges the shared config files, runs `init.py` and cleans up. See [using-the-template.md](docs/using-the-template.md). Manual steps:

1. Create a branch first (named per the branch-naming rule); this is repo work and follows Thunai's rules.
2. Copy this kit over the repo. **Merge, do not overwrite,** `.gitignore`, `.gitattributes`, `.vscode/settings.json` and any existing `.claude/settings.json`.
3. Run `python init.py`, then `python .thunai/sync.py --check` (it warns about leftovers) and `python .thunai/hooks/test_git_guard.py`.
4. Fill in the config, then open each tool once and run `/orient`.

## Guardrails
Every git or `gh` write (add, commit, push, merge, checkout, PR/issue create or comment, and so on) asks you first; a few violations (git add ., force-push, push or commit on main) are blocked outright. Claude Code uses a hook (`python .thunai/hooks/test_git_guard.py` runs its self-test); OpenCode and Copilot use permission and auto-approve rules, where the "not on main" check is rule-based. See `.thunai/hooks/HOOKS.md`.

## Layout
`AGENTS.md` always-on persona, gates, routing | `skills/` canonical skills | `packs/` optional stack skills | `.thunai/src/` agents, rules, commands | `.thunai/memory/` persistent rules | `.thunai/agents/AGENTS.md` registry | `.thunai/instructions/INSTRUCTIONS.md` rule map | `.thunai/tracking/` local issue/PR drafts (git-ignored, created on demand)
